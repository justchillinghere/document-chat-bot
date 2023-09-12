from telegram.ext import CommandHandler


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! How can I assist you?"
    )


start_handler = CommandHandler("start", start)
