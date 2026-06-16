def detect_saturation(metrics):
    """
    Detects if system components are saturated (non-linear thresholds).
    """
    saturation = {}

    # Memory > 80% is saturation risk
    if metrics.get("memory", 0) > 80.0:
        saturation["memory_high"] = True
    else:
        saturation["memory_high"] = False

    # High swap in/out indicates thrashing
    if metrics.get("swap_in", 0) > 100 or metrics.get("swap_out", 0) > 100:
        saturation["swap_thrashing"] = True
    else:
        saturation["swap_thrashing"] = False

    # IO Wait proxy (disk read/write burst)
    if (
        metrics.get("io_read_bytes", 0) > 50_000_000
        or metrics.get("io_write_bytes", 0) > 50_000_000
    ):
        saturation["io_high"] = True
    else:
        saturation["io_high"] = False

    # GPU / UI Lag proxy
    if metrics.get("gpu_load", 0) > 30.0:
        saturation["gpu_high"] = True
    else:
        saturation["gpu_high"] = False

    # Wakeups Proxy
    if metrics.get("wakeups", 0) > 20000:  # heuristic
        saturation["wakeups_high"] = True
    else:
        saturation["wakeups_high"] = False

    # CPU Low
    if metrics.get("cpu", 0) < 30.0:
        saturation["cpu_low"] = True
    else:
        saturation["cpu_low"] = False

    return saturation
