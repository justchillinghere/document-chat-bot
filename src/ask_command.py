from PDF_handlerlangchain import Dialog

async def ask(update, context):
	question_to_ask = update.message.text
	reply = Dialog(update.message.from_user.id).ask(question_to_ask)
	await context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply
    )
    
