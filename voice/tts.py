from elevenlabs.client import ElevenLabs
from yaml import safe_load
from pathlib import Path
from core.state import state
import pygame
import tempfile
import os

pygame.mixer.init()
BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

ELEVEN_LABS_API_KEY = config["ELEVEN_LABS_API_KEY"]
client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)

pygame.mixer.init()


def speak(text: str):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="onwK4e9ZLuTAKqWW03F9",
        model_id="eleven_v3",
        output_format="mp3_44100_128",
    )

    # zapisz do pliku tymczasowego
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        for chunk in audio:
            f.write(chunk)
        tmp_path = f.name

    state.start_speaking()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    state.stop_speaking()
    pygame.mixer.music.unload()
    os.remove(tmp_path)