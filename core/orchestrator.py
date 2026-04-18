from utils.spotify import spotify_play, spotify_pause, spotify_next, spotify_prev, spotify_current_track
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from pynput.keyboard import Key
from utils.weather import get_weather
from yaml import safe_load
from pathlib import Path
from core.state import state
import pygetwindow as gw
from urllib.parse import quote
import pywinauto
import subprocess
import webbrowser
import threading
import cv2
from PIL import ImageGrab
from datetime import datetime
import numpy as np
import time
import ollama
import json
import requests
import sys
import os


# config
BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

debug = config["utils"]["debug"]
model = config["Jarvis"]["model"]
client_id = config["Spotify"]["client_id"]
client_secret=config["Spotify"]["client_secret"]
redirect_uri=config["Spotify"]["redirect_uri"]
weather_api_key = config["Weather"]["api_key"]

sysUserName = os.getlogin()

keyboard = KeyboardController()
mouse = MouseController()
conversation_history = []

SPOTIFY_ENABLED = client_id != "" and client_secret != ""
SPOTIFY_DISABLED = client_id == "" and client_secret == ""
is_weather_reachable = weather_api_key == ""


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
        subprocess.Popen(r"C:\Users\sysUserName\AppData\Local\Programs\Opera GX\opera.exe" + " --remote-debugging-port=9222")


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


def build_search_url(query: str, engine: str = "google") -> str:
    engines = {
        "google": "https://www.google.com/search?q=",
        "youtube": "https://www.youtube.com/results?search_query=",
        "bing": "https://www.bing.com/search?q=",
    }
    base = engines.get(engine, engines["google"])
    return base + quote(query)


def read_todos():
    try:
        with open(f"{BASE_DIR}\\memory\\TODO", "r") as file:
            lines = file.read().strip().splitlines()
        return lines
    except FileNotFoundError:
        return []

def write_todos(lines: list):
    with open(f"{BASE_DIR}\\memory\\TODO", "w") as file:
        file.write("\n".join(lines))


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


@tool("open_discord")
def open_discord():
    discord_windows = [w for w in gw.getAllWindows() if "Discord" in w.title]
    
    if discord_windows:
        app = pywinauto.Application().connect(handle=discord_windows[0]._hWnd)
        app.window(handle=discord_windows[0]._hWnd).set_focus()
        return "Focusing discord"
    else:
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\Discord\Update.exe")


@tool("open_medal")
def open_medal():
    medal_windows = [w for w in gw.getAllWindows() if "Medal" in w.title]
    
    if medal_windows:
        app = pywinauto.Application().connect(handle=medal_windows[0]._hWnd)
        app.window(handle=medal_windows[0]._hWnd).set_focus()
        return "Focusing Medal"
    else:
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\Medal\app-4.3255.0\Medal.exe")
    

@tool("open_vscode")
def open_vscode():
    vscode_windows = [w for w in gw.getAllWindows() if "Visual Studio Code" in w.title]
    
    if vscode_windows:
        app = pywinauto.Application().connect(handle=vscode_windows[0]._hWnd)
        app.window(handle=vscode_windows[0]._hWnd).set_focus()
        return "Focusing Visual Studio Code"
    else:
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\Programs\Microsoft VS Code\Code.exe")


