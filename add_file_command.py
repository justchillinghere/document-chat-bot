from telegram.ext import CommandHandler


def add_file(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Please upload the file."
    )


add_file_handler = CommandHandler("add_file", add_file)
