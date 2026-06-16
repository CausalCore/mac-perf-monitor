import psutil
from collections import defaultdict


def get_network_connections():
    """
    Groups open network connections by process name.
    Does not require sudo.
    """
    try:
        conns = psutil.net_connections(kind="inet")
        proc_counts = defaultdict(int)

        for c in conns:
            if c.status == "ESTABLISHED" and c.pid:
                try:
                    p = psutil.Process(c.pid)
                    proc_counts[p.name()] += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        sorted_counts = sorted(proc_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_counts[:10]
    except Exception:
        # AccessDenied or unsupported on some macOS configurations without root
        return []
