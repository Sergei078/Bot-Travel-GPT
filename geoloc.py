import requests
from config import GEO_TOKEN
import logging

logging.basicConfig(filename='logConfig.log', encoding='utf-8', level=logging.WARNING,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s")
logger = logging.getLogger(__name__)


def i_know_where_you_live(lat, long):
    try:
        headers = {'Accept-Language': 'ru'}
        address = requests.get(
            f'https://eu1.locationiq.com/v1/reverse.php?key={GEO_TOKEN}&lat={lat}&lon={long}&format=json',
            headers=headers).json()

        # address['address']['county_code'] - код страны по стандарту ISO 3166-1 alpha-2, поможет определить язык?
        city = address['address'].get('city')
        country = address['address'].get('country')
        if address.status_code == 200:
            return True, city, country
        else:
            logger.error(address.status_code)
            return False, f'ошибка в получении геоданных: {address.status_code}'

    except Exception as e:
        err_msg = f'ошибка: {e}'
        logger.error(err_msg)
        return False, 'что то пошло не так'
