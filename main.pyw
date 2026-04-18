import ctypes
ctypes.windll.ole32.CoInitializeEx(None, 0x0)

import pygame
pygame.mixer.init()

import speech_recognition as sr
from voice.stt import listen
from voice.tts import speak
from core.orchestrator import handle_command
from core.state import state
from ui.overlay import Overlay
from yaml import safe_load
from pathlib import Path
import threading
import logging
import time
import sys
import os

BASE_DIR = Path(__file__).parent

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.stdout = open("debug.log", "a", encoding="utf-8")
sys.stderr = open("debug.log", "a", encoding="utf-8")

logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)


# config
with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

prefix = config["Jarvis"]["prefix"]
wake_word = config["Jarvis"]["wake_word"]
mic = config["Setup"]["microphone_id"]

overlay = Overlay()


# logic
def speak_async(text: str):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()

def main_loop():
    while True:
        if state.speaking():
            time.sleep(0.1)
            continue

        if not state.is_active():
            overlay.set_idle()
            text = listen()
        else:
            overlay.set_listening()
            text = listen()

        if not text:
            continue

        if wake_word in text:
            state.activate()
            overlay.set_speaking("What can I do for you?")
            speak_async("What can I do for you?")
            continue

        overlay.set_thinking()
        response = handle_command(text)

        if response:
            overlay.set_speaking(response)
            speak_async(response)
        else:
            overlay.set_idle()

threading.Thread(target=main_loop, daemon=True).start()
overlay.run()