import psutil


def get_wakeups_proxy():
    """
    Uses psutil context switches as a proxy for CPU wakeups.
    Returns the total system context switches.
    """
    try:
        stats = psutil.cpu_stats()
        return {
            "ctx_switches": stats.ctx_switches,
            "interrupts": stats.interrupts,
            "syscalls": stats.syscalls,
        }
    except Exception:
        return {"ctx_switches": 0, "interrupts": 0, "syscalls": 0}
