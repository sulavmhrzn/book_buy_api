from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response

from models.books import Book
from models.carts import Cart
from models.users import User
from schemas.carts import (
    CreateCartItemSchema,
    CreateCartSchema,
    CreateCartSchemaInDB,
    OutputCartSchema,
)
from utils.security import get_current_user

router = APIRouter()


@router.post("/")
async def create_cart(cart: CreateCartSchema, user: User = Depends(get_current_user)):
    """Create a new cart"""
    exists = await Cart.find_one(Cart.user_id == user.id)
    if exists:
        return OutputCartSchema(**exists.model_dump(by_alias=True))
    new_cart = CreateCartSchemaInDB(**cart.model_dump(), user_id=user.id)
    cart_in_db = await Cart(**new_cart.model_dump()).insert()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=OutputCartSchema(**cart_in_db.model_dump(by_alias=True)).model_dump(),
    )


@router.post("/add-book-to-cart")
async def add_book_to_cart(
    cart_item: CreateCartItemSchema, user: User = Depends(get_current_user)
):
    """Add a book to cart"""
    book = await Book.get(cart_item.book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    cart = await Cart.find_one(Cart.user_id == user.id)
    if not cart:
        cart = await Cart(user_id=user.id).insert()
    await cart.add_to_cart(book_id=cart_item.book_id, quantity=cart_item.quantity)
    return JSONResponse(status_code=status.HTTP_200_OK, content="cart updated")


@router.delete("/remove-book-from-cart")
async def remove_book_from_cart(
    book_id: Annotated[PydanticObjectId, Body()], user: User = Depends(get_current_user)
):
    """Remove a book from cart"""
    book = await Book.get(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    cart = await Cart.find_one(Cart.user_id == user.id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    await cart.remove_from_cart(book_id=book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
