import requests
import logging
from config import LOGS, MAX_GPT_TOKENS, SYSTEM_PROMPT, IAM_TOKEN, FOLDER_ID, TOKENIZE_URL, GPT_MODEL, GPT_URL

logging.basicConfig(filename=LOGS, level=logging.DEBUG,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="a")


session = requests.Session()


def count_gpt_tokens(messages):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "messages": messages
    }
    try:
        response = session.post(url=TOKENIZE_URL, json=data, headers=headers).json()['tokens']
        return len(response)
    except Exception as e:
        logging.error("Error counting GPT tokens: %s", e, exc_info=True)
        return 0


def ask_gpt(messages):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/{GPT_MODEL}",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": SYSTEM_PROMPT + messages
    }
    try:
        response = session.post(GPT_URL, headers=headers, json=data)
        if response.status_code != 200:
            logging.error("GPT API error with status code: %s", response.status_code)
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error("Failed to connect to GPT: %s", e, exc_info=True)
        return False, "Не удалось подключиться к GPT", None


if __name__ == '__main__':
    print(count_gpt_tokens([{'role': 'user', 'text': 'Привет'}]))
