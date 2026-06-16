import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from mac_monitor.engine.analyzer import analyzer
from mac_monitor.control.recommender import generate_action_plan

console = Console()


def run_analysis(duration_sec=10):
    """Runs the full intelligence pipeline with a UI spinner."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description=f"Running Multi-Baseline Diagnostics (Micro-Buffer: {duration_sec}s)...",
            total=None,
        )
        report = analyzer.analyze()
    return report


def print_causality_graph(report):
    """Prints the DAG root cause graph in a beautiful format."""
    console.print("\n[bold cyan]Causality Engine Graph (Root Causes)[/bold cyan]")

    roots = report.get("root_causes", [])
    if not roots:
        console.print(
            "[green]No significant bottlenecks detected. System is healthy.[/green]"
        )
        return

    for idx, cause in enumerate(roots):
        c_name = cause.get("cause", "Unknown")
        c_score = cause.get("score", 0)
        prefix = "├──" if idx < len(roots) - 1 else "└──"

        console.print(f"[bold red]Lag Event[/bold red]")
        console.print(
            f" {prefix} [bold yellow]Bottleneck[/bold yellow] (Score: {c_score:.1f})"
        )
        console.print(f"     └── [bold magenta]{c_name}[/bold magenta]")


def cmd_analyze(args):
    console.print("[bold]macOS Behavioral Causality Intelligence Engine[/bold]")

    report = run_analysis(10)

    # 1. Print Score & Deviations
    dev = report["deviations"]
    calib = " (Calibration Mode)" if dev.get("is_calibrating") else ""
    color = (
        "red" if report["score"] > 60 else "yellow" if report["score"] > 30 else "green"
    )

    panel_txt = f"Slowdown Score: [{color}]{report['score']:.1f}/100[/{color}]{calib}\n"
    if not dev.get("is_calibrating"):
        panel_txt += f"CPU Deviation: {dev['cpu_dev']:.1f}% | RAM Deviation: {dev['memory_dev']:.1f}%\n"

    sat = [k for k, v in report["saturation"].items() if v]
    if sat:
        panel_txt += f"Saturation: {', '.join(sat)}"

    console.print(Panel(panel_txt, title="System Diagnostics", border_style=color))

    # 2. Causality Graph
    print_causality_graph(report)

    # 3. Recurring Memory
    recs = report.get("recurring_causes", [])
    if recs:
        console.print("\n[bold]Long-Term Pattern Memory:[/bold]")
        for r in recs:
            console.print(
                f"  - [dim]{r['cause']} (Seen {r['frequency']} times recently)[/dim]"
            )


def cmd_boost(args):
    console.print(
        "[bold]macOS Behavioral Causality Intelligence Engine - Boost Mode[/bold]"
    )
    report = run_analysis(10)

    actions = generate_action_plan(report)
    if not actions:
        console.print(Panel("[green]No actions required. System is stable.[/green]"))
        return

    table = Table(title="Boost Plan (Safe Mode)", box=box.SIMPLE)
    table.add_column("Target")
    table.add_column("Action", style="cyan")
    table.add_column("Reason", style="yellow")

    for a in actions:
        table.add_row(a["target"], a["action"], a["reason"])

    console.print(table)

    if args.apply:
        console.print("\n[bold]Execution Commands (Copy & Paste):[/bold]")
        for a in actions:
            console.print(f"  [green]{a['command']}[/green]")


def main():
    parser = argparse.ArgumentParser(
        description="macOS Behavioral Causality Intelligence Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze
    parser_analyze = subparsers.add_parser(
        "analyze", help="Run full causality diagnostics (DAG + Root Cause)"
    )

    # Dashboard
    parser_dash = subparsers.add_parser(
        "dashboard", help="Launch the Live TUI Dashboard"
    )

    # Tray
    parser_tray = subparsers.add_parser("tray", help="Launch macOS Native Menu Bar App")

    # Boost
    parser_boost = subparsers.add_parser(
        "boost", help="Generate and apply behavior optimizations"
    )
    parser_boost.add_argument(
        "--plan", action="store_true", help="Show optimization plan"
    )
    parser_boost.add_argument(
        "--apply",
        action="store_true",
        help="Show terminal commands to execute the plan",
    )

    # Report
    parser_report = subparsers.add_parser(
        "report", help="Generate a weekly HTML health report"
    )

    # Battery
    parser_battery = subparsers.add_parser(
        "battery", help="Detect background battery drainers"
    )

    # Focus
    parser_focus = subparsers.add_parser(
        "focus", help="Enable Focus Mode (Pause background syncs)"
    )
    parser_unfocus = subparsers.add_parser("unfocus", help="Disable Focus Mode")

    # Clean
    parser_clean = subparsers.add_parser(
        "clean", help="Find hidden storage bloat and caches"
    )

    # Share
    parser_share = subparsers.add_parser(
        "share", help="Generate a shareable health score ASCII art"
    )

    # Network
    parser_network = subparsers.add_parser(
        "network", help="Scan for network privacy hogs"
    )

    # Widget
    parser_widget = subparsers.add_parser(
        "widget", help="Launch transparent Desktop Widget Proxy"
    )

    # Chat
    parser_chat = subparsers.add_parser(
        "chat", help="Chat with Local AI about system health"
    )
    parser_chat.add_argument(
        "prompt", nargs="?", default=None, help="Your question to the AI"
    )

    # Autostart
    parser_autostart = subparsers.add_parser(
        "autostart", help="Find and disable startup bloat (LaunchAgents)"
    )

    # Uninstall
    parser_uninstall = subparsers.add_parser(
        "uninstall", help="Deep clean app remnants"
    )
    parser_uninstall.add_argument("app", help="Name of the app to eradicate")

    # Free RAM
    parser_freeram = subparsers.add_parser(
        "free-ram", help="Force flush RAM disk cache"
    )

    # Nuke
    parser_nuke = subparsers.add_parser("nuke", help="Wipe all Docker developer junk")

    args = parser.parse_args()

    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "dashboard":
        from mac_monitor.cli.dashboard import run_dashboard

        try:
            run_dashboard()
        except KeyboardInterrupt:
            console.print("\n[green]Dashboard closed.[/green]")
    elif args.command == "boost":
        cmd_boost(args)
    elif args.command == "report":
        from mac_monitor.cli.report import generate_report

        out = generate_report()
        console.print(f"[bold green]Report generated at: {out}[/bold green]")
    elif args.command == "tray":
        from mac_monitor.cli.tray import run_tray

        console.print("[bold cyan]Launching MacMon Menu Bar App...[/bold cyan]")
        run_tray()
    elif args.command == "battery":
        from mac_monitor.cli.battery import run_battery_analysis

        run_battery_analysis()
    elif args.command == "focus":
        from mac_monitor.cli.focus import run_focus_mode

        run_focus_mode(enable=True)
    elif args.command == "unfocus":
        from mac_monitor.cli.focus import run_focus_mode

        run_focus_mode(enable=False)
    elif args.command == "clean":
        from mac_monitor.cli.clean import run_clean_scan

        run_clean_scan()
    elif args.command == "share":
        from mac_monitor.cli.share import run_share

        run_share()
    elif args.command == "network":
        from mac_monitor.cli.network import run_network_sentinel

        run_network_sentinel()
    elif args.command == "widget":
        from mac_monitor.cli.widget import run_widget

        try:
            run_widget()
        except KeyboardInterrupt:
            console.print("\n[green]Widget closed.[/green]")
    elif args.command == "chat":
        from mac_monitor.cli.chat import run_chat

        run_chat(args.prompt)
    elif args.command == "autostart":
        from mac_monitor.cli.autostart import run_autostart_scan

        run_autostart_scan()
    elif args.command == "uninstall":
        from mac_monitor.cli.uninstall import run_uninstall

        run_uninstall(args.app)
    elif args.command == "free-ram":
        from mac_monitor.cli.freeram import run_freeram

        run_freeram()
    elif args.command == "nuke":
        from mac_monitor.cli.nuke import run_nuke

        run_nuke()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
