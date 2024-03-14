import requests
import os
from dotenv import load_dotenv

def get_weather_info():
    load_dotenv()

    api_key = os.getenv('API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}&units=metric'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_conditions = data['weather'][0]['main']
        cities_weather = {data['name']: weather_conditions}
        return cities_weather
    else:
        return {}