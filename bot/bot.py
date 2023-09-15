import telegram
import asyncio
import os
import logging
from telegram.ext import Updater, CommandHandler, ApplicationBuilder, ContextTypes
from start_command import start
from question_command import question
from add_file_command import add_file
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def main():
    # Create the bot and get the token from BotFather
    application = ApplicationBuilder().token("BOT_TOKEN").build()

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

    application.run_polling


if __name__ == "__main__":
    asyncio.run(main())
