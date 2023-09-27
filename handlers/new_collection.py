from aiogram import Router, F
import os
from aiogram.filters import Command
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from data_processing.async_PDF import Dialog
from dotenv import load_dotenv
import logging
from keyboards.simple_row import make_row_keyboard


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
logger = logging.getLogger()

router = Router()

class UploadFiles(StatesGroup):
    uploading_files = State()
    naming_collection = State()
    processing_collection = State()
    
new_collection_options = ["Готово", "Отмена"]
@router.message(Command("new_collection"))
async def cmd_new_collection(message: Message, state: FSMContext):
    await message.answer(
        text="Загрузите ваши файлы. Важно!\n\
            1. Размер каждого файла не должен превышать 20 МБ.\n\
                2. Количество файлов не должно превышать 5.",
        reply_markup=make_row_keyboard(new_collection_options)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(UploadFiles.uploading_files)
    await state.update_data(data={"file_paths": [], "name": ""}) # Here we store file_ids and name of the current collection

@router.message(UploadFiles.uploading_files, F.document.mime_type == "application/pdf")
async def new_file(message: Message, state: FSMContext, bot: Bot):
		current_paths: dict = await state.get_data()
		file = await bot.get_file(message.document.file_id)
		current_paths["file_paths"].append(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}")
		await state.update_data(data=current_paths)
		await message.answer(
		text="Принято! Загрузите еще файлы или нажмите готово.",
		reply_markup=make_row_keyboard(new_collection_options)
		)


@router.message(UploadFiles.uploading_files, F.text == "Готово")
async def name_collection(message: Message, state: FSMContext):
    await message.answer(
        text="Файлы загружены, назовите вашу коллекцию",
	)
    await state.set_state(UploadFiles.naming_collection)

@router.message(UploadFiles.naming_collection, F.text)
async def uploaded(message: Message, state: FSMContext):
	file_processor = Dialog(user_id=message.from_user.id)
	current_paths: list[str] = await state.get_data()
	current_paths["name"] = message.text # add collecntion name
	state.update_data(current_paths)
	await message.answer(
		text="Коллекция создана! Подождите обработки файлов",
	)
	await state.set_state(state=UploadFiles.processing_collection)
	await file_processor.load_documents_to_vec_db(current_paths["file_paths"])
	await message.answer(
		text="Файлы загружены. Вы можете начать с ними диалог, выбрав коллекцию по команде /collections",
	)
	await state.set_state(state=None)
