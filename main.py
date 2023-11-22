import requests
from pprint import pprint
from environs import Env
import logging
import functools
from time import sleep


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
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def main():
    env = Env()
    env.read_env()

    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)

    devman_token = env.str("DEVMAN_AUTH")
    timestamp = None
    while True:
        response = get_dvmn_response(devman_token, timestamp)
        if response["status"] == "timeout":
            timestamp = response["timestamp_to_request"]
        if response["status"] == "found":
            timestamp = response["last_attempt_timestamp"]
        pprint(response)


if __name__ == '__main__':
    main()
