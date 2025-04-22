from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from cache import lifespan
from routers import router

app = FastAPI(lifespan=lifespan)

app_v1 = FastAPI(
    title="Домашняя работа №5",
    summary="Тема № 5 FastAPI",
    version="1.0.0",
    redoc_url=None,
)

@app_v1.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

app.mount("/v1", app_v1)

app_v1.include_router(router)
