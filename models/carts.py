from beanie import Document, PydanticObjectId
from pydantic import Field

from models.books import Book
from schemas.carts import CartItemSchema


class Cart(Document):
    user_id: PydanticObjectId
    cart_items: list[CartItemSchema] = []
    total_price: int = 0

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

    async def remove_from_cart(self, *, book_id: PydanticObjectId):
        if not self.cart_items:
            return
        for item in self.cart_items:
            if item.book_id == book_id:
                self.cart_items.remove(item)
                await self.save()

    async def update_cart_items(self, *, book_id: PydanticObjectId, quantity: int):
        if not self.cart_items:
            return
        for item in self.cart_items:
            if item.book_id == book_id:
                item.quantity = quantity
                await self.save()
                return

    async def calculate_total_price(self):
        for item in self.cart_items:
            book = await Book.get(item.book_id)
            self.total_price += book.price * item.quantity
        await self.save()
