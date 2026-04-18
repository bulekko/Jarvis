import requests
from yaml import safe_load
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

api_key = config["Weather"]["api_key"]
city = config["Weather"]["city"]
units = config["Weather"]["units"]


def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
        data = requests.get(url).json()

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return f"In {city} it's {temp}°C, feels like {feels_like}°C, {description}, humidity {humidity}%"
    except:
        return "Couldn't fetch weather"