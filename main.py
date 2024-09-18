import typer
import requests
import orjson
import api

app = typer.Typer()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q=" # city,state,country
KEY_APPEND = "&appid=" # API KEY
METRIC_APPEND = "&units=metric"

@app.command()
def check_weather(city: str, state: str):
	country: str = "US" # Hard coding US only
	
	requests_url = BASE_URL + city + "," + state + "," + country + KEY_APPEND + api.testing_key + METRIC_APPEND

	r = requests.get(requests_url)
	print(r.json())


if __name__ == "__main__":
	app()