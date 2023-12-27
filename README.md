# Devman Notification Bot
Get notifications when your lessons are reviewed!

## How to install
Python should already be installed. This project is tested on Python 3.10 and 3.12. You may use other versions as you will, but YMMV.

Clone the repo / download code

Using virtual environment [virtualenv/venv](https://docs.python.org/3/library/venv.html) is recommended for project isolation.

Install requirements:
```commandline
pip install -r requirements.txt
```

Set up environmental variables.  
Create `.env` file in root folder and write down the following variables:
- `DEVMAN_AUTH` - Devman API user access token. Get it from the [API docs](https://dvmn.org/api/docs/).
- `TELEGRAM_BOT_TOKEN` - Access token of your bot. You get one from [BotFather Telegram bot](https://t.me/BotFather) when you create a bot.
- `TELEGRAM_USER_ID` - Your numeric Telegram ID. Can be checked by writing to special [user info bot](https://t.me/userinfobot).
- `LOG_LEVEL` - Sets the threshold for this logger. Accepts numbers or strings (such as `10` or `"DEBUG"` for DEBUG level)

### Running on Windows note  
If run on Windows, long-polling requests won't allow to stop the program (by using `Ctrl+C`) until they finish. Thus, using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) might be useful.

## How to use

Run the script:
```commandline
python main.py
```
If that's your first interaction with your bot, send it a `/start` command, or it won't be able to send you messages.

And you're all set!
When you get updates on your submitted lessons, you'll receive a message from the bot.

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
