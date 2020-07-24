import os
import requests
import telegram
from datetime import datetime

telegram_bot_token = os.environ("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.environ("CHAT_ID")
dvmn_auth_token = os.environ("DVMN_AUTH_TOKEN")

telegram_bot = telegram.Bot(token=telegram_bot_token)

api_url = "https://dvmn.org/api/"


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
  print("{0} Received attempts with data:\n{1}".format(datetime.now(), data))
  return { new_timestamp }


def on_timeout_response(data):
  new_timestamp = data['timestamp_to_request']
  print("{0} Timeout Occured:".format(datetime.now()))
  print("Resending with timestamp {} ...".format(new_timestamp))
  return { new_timestamp }


while True:
  headers = {
    "Authorization": "Token {}".format(dvmn_auth_token)
  }
  params = {}
  
  try:
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
    print("Connection Failed:\n{0}".format(error_connection))