import random
import requests
import logging

logging.basicConfig(filename='logConfig.log', encoding='utf-8', level=logging.WARNING,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s")
logger = logging.getLogger(__name__)

cities_list = {
    'Санкт-Петербург': 'spb',
    'Москва': 'msk',
    'Новосибирск': 'nsk',
    'Екатеринбург': 'ekb',
    'Нижний Новгород': 'nnv',
    'Казань': 'kzn',
    'Выборг':  'vbg',
    'Самара': 'smr',
    'Краснодар': 'krd',
    'Сочи': 'sochi',
    'Уфа': 'ufa',
    'Красноярск': 'krasnoyarsk',
    'Киев': 'kev',
    'Нью Йорк': 'new-york',
}

slugs_list = [
    'amusement',
    'strip-club',
    'restaurants',
    'photo-places',
    'sights',
    'recreation',
    'park',
    'palace',
    'fountain',
    'bridge',
    'art-centers',
    'attractions',
    'museums',
    'theatre'
]
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
                return True, name, description, address, img_source
            else:
                logger.error(req.status_code)
                return False, 'ошибка поиска мест'

        except Exception as e:
            logger.error(f'ошибка: {e}')
            return False, 'что то пошло не так'
    else:
        return False, 'для вашего города нет информации'



