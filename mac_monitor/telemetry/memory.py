import psutil
import subprocess
import re


def get_memory_metrics():
    """
    Collects memory pressure, RAM usage, and swap delta proxies.
    Returns: dict with memory metrics.
    """
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # Try to get vm_stat for deeper compression and page metrics
    vm_stat_data = {}
    try:
        out = subprocess.check_output(["vm_stat"], text=True)
        for line in out.splitlines():
            if ":" in line:
                key, val = line.split(":")
                key = key.strip().replace('"', "")
                val = int(re.sub(r"\D", "", val))
                vm_stat_data[key] = val
    except Exception:
        pass

    pages_swapped_in = vm_stat_data.get("Pageins", 0)
    pages_swapped_out = vm_stat_data.get("Pageouts", 0)
    compressed_pages = vm_stat_data.get("Pages compressed", 0)

    return {
        "percent": mem.percent,
        "used_mb": mem.used / (1024 * 1024),
        "swap_used_mb": swap.used / (1024 * 1024),
        "swap_in": pages_swapped_in,
        "swap_out": pages_swapped_out,
        "compressed": compressed_pages,
    }
