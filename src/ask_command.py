from PDF_handlerlangchain import Dialog

def ask(update, context):
    """
    Receive a message from user, and reply to it.
    """
	question_to_ask = update.message.text
    
