# import requests

# class calculator_tool():
#     def add(self,a,b):
#         return a+b 
#     def subtract(self,a,b):
#         return a-b  
#     def multiply(self,a,b):
#         return a*b
#     def divide(self,a,b):
#         if b==0:
#             return "Division by zero is not allowed"
#         return a/b
# class weather_tool():
#     def __init__(self,api_key):
#         self.api_key=api_key
#     def perform_task(self,city):
#         url=f"https://api.tomorrow.io/v4/timelines?location={city}&fields=temperature,weatherCode&units=metric&timesteps=1d&apikey={self.api_key}"
#         try:
#             res=requests.get(url)    
#             res.raise_for_status()  
#             data=res.json()          
#         except requests.exceptions.RequestException as e:
#             return f"Error fetching weather:{e}"   
#         try:
#             timelines=data.get("data",{}).get("timelines",[])
#             if not timelines:
#                 return "No weather data available" 
#             intervals=timelines[0].get("intervals",[])
#             if not intervals:
#                 return "No intervals found in weather data" 
#             try:
#                 weather_info=intervals[0].get("values",{})
#                 temperature=weather_info.get("temperature","N/A")
#                 weathercode=weather_info.get("weatherCode","N/A") 
#                 return f"Temperature in {city} is {temperature}°C with weather code {weathercode}"
#             except Exception as e:
#                 return f"Error processing weather data: {e}"
#         except Exception as e:
#             return f"Error parsing weather data: {e}" 

# tool.py
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
