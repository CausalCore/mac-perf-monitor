import os
from rich.console import Console
from rich.table import Table

console = Console()

def run_autostart_scan():
    console.print("[bold cyan]Scanning for Startup Bloat (LaunchAgents)...[/bold cyan]\n")
    
    paths_to_scan = [
        "~/Library/LaunchAgents"
    ]
    
    table = Table(title="Background Launch Agents (Autostart)")
    table.add_column("Agent ID", style="cyan")
    table.add_column("Disable Command (Run Manually)", style="green")
    
    found_any = False
    
    for base_path in paths_to_scan:
        expanded = os.path.expanduser(base_path)
        if os.path.exists(expanded):
            try:
                for filename in os.listdir(expanded):
                    if filename.endswith(".plist"):
                        found_any = True
                        agent_id = filename.replace(".plist", "")
                        full_path = os.path.join(expanded, filename)
                        disable_cmd = f"launchctl unload -w '{full_path}'"
                        table.add_row(agent_id, disable_cmd)
            except PermissionError:
                console.print(f"[bold red]Permission Denied:[/bold red] Terminal needs 'Full Disk Access' to scan {expanded}")
                return
                    
    if found_any:
        console.print(table)
        console.print("\n[dim]Note: Disabling agents like 'com.adobe.ARMD' stops them from running on startup. Be careful not to disable services you actually need.[/dim]")
    else:
        console.print("[green]No user-level startup bloat found in ~/Library/LaunchAgents.[/green]")
