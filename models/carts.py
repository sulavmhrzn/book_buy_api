from beanie import Document, PydanticObjectId
from pydantic import Field

from schemas.carts import CartItemSchema


class Cart(Document):
    user_id: PydanticObjectId
    cart_items: list[CartItemSchema] = []

    class Settings:
        name = "carts"

    async def add_to_cart(self, *, book_id: PydanticObjectId, quantity: int = 1):
        if not self.cart_items:
            self.cart_items = []

        for item in self.cart_items:
            if item.book_id == book_id:
                item.quantity += quantity
                await self.save()
                return
        self.cart_items.append(CartItemSchema(book_id=book_id, quantity=quantity))
        await self.save()
