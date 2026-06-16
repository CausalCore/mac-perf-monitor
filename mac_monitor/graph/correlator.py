import math

def calculate_decay(time_gap_seconds):
    """
    Decay curve for temporal causality weighting.
    0-2 sec -> strong (1.0)
    2-10 sec -> medium (decaying to 0.5)
    >10 sec -> weak (<0.5)
    """
    if time_gap_seconds <= 2:
        return 1.0
    elif time_gap_seconds <= 10:
        return math.exp(-0.1 * (time_gap_seconds - 2))
    else:
        return 0.2

def evaluate_causality(correlation, time_precedence_score, time_gap):
    """
    cause_score = correlation * time_precedence_score * decay_function(time_gap)
    """
    decay = calculate_decay(time_gap)
    return correlation * time_precedence_score * decay

def correlate_graph_edges(graph, saturation_signals, process_telemetry):
    """
    Links processes to metrics, and metrics to symptoms using causal weighting.
    """
    # 1. Metrics -> Symptom
    if saturation_signals.get("io_high"):
        graph.add_edge("IO_SPIKE", "UI_LAG", evaluate_causality(0.9, 1.0, 1.0))
        
    if saturation_signals.get("swap_thrashing"):
        graph.add_edge("SWAP_THRASH", "UI_LAG", evaluate_causality(0.95, 1.0, 0.5))
        
    if saturation_signals.get("gpu_high"):
        graph.add_edge("GPU_LOAD", "UI_LAG", evaluate_causality(0.8, 1.0, 0.5))
        
    if saturation_signals.get("wakeups_high"):
        graph.add_edge("WAKEUP_STORM", "UI_LAG", evaluate_causality(0.7, 1.0, 2.0))

    # 2. Processes -> Metrics
    for p in process_telemetry:
        p_node = f"PROC_{p['name']}"
        # CPU Hog
        if p['cpu_percent'] > 50:
            graph.add_edge(p_node, "CPU_HOG", evaluate_causality(0.8, 1.0, 1.0))
        # RAM Leak / Swap cause
        if p.get('memory_percent', 0) > 10.0:
            graph.add_edge(p_node, "MEM_LEAK", evaluate_causality(0.7, 1.0, 3.0))
            if saturation_signals.get("swap_thrashing"):
                graph.add_edge(p_node, "SWAP_THRASH", evaluate_causality(0.6, 1.0, 5.0))
        # Known IO / Wakeup offenders (Heuristic proxy if we don't have per-process IO)
        if "Chrome" in p['name'] or "Slack" in p['name']:
            if saturation_signals.get("wakeups_high"):
                graph.add_edge(p_node, "WAKEUP_STORM", evaluate_causality(0.75, 1.0, 2.0))
        if "Spotlight" in p['name'] or "mdworker" in p['name'] or "node" in p['name']:
            if saturation_signals.get("io_high"):
                graph.add_edge(p_node, "IO_SPIKE", evaluate_causality(0.85, 1.0, 1.0))
