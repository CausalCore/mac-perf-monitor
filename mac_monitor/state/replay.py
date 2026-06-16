import time
from mac_monitor.state.store import store

class EventReplayEngine:
    def __init__(self):
        self.data = store.load()
        if "events" not in self.data:
            self.data["events"] = []

    def record_lag_event(self, root_causes):
        """Records a lag event and its root causes into long-term memory."""
        now = time.time()
        self.data["events"].append({
            "timestamp": now,
            "root_causes": root_causes
        })
        # Keep only last 100 events
        if len(self.data["events"]) > 100:
            self.data["events"] = self.data["events"][-100:]
        store.save(self.data)

    def get_recurring_causes(self):
        """Analyzes past events to find recurring patterns."""
        causes_freq = {}
        for ev in self.data.get("events", []):
            for rc in ev.get("root_causes", []):
                cause_name = rc.get("cause", str(rc)) if isinstance(rc, dict) else str(rc)
                causes_freq[cause_name] = causes_freq.get(cause_name, 0) + 1
                
        # Sort by frequency
        sorted_causes = sorted(causes_freq.items(), key=lambda x: x[1], reverse=True)
        return [{"cause": k, "frequency": v} for k, v in sorted_causes]

replay_engine = EventReplayEngine()
