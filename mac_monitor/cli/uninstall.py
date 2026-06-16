import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run_uninstall(app_name):
    console.print(f"[bold cyan]Scanning for deep remnants of '{app_name}'...[/bold cyan]\n")
    
    # Use Spotlight (mdfind) to find related files
    try:
        out = subprocess.check_output(["mdfind", "-name", app_name], text=True)
        lines = out.splitlines()
    except Exception:
        lines = []
        
    # Filter for Application Support, Caches, Preferences in user home only
    home_dir = subprocess.check_output(["echo", "$HOME"], text=True).strip()
    
    targets = []
    for line in lines:
        if line.startswith(home_dir) and (
            "Library/Application Support" in line or 
            "Library/Caches" in line or 
            "Library/Preferences" in line or 
            "Library/Logs" in line or
            "Library/Containers" in line
        ):
            targets.append(line)
            
    if not targets:
        console.print(Panel(f"[green]No hidden remnants found for '{app_name}'.[/green]"))
        return
        
    table = Table(title="Hidden Remnants Found")
    table.add_column("Path", style="magenta")
    table.add_column("Eradicate Command", style="red")
    
    for t in targets[:15]: # Show max 15 to avoid terminal flood
        # Safely quote the path
        clean_path = t.replace("'", "'\\''")
        table.add_row(t.replace(home_dir, "~"), f"rm -rf '{clean_path}'")
        
    console.print(table)
    
    if len(targets) > 15:
        console.print(f"\n[dim]...and {len(targets) - 15} more files. Run commands carefully.[/dim]")
    else:
        console.print("\n[dim]Copy and paste the 'Eradicate Command' to physically delete these remnants.[/dim]")
