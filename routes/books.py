from typing import Annotated

import cloudinary
import cloudinary.uploader
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.settings import settings
from models.authors import Author
from models.books import Book
from models.users import User
from schemas.books import BookCreateSchema, BookListOutSchema
from utils.security import get_admin_user

router = APIRouter()

config = cloudinary.config(secure=True)


@router.post("/")
async def create_book(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    price: Annotated[int, Form()],
    isbn: Annotated[str, Form()],
    lanugage: Annotated[str, Form()],
    author_id: Annotated[PydanticObjectId, Form()],
    genre: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
    user: User = Depends(get_admin_user),
):
    """Create a book"""
    author_exists = await Author.get(author_id)
    if not author_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    content_type = image.content_type
    if content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only jpeg, jpg and png images are allowed",
        )
    if image.size > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size should not be more than 2MB",
        )

    image_data = await image.read()
    result = cloudinary.uploader.upload(image_data, folder="book_buy")
    schema = BookCreateSchema(
        title=title,
        description=description,
        price=price,
        isbn=isbn,
        lanugage=lanugage,
        author_id=author_id,
        genre=[genre],
        image_url=result["secure_url"],
    )
    await Book(**schema.model_dump()).insert()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": "Book created"}
    )


@router.get("/")
async def get_books():
    """Get all books"""
    books = await Book.find_all(projection_model=BookListOutSchema).to_list()
    json_encoded = jsonable_encoder(books)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Books found", "books": json_encoded},
    )


@router.get("/{book_id}")
async def get_book(book_id: int):
    """Get a book by id"""
    pass


@router.delete("/{book_id}")
async def delete_book(book_id: int):
    """Delete a book by id"""
    pass


@router.put("/{book_id}")
async def update_book(book_id: int):
    """Update a book by id"""
    pass