@tool("open_github_desktop")
def open_github_desktop():
    githubdesktop_windows = [w for w in gw.getAllWindows() if "GitHub Desktop" in w.title]
    
    if githubdesktop_windows:
        app = pywinauto.Application().connect(handle=githubdesktop_windows[0]._hWnd)
        app.window(handle=githubdesktop_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\GitHubDesktop\GitHubDesktop.exe")


@tool("open_gaming_setup")
def open_gaming_setup():
    discord_windows = [w for w in gw.getAllWindows() if "Discord" in w.title]
    medal_windows = [w for w in gw.getAllWindows() if "Medal" in w.title]
    
    if discord_windows:
        app = pywinauto.Application().connect(handle=discord_windows[0]._hWnd)
        app.window(handle=discord_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\Discord\Update.exe")
    
    if medal_windows:
        app = pywinauto.Application().connect(handle=medal_windows[0]._hWnd)
        app.window(handle=medal_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\Medal\app-4.3255.0\Medal.exe")



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
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\GitHubDesktop\GitHubDesktop.exe")
    
    if vscode_windows:
        app = pywinauto.Application().connect(handle=vscode_windows[0]._hWnd)
        app.window(handle=vscode_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\Programs\Microsoft VS Code\Code.exe")
    


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
        subprocess.Popen(rf"C:\Users\{sysUserName}\AppData\Local\GitHubDesktop\GitHubDesktop.exe")

    if unity_windows:
        app = pywinauto.Application().connect(handle=unity_windows[0]._hWnd)
        app.window(handle=unity_windows[0]._hWnd).set_focus()
    else:
        subprocess.Popen(r"C:\Program Files\Unity Hub\Unity Hub.exe")
    


@tool("open_spotify")
def open_spotify():
    open_or_focus_url("https://open.spotify.com")


@tool("pause_music")
def pause_music():
    if SPOTIFY_DISABLED:
        focus_or_open_spotify()
        pos = find_image_on_screen(f"{BASE_DIR}\\assets\\btns\\spotify_pause_btn.png")
        if pos:
            x, y = pos["center"]
            mouse.position = (x, y)
            mouse.click(Button.left)
    else:
        spotify_pause()


@tool("play_music")
def play_music():
    if SPOTIFY_DISABLED:
        focus_or_open_spotify()
        pos = find_image_on_screen(f"{BASE_DIR}\\assets\\btns\\spotify_play_btn.png")
        if pos:
            x, y = pos["center"]
            if debug:
                print(x, y)
            mouse.position = (x, y)
            mouse.click(Button.left)
    else:
        spotify_play()


@tool("next_track")
def next_track():
    if SPOTIFY_ENABLED:
        spotify_next()
    else:
        return "Connect spotify developer app"

@tool("prev_track")
def prev_track():
    if SPOTIFY_ENABLED:
        spotify_prev()
    else:
        return "Connent spotify developer app"

@tool("current_track")
def current_track():
    if SPOTIFY_ENABLED:
        return spotify_current_track()
    else:
        return "Connect spotify developer app"


@tool("clear")
def clear():
    with keyboard.pressed(Key.cmd):
        keyboard.tap('d')


@tool("clip")
def clip():
    keyboard.tap(Key.f8)


@tool("shutdown")
def shutdown():
    sys.exit()


@tool("shutup")
def shutup():
    global conversation_history
    conversation_history = []
    state.deactivate()


@tool("search")
def search(query: str, engine: str = "google"):
    url = build_search_url(query, engine)
    open_or_focus_url(url, sleep_time=3)

@tool("task")
def task():
    lines = read_todos()
    if not lines:
        return "You have no tasks"

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. The user will give you a TODO list with checkboxes. Read it and summarize only the incomplete tasks in a short, natural, spoken sentence. No bullet points, no lists — just talk."
            },
            {
                "role": "user",
                "content": "\n".join(lines)
            }
        ]
    )

    return response["message"]["content"]


@tool("complete_task")
def complete_task(task: str):
    lines = read_todos()
    if not lines:
        return "You have no tasks"

    todos_text = "\n".join([f"{i}: {line}" for i, line in enumerate(lines)])
    
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You will receive a TODO list with line numbers and a task name. Return ONLY the line number of the best matching incomplete task. Return ONLY a single number, nothing else."
            },
            {
                "role": "user",
                "content": f"TODO list:\n{todos_text}\n\nTask to complete: {task}"
            }
        ]
    )

    try:
        index = int(response["message"]["content"].strip())
        if lines[index].startswith("[ ]"):
            lines[index] = lines[index].replace("[ ]", "[x]", 1)
            write_todos(lines)
            return f"Marked as done: {lines[index]}"
        else:
            return "Task already completed"
    except:
        return f"Task not found: {task}"
    

