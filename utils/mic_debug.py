import speech_recognition as sr
import logging

r = sr.Recognizer()

for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Testing mic {i}: {name}")
    
    try:
        with sr.Microphone(device_index=i) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Say something...")
            audio = r.listen(source, timeout=3)
            print("OK\n")
    except Exception as e:
        logging.debug(f"Failed: {e}\n")