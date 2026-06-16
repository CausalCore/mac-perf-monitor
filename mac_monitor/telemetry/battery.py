import subprocess


def get_battery_drainers():
    """
    Parses 'top' command output to get energy impact of top processes.
    Does not require sudo. Returns top 10 battery drainers.
    """
    try:
        # Run top for 1 sample, getting pid, command, power score
        out = subprocess.check_output(
            ["top", "-l", "1", "-stats", "pid,command,power", "-o", "power"], text=True
        )

        lines = out.splitlines()
        # Find where processes start (after "PID    COMMAND          POWER")
        start_idx = 0
        for i, line in enumerate(lines):
            if "PID" in line and "COMMAND" in line and "POWER" in line:
                start_idx = i + 1
                break

        drainers = []
        for line in lines[start_idx:]:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 3:
                pid = parts[0]
                power = parts[-1]
                cmd = " ".join(parts[1:-1])

                try:
                    power_val = float(power)
                    if power_val > 0:
                        drainers.append(
                            {"pid": pid, "name": cmd, "energy_impact": power_val}
                        )
                except ValueError:
                    pass

        return drainers[:10]
    except Exception:
        return []
