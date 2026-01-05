
import requests

class CalculatorTool:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return "Division by zero is not allowed"
        return a / b


class WeatherTool:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.openweathermap.org/data/2.5/weather"

    def perform_task(self, city):
        if not self.api_key:
            return "Weather API key missing"

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            res = requests.get(self.url, params=params)
            res.raise_for_status()
            data = res.json()

            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"Temperature in {city} is {temp}°C with {desc}"

        except Exception as e:
            return f"Weather error: {e}"
