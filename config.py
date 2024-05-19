from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv('TOKEN')
GEO_TOKEN = getenv('GEO_TOKEN')
FOLDER_ID = ''
IAM_TOKEN = ''
ADMINS_IDS = ''
MAX_GPT_TOKENS = 120
TOKENIZE_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
GPT_MODEL = 'yandexgpt-lite'
GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
LOGS = 'creds/logs.log'
SYSTEM_PROMPT = [{'role': 'system', 'text':"Ответы должны быть актуальными, информативными и привлекательно "
                                           "оформленными. Включи в ответ следующие элементы: краткое описание места, "
                                           "текущую погоду и советы по планированию путешествий. "}]