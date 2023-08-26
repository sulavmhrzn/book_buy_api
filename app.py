from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from config.settings import settings
from routes import authors, books, carts, users
from utils.database import init_db
from utils.redis import init_redis


def create_app() -> FastAPI:
    app = FastAPI(title="Book Buy API")
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(authors.router, prefix="/authors", tags=["authors"])
    app.include_router(books.router, prefix="/books", tags=["books"])
    app.include_router(carts.router, prefix="/carts", tags=["carts"])
    return app


app = create_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc.errors()[0].pop("url")
    exc.errors()[0].pop("ctx")
    json_encoded = jsonable_encoder({"status": "error", "message": exc.errors()})
    return JSONResponse(status_code=422, content=json_encoded)


@app.middleware("http")
async def check_jwt_blacklist(request: Request, call_next):
    auth_header = request.headers.get("authorization")
    token = auth_header.split(" ")[1] if auth_header else None
    if await app.state.redis.get(f"bl_{token}"):
        return JSONResponse(
            status_code=401,
            content={"message": "Token has been revoked"},
        )
    return await call_next(request)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()
    app.state.redis = await init_redis()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app", reload=settings.DEBUG, host=settings.HOST, port=settings.PORT
    )
