import psutil


def get_cpu_metrics():
    """Returns system CPU percent and top CPU-hogging processes."""
    total_cpu = psutil.cpu_percent(interval=None)
    procs = []

    for p in psutil.process_iter(["pid", "name", "cpu_percent"]):
        try:
            info = p.info
            cpu_val = info.get("cpu_percent")
            if cpu_val is not None and cpu_val > 0.5:
                procs.append(
                    {"pid": info["pid"], "name": info["name"], "cpu_percent": cpu_val}
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort by CPU
    procs.sort(key=lambda x: x["cpu_percent"], reverse=True)
    return {"system_cpu": total_cpu, "processes": procs[:50]}
