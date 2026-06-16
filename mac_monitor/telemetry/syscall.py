import psutil


def get_syscall_proxy():
    """
    Best effort proxy for syscall/filesystem metadata storms.
    Tracks total open file descriptors and threads across the system.
    """
    total_fds = 0
    total_threads = 0

    for p in psutil.process_iter(["num_fds", "num_threads"]):
        try:
            fds = p.info.get("num_fds")
            if fds:
                total_fds += fds
            threads = p.info.get("num_threads")
            if threads:
                total_threads += threads
        except Exception:
            continue

    return {"total_fds": total_fds, "total_threads": total_threads}
