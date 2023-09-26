from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard

router = Router()

class UploadFiles(StatesGroup):
    uploading_files = State()
    naming_collection = State()
    
new_collection_options = ["Готово", "Отмена"]
@router.message(Command("new_collection"))
async def cmd_new_collection(message: Message, state: FSMContext):
    await message.answer(
        text="Загрузите ваши файлы. Важно!\n\
            1. Размер каждого файла не должен превышать 10 МБ.\n\
                2. Количество файлов не должно превышать 5.",
        reply_markup=make_row_keyboard(new_collection_options)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(UploadFiles.uploading_files)
    await state.set_data({"paths": []})

# Этап выбора блюда #


@router.message(UploadFiles.uploading_files, F.document.mime_type == "application/pdf")
async def new_file(message: Message, state: FSMContext):
    file = await bot.get_file(message.document.file_id)
    current_paths: dict = state.get_data()
    current_paths["paths"].append(file.file_path)
    await state.update_data(current_paths)
    await message.answer(
        text="Принято! Загрузите еще файлы или завершите загрузку.",
        reply_markup=make_row_keyboard(new_collection_options)
    )


@router.message(UploadFiles.uploading_files)
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="Неизвестная комманда. Загрузите файл или выберете одну из кнопок",
        reply_markup=make_row_keyboard(new_collection_options)
    )

@router.message(UploadFiles.uploading_files, F.text == "Готово")
async def uploaded(message: Message, state: FSMContext):
    await message.answer(
        text="Файлы загружены, назовите вашу коллекцию",
	)
    await state.set_state(UploadFiles.naming_collection)

@router.message(UploadFiles.naming_collection, F.text)
async def uploaded(message: Message, state: FSMContext):
    current_paths: list[str] = state.get_data()
    current_paths["name"] = message.text # add collecntion name
    state.update_data(current_paths)
    await message.answer(
        text="Коллекция создана! Подождите обработки файлов",
	)
    await state.set_state(state=None)

