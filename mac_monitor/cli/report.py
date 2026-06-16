import os
from datetime import datetime
from mac_monitor.state.replay import replay_engine

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MacMon System Health Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 40px; background-color: #f5f5f7; color: #1d1d1f; }}
        h1 {{ color: #1d1d1f; }}
        .card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .bottleneck {{ display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; }}
        .bottleneck:last-child {{ border-bottom: none; }}
        .count {{ background: #ff3b30; color: white; padding: 2px 8px; border-radius: 12px; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>System Health Report</h1>
    <p>Generated on: {date}</p>
    
    <div class="card">
        <h2>Top Bottlenecks (Long-Term Memory)</h2>
        {bottlenecks_html}
    </div>
</body>
</html>
"""

def generate_report():
    causes = replay_engine.get_recurring_causes()
    
    if not causes:
        bottlenecks_html = "<p>No significant bottlenecks recorded. Your system is extremely healthy!</p>"
    else:
        bottlenecks_html = ""
        for c in causes:
            bottlenecks_html += f'<div class="bottleneck"><span>{c["cause"]}</span><span class="count">{c["frequency"]} occurrences</span></div>'
            
    html = HTML_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        bottlenecks_html=bottlenecks_html
    )
    
    out_path = os.path.join(os.getcwd(), "causalcore_report.html")
    
    try:
        with open(out_path, "w") as f:
            f.write(html)
        return out_path
    except PermissionError:
        # Fallback to tmp if current dir is not writable
        fallback_path = "/tmp/causalcore_report.html"
        with open(fallback_path, "w") as f:
            f.write(html)
        return fallback_path
