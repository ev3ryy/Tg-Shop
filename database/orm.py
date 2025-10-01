from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Product, Cart
from typing import List, Tuple

class ShopORM:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, tg_id: int, full_name: str, username: str = None):
        stmt = select(User).where(User.id == tg_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            user = User(id=tg_id, full_name=full_name, username=username)
            self.session.add(user)
        return user
    
    async def get_user_balance(self, tg_id: int) -> float:
        stmt = select(User.balance).where(User.id == tg_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() or 0.0
    
    async def get_all_products(self) -> List[Product]:
        stmt = select(Product).where(Product.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_product_by_id(self, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id, Product.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_balance(self, tg_id: int, amount: float):
        stmt = update(User).where(User.id == tg_id).values(
            balance=User.balance + amount
        )
        await self.session.execute(stmt)
    
    async def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1):
        stmt = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
        cart_item = (await self.session.execute(stmt)).scalar_one_or_none()

        if cart_item:
            cart_item.quantity += quantity
        else:
            new_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            self.session.add(new_item)

    async def get_cart_items_with_products(self, user_id: int) -> List[Tuple[Cart, Product]]:
        stmt = select(Cart, Product).join(Product).where(Cart.user_id == user_id)
        result = await self.session.execute(stmt)

        return result.all()
    
    async def clear_cart(self, user_id: int):
        stmt = delete(Cart).where(Cart.user_id == user_id)
        await self.session.execute(stmt)