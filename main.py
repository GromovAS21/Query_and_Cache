from fastapi import FastAPI

from routers import router

app = FastAPI()

app_v1 = FastAPI(
    title="Домашняя работа №5",
    summary="Тема № 5 FastAPI",
    version="1.0.0",
    redoc_url=None
)

app.mount("/v1", app_v1)

app_v1.include_router(router)