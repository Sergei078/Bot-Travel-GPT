from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv('TOKEN')
GEO_TOKEN = getenv('GEO_TOKEN')
API_WEATHER = getenv('API_WEATHER')
FOLDER_ID = getenv('FOLDER_ID')
IAM_TOKEN = getenv('IAM_TOKEN')
MAX_GPT_TOKENS = 1000
TOKENIZE_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
GPT_MODEL = 'yandexgpt'
GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
DB_FILE = 'user_city.db'
user_token = 5000
LOGS = 'logConfig.log'
SYSTEM_PROMPT = {
    'features_city': "Проанализируй и предоставь подробное описание достопримечательностей и интересных мест "
                     "следующего города:",
    'interesting_facts': "Перечисли интересные факты о следующем городе:",
    'clothes': "На основе текущих метеорологических данных: температура, скорость ветра и уровень влажности, "
               "предложи подходящие варианты одежды для нахождения на улице.",
    'beautiful_presentation': "Сформулируй информативный и визуально привлекательный текст о текущей погоде в "
                              "указанном городе, включая температуру, ветер и влажность, используя смайлики для "
                              "описания каждого погодного условия.",
    'nature_features': "Опиши природные особенности и как они влияют на жизнь в следующем городе:"
}