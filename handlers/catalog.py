from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm import ShopORM
from keyboards.inline import catalog_keyboard, ProductCallback, product_detail_keyboard, main_menu_inline
from fsm.cart import CartFSM

router = Router()

@router.callback_query(F.data == "show_catalog")
async def show_catalog(callback: CallbackQuery, session: AsyncSession) -> None:
    orm = ShopORM(session)
    products = await orm.get_all_products()

    if not products:
        text = "К сожалению, товаров пока нет в наличии 😔"
        keyboard = None
    else:
        text = "🛍️ **Каталог товаров:**"
        keyboard = catalog_keyboard(products)

        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='Markdown')
        await callback.answer()
@router.callback_query(ProductCallback.filter(F.action == "view"))
async def show_product_detail(callback: CallbackQuery, callback_data: ProductCallback, session: AsyncSession) -> None:
    orm = ShopORM(session)
    product = await orm.get_product_by_id(callback_data.product_id)

    if not product:
        await callback.answer("Товар не найден или недоступен.", show_alert=True)
        return
    
    text = (
        f"**{product.name}**\n\n"
        f"**Цена:** {product.price:.2f}\n"
        f"**Описание:** {product.description or 'Нет описания.'}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=product_detail_keyboard(product.id),
        parse_mode='Markdown'
    )
    await callback.answer()

@router.callback_query(ProductCallback.filter(F.action == "add"))
async def request_quantity(callback: CallbackQuery, callback_data: ProductCallback, state: FSMContext) -> None:
    await state.update_data(product_id=callback_data.product_id)
    await callback.message.edit_text("🔢 Введите желаемое количество товара:")

    await state.set_state(CartFSM.waiting_for_quantity)
    await callback.answer()

@router.message(CartFSM.waiting_for_quantity)
async def add_item_to_cart(message: Message, state: FSMContext, session: AsyncSession) -> None:
    try:
        quantity = int(message.text)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Некорректный ввод. Введите целое число больше нуля.")
        return

    data = await state.get_data()
    product_id = data.get('product_id')

    orm = ShopORM(session)
    product = await orm.get_product_by_id(product_id)

    if not product:
        await message.answer("❌ Товар не найден. Начните по новой.", reply_markup=main_menu_inline())
        await state.clear()
        return
    
    await orm.add_to_cart(message.from_user.id, product_id, quantity)

    await message.answer(
        f"✅ Добавлено **{quantity}** x `{product.name}` в корзину.",
        reply_markup=main_menu_inline(),
        parse_mode='Markdown'
    )

    await state.clear()