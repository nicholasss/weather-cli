import typer

app = typer.Typer()

@app.command()
def check_weather(city: str):
	print(f"The weather in {city} currently is 63 degress and rainy.")

if __name__ == "__main__":
	app()