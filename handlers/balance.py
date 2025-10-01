from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm import ShopORM
from keyboards.inline import main_menu_inline, cart_keyboard

router = Router()

@router.callback_query(F.data == "show_balance")
async def show_balance_callback(callback: CallbackQuery, session: AsyncSession) -> None:
    orm = ShopORM(session)
    balance = await orm.get_user_balance(callback.from_user.id)

    await callback.message.edit_text(
        f"💰 Ваш текущий баланс: **{balance:.2f}**.",
        reply_markup=main_menu_inline(),
        parse_mode='Markdown'
    )
    await callback.answer()

@router.callback_query(F.data == "show_cart")
async def show_cart(callback: CallbackQuery, session: AsyncSession) -> None:
    orm = ShopORM(session)

    cart_items_with_products = await orm.get_cart_items_with_products(callback.from_user.id)

    if not cart_items_with_products:
        text = "🛒 Ваша корзина пуста. Добавьте товары из каталога."
        keyboard = main_menu_inline()
    else:
        total_price = 0.0
        cart_details = []

        for cart_item, product in cart_items_with_products:
            item_total = product.price * cart_item.quantity
            total_price += item_total
            cart_details.append(
                f"**{product.name}**\n"
                f"`{cart_item.quantity} шт. x {product.price:.2f} = {item_total:.2f}`"
            )

        text = (
            "🛒 **Ваша корзина:**\n\n"
            + "\n--\n".join(cart_details) + "\n\n"
            f"**К оплате:** **{total_price:.2f}**"
        )
        keyboard = cart_keyboard()

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='Markdown')
    await callback.answer()

@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery, session: AsyncSession) -> None:
    orm = ShopORM(session)
    await orm.clear_cart(callback.from_user.id)

    await callback.message.edit_text("🗑️ Ваша корзина очищена.", reply_markup=main_menu_inline())
    await callback.answer("Корзина очищена!", show_alert=True)

@router.callback_query(F.data == "checkout")
async def process_checkout(callback: CallbackQuery, session: AsyncSession) -> None:
    orm = ShopORM(session)
    user_id = callback.from_user.id


    cart_items_with_products = await orm.get_cart_items_with_products(user_id)

    if not cart_items_with_products:
        await callback.asnwer("Корзина пуста!", show_alert=True)
        return
    
    total_price = sum(product.price * cart_item.quantity for cart_item, product in cart_items_with_products)
    user_balance = await orm.get_user_balance(user_id)

    if user_balance < total_price:
        await callback.answer(
            f" Недостаточно средств. Для покупки нужно {total_price:.2f}. Текущий баланс {user_balance:.2f}",
            show_alert=True
        )
        return

    await orm.update_balance(user_id, -total_price)

    purchased_items = [f"{product.name} ({cart_item.quantity} шт.)" for cart_item, product in cart_items_with_products]

    await orm.clear_cart(user_id)

    purchase_message = (
        "✅ **Покупка успешна!**\n\n"
        f"Со счета списано: **{total_price:.2f}**\n"
        f"Текущий баланс: **{user_balance - total_price:.2f}**\n\n"
        f"Получены товары:\n"
        + "\n".join([f"- {item}"] for item in purchased_items)
    )

    await callback.message.edit_text(purchase_message, parse_mode='Markdown', reply_markup=main_menu_inline())
    await callback.answer("Покупка завершена!", show_alert=True)