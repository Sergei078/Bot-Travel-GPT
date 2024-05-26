import random

import requests

from config import cities_list, slugs_list
from log import logger

slugs_sort = ','.join(slugs_list)


def get_place(city_key):
    if city_key in cities_list.keys():
        try:
            city = cities_list[city_key]
            req = requests.get(
                f'https://kudago.com/public-api/v1.4/places/?page_size=10&fields=title,address,images,description&location={city}&order_by=favorites_count&text_format=text&categories={slugs_sort}'
            )
            req_js = req.json()

            place = random.choice(req_js['results'])
            name = place['title']
            description = place['description']
            address = place['address']
            img_info = random.choice(place['images'])
            img_source = img_info['image']

            if req.status_code == 200:
                return name, description, address, img_source
            else:
                logger.error(req.status_code)
                return 'ошибка поиска мест'

        except Exception as e:
            logger.error(f'ошибка: {e}')
            return 'что то пошло не так'
    else:
        return 'для вашего города нет информации'
