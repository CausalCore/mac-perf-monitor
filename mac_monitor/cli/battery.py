from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from mac_monitor.telemetry.battery import get_battery_drainers
import psutil

console = Console()


def run_battery_analysis():
    console.print("[bold cyan]Analyzing Energy Impact...[/bold cyan]")

    battery = psutil.sensors_battery()
    if battery:
        plugged = "Plugged In 🔌" if battery.power_plugged else "On Battery 🔋"
        console.print(f"Current Status: [bold]{plugged}[/bold] ({battery.percent}%)\n")

    drainers = get_battery_drainers()

    if not drainers:
        console.print(
            Panel("[green]No significant background battery drain detected.[/green]")
        )
        return

    table = Table(title="Top Battery Drainers (Energy Impact)")
    table.add_column("Process Name", style="cyan")
    table.add_column("Energy Impact Score", justify="right", style="magenta")
    table.add_column("Verdict", style="yellow")

    for d in drainers:
        score = d["energy_impact"]
        if score > 100:
            verdict = "[bold red]Heavy Drainer[/bold red]"
        elif score > 30:
            verdict = "Moderate"
        else:
            verdict = "Normal"

        table.add_row(d["name"], f"{score:.1f}", verdict)

    console.print(table)
    console.print(
        "\n[dim]Tip: High Energy Impact processes drain your battery quickly. Consider restarting them.[/dim]"
    )
