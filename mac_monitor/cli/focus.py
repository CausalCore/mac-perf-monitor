from rich.console import Console
from rich.panel import Panel

console = Console()


def run_focus_mode(enable=True):
    if enable:
        console.print(
            Panel(
                "[bold cyan]Focus Mode: ENABLED[/bold cyan]\n\n"
                "Odaklanmanız (Oyun/Render) için arkaplan servislerini duraklatın:\n\n"
                "[yellow]1. Spotlight Indekslemeyi Durdur (Disk IO rahatlar):[/yellow]\n"
                "  [green]sudo mdutil -i off /[/green]\n\n"
                "[yellow]2. Time Machine Yedeklemesini Durdur:[/yellow]\n"
                "  [green]tmutil stopbackup[/green]\n\n"
                "[dim]Bulut senkronizasyonlarını (iCloud/Dropbox) menü çubuğundan manuel duraklatmanız tavsiye edilir.[/dim]",
                title="🎯 MacMon Focus Mode",
            )
        )
    else:
        console.print(
            Panel(
                "[bold cyan]Focus Mode: DISABLED[/bold cyan]\n\n"
                "Sistemi normal çalışma moduna döndürmek için:\n\n"
                "[yellow]1. Spotlight Indekslemeyi Başlat:[/yellow]\n"
                "  [green]sudo mdutil -i on /[/green]\n\n"
                "[dim]Manuel duraklattığınız servisleri yeniden başlatmayı unutmayın.[/dim]",
                title="🎯 MacMon Un-Focus Mode",
            )
        )
