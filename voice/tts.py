from yaml import safe_load
from pathlib import Path
from core.state import state
import pygame
import tempfile
import os
import threading

BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

tts_config = config["TTS"]
engine = tts_config["engine"]
volume = tts_config["volume"]

if engine == "TTS":
    from TTS.api import TTS
    tts = TTS(model_name=tts_config["model"], progress_bar=False)
elif engine == "elevenlabs":
    from elevenlabs.client import ElevenLabs
    tts = ElevenLabs(api_key=tts_config["ELEVEN_LABS_API_KEY"])


def speak(text: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        tmp_path = f.name

    if engine == "TTS":
        tts.tts_to_file(text=text, file_path=tmp_path)

    elif engine == "elevenlabs":
        tmp_path = tmp_path.replace(".wav", ".mp3")
        audio = tts.text_to_speech.convert(
            text=text,
            voice_id=tts_config["elevenlabs_voice_id"],
            model_id=tts_config["elevenlabs_model"],
            output_format="mp3_44100_128",
        )
        with open(tmp_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

    state.start_speaking()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    state.stop_speaking()
    pygame.mixer.music.unload()
    os.remove(tmp_path)

def speak_async(text: str):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()