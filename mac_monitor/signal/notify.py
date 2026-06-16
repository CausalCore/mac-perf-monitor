import subprocess


def send_mac_notification(title, message, subtitle=""):
    """
    Sends a native macOS notification using AppleScript (osascript).
    """
    applescript = (
        f'display notification "{message}" with title "{title}" subtitle "{subtitle}"'
    )
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
    except Exception:
        pass
