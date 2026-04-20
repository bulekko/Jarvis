import spotipy
from spotipy.oauth2 import SpotifyOAuth
from yaml import safe_load
from pathlib import Path
import logging

BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

client_id=config["Spotify"]["client_id"]
client_secret=config["Spotify"]["client_secret"]
redirect_uri=config["Spotify"]["redirect_uri"]
sp = None

if client_id != "" and client_secret != "":
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-modify-playback-state user-read-playback-state"
    ))
else:
    logging.debug("No spotify client_id or client_secret")


def spotify_play():
    if sp:
        sp.start_playback()

def spotify_pause():
    if sp:
        sp.pause_playback()

def spotify_next():
    if sp:
        sp.next_track()

def spotify_prev():
    if sp:
        sp.previous_track()

def spotify_current_track():
    if sp:
        track = sp.current_playback()
        if track and track["is_playing"]:
            name = track["item"]["name"]
            artist = track["item"]["artists"][0]["name"]
            return f"{name} by {artist}"
    return "Nothing is playing"