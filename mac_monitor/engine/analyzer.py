from mac_monitor.telemetry.cpu import get_cpu_metrics
from mac_monitor.telemetry.memory import get_memory_metrics
from mac_monitor.telemetry.io import get_io_metrics
from mac_monitor.telemetry.wakeups import get_wakeups_proxy
from mac_monitor.telemetry.gpu import get_gpu_proxy
from mac_monitor.telemetry.syscall import get_syscall_proxy
from mac_monitor.telemetry.thermal import get_thermal_proxy

from mac_monitor.signal.baseline import baseline_manager
from mac_monitor.signal.anomaly import detect_saturation
from mac_monitor.signal.trend import calculate_trend

from mac_monitor.core.scoring import compute_slowdown_score
from mac_monitor.graph.builder import build_graph
from mac_monitor.graph.correlator import correlate_graph_edges
from mac_monitor.graph.root_cause import extract_root_causes

from mac_monitor.state.replay import replay_engine

import time

class AnalyzerEngine:
    def collect_snapshot(self):
        cpu = get_cpu_metrics()
        mem = get_memory_metrics()
        io = get_io_metrics()
        wakeups = get_wakeups_proxy()
        gpu = get_gpu_proxy()
        syscall = get_syscall_proxy()
        thermal = get_thermal_proxy()
        
        return {
            "timestamp": time.time(),
            "metrics": {
                "cpu": cpu["system_cpu"],
                "memory": mem["percent"],
                "swap_in": mem["swap_in"],
                "swap_out": mem["swap_out"],
                "io_read_bytes": io["read_bytes"],
                "io_write_bytes": io["write_bytes"],
                "wakeups": wakeups["ctx_switches"],
                "gpu_load": gpu["windowserver_cpu"],
                "syscalls": syscall["total_fds"],
                "thermal": thermal["thermal_level"]
            },
            "processes": cpu["processes"]
        }

    def run_micro_buffer(self, duration_sec=5, interval=1):
        """Runs a short polling buffer to collect metrics and filter noise."""
        snapshots = []
        for _ in range(int(duration_sec / interval)):
            snapshots.append(self.collect_snapshot())
            time.sleep(interval)
            
        # Average the metrics to filter noise
        avg_metrics = {}
        for key in snapshots[0]["metrics"].keys():
            valid_vals = [s["metrics"][key] for s in snapshots if s["metrics"].get(key) is not None]
            avg_metrics[key] = sum(valid_vals) / len(valid_vals) if valid_vals else 0.0
            
        return avg_metrics, snapshots[-1]["processes"], snapshots

    def analyze(self):
        """Full causality pipeline."""
        avg_metrics, processes, snapshots = self.run_micro_buffer()
        
        # 1. Update & Check Baseline
        baseline_manager.update_baseline(avg_metrics)
        deviations = baseline_manager.get_baseline_deviations(avg_metrics)
        
        # 2. Detect Anomalies & Saturation
        saturation = detect_saturation(avg_metrics)
        
        # 3. Calculate Trends
        mem_history = [s["metrics"]["memory"] for s in snapshots]
        mem_trend = calculate_trend(mem_history)
        io_history = [s["metrics"]["io_read_bytes"] + s["metrics"]["io_write_bytes"] for s in snapshots]
        io_trend = calculate_trend(io_history)
        
        # 4. Score the Slowdown
        # Map avg_metrics to scoring expectations
        score_metrics = {
            "cpu": avg_metrics["cpu"],
            "memory": avg_metrics["memory"],
            "io_wait": avg_metrics["io_read_bytes"] / 1_000_000, # proxy scale
            "wakeups": avg_metrics["wakeups"],
            "swap": avg_metrics["swap_in"] + avg_metrics["swap_out"],
            "thermal": 0 # Not implemented in MVP without external tools
        }
        score = compute_slowdown_score(score_metrics, saturation, mem_trend, io_trend)
        
        # 5. Build Graph & Root Cause Extraction
        graph = build_graph(snapshots, processes, current_lag_event=(score > 50))
        correlate_graph_edges(graph, saturation, processes)
        roots = extract_root_causes(graph, top_k=3)
        
        if score > 50:
            replay_engine.record_lag_event(roots)
            
        if score > 80:
            from mac_monitor.signal.notify import send_mac_notification
            cause_str = roots[0]["cause"] if roots else "Bilinmeyen Darboğaz"
            send_mac_notification(
                "MacMon: Sistem Darboğazı",
                f"Kök neden: {cause_str}. Optimize etmek için 'macmon boost' çalıştırın.",
                "Yüksek yavaşlama skoru tespit edildi!"
            )
            
        recurring = replay_engine.get_recurring_causes()
            
        return {
            "score": score,
            "saturation": saturation,
            "deviations": deviations,
            "root_causes": roots,
            "recurring_causes": recurring[:3] if recurring else [],
            "raw_metrics": avg_metrics
        }

analyzer = AnalyzerEngine()
