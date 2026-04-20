import cv2
import mediapipe as mp
import pyautogui
import threading
import time
from yaml import safe_load
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

g = config["Gesture"]
camera_index = g["camera_index"]
detection_confidence = g["detection_confidence"]
tracking_confidence = g["tracking_confidence"]
mouse_smoothing = g["mouse_smoothing"]
click_delay = g["click_delay"]
scroll_delay = g["scroll_delay"]
scroll_speed = g["scroll_speed"]

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=detection_confidence,
    min_tracking_confidence=tracking_confidence
)

cap = None
running = False
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False


def fingers_up(landmarks):
    tips = [8, 12, 16, 20]
    fingers = []
    fingers.append(landmarks[4].x < landmarks[3].x)
    for tip in tips:
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)
    return fingers


def get_gesture_name(fingers):
    if fingers[1] and not fingers[2]:
        return "Move mouse"
    elif fingers[1] and fingers[2] and not fingers[3]:
        return "Left click"
    elif fingers[0] and not fingers[1]:
        return "Right click"
    elif fingers[1] and fingers[2] and fingers[3] and fingers[4]:
        return "Scroll up"
    elif not any(fingers):
        return "Scroll down"
    return "Unknown"


def gesture_loop():
    global cap, running
    cap = cv2.VideoCapture(camera_index)

    while running:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            lm = result.multi_hand_landmarks[0].landmark
            fingers = fingers_up(lm)
            mp_drawing.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

            ix_frame = int(lm[8].x * w)
            iy_frame = int(lm[8].y * h)
            cv2.circle(frame, (ix_frame, iy_frame), 10, (0, 255, 0), -1)

            gesture = get_gesture_name(fingers)
            cv2.putText(frame, gesture, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ix = int(lm[8].x * screen_w)
            iy = int(lm[8].y * screen_h)

            if fingers[1] and not fingers[2]:
                pyautogui.moveTo(ix, iy, duration=mouse_smoothing)
            elif fingers[1] and fingers[2] and not fingers[3]:
                pyautogui.click()
                time.sleep(click_delay)
            elif fingers[0] and not fingers[1]:
                pyautogui.rightClick()
                time.sleep(click_delay)
            elif fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                pyautogui.scroll(scroll_speed)
                time.sleep(scroll_delay)
            elif not any(fingers):
                pyautogui.scroll(-scroll_speed)
                time.sleep(scroll_delay)
        else:
            cv2.putText(frame, "No hand detected", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Jarvis - Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            running = False
            break

    cap.release()
    cv2.destroyAllWindows()


def start_gesture_control():
    global running
    if not running:
        running = True
        if threading.current_thread() is threading.main_thread():
            gesture_loop()
        else:
            threading.Thread(target=gesture_loop, daemon=False).start()


def stop_gesture_control():
    global running
    running = False


if __name__ == "__main__":
    start_gesture_control()