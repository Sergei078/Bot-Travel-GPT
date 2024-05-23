import requests
from config import GEO_TOKEN
import logging

logging.basicConfig(filename='logConfig.log', encoding='utf-8', level=logging.WARNING,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s")
logger = logging.getLogger(__name__)

keys_list = ['city', 'town', 'village', 'state', 'district']


def i_know_where_you_live(lat, long):
    try:
        headers = {'Accept-Language': 'ru'}
        req = requests.get(
            f'https://eu1.locationiq.com/v1/reverse.php?key={GEO_TOKEN}&lat={lat}&lon={long}&format=json',
            headers=headers).json()

        # req['req']['county_code'] - код страны по стандарту ISO 3166-1 alpha-2, поможет определить язык?

        city = 'не найдено'
        for key in keys_list:
            if key in req['address']:
                city = req['address'].get(key)

        country = req['address'].get('country')
        if req.status_code == 200:
            return True, city, country
        else:
            logger.error(req.status_code)
            return False, f'ошибка в получении геоданных'

    except Exception as e:
        logger.error(f'ошибка: {e}')
        return False, 'что то пошло не так'
