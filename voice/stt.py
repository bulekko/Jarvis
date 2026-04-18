import speech_recognition as sr
from yaml import safe_load
from pathlib import Path
import whisper
import numpy as np
import logging

BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

mic = config["Setup"]["microphone_id"]
debug = config["utils"]["debug"]
energy_threshold = config["Jarvis"]["energy_threshold"]
whisper_model = config["Jarvis"]["whisper_model"]  # "tiny", "base", "small", "medium"

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5
recognizer.energy_threshold = energy_threshold

model = whisper.load_model(whisper_model)


def listen():
    if debug:
        logging.debug("LISTEN START")

    with sr.Microphone(device_index=mic) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        if debug:
            logging.debug("MIC OPEN")
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
        if debug:
            logging.debug("AUDIO RECORDED")

    try:
        raw = np.frombuffer(
            audio.get_raw_data(convert_rate=16000, convert_width=2),
            np.int16
        ).astype(np.float32) / 32768.0

        result = model.transcribe(raw, language="en", fp16=False)

        text = result["text"].strip()
        if debug:
            logging.debug(f"Text: {text}")
        return text
    except Exception as e:
        if debug:
            logging.debug(f"ERROR: {e}")
        return None