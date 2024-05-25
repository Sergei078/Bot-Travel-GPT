import requests
from config import FOLDER_ID, IAM_TOKEN, lang_code


def translate(text, lang):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {IAM_TOKEN}"
        }
        body = {
            "targetLanguageCode": lang_code[lang],
            "texts": text,
            "folderId": FOLDER_ID,
        }

        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                 json=body,
                                 headers=headers
                                 ).json()
        return response['translations'][0]['text']
    except:
        return f'Произошла ошибка в переводе'
