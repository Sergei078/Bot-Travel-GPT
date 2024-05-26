from os import getenv

from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('TOKEN')
GEO_TOKEN = getenv('GEO_TOKEN')
API_WEATHER = getenv('API_WEATHER')
FOLDER_ID = getenv('FOLDER_ID')
IAM_TOKEN = getenv('IAM_TOKEN')
MAX_GPT_TOKENS = 1500
TOKENIZE_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
GPT_MODEL = 'yandexgpt'
GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
DB_FILE = 'user_city1.db'
user_token = 20000
LOGS = 'logs.log'
DEVELOPER = ["https://t.me/ild1kpy", "https://t.me/ArtemSav5", "https://t.me/SergeiDobrynkin07",
             "https://t.me/Programist337)", "https://t.me/matvejkazxc"]
SYSTEM_PROMPT = {
    'features_city': "Проанализируй и предоставь подробное описание достопримечательностей и интересных мест "
                     "следующего города:",
    'interesting_facts': "Перечисли интересные факты о следующем городе:",
    'clothes': "На основе текущих метеорологических данных: температура, скорость ветра и уровень влажности, "
               "предложи подходящие варианты одежды для нахождения на улице.",
    'beautiful_presentation': "Сформулируй информативный и визуально привлекательный текст о текущей погоде в "
                              "указанном городе, включая температуру, ветер и влажность, используя смайлики для "
                              "описания каждого погодного условия.",
    'nature_features': "Опиши природные особенности и как они влияют на жизнь в следующем городе:",
    'retelling': 'Выдели самое главное в тексте'
}

lang_code = {
    '🇷🇺': "ru",
    '🇬🇧': "en",
    '🇧🇾': "be",
    '🇩🇪': "de",
    '🇪🇸': "es",
    '🇪🇪': "et",
    '🇫🇷': "fr",
    '🇯🇵': "ja",
    '🇵🇹': "pt",
    '🇷🇴': "ro",
    '🇰🇿': "kk"
}

cities_list = {
    'санкт-Петербург': 'spb',
    'москва': 'msk',
    'новосибирск': 'nsk',
    'екатеринбург': 'ekb',
    'нижний Новгород': 'nnv',
    'казань': 'kzn',
    'выборг': 'vbg',
    'красноярск': 'krasnoyarsk',
}

slugs_list = [
    'amusement',
    'photo-places',
    'sights',
    'park',
    'palace',
    'fountain',
    'bridge',
    'art-centers',
    'attractions',
    'museums',
    'theatre'
]
