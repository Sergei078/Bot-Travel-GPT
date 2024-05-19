import requests
import os
from dotenv import load_dotenv
from code_to_smail import code

load_dotenv()


def getting_the_weather(city: str):
    try:
        params = {
            'q': city,
            'units': 'metric',
            'lang': 'ru',
            'appid': os.getenv('API_WEATHER')
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(url='https://api.openweathermap.org/data/2.5/weather?', params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            temperature = int(data["main"]["temp"])
            pressure = int(data["main"]["pressure"] * 0.750062)
            humidity = data["main"]["humidity"]
            wind = int(data["wind"]["speed"])
            description = str(data['weather'][0]['id'])
            if description in code:
                info_description = code[description]
            else:
                info_description = 'Нет информации.'
            return temperature, pressure, wind, humidity, info_description
        else:
            return 'Ошибка в получении погоды'
    except:
        return 'Ошибка в получении погоды'