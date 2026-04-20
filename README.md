# Jarvis

Jarvis is a voice-controlled personal assistant for automating daily tasks on Windows. Say the wake word, give a command — Jarvis handles the rest.

---

## Requirements

- Windows 10/11
- Python 3.11
- [Ollama](https://ollama.com) with `llama3.2:3b` model
- opera_gx, chrome, firefox or edge browser
- Spotify Premium + Developer account (optional)
- OpenWeatherMap API key (optional)
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
pip install speechrecognition openai-whisper pynput pygetwindow pywinauto opencv-python pillow numpy pyyaml ollama requests spotipy pygame customtkinter pystray TTS
```

### 4. Install Ollama and pull the model

Download Ollama from [ollama.com](https://ollama.com), then run:

```bash
ollama pull llama3.2:3b
```

### 5. Configure Opera GX for DevTools

Find your Opera GX shortcut, right-click -> Properties, and add this flag to the Target field:

```
"C:\Users\YOUR_USERNAME\AppData\Local\Programs\Opera GX\launcher.exe" --remote-debugging-port=9222
```

> Opera GX must always be launched using this shortcut for tab detection to work.

### 6. Configure `config/config.yml`

```yaml
Jarvis:
  prefix: "Jarvis"
  wake_word: "Hello Jarvis"
  no_speech_timeout: 15
  energy_threshold: 4000  # more = less ambient noise
  model: "llama3.2:3b"
  whisper_model: "medium"
  language: "en"          # language of Jarvis responses (en, pl, de, fr, etc.)
  personality: "You are Jarvis, a smart and slightly sarcastic AI assistant. You are helpful, efficient, and occasionally witty."
  # “You are a formal British butler named Jarvis.” — formal and elegant
  # “You are a friendly and enthusiastic assistant.” — enthusiastic
  # “You are a concise assistant. Keep all responses under 10 words.” — very brief

Spotify:
  client_id: ""
  client_secret: ""
  redirect_uri: "http://127.0.0.1:8888/callback"

Weather:
  api_key: ""
  city: "London"
  units: "metric"

Setup:
  microphone_id: 1

TTS:
  engine: "TTS"                                 # "TTS" or "elevenlabs"
  model: "tts_models/en/ljspeech/tacotron2-DDC" # you can also use "tts_models/en/vctk/vits", but its heavier

  volume: 1.0                                   # 0.0 - 1.0
  
  ELEVEN_LABS_API_KEY: ""
  elevenlabs_voice_id: "onwK4e9ZLuTAKqWW03F9"
  elevenlabs_model: "eleven_v3"

STT:
  language: "en"          # recognition language
  phrase_time_limit: 5    # maximum recording length in seconds
  volume_threshold: 0.01  # below this value, RMS = silence/noise; ignore
  pause_threshold: 0.5    # number of seconds of silence = end of command

Overlay:
  size: 64                # window and circle size in pixels
  position_x: 100         # distance from the right edge of the screen
  position_y: 100         # distance from the bottom edge of the screen
  opacity: 1.0            # transparency 0.0–1.0 (you have to use decimals)
  color_idle: "#626262"
  color_listening: "#00C864"
  color_thinking: "#FFB300"
  color_speaking: "#0096FF"

Gesture:
  camera_index: 0           # camera index (0 = default)
  detection_confidence: 0.7 # hand detection confidence 0.0 - 1.0
  tracking_confidence: 0.7  # hand tracking confidence 0.0 - 1.0
  mouse_smoothing: 0.05     # mouse movement smoothness (lower = smoother but slower)
  click_delay: 0.3          # time between clicks in seconds
  scroll_delay: 0.1         # time between scrolls in seconds
  scroll_speed: 5           # how many units scroll per gesture

Browser:
  type: "opera_gx"        # "opera_gx", "chrome", "firefox", "edge"
  debugging_port: 9222    # port for DevTools (opera_gx and chrome only)
  paths:
    opera_gx: 'C:\Users\YOUR_USERNAME\AppData\Local\Programs\Opera GX\opera.exe' # leave empty if you don't have
    chrome: 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    firefox: 'C:\Program Files\Mozilla Firefox\firefox.exe'
    edge: 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'


Apps: # paths to your .exe files
  discord: 'C:\Users\YOUR_USER_NAME\AppData\Local\Discord\Update.exe'
  medal: 'C:\Users\YOUR_USER_NAME\AppData\Local\Medal\Medal.exe'
  vscode: 'C:\Users\YOUR_USER_NAME\AppData\Local\Programs\Microsoft VS Code\Code.exe'
  unity_hub: 'C:\Program Files\Unity Hub\Unity Hub.exe'
  Github_desktop: 'C:\Users\YOUR_USER_NAME\AppData\Local\GitHubDesktop\GitHubDesktop.exe'

utils:
  debug: false
  javris_location: "C:\Users\YOUR_USER_NAME\Jarvis"
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
pythonw main.pyw
```

Or double-click `main.pyw` — no console window will appear.

---

## Voice Commands

| What you say | What happens |
|---|---|
| `"open browser"` | Opens or focuses Opera GX |
| `"open Spotify"` | Opens or focuses Spotify tab |
| `"open YouTube"` | Opens or focuses YouTube tab |
| `"open Discord"` | Opens or focuses Discord |
| `"open Unity Hub"` | Opens or focuses Unity Hub |
| `"open VS Code"` | Opens or focuses Visual Studio Code |
| `"open GitHub Desktop"` | Opens or focuses GitHub Desktop |
| `"open Medal"` | Opens or focuses Medal | #
| `"gaming setup"` | Opens Discord and Medal | #
| `"coding setup"` | Opens VS Code, GitHub Desktop, GitHub and Spotify |
| `"unity setup"` | Opens Unity Hub, GitHub Desktop, GitHub and Spotify |
| `"play music"` | Plays music on Spotify |
| `"pause music"` | Pauses music on Spotify |
| `"next song"` / `"skip"` | Skips to next track (requires Spotify API) |
| `"previous song"` | Goes to previous track (requires Spotify API) |
| `"what's playing"` | Says current track name (requires Spotify API) |
| `"search [query]"` | Searches on Google |
| `"search [query] on YouTube"` | Searches on YouTube |
| `"search [query] on Bing"` | Searches on Bing |
| `"what's the weather"` | Says current weather (requires OpenWeatherMap) |
| `"what should I do today"` | Reads your TODO list |
| `"mark [task] as done"` | Marks a task as completed |
| `"what time is it"` | Says current time and date |
| `"take a screenshot"` | Saves screenshot to screenshots/ folder |
| `"clear"` / `"clean up"` | Minimizes all windows (Win+D) |
| `"close this"` | Closes the active window |
| `"close [app]"` | Closes a specific app |
| `"clip that"` | Presses F8 (e.g. for game clip) |
| `"shut up"` | Mutes Jarvis until next wake word |
| `"goodbye"` / `"bye"` | Closes Jarvis |
| `"Where are you?"` | Opens github page |

---

## Project Structure

```
Jarvis/
├── main.pyw                 # Entry point (no console window)
├── config/
│   └── config.yml           # All configuration
├── core/
│   ├── orchestrator.py      # Tools, AI brain, command executor
│   └── state.py             # Active/idle/speaking state
├── voice/
│   ├── stt.py               # Speech-to-text (Whisper)
│   └── tts.py               # Text-to-speech (Coqui TTS or ElevenLabs)
├── ui/
│   └── overlay.py           # Floating status overlay + system tray
├── utils/
│   ├── spotify.py           # Spotify API integration
│   ├── weather.py           # OpenWeatherMap integration
│   └── mic_debug.py         # Microphone ID finder
├── memory/
│   └── TODO                 # Task list
├── screenshots/             # Saved screenshots
└── assets/
    └── btns/                # Button screenshots for image detection fallback
        ├── spotify_play_btn.png
        └── spotify_pause_btn.png
```

---

## Overlay UI

Jarvis displays a small floating overlay in the bottom-right corner of the screen showing the current status:

- Gray / Sleeping — waiting for wake word
- Green / Listening — active and listening for commands
- Yellow / Thinking — processing command
- Blue / Speaking — Jarvis is talking

The overlay can be dragged anywhere on the screen. It can be minimized to the system tray by closing the window, and restored by clicking the tray icon.

---

## TTS Options

By default Jarvis uses Coqui TTS which works fully offline. On first run it will download the model (~200MB automatically).

---

## Spotify API Setup (optional, requires Spotify Premium)

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Click Create App
3. Set Redirect URI to `http://127.0.0.1:8888/callback`
4. Copy Client ID and Client Secret to `config.yml`

On first run, a browser window will open asking you to log in to Spotify. After that, the token is saved locally and won't be asked again.

Without Spotify API, play/pause falls back to image detection on Spotify Web.

---

## Weather Setup (optional)

1. Register at [openweathermap.org](https://openweathermap.org)
2. Copy your API key to `config.yml`
3. Set your city and units (`metric` / `imperial`)

---

## TODO List

Edit `memory/TODO` manually using this format:

```
[ ] buy milk
[ ] call mom
[x] finish project
```

Jarvis will only read incomplete tasks and you can mark them as done with your voice.

---

## Adding Spotify Button Assets

Used as fallback when Spotify API is not configured. Take screenshots of the play/pause buttons on Spotify Web and save them to `assets/btns/`:

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
    else:
        subprocess.Popen(r"C:\Path\To\Code.exe")
```

Then add it to `SYSTEM_PROMPT` in the same file so the AI knows it exists:

```
- open_vscode
```

---

## Debug Mode

Set `debug: true` in `config.yml` to write logs to `debug.log` in the project root.
