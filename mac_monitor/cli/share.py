from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from mac_monitor.engine.analyzer import analyzer

console = Console()


def run_share():
    report = analyzer.analyze()
    score = report["score"]

    health = (
        "PERFECT 🟢" if score < 30 else "OKAY 🟡" if score < 60 else "STRUGGLING 🔴"
    )

    ascii_art = f"""
    [bold cyan]█▀▄▀█   ▄▀█   █▀▀   █▀▄▀█   █▀█   █▄░█[/bold cyan]
    [bold cyan]█░▀░█   █▀█   █▄▄   █░▀░█   █▄█   █░▀█[/bold cyan]
    
         [bold]Mac Health Score:[/bold] {100 - score:.1f} / 100
         [bold]Verdict:[/bold] {health}
         
    [dim]Analyzed by MacMon Causality Engine[/dim]
    [dim]github.com/Antigravity/mac-perf-monitor[/dim]
    """

    console.print(Panel(Align.center(ascii_art), border_style="cyan", padding=(1, 5)))
    console.print(
        "\n[bold green]Screenshot this box and share it on Twitter/Reddit![/bold green]"
    )
