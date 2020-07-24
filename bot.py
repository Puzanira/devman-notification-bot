import os
import requests
import telegram
import logging
from datetime import datetime

from custom_logger import MyLogsHandler


telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
logger_bot_token = os.environ["LOGGER_BOT_TOKEN"]
telegram_chat_id = os.environ["CHAT_ID"]
dvmn_auth_token = os.environ["DVMN_AUTH_TOKEN"]

telegram_bot = telegram.Bot(token=telegram_bot_token)
logger_bot = telegram.Bot(token=logger_bot_token)

api_url = "https://dvmn.org/api/"


def logger_callback(message):
    return logger_bot.send_message(chat_id=telegram_chat_id, text=message)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(MyLogsHandler(logger_callback))


def interpret_solution_attempts(attempts):
  messages = []
  message_template = "Задание \"{0}\" {1}\nБольше по ссылке: {2}"
  for attempt in attempts:
    lesson = attempt['lesson_title']
    url = attempt['lesson_url']
    status = "отправлено на доработку." if attempt['is_negative'] else "принято!" 
    messages.append(message_template.format(lesson, status, api_url + url))
  return messages    


def on_found_response(data):
  messages = interpret_solution_attempts(data['new_attempts'])
  new_timestamp = data['last_attempt_timestamp']
  for message in messages:
    telegram_bot.send_message(chat_id=telegram_chat_id, text=message)
  return { new_timestamp }


def on_timeout_response(data):
  new_timestamp = data['timestamp_to_request']
  return { new_timestamp }


if __name__ == '__main__':
    logger.info('Bot started')

    while True:
      headers = {
        "Authorization": "Token {}".format(dvmn_auth_token)
      }
      params = {}

      try:
        0/0
        response = requests.get(
          api_url + 'long_polling',
          timeout=100,
          headers=headers,
          params=params)
        response.raise_for_status()

        data = response.json()

        if data['status'] == "timeout":
          params = on_timeout_response(data)

        if data['status'] == "found":
          params = on_found_response(data)

      except requests.exceptions.ReadTimeout:
        pass

      except ConnectionError as error_connection:
        logger.error("Connection Failed:\n{0}".format(error_connection), exc_info=True)

      except Exception as err:
        logging.error(err, exc_info=True)