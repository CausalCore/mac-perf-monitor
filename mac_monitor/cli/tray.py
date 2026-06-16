import rumps
import threading
import time
from mac_monitor.engine.analyzer import analyzer

class MacMonTrayApp(rumps.App):
    def __init__(self):
        super(MacMonTrayApp, self).__init__("MacMon: 🟢", quit_button="Quit MacMon")
        self.menu = ["Analyze Now", "Open Dashboard"]
        self.timer = rumps.Timer(self.on_tick, 10)
        self.timer.start()

    @rumps.clicked("Analyze Now")
    def run_analysis(self, _):
        self.title = "MacMon: ⏳"
        report = analyzer.analyze()
        self.update_ui(report)

    @rumps.clicked("Open Dashboard")
    def open_dashboard(self, _):
        import subprocess
        subprocess.Popen(["open", "-a", "Terminal", "-e", "macmon dashboard"])

    def on_tick(self, sender):
        # Run in background thread to not block UI
        threading.Thread(target=self.bg_analyze).start()
        
    def bg_analyze(self):
        report = analyzer.analyze()
        self.update_ui(report)
        
    def update_ui(self, report):
        score = report["score"]
        if score > 60:
            self.title = f"MacMon: 🔴 ({score:.0f})"
            # Notification is handled by analyzer if score > 80
        elif score > 30:
            self.title = f"MacMon: 🟡 ({score:.0f})"
        else:
            self.title = f"MacMon: 🟢 ({score:.0f})"

def run_tray():
    MacMonTrayApp().run()
