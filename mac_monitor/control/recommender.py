from mac_monitor.control.policies import is_protected

def generate_action_plan(analysis_report):
    """
    Generates safe, Apple-compliant control actions based on root causes.
    Provides `sudo renice` suggestions instead of raw force kills where possible.
    """
    actions = []
    
    score = analysis_report["score"]
    if score < 40:
        return actions # System is relatively stable
        
    for cause in analysis_report["root_causes"]:
        name = cause["cause"]
        
        # If the root cause is a system-wide metric (no single process found)
        if name in ["SWAP_THRASH", "IO_SPIKE", "MEM_LEAK", "CPU_HOG", "GPU_LOAD", "WAKEUP_STORM"]:
            if name == "SWAP_THRASH" or name == "MEM_LEAK":
                actions.append({
                    "target": "System Wide",
                    "action": "Close Inactive Apps",
                    "reason": "Genel bellek/swap darboğazı. Tek bir uygulama sorumlu değil.",
                    "command": "(Manuel) Kullanılmayan tarayıcı sekmelerini kapatın."
                })
            elif name == "IO_SPIKE":
                actions.append({
                    "target": "Disk IO",
                    "action": "Pause Indexing/Sync",
                    "reason": "Genel disk I/O yorgunluğu. (Spotlight veya Cloud Sync kaynaklı olabilir).",
                    "command": "(Manuel) iCloud/Dropbox duraklatın veya: sudo mdutil -i off /"
                })
            elif name == "GPU_LOAD" or name == "WAKEUP_STORM":
                actions.append({
                    "target": "WindowServer/UI",
                    "action": "Reduce Motion / Animations",
                    "reason": "Arayüz oluşturma (Render) darboğazı.",
                    "command": "(Manuel) Ayarlar -> Erişilebilirlik -> Hareketi Azalt seçeneğini açın."
                })
            continue

        if is_protected(name):
            continue # Skip system processes
            
        # Rule 1: High Swap / Memory Leak -> Suggest Restart App or Kill
        if analysis_report["saturation"].get("swap_thrashing") or analysis_report["saturation"].get("memory_high"):
            actions.append({
                "target": name,
                "action": "Restart App / Kill",
                "reason": "Bu süreç (process) bellekte (RAM) thrashing yaratıyor.",
                "command": f"killall -9 {name} (if unresponsive)"
            })
            
        # Rule 2: High Wakeups / CPU Hog -> Suggest Renice
        if analysis_report["saturation"].get("wakeups_high") or analysis_report["saturation"].get("cpu_low"):
            actions.append({
                "target": name,
                "action": "Lower Priority (Renice)",
                "reason": "Bu süreç (process) arka planda işlemciyi meşgul ediyor.",
                "command": f"sudo renice -10 $(pgrep {name})"
            })
            
        # Rule 3: High IO -> Suggest Defer
        if analysis_report["saturation"].get("io_high"):
            actions.append({
                "target": name,
                "action": "Defer / Pause",
                "reason": "Bu süreç (process) diski meşgul ediyor.",
                "command": f"Pause sync or indexing manually in app settings."
            })

    # Deduplicate by target
    unique_actions = []
    seen = set()
    for a in actions:
        if a["target"] not in seen:
            unique_actions.append(a)
            seen.add(a["target"])
            
    return unique_actions
