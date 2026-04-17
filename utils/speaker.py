import time

def safe_speak(state, speak_func, text):
    state.start_speaking()
    speak_func(text)
    time.sleep(0.3)
    state.stop_speaking()