import time
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

from mac_monitor.engine.analyzer import analyzer


def create_dashboard_layout():
    layout = Layout()
    layout.split_column(Layout(name="header", size=3), Layout(name="main"))
    layout["main"].split_row(
        Layout(name="metrics", ratio=1), Layout(name="dag", ratio=2)
    )
    return layout


def update_metrics_panel(report):
    m = report["raw_metrics"]
    table = Table(show_header=False, expand=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("System CPU", f"{m.get('cpu', 0):.1f}%")
    table.add_row("Memory", f"{m.get('memory', 0):.1f}%")
    table.add_row("Swap In/Out", f"{m.get('swap_in', 0)} / {m.get('swap_out', 0)}")
    table.add_row("Wakeups (CTX)", f"{m.get('wakeups', 0)}")
    table.add_row("GPU Proxy", f"{m.get('gpu_load', 0):.1f}%")
    table.add_row("Thermal", f"{m.get('thermal', 0)}")

    color = (
        "red" if report["score"] > 60 else "yellow" if report["score"] > 30 else "green"
    )
    return Panel(
        Align.center(table),
        title=f"Telemetry | Score: [{color}]{report['score']:.1f}[/{color}]",
        border_style=color,
    )


def update_dag_panel(report):
    roots = report.get("root_causes", [])
    if not roots:
        return Panel(
            Align.center("[green]\n\nSystem Healthy\nNo bottlenecks detected.[/green]"),
            title="Causality DAG",
        )

    text = "[bold red]Lag Event[/bold red]\n"
    for idx, cause in enumerate(roots):
        c_name = cause.get("cause", "Unknown")
        c_score = cause.get("score", 0)
        prefix = "├──" if idx < len(roots) - 1 else "└──"

        text += (
            f" {prefix} [bold yellow]Bottleneck[/bold yellow] (Score: {c_score:.1f})\n"
        )
        text += f"     └── [bold magenta]{c_name}[/bold magenta]\n"

    return Panel(text, title="Causality DAG", border_style="cyan")


def run_dashboard():
    layout = create_dashboard_layout()
    layout["header"].update(
        Panel(
            Align.center(
                "[bold cyan]macOS Behavioral Causality Engine - Live TUI[/bold cyan]"
            )
        )
    )

    with Live(layout, refresh_per_second=1, screen=True) as live:
        while True:
            # Short buffer for live updates
            report = analyzer.analyze()
            layout["metrics"].update(update_metrics_panel(report))
            layout["dag"].update(update_dag_panel(report))
