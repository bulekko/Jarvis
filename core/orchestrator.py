from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from yaml import safe_load
from pathlib import Path
import subprocess
import webbrowser
import cv2
from PIL import ImageGrab
import numpy as np
import time
import ollama
import json


# config
BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

debug = config["utils"]["debug"]

keyboard = KeyboardController()
mouse = MouseController()


# image detection
def find_image_on_screen(template_path, threshold=0.8):
    template = cv2.imread(template_path)
    if template is None:
        if debug:
            print(f"Can't load image: {template_path}")
        return None

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    h, w = template_gray.shape

    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if debug:
        print(f"Matching: {max_val:.3f} (required: {threshold})")

    if max_val >= threshold:
        x, y = max_loc

        return {
            "top_left": (x, y),
            "center": (x + w // 2, y + h // 2),
            "size": (w, h),
            "confidence": max_val
        }

    return None


# tool system
TOOLS = {}

def tool(name):
    def wrapper(func):
        TOOLS[name] = func
        return func
    return wrapper


# actions
@tool("open_discord")
def open_discord():
    subprocess.Popen("discord")
    return "Opening Discord"


@tool("open_spotify")
def open_spotify():
    webbrowser.open("https://open.spotify.com")
    return "Opening Spotify"


@tool("pause_music")
def pause_music():
    webbrowser.open_new_tab("https://open.spotify.com")

    time.sleep(6)

    pos = find_image_on_screen(
        f"{BASE_DIR}\\assets\\btns\\spotify_pause_btn.png"
    )

    if pos:
        x, y = pos["center"]
        mouse.position = (x, y)
        mouse.click(Button.left)

    return "Pausing music"


@tool("play_music")
def play_music():
    webbrowser.open_new_tab("https://open.spotify.com")

    time.sleep(6)

    pos = find_image_on_screen(
        f"{BASE_DIR}\\assets\\btns\\spotify_play_btn.png"
    )

    if pos:
        x, y = pos["center"]
        if debug:
            print(x, y)
        mouse.position = (x, y)
        mouse.click(Button.left)

    return "Playing music"

# AI prompt
SYSTEM_PROMPT = """
You are a system controller for a desktop AI assistant.

Return ONLY valid JSON in this format:

{
  "tool": "tool_name",
  "args": {}
}

Available tools:
- open_discord
- open_spotify
- pause_music
- play_music

If no tool matches, return:
{
  "tool": "unknown",
  "args": {}
}
"""


# AI brain
def ask_model(text: str):
    response = ollama.chat(
        model="qwen3:0.6b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )

    return response["message"]["content"]


# executor
def execute(action_json: str):
    try:
        action = json.loads(action_json)

        tool_name = action.get("tool")

        if tool_name in TOOLS:
            return TOOLS[tool_name]()

        return "Tool not found"

    except Exception as e:
        if debug:
            print("Execution error:", e)
        return "Invalid AI response"


# main orchestrator
def handle_command(text: str):
    text = text.lower()

    if debug:
        print("User:", text)

    ai_response = ask_model(text)

    if debug:
        print("AI:", ai_response)

    return execute(ai_response)