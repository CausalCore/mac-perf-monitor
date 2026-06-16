import os
import json
import time

STATE_DIR = os.path.expanduser("~/.macmon")
STATE_FILE = os.path.join(STATE_DIR, "v10_history.json")


class StateStore:
    def __init__(self):
        if not os.path.exists(STATE_DIR):
            os.makedirs(STATE_DIR, exist_ok=True)

    def load(self):
        if not os.path.exists(STATE_FILE):
            return {"telemetry": [], "baselines": {}, "events": []}
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"telemetry": [], "baselines": {}, "events": []}

    def save(self, data):
        try:
            with open(STATE_FILE, "w") as f:
                json.dump(data, f)
        except Exception:
            pass


store = StateStore()
