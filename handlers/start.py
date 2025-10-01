from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.inline import main_menu_inline

router = Router()

@router.message(Command("start"))
async def handle_start_command(message: Message) -> None:
    await message.answer(
        "👋 Добро пожаловать в магазин [name]! Выберите действие:",
        reply_markup=main_menu_inline()
    )

@router.callback_query(F.data == "main_menu")
async def handle_main_menu_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Вы вернулись в главное меню. Выберите действие:",
        reply_markup=main_menu_inline()
    )
    await callback.answer()