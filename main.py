import functools
import logging
from pprint import pprint
from time import sleep

import requests
from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler


def retry_on_failure(exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry_attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.warning(f"Failed to execute {func.__name__}. Retrying in {4 ** retry_attempt}s. Error: {e}")
                    sleep(4 ** retry_attempt)
                    retry_attempt = retry_attempt + 1 if retry_attempt < 5 else retry_attempt
        return wrapper
    return decorator


@retry_on_failure(exceptions=(requests.ConnectionError, requests.ConnectTimeout))
def get_dvmn_response(token, timestamp=None):
    url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {token}"
    }
    params = {
        "timestamp": timestamp
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Heyo, {update.effective_user.first_name} I'm a notification bot! 'Sup?"
    )


def main():
    env = Env()
    env.read_env()

    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)

    devman_token = env.str("DEVMAN_AUTH")
    bot_token = env.str("TELEGRAM_BOT_TOKEN")
    tg_user_id = env.str("TELEGRAM_USER_ID")

    updater = Updater(token=bot_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()

    timestamp = None
    while True:
        response = get_dvmn_response(devman_token, timestamp)
        if response["status"] == "timeout":
            timestamp = response["timestamp_to_request"]
        if response["status"] == "found":
            timestamp = response["last_attempt_timestamp"]
            dp.bot.send_message(
                chat_id=tg_user_id,
                text="There's an update for your work!"
            )


if __name__ == '__main__':
    main()
