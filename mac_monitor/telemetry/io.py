import psutil

def get_io_metrics():
    """Returns disk IO read/write counters."""
    try:
        counters = psutil.disk_io_counters()
        if counters:
            return {
                "read_bytes": counters.read_bytes,
                "write_bytes": counters.write_bytes,
                "read_count": counters.read_count,
                "write_count": counters.write_count
            }
    except Exception:
        pass
        
    return {"read_bytes": 0, "write_bytes": 0, "read_count": 0, "write_count": 0}
