def compute_slowdown_score(metrics, saturation, memory_trend, io_trend):
    """
    Computes the final Slowdown Score (0-100) using a non-linear model.
    metrics dict expects: cpu, memory, io_wait, wakeups, swap, thermal
    """
    # Linear base
    s = (
        0.25 * metrics.get("cpu", 0)
        + 0.25 * metrics.get("memory", 0)
        + 0.20 * metrics.get("io_wait", 0)
        + 0.15 * min(metrics.get("wakeups", 0) / 1000, 100)  # normalize
        + 0.10 * metrics.get("swap", 0)
        + 0.05 * metrics.get("thermal", 0)
    )

    # Interaction Effects (Saturation Multipliers)
    if saturation.get("memory_high") and saturation.get("io_high"):
        s *= 2.2

    if saturation.get("wakeups_high") and saturation.get("cpu_low"):
        s *= 1.4

    if saturation.get("gpu_high") and saturation.get("io_high"):
        s *= 1.6

    if saturation.get("swap_thrashing"):
        s *= 1.7

    if metrics.get("thermal", 0) > 0:
        # Thermal throttling is a major slowdown cause
        s *= 1.8

    if memory_trend > 0:
        s += 10  # additive penalty for memory leak

    return min(s, 100)
