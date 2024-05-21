from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv('TOKEN')
GEO_TOKEN = getenv('GEO_TOKEN')
FOLDER_ID = ''
IAM_TOKEN = ''
ADMINS_IDS = ''
GPT_MODEL = 'yandexgpt-lite'
GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
LOGS = 'log/logs.log'
SYSTEM_PROMPTS = {
    'features_city': "Проанализируй и предоставь подробное описание особенностей и интересных мест следующего города:",
    'clothes': "На основе текущих метеорологических данных: температура, скорость ветра и уровень влажности, "
               "предложи подходящие варианты одежды для нахождения на улице. Дополнительно учти следующее описание "
               "ситуации:",
    'beautiful_presentation': "Сформулируй информативный и визуально привлекательный текст о текущей погоде в "
                              "указанном городе,"
                              "включая температуру, ветер и влажность, используя смайлики для описания каждого "
                              "погодного условия."
}
