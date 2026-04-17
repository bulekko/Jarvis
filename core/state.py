import time
from yaml import safe_load
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


# config
with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

no_speech_timeout = config["Jarvis"]["no_speech_timeout"]


# logic
class State:
    def __init__(self):
        self.mode = "idle"
        self.last_active_time = None
        self.timeout = no_speech_timeout
        self.is_speaking = False

    # --- MODE ---
    def is_idle(self):
        if self.mode == "idle":
            return True
        else:
            return False

    def is_active(self):
        if self.mode == "active":
            return True
        else:
            return False

    def activate(self):
        self.mode = "active"
        self.last_active_time = time.time()

    def deactivate(self):
        self.mode = "idle"
        self.last_active_time = None

    # --- SPEAKING ---
    def start_speaking(self):
        self.is_speaking = True

    def stop_speaking(self):
        self.is_speaking = False

    def speaking(self):
        return self.is_speaking

    # --- TIMEOUT ---
    def update_activity(self):
        self.last_active_time = time.time()

    def check_timeout(self):
        if self.is_active() and self.last_active_time:
            if time.time() - self.last_active_time > self.timeout:
                self.deactivate()
                return True
        return False