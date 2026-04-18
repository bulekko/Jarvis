import speech_recognition as sr
from yaml import safe_load
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


# config
with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

mic = config["Setup"]["microphone_id"]
debug = config["utils"]["debug"]
energy_threshold = config["Jarvis"]["energy_threshold"]


# variables
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5
recognizer.energy_threshold = energy_threshold

# logic
def listen():
    if debug:
        print("LISTEN START")

    with sr.Microphone(device_index=mic) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        if debug:
            print("MIC OPEN")
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
        if debug:
            print("AUDIO RECORDED")

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        if debug:
            print(f"Text: {text}")
        return text
    except Exception as e:
        if debug:
            print("ERROR:", e)
        return None