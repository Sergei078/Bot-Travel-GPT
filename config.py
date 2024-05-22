from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv('TOKEN')
GEO_TOKEN = getenv('GEO_TOKEN')
API_WEATHER = getenv('API_WEATHER')
FOLDER_ID = getenv('FOLDER_ID')
IAM_TOKEN = getenv('IAM_TOKEN')
ADMINS_IDS = ''
MAX_GPT_TOKENS = 5000
TOKENIZE_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
GPT_MODEL = 'yandexgpt-lite'
GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
LOGS = 'creds/logs.log'
SYSTEM_PROMPT = {
    'features_city': "Проанализируй и предоставь подробное описание достопримечательностей и интересных мест "
                     "следующего города:",
    'interesting_facts': "Перечисли интересные факты о следующем городе:",
    'clothes': "На основе текущих метеорологических данных: температура, скорость ветра и уровень влажности, "
               "предложи подходящие варианты одежды для нахождения на улице.",
    'beautiful_presentation': "Сформулируй информативный и визуально привлекательный текст о текущей погоде в "
                              "указанном городе, включая температуру, ветер и влажность, используя смайлики для "
                              "описания каждого погодного условия."
}

