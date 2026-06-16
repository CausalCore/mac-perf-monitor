from rich.console import Console
from rich.panel import Panel

console = Console()

def run_freeram():
    console.print(Panel(
        "[bold cyan]God Mode: RAM Wiper (Purge)[/bold cyan]\n\n"
        "macOS 'Cached Files' (Önbellek) yüzünden RAM dolduğunda, uygulamaları kapatsanız bile bellek açılmaz.\n\n"
        "Bunu fiziksel olarak zorla temizlemek için macOS'un yerleşik gizli komutunu kullanabilirsiniz:\n\n"
        "  [bold green]sudo purge[/bold green]\n\n"
        "[dim]Not: Bu komut şifre ister ve anlık bir donma yaşatabilir, ancak sonrasında RAM'iniz tertemiz olur.[/dim]",
        title="🧠 Free RAM"
    ))
