from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.filters.callback_data import CallbackData

class ProductCallback(CallbackData, prefix="prod"):
    action: str
    product_id: int

def main_menu_inline() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="🛍️ Каталог", callback_data="show_catalog")],
        [InlineKeyboardButton(text="🛒 Корзина", callback_data="show_cart")],
        [InlineKeyboardButton(text="💰 Баланс", callback_data="show_balance")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def catalog_keyboard(products) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for product in products:
        callback_data = ProductCallback(action='view', product_id=product.id).pack()
        builder.button(text=f"{product.name} ({product.price:.2f})", callback_data=callback_data)

    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu"))
    return builder.as_markup()

def product_detail_keyboard(product_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    add_to_cart_data = ProductCallback(action='add', product_id=product_id).pack()

    builder.button(text="➕ Добавить в корзину", callback_data=add_to_cart_data)
    builder.button(text="🔙 Назад в каталог", callback_data="show_catalog")
    builder.adjust(1)
    return builder.as_markup()

def cart_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton(text="🗑️ Очистить корзину", callback_data="clear_cart")],
        [InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)