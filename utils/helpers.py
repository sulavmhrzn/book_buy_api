from typing import Type, TypeVar, Union

from beanie import Document, PydanticObjectId
from fastapi import HTTPException, status

T = TypeVar("T", bound=Document)


async def get_object_or_404(
    obj: Type[T], key: PydanticObjectId
) -> Union[T, HTTPException]:
    """Get object or raise 404"""
    result = await obj.get(key)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{obj.__name__} not found"
        )
    return result
