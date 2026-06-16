import os
from rich.console import Console
from rich.table import Table

console = Console()

def get_dir_size(path):
    total = 0
    try:
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)
    except Exception:
        pass
    return total

def run_clean_scan():
    console.print("[bold cyan]Scanning for System Bloat (Hidden Caches)...[/bold cyan]\n")
    
    targets = [
        {"name": "Xcode DerivedData", "path": "~/Library/Developer/Xcode/DerivedData"},
        {"name": "npm cache", "path": "~/.npm"},
        {"name": "pip cache", "path": "~/Library/Caches/pip"},
        {"name": "System Caches", "path": "~/Library/Caches"},
        {"name": "Yarn cache", "path": "~/Library/Caches/Yarn"}
    ]
    
    table = Table(title="Storage Bloat Targets")
    table.add_column("Target", style="cyan")
    table.add_column("Size", justify="right", style="magenta")
    table.add_column("Cleanup Command", style="green")
    
    total_bloat = 0
    
    for t in targets:
        exp_path = os.path.expanduser(t["path"])
        if os.path.exists(exp_path):
            size_bytes = get_dir_size(exp_path)
            size_mb = size_bytes / (1024 * 1024)
            if size_mb > 50: # Only show if > 50MB
                total_bloat += size_mb
                table.add_row(t["name"], f"{size_mb:.1f} MB", f"rm -rf {t['path']}")
                
    if total_bloat == 0:
        console.print("[green]Your system is remarkably clean! No major hidden bloat found.[/green]")
    else:
        console.print(table)
        console.print(f"\n[bold yellow]Total Potential Space to Free: {total_bloat/1024:.2f} GB[/bold yellow]")
        console.print("[dim]Run the commands above manually to free up space and reduce Disk IO load.[/dim]")
