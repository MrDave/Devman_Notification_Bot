import requests
from pprint import pprint
from environs import Env
import logging


def get_dvmn_response(token):
    url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    return response.json()


def main():
    env = Env()
    env.read_env()

    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)

    devman_token = env.str("DEVMAN_AUTH")

    while True:
        try:
            response = get_dvmn_response(devman_token)
            pprint(response)
        except requests.exceptions.Timeout as error:
            logging.debug(f"Timeout: {error}")


if __name__ == '__main__':
    main()
