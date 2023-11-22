import requests
from pprint import pprint
from environs import Env


def main():
    env = Env()
    env.read_env()

    devman_token = env.str("DEVMAN_AUTH")
    url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization": f"Token {devman_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    pprint(response.json())


if __name__ == '__main__':
    while True:
        main()
