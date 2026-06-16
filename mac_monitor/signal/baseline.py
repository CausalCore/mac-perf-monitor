import time
import psutil
from mac_monitor.state.store import store

class BaselineManager:
    def __init__(self):
        self.data = store.load()
        if "baselines" not in self.data:
            self.data["baselines"] = {}

    def _get_time_bucket(self):
        hour = time.localtime().tm_hour
        if 6 <= hour < 12: return "morning"
        if 12 <= hour < 18: return "afternoon"
        if 18 <= hour < 24: return "evening"
        return "night"

    def _get_power_state(self):
        try:
            battery = psutil.sensors_battery()
            return "battery" if battery and not battery.power_plugged else "charger"
        except Exception:
            return "charger"

    def get_current_profile_key(self):
        return f"{self._get_time_bucket()}_{self._get_power_state()}"

    def update_baseline(self, metrics):
        """Updates the baseline for the current profile with new metrics."""
        profile = self.get_current_profile_key()
        
        if profile not in self.data["baselines"]:
            self.data["baselines"][profile] = {
                "cpu": metrics.get("cpu", 0),
                "memory": metrics.get("memory", 0),
                "samples": 1
            }
        else:
            b = self.data["baselines"][profile]
            n = b["samples"]
            # Running average
            b["cpu"] = (b["cpu"] * n + metrics.get("cpu", 0)) / (n + 1)
            b["memory"] = (b["memory"] * n + metrics.get("memory", 0)) / (n + 1)
            b["samples"] = n + 1
            
        store.save(self.data)

    def get_baseline_deviations(self, current_metrics):
        """Returns how much the current metrics deviate from the baseline."""
        profile = self.get_current_profile_key()
        b = self.data["baselines"].get(profile)
        
        if not b or b["samples"] < 3: # Not enough data for baseline yet
            return {"cpu_dev": 0.0, "memory_dev": 0.0, "is_calibrating": True}
            
        return {
            "cpu_dev": current_metrics.get("cpu", 0) - b["cpu"],
            "memory_dev": current_metrics.get("memory", 0) - b["memory"],
            "is_calibrating": False
        }

baseline_manager = BaselineManager()
