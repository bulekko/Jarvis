# Jarvis

Jarvis is a voice-controlled personal assistant for automating daily tasks on Windows. Say the wake word, give a command — Jarvis handles the rest.

---

## Requirements

- Windows 10/11
- Python 3.11
- [Ollama](https://ollama.com) with `qwen3:0.6b` model
- Opera GX browser
- ElevenLabs API key
- ffmpeg

---

## Installation

### 1. Install ffmpeg

```bash
winget install ffmpeg
```

or if you have Chocolatey:

```bash
choco install ffmpeg
```

### 2. Clone the repository

```bash
git clone https://github.com/bulekko/Jarvis.git
cd Jarvis
```

### 3. Install Python dependencies

```bash
pip install speechrecognition elevenlabs pynput pygetwindow pywinauto opencv-python pillow numpy pyyaml ollama requests
```

### 4. Install Ollama and pull the model

Download Ollama from [ollama.com](https://ollama.com), then run:

```bash
ollama pull qwen3:0.6b
```

### 5. Configure Opera GX for DevTools

Find your Opera GX shortcut, right-click → **Properties**, and add this flag to the **Target** field:

```
"C:\Users\YOUR_USERNAME\AppData\Local\Programs\Opera GX\launcher.exe" --remote-debugging-port=9222
```

> Opera GX must always be launched using this shortcut for tab detection to work.

### 6. Configure `config/config.yml`

```yaml
ELEVEN_LABS_API_KEY: "your_api_key_here"

Jarvis:
  wake_word: "jarvis"
  sleep_word: "goodbye"
  prefix: "hey"
  no_speech_timeout: 30

Setup:
  microphone_id: 0

utils:
  debug: false
```

To find your microphone ID, run this in Python:

```python
import speech_recognition as sr
for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(i, mic)
```
> You can also run `utils\mic_debug.py`
---

## Running Jarvis

```bash
python main.py
```

---

## Voice Commands

| What you say | What happens |
|---|---|
| `"Jarvis"` | Wakes up Jarvis |
| `"open browser"` | Opens or focuses Opera GX |
| `"open Spotify"` | Opens or focuses Spotify tab |
| `"open YouTube"` | Opens or focuses YouTube tab |
| `"play music"` | Clicks play button on Spotify |
| `"pause music"` | Clicks pause button on Spotify |
| `"open Discord"` | Launches Discord |
| `"open Unity Hub"` | Opens or focuses Unity Hub |
| `"clear"` / `"clean up"` | Minimizes all windows (Win+D) |
| `"clip that"` | Presses F8 (e.g. for game clip) |
| `"shut up"` | Mutes Jarvis until next wake word |
| `"shutdown"` | Closes Jarvis |

---

## Project Structure

```
Jarvis/
├── main.py              # Entry point
├── config/
│   └── config.yml       # All configuration
├── core/
│   ├── orchestrator.py  # Tools, AI brain, command executor
│   └── state.py         # Active/idle/speaking state
├── voice/
│   ├── stt.py           # Speech-to-text (microphone input)
│   └── tts.py           # Text-to-speech (ElevenLabs)
├── utils/
│   └── speaker.py       # Safe speak helper
├── memory/              # Reserved for future memory features
└── assets/
    └── btns/            # Button screenshots for image detection
        ├── spotify_play_btn.png
        └── spotify_pause_btn.png
```

---

## Adding Spotify Button Assets

Jarvis uses image detection to click the play/pause buttons on Spotify Web. You need to take screenshots of those buttons and save them to `assets/btns/`:

- `spotify_play_btn.png` — screenshot of the play button
- `spotify_pause_btn.png` — screenshot of the pause button

Make sure the screenshots are taken at your native resolution.

---

## Adding New Commands

Open `core/orchestrator.py` and add a new tool:

```python
@tool("open_vscode")
def open_vscode():
    windows = [w for w in gw.getAllWindows() if "Visual Studio Code" in w.title]
    if windows:
        app = pywinauto.Application().connect(handle=windows[0]._hWnd)
        app.window(handle=windows[0]._hWnd).set_focus()
        return "Focusing VS Code"
    else:
        subprocess.Popen(r"C:\Path\To\Code.exe")
        return "Opening VS Code"
```

Then add it to the `SYSTEM_PROMPT` in the same file so the AI knows it exists:

```
- open_vscode
```

---

## Debug Mode

Set `debug: true` in `config.yml` to see what Jarvis hears and what the AI responds with in the console.
