from rich.console import Console
from rich.panel import Panel

console = Console()

def run_nuke():
    console.print(Panel(
        "[bold red]God Mode: Docker Nuke (Dev Cleaner)[/bold red]\n\n"
        "Kullanılmayan sanal makineler (Containers), sarkan imajlar (Dangling Images) ve hacimler (Volumes) diski ve işlemciyi tüketir.\n\n"
        "Docker'ı bir saniyede fabrika ayarlarına döndürüp GB'larca yer açmak için:\n\n"
        "  [bold green]docker system prune -a --volumes -f[/bold green]\n\n"
        "[dim]DİKKAT: Bu komut çalışanlar dışındaki tüm Docker imajlarını siler. Sadece geliştiriciler (Developers) için önerilir.[/dim]",
        title="☢️ Docker Nuke",
        border_style="red"
    ))
