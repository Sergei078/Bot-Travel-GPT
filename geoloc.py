import requests

from config import GEO_TOKEN
from log import logger

keys_list = ['city', 'village', 'town', 'state', 'district']


def i_know_where_you_live(lat, long):
    try:
        headers = {'Accept-Language': 'ru'}
        req = requests.get(
            f'https://eu1.locationiq.com/v1/reverse.php?key={GEO_TOKEN}&lat={lat}&lon={long}&format=json&zoom=400',
            headers=headers)

        # req['req']['county_code'] - код страны по стандарту ISO 3166-1 alpha-2, поможет определить язык?
        req_js = req.json()

        city = 'не найдено'
        for key in keys_list:
            if key in req_js['address']:
                city = req_js['address'].get(key)
                break

        country = req_js['address'].get('country')
        if req.status_code == 200:
            return city, country
        else:
            logger.error(req.status_code)
            return f'ошибка в получении геоданных'

    except Exception as e:
        logger.error(f'ошибка: {e}')
        return False, 'что то пошло не так'


def you_know_where_you_live(city):
    try:
        headers = {'Accept-Language': 'ru'}
        address = requests.get(
            f'https://eu1.locationiq.com/v1/search?key={GEO_TOKEN}&q={city}&format=json',
            headers=headers).json()
        capital = address[0]['display_name']
        return capital
    except Exception as e:
        err_msg = f'ошибка в геолокации'
        logger.error(err_msg + str(e))
        return err_msg
