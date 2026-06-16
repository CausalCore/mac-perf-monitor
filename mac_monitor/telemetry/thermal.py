import subprocess

def get_thermal_proxy():
    """
    Checks if the Mac is thermally throttled via sysctl.
    Returns an integer: 0 is normal, higher means thermal throttling.
    """
    try:
        # machdep.xcpm.cpu_thermal_level is an Intel-only metric
        # We suppress stderr so Apple Silicon Macs don't spam 'unknown oid' to the console.
        out = subprocess.check_output(
            ["sysctl", "-n", "machdep.xcpm.cpu_thermal_level"],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        level = int(out)
        return {"thermal_level": level}
    except Exception:
        # Fallback if sysctl fails or is unsupported on Apple Silicon
        return {"thermal_level": 0}
