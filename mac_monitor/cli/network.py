from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from mac_monitor.telemetry.network import get_network_connections

console = Console()

def run_network_sentinel():
    console.print("[bold cyan]Scanning Active Network Connections (Privacy Sentinel)...[/bold cyan]\n")
    
    conns = get_network_connections()
    
    if not conns:
        console.print(Panel("[yellow]Unable to read active connections without sudo, or no established connections found.[/yellow]"))
        return
        
    table = Table(title="Top Network Consumers (Established Connections)")
    table.add_column("Process Name", style="cyan")
    table.add_column("Active Connections", justify="right", style="magenta")
    table.add_column("Verdict", style="yellow")
    
    for name, count in conns:
        if count > 50:
            verdict = "[bold red]Suspect/Heavy[/bold red]"
        elif count > 15:
            verdict = "Moderate"
        else:
            verdict = "Normal"
            
        table.add_row(name, str(count), verdict)
        
    console.print(table)
    console.print("\n[dim]Note: Browsers naturally have many connections. Look out for unknown background apps![/dim]")
