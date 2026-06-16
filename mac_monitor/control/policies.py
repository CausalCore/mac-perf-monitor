# Critical macOS and System processes that should never be touched
SAFE_PROCESSES = {
    "kernel_task", "launchd", "WindowServer", "syslogd", "logd",
    "fseventsd", "UserEventAgent", "coreaudiod", "hidd",
    "mds", "mdworker", "mdworker_shared", "loginwindow",
    "Dock", "Finder", "SystemUIServer", "AirPlayUIAgent",
    "Spotlight", "Activity Monitor", "Terminal", "python3"
}

def is_protected(process_name):
    """Check if a process is a known critical system process."""
    if not process_name:
        return True
    name = process_name.lower()
    if process_name in SAFE_PROCESSES:
        return True
    if name.endswith("d") and name.startswith("com.apple."):
        return True
    if name.startswith("core") and name.endswith("d"):
        return True
    return False

SAFE_MODE_ENABLED = True
