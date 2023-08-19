from fastapi import FastAPI

from config.settings import settings
from routes import users
from utils.database import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="Book Buy API")
    app.include_router(users.router, prefix="/users", tags=["users"])
    return app


app = create_app()


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app", reload=settings.DEBUG, host=settings.HOST, port=settings.PORT
    )
