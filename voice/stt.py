import speech_recognition as sr
from yaml import safe_load
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


# config
with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

mic = config["Setup"]["microphone_id"]
debug = config["utils"]["debug"]


# variables
recognizer = sr.Recognizer()


# logic
#def listen():
#    mic_index = mic
#    
#    with sr.Microphone(device_index=mic_index) as source:
#        #recognizer.adjust_for_ambient_noise(source, duration=0.5)
#        audio = recognizer.listen(source)
#    try:
#        text = recognizer.recognize_google(audio, language="en-US")
#        return text
#    except sr.UnknownValueError:
#        return None
#    except sr.RequestError as e:
#        print(f"STT error: {e}")
#        #return None

def listen():
    recognizer = sr.Recognizer()

    if debug:
        print("LISTEN START")

    with sr.Microphone() as source:
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

if __name__ == "__main__":
    while debug:
        print(listen())