from fastapi import FastAPI

from config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Book Buy API")
    return app


app = create_app()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app", reload=settings.DEBUG, host=settings.HOST, port=settings.PORT
    )
