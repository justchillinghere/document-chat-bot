from telegram.ext import CommandHandler


async def start(update, context):
    """
    Send a message to the chat with the given chat ID.

    Args:
        update (Update): The update object containing information about the chat.
        context (CallbackContext): The context object for the current chat session.

    Returns:
        None
    """
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! How can I assist you?"
    )


start_handler = CommandHandler("start", start)
