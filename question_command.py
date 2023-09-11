from telegram.ext import CommandHandler


def question(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="What is your question?"
    )


question_handler = CommandHandler("question", question)
