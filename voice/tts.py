from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from yaml import safe_load
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


# config
with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

ELEVEN_LABS_API_KEY = config["ELEVEN_LABS_API_KEY"]


# variables
client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)


# logic
def speak(text: str):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="onwK4e9ZLuTAKqWW03F9",
        model_id="eleven_v3",
        output_format="mp3_44100_128",
    )

    play(audio)