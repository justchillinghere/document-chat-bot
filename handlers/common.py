from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
    text="Привет! Я бот, где вы можете пообщаться с коллекцией документов.\n"
         "Вы можете:\n"
         "1. Создать новую коллекцию документов (/new_collection)\n"
         "2. Выбрать из существующих (/choose_collection)\n"
         "Для вывода всех комманд нажмите /help",
    reply_markup=ReplyKeyboardRemove()
	)


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено. Вы можете создать новую коллекцию документов (/new_collection)\
или выбрать из существующих (/choose_collection).\nДля вывода всех комманд нажмите /help",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command(commands=["help"]))
@router.message(F.text.lower() == "помощь")
@router.message(F.text.lower() == "help")
async def cmd_cancel(message: Message, state: FSMContext):
    await message.answer(
        text="Вы можете создать новую коллекцию документов (/new_collection)\
или выбрать из существующих (/choose_collection).\nДля вывода всех комманд нажмите /help",
        reply_markup=ReplyKeyboardRemove()
    )