import json
import urllib.request
import urllib.error
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from mac_monitor.engine.analyzer import analyzer

console = Console()


def run_chat(prompt=None):
    console.print("[bold cyan]🤖 AuraMac Local AI (Ollama)[/bold cyan]\n")

    # 1. Gather System Context
    report = analyzer.analyze()
    score = report["score"]
    roots = report.get("root_causes", [])

    cause_str = (
        ", ".join([r["cause"] for r in roots])
        if roots
        else "No specific process bottlenecks."
    )

    context = f"""
    System Context:
    - Slowdown Score: {score:.1f}/100
    - Root Causes: {cause_str}
    - Saturation Events: {list(report['saturation'].keys())}
    - CPU: {report['raw_metrics'].get('cpu', 0)}%
    - Swap In/Out: {report['raw_metrics'].get('swap_in', 0)} / {report['raw_metrics'].get('swap_out', 0)}
    - Thermal Level: {report['raw_metrics'].get('thermal', 0)}
    """

    user_prompt = (
        prompt
        if prompt
        else "Mac'im şu an neden yavaş hissettiriyor olabilir? Kısa ve öz bir özet yap."
    )
    full_prompt = f"Sen AuraMac isimli bir macOS performans asistanısın. Aşağıdaki sistem bağlamını kullanarak kullanıcının sorusunu kısaca yanıtla.\n\n{context}\n\nKullanıcı Sorusu: {user_prompt}"

    console.print(f"[dim]Soru: {user_prompt}[/dim]\n")
    console.print("[yellow]Ollama'ya bağlanılıyor (localhost:11434)...[/yellow]\n")

    data = json.dumps(
        {"model": "llama3", "prompt": full_prompt, "stream": False}
    ).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            answer = result.get("response", "No response received.")
            console.print(
                Panel(Markdown(answer), title="AuraMac AI", border_style="green")
            )

    except urllib.error.URLError as e:
        console.print("[bold red]Bağlantı Hatası![/bold red]")
        console.print(
            Panel(
                "Yapay Zeka özelliğini kullanmak için [bold]Ollama[/bold]'nın sisteminizde kurulu ve çalışıyor olması gerekir.\n\n"
                "Kurulum İçin:\n"
                "1. [cyan]https://ollama.com[/cyan] adresinden Ollama'yı indirin.\n"
                "2. Terminalde [cyan]ollama run llama3[/cyan] komutunu çalıştırın.\n"
                "3. AuraMac'i tekrar deneyin.",
                title="Ollama Bulunamadı",
                border_style="red",
            )
        )
    except Exception as e:
        console.print(f"[bold red]Bir hata oluştu:[/bold red] {e}")
