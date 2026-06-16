import argparse
import time
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich import box

from mac_monitor.detector.system import get_cpu_metrics, get_memory_metrics, get_disk_io_metrics
from mac_monitor.detector.process import get_top_processes
from mac_monitor.detector.startup import collect_all_startup_info
from mac_monitor.decision.scorer import scorer
from mac_monitor.decision.policy import evaluate_process_action, evaluate_startup_action
from mac_monitor.actions.executor import kill_process, remove_login_item, stop_brew_service
from mac_monitor.safety.guard import confirm_action

console = Console()

def generate_action_plan():
    """Generates the V3 action plan based on time-series telemetry."""
    # 1. Telemetry
    _, cpu_total = get_cpu_metrics()
    mem = get_memory_metrics()
    io_metrics = get_disk_io_metrics()
    top_procs = get_top_processes(limit=10, sort_by="cpu")
    startup_info = collect_all_startup_info()
    
    # 2. Update Time-Series
    scorer.update_snapshot(cpu_total, mem['percent'], io_metrics, top_procs)
    trends = scorer.analyze_metrics()
    
    # 3. Formulate Action Plan
    actions = []
    
    # Evaluate Processes
    for p in top_procs:
        p_trends = trends["process_trends"].get(str(p['pid']), {})
        score, reason, action = evaluate_process_action(p, p_trends.get("cpu_growth", False), p_trends.get("ram_growth", False))
        if action:
            actions.append(action)
            
    # Evaluate Startup Items (Brew)
    for s in startup_info.get("brew_services", []):
        if s.get("status") in ["started", "running"]:
            score, action = evaluate_startup_action("brew_service", s["name"])
            if action: actions.append(action)
            
    # Evaluate Login Items
    for item in startup_info.get("login_items", []):
        score, action = evaluate_startup_action("login_item", item)
        if action: actions.append(action)
        
    # Sort actions by confidence (highest first)
    actions.sort(key=lambda x: x["confidence"], reverse=True)
    return actions

def cmd_optimize(args):
    """The core System Optimization Engine command."""
    is_dry = args.dry
    is_apply = args.apply
    
    if not is_apply and not is_dry:
        # Default is --plan
        is_plan = True
    else:
        is_plan = not is_apply and not is_dry # if somehow empty
        
    console.print("[bold cyan]Analyzing System Telemetry and Time-Series Data...[/bold cyan]")
    
    # Needs a few snapshots if not already cached
    for i in range(3):
        generate_action_plan()
        if i < 2: time.sleep(0.5)
        
    actions = generate_action_plan()
    
    if not actions:
        console.print(Panel("[green]System is fully optimized. No critical anomalies detected.[/green]", title="Optimization Engine"))
        return
        
    # Print the Plan
    table = Table(title="Optimization Action Plan", box=box.SIMPLE)
    table.add_column("Confidence", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Target")
    table.add_column("Reason", style="yellow")
    
    for a in actions:
        conf = f"{a['confidence']}/100"
        table.add_row(conf, a['type'].upper(), a.get('name', str(a.get('pid'))), a['reason'])
        
    console.print(table)
    
    if args.plan_only:
        return
        
    # Execution Phase
    console.print("\n[bold]Execution Phase[/bold]")
    for a in actions:
        desc = f"Execute {a['type'].upper()} on {a.get('name')} (Confidence: {a['confidence']})"
        
        # Only prompt if it's safe enough, or if we force
        if a['confidence'] < 75 and not is_apply:
            console.print(f"[dim]Skipping low confidence action: {desc}[/dim]")
            continue
            
        if confirm_action(desc, dry_run=is_dry, auto_apply=is_apply):
            if a['type'] == 'kill':
                success, msg = kill_process(a['pid'])
            elif a['type'] == 'stop_brew_service':
                success, msg = stop_brew_service(a['name'])
            elif a['type'] == 'remove_login_item':
                success, msg = remove_login_item(a['name'])
                
            color = "green" if success else "red"
            console.print(f"[{color}]{msg}[/{color}]")

def cmd_kill(args):
    """Safe manual kill command."""
    pid = args.pid
    
    # Try to find process name
    procs = get_top_processes(limit=100)
    p_info = next((p for p in procs if str(p['pid']) == str(pid)), None)
    
    if p_info:
        score, reason, _ = evaluate_process_action(p_info, False, False)
        if score == 0:
            console.print(f"[bold red]BLOCKED:[/bold red] PID {pid} ({p_info['name']}) is a protected system process.")
            return
            
    desc = f"Kill PID {pid}"
    if confirm_action(desc, dry_run=False, auto_apply=args.force):
        success, msg = kill_process(pid)
        color = "green" if success else "red"
        console.print(f"[{color}]{msg}[/{color}]")

def main():
    parser = argparse.ArgumentParser(description="macOS Local Autonomous System Controller")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # optimize command
    parser_opt = subparsers.add_parser("optimize", help="Run the AI optimization engine")
    parser_opt.add_argument("--plan", action="store_true", dest="plan_only", help="Only show the decision plan (default if no other flags)")
    parser_opt.add_argument("--dry", action="store_true", help="Run the plan but simulate actions")
    parser_opt.add_argument("--apply", action="store_true", help="Execute the plan immediately (requires YES confirm per action)")

    # kill command
    parser_kill = subparsers.add_parser("kill", help="Safely kill a process")
    parser_kill.add_argument("pid", type=int, help="PID to kill")
    parser_kill.add_argument("--force", action="store_true", help="Skip confirmation (still respects whitelist)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "optimize":
        cmd_optimize(args)
    elif args.command == "kill":
        cmd_kill(args)

if __name__ == "__main__":
    main()
