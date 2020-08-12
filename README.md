# devman-notification-bot

## Description

This bot works with Devman API https://dvmn.org/api/docs/
and sends a notification to a telegram chat when a devman task is reviewed.

## Requirements

Python 3.8

## Install 

1. ##### Install requirements:
    `pip install -r requirements.txt`

2. ##### Setup environment variables:
    * `TELEGRAM_BOT_TOKEN` - a notification bot authorization token 
    * `LOGGER_BOT_TOKEN` - a logger bot authorization token
    * `CHAT_ID` - your personal chat ID can be obtainned by talking to [@userinfobot](https://telegram.me/userinfobot)
    * `DVMN_AUTH_TOKEN` - your devman API authorization token 
    
    Useful links: Read about authorization tokens on [Official Telegam Documentation: Creating bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
    Read about devman API on [Devman API Documentation](https://dvmn.org/api/docs/).

3. ##### Run bot.py:
    `python bot.py`
