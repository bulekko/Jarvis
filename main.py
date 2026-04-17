import speech_recognition as sr
from voice.stt import listen
from voice.tts import speak
from utils.speaker import safe_speak
from core.orchestrator import handle_command
from core.state import state
from yaml import safe_load
from pathlib import Path
import time
import sys
import os

BASE_DIR = Path(__file__).parent

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# config
with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

prefix = config["Jarvis"]["prefix"]
wake_word = config["Jarvis"]["wake_word"]
mic = config["Setup"]["microphone_id"]


# logic
while True:
    if state.speaking():
        continue

    text = listen()

    if not text:
        continue

    if wake_word in text:
        state.activate()
        speak("What can I do for you?")
        continue

    response = handle_command(text)
    if response:
        speak(response)