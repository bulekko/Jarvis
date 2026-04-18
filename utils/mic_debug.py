import speech_recognition as sr
import logging

r = sr.Recognizer()

for i, name in enumerate(sr.Microphone.list_microphone_names()):
    logging.debug(f"Testing mic {i}: {name}")
    
    try:
        with sr.Microphone(device_index=i) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            logging.debug("Say something...")
            audio = r.listen(source, timeout=3)
            logging.debug("OK\n")
    except Exception as e:
        logging.debug(f"Failed: {e}\n")