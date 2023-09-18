from telegram import Update
import asyncio
import os
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
from start_command import start
from question_command import question
from add_file_command import add_file
from echo_command import echo
from dotenv import load_dotenv
from error_handler import error_handler

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():
    # Create the bot and get the token from BotFather
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_error_handler(error_handler)

    # Register the start command handler
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Register the question command handler
    question_handler = CommandHandler("question", question)
    application.add_handler(question_handler)

    # Register the add_file command handler
    add_file_handler = MessageHandler(filters.Document.PDF, add_file)
    application.add_handler(add_file_handler)

	
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
