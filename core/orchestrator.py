from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from pynput.keyboard import Key
from yaml import safe_load
from pathlib import Path
from core.state import state
import pygetwindow as gw
import pywinauto
import subprocess
import webbrowser
import cv2
from PIL import ImageGrab
import numpy as np
import time
import ollama
import json
import requests
import sys


# config
BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

debug = config["utils"]["debug"]

keyboard = KeyboardController()
mouse = MouseController()


# functions
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


def focus_or_open_spotify():
    open_or_focus_url("https://open.spotify.com")


def get_opera_spotify_tab():
    try:
        tabs = requests.get("http://localhost:9222/json").json()
        return next((t for t in tabs if "open.spotify.com" in t.get("url", "")), None)
    except:
        return None

  
def open_opera():
    opera_windows = [w for w in gw.getAllWindows() if "Opera" in w.title]
    
    if opera_windows:
        app = pywinauto.Application().connect(handle=opera_windows[0]._hWnd)
        app.window(handle=opera_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\Programs\Opera GX\opera.exe" + " --remote-debugging-port=9222")


def open_or_focus_url(url: str, sleep_time: int = 6):
    opera_windows = [w for w in gw.getAllWindows() if "Opera" in w.title]

    if not opera_windows:
        webbrowser.open(url)
        time.sleep(sleep_time)
        return

    try:
        tabs = requests.get("http://localhost:9222/json").json()
        tab = next((t for t in tabs if url in t.get("url", "")), None)
    except:
        tab = None

    if tab:
        tab_title = tab.get("title", "")
        opera_window = next((w for w in opera_windows if tab_title in w.title), None)

        if opera_window:
            app = pywinauto.Application().connect(handle=opera_window._hWnd)
            app.window(handle=opera_window._hWnd).set_focus()
            time.sleep(1)
    else:
        webbrowser.open_new_tab(url)
        time.sleep(sleep_time)


# tool system
TOOLS = {}

def tool(name):
    def wrapper(func):
        TOOLS[name] = func
        return func
    return wrapper


# actions
@tool("open_browser")
def open_browser():
    open_opera()
    return "Opening browser"


@tool("open_youtube")
def open_youtube():
    open_or_focus_url("https://youtube.com")


@tool("open_github")
def open_github():
    open_or_focus_url("https://github.com")


@tool("open_unityhub")
def open_unityhub():
    unity_windows = [w for w in gw.getAllWindows() if "Unity Hub" in w.title]
    
    if unity_windows:
        app = pywinauto.Application().connect(handle=unity_windows[0]._hWnd)
        app.window(handle=unity_windows[0]._hWnd).set_focus()
        return "Focusing Unity Hub"
    else:
        subprocess.Popen(r"C:\Program Files\Unity Hub\Unity Hub.exe")
        return "Opening Unity Hub"
    

@tool("open_discord")
def open_discord():
    discord_windows = [w for w in gw.getAllWindows() if "Discord" in w.title]
    
    if discord_windows:
        app = pywinauto.Application().connect(handle=discord_windows[0]._hWnd)
        app.window(handle=discord_windows[0]._hWnd).set_focus()
        return "Focusing discord"
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\Discord\Update.exe")
        return "Opening discord"


@tool("open_medal")
def open_medal():
    medal_windows = [w for w in gw.getAllWindows() if "Medal" in w.title]
    
    if medal_windows:
        app = pywinauto.Application().connect(handle=medal_windows[0]._hWnd)
        app.window(handle=medal_windows[0]._hWnd).set_focus()
        return "Focusing Medal"
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\Medal\app-4.3255.0\Medal.exe")
        return "Opening medal"
    

@tool("open_vscode")
def open_vscode():
    vscode_windows = [w for w in gw.getAllWindows() if "Visual Studio Code" in w.title]
    
    if vscode_windows:
        app = pywinauto.Application().connect(handle=vscode_windows[0]._hWnd)
        app.window(handle=vscode_windows[0]._hWnd).set_focus()
        return "Focusing Visual Studio Code"
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        return "Opening Visual Studio Code"


@tool("open_github_desktop")
def open_github_desktop():
    githubdesktop_windows = [w for w in gw.getAllWindows() if "GitHub Desktop" in w.title]
    
    if githubdesktop_windows:
        app = pywinauto.Application().connect(handle=githubdesktop_windows[0]._hWnd)
        app.window(handle=githubdesktop_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\GitHubDesktop\GitHubDesktop.exe")
        return "Opening github desktop"


@tool("open_gaming_setup")
def open_gaming_setup():
    discord_windows = [w for w in gw.getAllWindows() if "Discord" in w.title]
    medal_windows = [w for w in gw.getAllWindows() if "Medal" in w.title]
    
    if discord_windows:
        app = pywinauto.Application().connect(handle=discord_windows[0]._hWnd)
        app.window(handle=discord_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\Discord\Update.exe")
    
    if medal_windows:
        app = pywinauto.Application().connect(handle=medal_windows[0]._hWnd)
        app.window(handle=medal_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\Medal\app-4.3255.0\Medal.exe")

    return "Opening gaming setup"


@tool("open_coding_setup")
def open_coding_setup():
    open_or_focus_url("https://github.com")
    open_or_focus_url("https://open.spotify.com")

    githubdesktop_windows = [w for w in gw.getAllWindows() if "github desktop" in w.title]
    vscode_windows = [w for w in gw.getAllWindows() if "Visual Studio Code" in w.title]
    
    if githubdesktop_windows:
        app = pywinauto.Application().connect(handle=githubdesktop_windows[0]._hWnd)
        app.window(handle=githubdesktop_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\GitHubDesktop\GitHubDesktop.exe")
    
    if vscode_windows:
        app = pywinauto.Application().connect(handle=vscode_windows[0]._hWnd)
        app.window(handle=vscode_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\Programs\Microsoft VS Code\Code.exe")
    
    return "Opening coding setup"


@tool("open_unity_setup")
def open_unity_setup():
    open_or_focus_url("https://github.com")
    open_or_focus_url("https://open.spotify.com")

    githubdesktop_windows = [w for w in gw.getAllWindows() if "github desktop" in w.title]
    unity_windows = [w for w in gw.getAllWindows() if "Unity Hub" in w.title]
    
    if githubdesktop_windows:
        app = pywinauto.Application().connect(handle=githubdesktop_windows[0]._hWnd)
        app.window(handle=githubdesktop_windows[0]._hWnd).set_focus()
        return "Focusing github desktop"
    else:
        subprocess.Popen(r"C:\Users\raubo\AppData\Local\GitHubDesktop\GitHubDesktop.exe")

    if unity_windows:
        app = pywinauto.Application().connect(handle=unity_windows[0]._hWnd)
        app.window(handle=unity_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(r"C:\Program Files\Unity Hub\Unity Hub.exe")
    
    return "Opening unity setup"


@tool("open_spotify")
def open_spotify():
    open_or_focus_url("https://open.spotify.com")
    return "Opening Spotify"


@tool("pause_music")
def pause_music():
    focus_or_open_spotify()
    pos = find_image_on_screen(f"{BASE_DIR}\\assets\\btns\\spotify_pause_btn.png")
    if pos:
        x, y = pos["center"]
        mouse.position = (x, y)
        mouse.click(Button.left)
    return "Pausing music"


@tool("play_music")
def play_music():
    focus_or_open_spotify()
    pos = find_image_on_screen(f"{BASE_DIR}\\assets\\btns\\spotify_play_btn.png")
    if pos:
        x, y = pos["center"]
        if debug:
            print(x, y)
        mouse.position = (x, y)
        mouse.click(Button.left)
    return "Playing music"


@tool("clear")
def clear():
    with keyboard.pressed(Key.cmd):
        keyboard.tap('d')
    return "Cleaning up"


@tool("clip")
def clip():
    keyboard.tap(Key.f8)
    return "Clipping that"


@tool("shutdown")
def shutdown():
    sys.exit()


@tool("shutup")
def shutup():
    state.deactivate()


# AI prompt
SYSTEM_PROMPT = """
You are a system controller for a desktop AI assistant.

Return ONLY valid JSON in this format:

{
  "tool": "tool_name",
  "args": {}
}

Available tools:
- open_browser
- open_spotify
- pause_music
- play_music
- shutdown
- shutup ("tool": "shutup")
- open_youtube
- clip (aka. "Javis, clip that shit")
- open_github ("tool": "open_github")
- open_unityhub
- open_medal
- clear (aka. "clean it up")
- open_discord
- open_vscode (aka. "open Visual Studio")
- open_github_desktop
- open_gaming_setup
- open_coding_setup ("tool": "open_coding_setup")
- open_unity_setup

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
        args = action.get("args", {})

        if tool_name in TOOLS:
            return TOOLS[tool_name](**args)

        return "Tool not found"

    except Exception as e:
        if debug:
            print("Execution error:", e)
        return "Invalid AI response"


# main orchestrator
def handle_command(text: str):
    if state.is_active():
        text = text.lower()
        if debug:
            print("User:", text)
        ai_response = ask_model(text)
        if debug:
            print("AI:", ai_response)
        return execute(ai_response)
    else:
        if debug:
            print("Jarvis is chilling")
        return None