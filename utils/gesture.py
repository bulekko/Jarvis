import cv2
import mediapipe as mp
import pyautogui
import threading
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
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


def gesture_loop():
    global cap, running
    cap = cv2.VideoCapture(0)

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

            ix = int(lm[8].x * screen_w)
            iy = int(lm[8].y * screen_h)

            if fingers[1] and not fingers[2]:
                pyautogui.moveTo(ix, iy, duration=0.05)

            elif fingers[1] and fingers[2] and not fingers[3]:
                pyautogui.click()
                time.sleep(0.3)

            elif fingers[0] and not fingers[1]:
                pyautogui.rightClick()
                time.sleep(0.3)

            elif fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                pyautogui.scroll(3)
                time.sleep(0.1)

            elif not any(fingers):
                pyautogui.scroll(-3)
                time.sleep(0.1)

    cap.release()


def start_gesture_control():
    global running
    if not running:
        running = True
        threading.Thread(target=gesture_loop, daemon=True).start()


def stop_gesture_control():
    global running
    running = False