@tool("close_window")
def close_window():
    window = gw.getActiveWindow()
    if window:
        app = pywinauto.Application().connect(handle=window._hWnd)
        app.window(handle=window._hWnd).close()


@tool("close_app")
def close_app(name: str):
    windows = [w for w in gw.getAllWindows() if name.lower() in w.title.lower()]
    if windows:
        app = pywinauto.Application().connect(handle=windows[0]._hWnd)
        app.window(handle=windows[0]._hWnd).close()


@tool("weather")
def weather():
    if is_weather_reachable:
        print(get_weather())
        return get_weather()


@tool("screenshot")
def screenshot():
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"{BASE_DIR}\\screenshots\\{timestamp}.png"
    
    os.makedirs(f"{BASE_DIR}\\screenshots", exist_ok=True)
    
    screenshot = ImageGrab.grab()
    screenshot.save(path)
    
    return "Screenshot taken"


@tool("time")
def current_time():
    now = datetime.now()
    return f"It's {now.strftime('%H:%M')}, {now.strftime('%A, %B %d %Y')}"


# AI prompt
SYSTEM_PROMPT = """
You are a system controller for a desktop AI assistant.

Return ONLY valid JSON array in this format:

[
  {"tool": "tool_name", "args": {}},
  {"tool": "tool_name", "args": {}}
]

Always return an array, even for single commands.

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
- search(query, engine) — search the web, engine can be "google", "youtube", "bing". Default is "google".
    Examples:
    "search cats" → {"tool": "search", "args": {"query": "cats"}}
    "search cats on youtube" → {"tool": "search", "args": {"query": "cats", "engine": "youtube"}}
- task (when user says "what shoud I do?" or "what I have to do?" or "show me my tasks"  ---> "tool": "task")
- complete_task(task) — mark a task as done
    Examples:
    "mark buy milk as done" → {"tool": "complete_task", "args": {"task": "buy milk"}}
    "I did buy milk" → {"tool": "complete_task", "args": {"task": "buy milk"}}
- close_window (aka. "close this", "close current window")
- close_app(name) — close a specific app
    Examples:
    "close discord" → {"tool": "close_app", "args": {"name": "Discord"}}
    "close spotify" → {"tool": "close_app", "args": {"name": "Spotify"}}
- weather (aka. "what's the weather", "how's the weather today")
- screenshot (aka. "take a screenshot", "screenshot")
- time (aka. "what time is it", "what's the date", "what day is it")


If no tool matches, return:
[{"tool": "unknown", "args": {}}]
"""


# AI brain
def ask_model(text: str):
    global conversation_history

    conversation_history.append({"role": "user", "content": text})

    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history
        ]
    )

    reply = response["message"]["content"]

    try:
        actions = json.loads(reply)
        if isinstance(actions, dict):
            actions = [actions]
        tools_done = [a.get("tool") for a in actions if a.get("tool") != "unknown"]
        summary = f"Done: {', '.join(tools_done)}" if tools_done else "No action taken"
    except:
        summary = reply

    conversation_history.append({"role": "assistant", "content": summary})

    return reply


# executor
def execute(action_json: str):
    try:
        actions = json.loads(action_json)

        if isinstance(actions, dict):
            actions = [actions]

        executed_tools = []
        tool_response = None
        threads = []

        for action in actions:
            tool_name = action.get("tool")
            args = action.get("args", {})

            if tool_name in TOOLS:
                executed_tools.append(tool_name)
                t = threading.Thread(target=TOOLS[tool_name], kwargs=args)
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

        if not executed_tools:
            return "Tool not found"

        if "task" in executed_tools:
            tool_response = TOOLS["task"]()

        if tool_response:
            return tool_response

        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, a desktop AI assistant. The user gave a command and these tools were executed. Reply with one short, natural spoken sentence confirming what you did. No lists, no bullet points."
                },
                {
                    "role": "user",
                    "content": f"Executed tools: {', '.join(executed_tools)}"
                }
            ]
        )

        return response["message"]["content"]

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