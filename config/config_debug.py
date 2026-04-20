from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.yml"

content = r"""
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
"""
def rewrite_config():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(content)