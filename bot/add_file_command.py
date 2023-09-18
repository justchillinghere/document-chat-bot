from telegram.ext import CommandHandler, ContextTypes
from telegram import File, Update, Document
import typing


async def add_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> File | None:

	if (not hasattr(update.message.document, "mime_type") 
	 	or update.message.document.mime_type != "application/pdf"):
		await update.message.reply_text("Please load PDF")
		return
	file = await context.bot.get_file(update.message.document.file_id)
	loader = PyPDFLoader(file.file_path)
	pages = loader.load_and_split()

    # message = update.message
    # if "document" in message.effective_attachment.get_file():
    #     document: Document = update.message.effective_attachment["document"]
    #     if document.mime_type == "application/pdf":
    #         file = document.get_file(document.file_id)
    #         context.bot.send_message(
    #             chat_id=update.effective_chat.id,
    #             text="File uploaded and processed successfully.",
    #         )
    #         print(file)
    #     else:
    #         context.bot.send_message(
    #             chat_id=update.effective_chat.id, text="Please upload a PDF file."
    #         )
    # else:
    #     context.bot.send_message(
    #         chat_id=update.effective_chat.id, text="Please upload a file."
    #     )
