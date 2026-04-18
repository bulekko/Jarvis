from TTS.api import TTS
from yaml import safe_load
from pathlib import Path
from core.state import state
import pygame
import tempfile
import os

BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)


def speak(text: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        tmp_path = f.name

    tts.tts_to_file(text=text, file_path=tmp_path)

    state.start_speaking()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    state.stop_speaking()
    pygame.mixer.music.unload()
    os.remove(tmp_path)