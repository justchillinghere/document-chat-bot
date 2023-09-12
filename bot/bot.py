import telegram
from telegram.ext import Updater, CommandHandler
from start_command import start
from question_command import question
from add_file_command import add_file
from config_reader import config

BOT_TOKEN = config.bot_token.get_secret_value()


def main():
    # Create the bot and get the token from BotFather
    bot = telegram.Bot(token=BOT_TOKEN)

    # Create the updater and pass the bot token
    updater = Updater(token=BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the start command handler
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    # Register the question command handler
    question_handler = CommandHandler("question", question)
    dispatcher.add_handler(question_handler)

    # Register the add_file command handler
    add_file_handler = CommandHandler("add_file", add_file)
    dispatcher.add_handler(add_file_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()
