import requests
import logging
from config import LOGS, SYSTEM_PROMPT, IAM_TOKEN, FOLDER_ID, GPT_MODEL, GPT_URL, MAX_GPT_TOKENS

logging.basicConfig(filename=LOGS, level=logging.DEBUG,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="a")

session = requests.Session()


def ask_gpt(prompt_key, messages, max_tokens=MAX_GPT_TOKENS, temperature=0.3):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/{GPT_MODEL}",
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": max_tokens
        },
        "messages": [
            {
                "role": "system",
                "text": SYSTEM_PROMPT[prompt_key]
            },
            {
                "role": "user",
                "text": messages
            }
        ]
    }
    try:
        response = session.post(GPT_URL, headers=headers, json=data)
        logging.debug("GPT API response: %s", response.text)
        if response.status_code != 200:
            logging.error("GPT API error with status code: %s", response.status_code)
            return "Ошибка в нейросети"
        answer = response.json()['result']['alternatives'][0]['message']['text']
        return answer
    except Exception as e:
        logging.error("Failed to connect to GPT: %s", e, exc_info=True)
        return "Ошибка в нейросети"


def yandex_gpt_attractions_city(city, max_tokens=MAX_GPT_TOKENS, temperature=0.7):
    try:
        return ask_gpt('features_city', city, max_tokens=max_tokens, temperature=temperature)
    except Exception:
        return "Ошибка в нейросети"


def yandex_gpt_interesting_facts(city, max_tokens=MAX_GPT_TOKENS, temperature=0.7):
    try:
        return ask_gpt('interesting_facts', city, max_tokens=max_tokens, temperature=temperature)
    except Exception:
        return "Ошибка в нейросети"


def yandex_gpt_clothes(temperature, wind, humidity, info_description):
    try:
        prompt = f" температура {temperature}, ветер {wind}, влажность {humidity}. {info_description}"
        return ask_gpt('clothes', prompt)
    except Exception:
        return "Ошибка в нейросети"


def yandex_gpt_beautiful_presentation_of_information(city, temperature, wind, humidity, info_description):
    try:
        prompt = f" {city} погода: температура {temperature}, ветер {wind}, влажность {humidity}. {info_description}, "
        return ask_gpt('beautiful_presentation', prompt)
    except Exception:
        return "Ошибка в нейросети"


def yandex_gpt_nature_features(city):
    try:
        return ask_gpt('nature_features', city)
    except Exception:
        return "Ошибка в нейросети"


def yandex_summarize(prompt_key, messages, max_tokens=MAX_GPT_TOKENS, temperature=0.7):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/{summarize_MODEL}",
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": max_tokens
        },
        "messages": [
            {
                "role": "system",
                "text": prompt_key
            },
            {
                "role": "user",
                "text": messages
            }
        ]
    }
    try:
        response = session.post(GPT_URL, headers=headers, json=data)
        logging.debug("GPT API response: %s", response.text)
        if response.status_code != 200:
            logging.error("GPT API error with status code: %s", response.status_code)
            return "Ошибка в нейросети"
        answer = response.json()['result']['alternatives'][0]['message']['text']
        return answer
    except Exception as e:
        logging.error("Failed to connect to GPT: %s", e, exc_info=True)
        return "Ошибка в нейросети"
