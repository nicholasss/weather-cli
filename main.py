import typer
from rich.console import Console
import requests
import orjson
import api

app = typer.Typer()

console = Console()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="
# city,state,country
KEY_APPEND = "&appid="  # API KEY
METRIC_APPEND = "&units=metric"


@app.command()
def check_weather(city: str, state: str):
    country: str = "US"  # Hard coding US only

    requests_url = BASE_URL + city + "," + state + "," + \
        country + KEY_APPEND + api.testing_key + METRIC_APPEND

    with console.status("Receiving Weather Data...", spinner="dots"):
        weather_response = requests.get(requests_url).json()

    console.print_json(data=weather_response)
    print(f"Coordinates: {return_coords(weather_response)}")
    print(f"Current Temp: {return_curr_temp(weather_response)}°C")
    print(f"Feels Like: {return_feelslike_temp(weather_response)}°C")


def return_coords(json_object):
    coord_object = json_object["coord"]
    return (coord_object["lat"], coord_object["lon"])


def return_curr_temp(json_object):
    return json_object["main"]["temp"]


def return_feelslike_temp(json_object):
    return json_object["main"]["feels_like"]


if __name__ == "__main__":
    app()
