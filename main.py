import functools
import logging
from time import sleep

import requests
from environs import Env
from telegram.ext import Updater


logger = logging.getLogger()


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


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


def main():
    env = Env()
    env.read_env()

    devman_token = env.str("DEVMAN_AUTH")
    bot_token = env.str("TELEGRAM_BOT_TOKEN")
    tg_user_id = env.str("TELEGRAM_USER_ID")

    updater = Updater(token=bot_token)
    dp = updater.dispatcher

    log_level = env.log_level("LOG_LEVEL", logging.WARNING)
    logger.setLevel(level=log_level)
    logger.addHandler(TelegramLogsHandler(dp.bot, tg_user_id))

    logger.info("Бот запущен!")

    timestamp = None
    while True:
        try:
            response = get_dvmn_response(devman_token, timestamp)
        except requests.ReadTimeout:
            logger.debug("ReadTimeout, trying again")
            continue
        except Exception as e:
            logger.exception(f"Бот упал с ошибкой:\n")
            raise

        if response["status"] == "timeout":
            timestamp = response["timestamp_to_request"]
        if response["status"] == "found":
            timestamp = response["last_attempt_timestamp"]
            for attempt in response["new_attempts"]:
                title = attempt["lesson_title"]
                link = attempt["lesson_url"]
                is_negative = attempt["is_negative"]
                if is_negative:
                    success_or_not_text = "Нужно что\-то доработать\."
                else:
                    success_or_not_text = "Работа принята\!"
                text = f"Урок [{title}]({link}) вернулся с проверки\.\n\n{success_or_not_text}"
                dp.bot.send_message(
                    chat_id=tg_user_id,
                    text=text,
                    disable_web_page_preview=True,
                    parse_mode="MarkdownV2",
                )


if __name__ == '__main__':
    main()
