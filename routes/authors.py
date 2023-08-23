from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.authors import Author
from models.users import User
from schemas.authors import CreateAuthorSchema, OutputAuthorSchema, UpdateAuthorSchema
from utils.helpers import get_object_or_404
from utils.security import get_admin_user

router = APIRouter()


@router.post("/")
async def create_author(
    author: CreateAuthorSchema, user: User = Depends(get_admin_user)
):
    """Create an author"""
    await Author(
        first_name=author.first_name.lower(), last_name=author.last_name.lower()
    ).insert()
    return JSONResponse(status_code=201, content={"message": "Author created"})


@router.get("/")
async def get_authors(
    first_name: Optional[str] = None, last_name: Optional[str] = None
):
    """Get all authors"""
    authors = Author.find()
    if first_name:
        authors = authors.find(Author.first_name == first_name.lower())
    if last_name:
        authors = authors.find(Author.last_name == last_name.lower())

    authors = await authors.project(OutputAuthorSchema).to_list()
    json_encoded = jsonable_encoder(authors)
    return JSONResponse(status_code=200, content={"authors": json_encoded})


@router.get("/{author_id}")
async def get_author(author_id: PydanticObjectId):
    """Get an author by id"""
    author = await get_object_or_404(Author, author_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=OutputAuthorSchema(**author.model_dump(by_alias=True)).model_dump(),
    )


@router.delete("/{author_id}")
async def delete_author(
    author_id: PydanticObjectId, user: User = Depends(get_admin_user)
):
    """Delete an author by id"""
    author = await get_object_or_404(Author, author_id)

    await author.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{author_id}")
async def update_author(
    author_id: PydanticObjectId,
    update_author: UpdateAuthorSchema,
    user: User = Depends(get_admin_user),
):
    """Update an author by id"""
    author = await get_object_or_404(Author, author_id)

    await author.set(
        update_author.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude_none=True
        )
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Author updated",
    )
