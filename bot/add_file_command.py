from telegram.ext import CommandHandler, ContextTypes
from telegram import File, Update, Document
import typing
from langchain.document_loaders import PyPDFLoader

async def add_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> File | None:

	if (not hasattr(update.message.document, "mime_type") 
	 	or update.message.document.mime_type != "application/pdf"):
		await update.message.reply_text("Please load PDF")
		return
	file = await context.bot.get_file(update.message.document.file_id)
	loader = PyPDFLoader(file.file_path)
	pages = loader.load_and_split()
