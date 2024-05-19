import requests
from config import GEO_TOKEN


def i_know_where_you_live(lat, long):
    headers = {'Accept-Language': 'ru'}
    address = requests.get(
        f'https://eu1.locationiq.com/v1/reverse.php?key={GEO_TOKEN}&lat={lat}&lon={long}&format=json',
        headers=headers).json()
    # address['address']['county_code'] - код страны по стандарту ISO 3166-1 alpha-2, поможет определить язык?
    city = address['address'].get('city')
    country = address['address'].get('country')
    return city, country
