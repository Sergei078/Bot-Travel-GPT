from datetime import datetime

import requests

from code_to_smail import code
from config import API_WEATHER
from log import logger


def getting_the_weather(city):
    try:
        params = {
            'q': city,
            'units': 'metric',
            'lang': 'ru',
            'appid': API_WEATHER
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(url='https://api.openweathermap.org/data/2.5/weather?', params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            temperature = int(data["main"]["temp"])
            humidity = data["main"]["humidity"]
            wind = int(data["wind"]["speed"])
            description = str(data['weather'][0]['id'])
            if description in code:
                info_description = code[description]
            else:
                info_description = 'Нет информации.'
            return temperature, wind, humidity, info_description
        else:
            return 'Ошибка в получении погоды'
    except Exception as e:
        logger.error(f'ошибка погоды: {e}')
        return 'Ошибка в получении погоды'


def getting_the_weather_tomorrow(city):
    try:
        params = {
            'q': city,
            'units': 'metric',
            'lang': 'ru',
            'appid': API_WEATHER
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(url='https://api.openweathermap.org/data/2.5/forecast?', params=params,
                                headers=headers)

        if response.status_code == 200:
            data = response.json()
            forecasts = data['list']
            tomorrow = forecasts[8]
            for forecast in forecasts:
                if forecast['dt_txt'].split()[1] == '12:00:00':
                    tomorrow = forecast
                    break
            temperature_tomorrow = int(tomorrow['main']['temp'])
            tomorrow_feels = int(tomorrow['main']['feels_like'])
            tomorrow_humidity = int(tomorrow['main']['humidity'])
            pressure_tomorrow = int(tomorrow['main']['pressure'] * 0.750062)
            wind_speed_tomorrow = tomorrow['wind']['speed']
            description = str(tomorrow['weather'][0]['id'])
            if description in code:
                info_description = code[description]
            else:
                info_description = 'Нет информации.'
            weather_response_info = (f"<b>Погода на завтра🌅\n</b>"
                                     f"Локация: <b>{city}📍\n\n</b>"
                                     f" · <b>{info_description}</b>\n"
                                     f" · Температура: <b>{temperature_tomorrow}</b> °C\n"
                                     f" · Ощущается: <b>{tomorrow_feels}</b> °C\n"
                                     f" · Давление: <b>{pressure_tomorrow}</b> мм рт.ст\n"
                                     f" · Порывы ветра: <b>{wind_speed_tomorrow}</b> м/с\n"
                                     f" · Влажность: <b>{tomorrow_humidity}</b> %\n\n"
                                     f"<b>Данные из OpenWeather🌥</b>")
            return weather_response_info
        else:
            return 'Произошла ошибка!'
    except Exception as e:
        logger.error(f'ошибка погоды: {e}')
        return 'Ошибка в получении погоды'


def getting_the_weather_five_day(city):
    try:
        params = {
            'q': city,
            'units': 'metric',
            'lang': 'ru',
            'appid': API_WEATHER
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(url='https://api.openweathermap.org/data/2.5/forecast?', params=params,
                                headers=headers)

        if response.status_code == 200:
            data = response.json()
            weather_message = f'Локация: <b>{city}</b> 📍\n\n'
            day_count = 0
            for forecast in data['list']:
                date_time = datetime.fromisoformat(forecast['dt_txt'])
                if date_time.hour != 12:
                    continue
                dt = datetime.fromisoformat(datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%dT%H:%M:%S.%f'))
                temperature = int(forecast['main']['temp'])
                humidity = int(forecast['main']['humidity'])
                pressure = int(forecast['main']['pressure'] * 0.750062)
                description = str(forecast['weather'][0]['id'])
                if description in code:
                    info_description = code[description]
                else:
                    info_description = 'Нет информации.'
                data_five_day = dt.strftime("%Y-%m-%d - %H:%M")
                weather_message += f"<b>{data_five_day}🕰</b>\n"
                weather_message += f"\t\t· <b>{info_description}</b>\n"
                weather_message += f"\t\t· Температура: <b>{temperature}</b> °C\n"
                weather_message += f"\t\t· Влажность: <b>{humidity}</b> %\n"
                weather_message += f"\t\t· Давление: <b>{pressure}</b> мм рт.ст\n"
                weather_message += "--------------------------------------------\n"
                day_count += 1
                if day_count >= 5:
                    break
            weather_message += '\n<b>Данные из OpenWeather🌥</b>'
            return weather_message
        else:
            return 'Произошла ошибка!'
    except Exception as e:
        logger.error(f'ошибка погоды: {e}')
        return 'Ошибка в получении погоды'
