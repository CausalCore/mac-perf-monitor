import time
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

from mac_monitor.engine.analyzer import analyzer


def create_widget_layout():
    return Layout()


def run_widget():
    layout = create_widget_layout()

    with Live(layout, refresh_per_second=1, screen=True) as live:
        while True:
            report = analyzer.analyze()
            score = report["score"]
            color = "red" if score > 60 else "yellow" if score > 30 else "green"

            roots = report.get("root_causes", [])
            cause_str = roots[0]["cause"] if roots else "System Healthy"

            content = (
                f"\n[bold]Health Score:[/bold] [{color}]{100 - score:.0f}[/{color}]\n\n"
            )
            content += f"[bold]Status:[/bold] {cause_str}\n"
            content += f"[dim]CPU: {report['raw_metrics'].get('cpu', 0):.0f}%[/dim]\n"

            panel = Panel(
                Align.center(content),
                title="[bold cyan]AuraMac[/bold cyan]",
                border_style=color,
                padding=(1, 2),
            )

            layout.update(panel)
