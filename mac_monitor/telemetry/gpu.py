import psutil


def get_gpu_proxy():
    """
    Tracks WindowServer CPU usage as a proxy for GUI lag / GPU compositing pressure.
    """
    windowserver_cpu = 0.0
    for p in psutil.process_iter(["name", "cpu_percent"]):
        try:
            if p.info["name"] == "WindowServer":
                windowserver_cpu = p.info["cpu_percent"]
                break
        except Exception:
            continue

    return {"windowserver_cpu": windowserver_cpu}
