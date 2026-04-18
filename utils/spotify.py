import spotipy
from spotipy.oauth2 import SpotifyOAuth
from yaml import safe_load
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config["Spotify"]["client_id"],
    client_secret=config["Spotify"]["client_secret"],
    redirect_uri=config["Spotify"]["redirect_uri"],
    scope="user-modify-playback-state user-read-playback-state"
))


def spotify_play():
    sp.start_playback()

def spotify_pause():
    sp.pause_playback()

def spotify_next():
    sp.next_track()

def spotify_prev():
    sp.previous_track()

def spotify_current_track():
    track = sp.current_playback()
    if track and track["is_playing"]:
        name = track["item"]["name"]
        artist = track["item"]["artists"][0]["name"]
        return f"{name} by {artist}"
    return "Nothing is playing"