import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Heyo, {update.effective_user.first_name} I'm a notification bot! 'Sup?"
    )


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    env = Env()
    env.read_env()

    bot_token = env.str("TELEGRAM_BOT_TOKEN")

    updater = Updater(token=bot_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()


if __name__ == '__main__':
    main()
