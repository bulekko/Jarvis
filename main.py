import speech_recognition as sr
from voice.stt import listen
from voice.tts import speak
from utils.speaker import safe_speak
from core.orchestrator import handle_command
from core.state import State
from yaml import safe_load
from pathlib import Path
import time
import sys
import os

state = State()
BASE_DIR = Path(__file__).parent

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# config
with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

prefix = config["Jarvis"]["prefix"]
wake_word = config["Jarvis"]["wake_word"]
sleep_word = config["Jarvis"]["sleep_word"]
mic = config["Setup"]["microphone_id"]


# logic
while True:
    if state.speaking():
        continue

    text = listen()

    if not text:
        continue

    # wake word
    if wake_word in text:
        state.activate()
        safe_speak(state, speak, "What can I do for you?")
        time.sleep(2)
        continue

    # shutdown
    if sleep_word in text:
        safe_speak(state, speak, "Shutting down")
        break

    # normal command
    response = handle_command(text)
    safe_speak(state, speak, response)