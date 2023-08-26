from typing import Any, Optional, Type, TypeVar, Union

from beanie import Document, PydanticObjectId
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

T = TypeVar("T", bound=Document)


async def get_object_or_404(
    obj: Type[T], key: PydanticObjectId
) -> Union[T, HTTPException]:
    """Get object or raise 404"""
    result = await obj.get(key)
    if not result:
        raise error_response(
            status_code=status.HTTP_404_NOT_FOUND, message=f"{obj.__name__} not found"
        )
    return result


def error_response(
    status_code: int, message: Any, headers: Optional[dict[str, str]] = None
) -> HTTPException:
    """Return an HTTPException with a JSON body."""
    return HTTPException(
        status_code=status_code,
        detail={"status": "error", "message": message},
        headers=headers,
    )


def success_response(
    message: Any, status_code: int = 200, headers: Optional[dict[str, str]] = None
) -> JSONResponse:
    """Return a JSONResponse with a JSON body."""
    return JSONResponse(
        status_code=status_code,
        content={"status": "success", "detail": message},
        headers=headers,
    )
