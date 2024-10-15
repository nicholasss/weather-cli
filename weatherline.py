import typer
from rich.console import Console
from rich.padding import Padding
import requests
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta
import orjson
import api

app = typer.Typer(no_args_is_help=True,
                  help="""Check Weather with the OpenWeatherMap API\n
                  Not designed for international usage.\n
                  Will be coming in a future update.""")

console = Console()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="
# city,state,country
KEY_APPEND = "&appid="  # API KEY
METRIC_APPEND = "&units=metric"


CONFIG_FILE = "./weatherline.config"


@app.callback("check", invoke_without_command=True)
def check_weather(city: str, state: str):
    """
    Check the weather of a given location.
    """
    country: str = "US"  # Hard coding US only
    requests_url = BASE_URL + city + "," + state + "," + \
        country + KEY_APPEND + api.testing_key + METRIC_APPEND

    with console.status("Receiving Weather Data...", spinner="dots"):
        weather_response = requests.get(requests_url).json()

    console.print_json(data=weather_response)

    console.rule(f"[bold]Current Weather in {weather_response["name"]} {
                 __return_country_code(weather_response)}")

    console.print(f"Coordinates: {__return_coords(weather_response)}")
    console.print(f"Current Temp: {__return_curr_temp(weather_response)}°C")
    console.print(f"Feels Like: {__return_feelslike_temp(weather_response)}°C")
    console.print(f"Current Time: {__current_local_time(weather_response)} ({
                  __return_timezone(weather_response)})")
    console.print(f"Local Sunrise Time: {
                  __return_local_sunrise(weather_response)}")
    console.print(f"Local Sunset Time: {
                  __return_local_sunset(weather_response)}")


@app.command()
def config(status: str, setting: str):
    """
    Set or show configuration.
    """
    pass


# Location and helper functions
def __return_coords(json_object):
    coord_object = json_object["coord"]
    return (coord_object["lat"], coord_object["lon"])


def __return_country_code(json_object):
    return json_object["sys"]["country"]


def __return_timezone(json_object):
    local_timezone = tz(timedelta(seconds=json_object["timezone"]))
    return local_timezone.tzname(dt.now())


# Temperature and helper functions
def __return_curr_temp(json_object):
    return json_object["main"]["temp"]


def __return_feelslike_temp(json_object):
    return json_object["main"]["feels_like"]


# Timezone and helper functions
def __current_local_time(json_object):
    current_time = dt.now(tz=tz(timedelta(seconds=json_object["timezone"])))
    return __time_format(current_time)


def __return_local_sunrise(json_object):
    sunrise_time = __unix_to_utc(json_object["sys"]["sunrise"])
    return __utc_to_local(sunrise_time, json_object)


def __return_local_sunset(json_object):
    sunset_time = __unix_to_utc(json_object["sys"]["sunset"])
    return __utc_to_local(sunset_time, json_object)


def __utc_to_local(datetime_object, json_object):
    local_time = datetime_object.astimezone(
        tz=tz(timedelta(seconds=json_object["timezone"])))
    return __time_format(local_time)


def __unix_to_utc(unix_seconds):
    return dt.fromtimestamp(unix_seconds, tz.utc)


def __time_format(datetime_object):
    return datetime_object.strftime("%I:%M:%S %p")


if __name__ == "__main__":
    app()
