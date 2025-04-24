from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.requests import Request
from starlette.responses import JSONResponse
import redis.asyncio as redis

from cache import JsonCoder
from routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.from_url(
        "redis://localhost:6379",
        encoding="utf8",
        decode_responses=False
    )
    FastAPICache.init(
        RedisBackend(redis_client),
        prefix="fastapi-cache",
        coder=JsonCoder
    )
    yield
    await redis_client.aclose()


app = FastAPI(
    lifespan=lifespan,
    title="Приложение с функцией кэша и написанными тэстами",
    summary="Работает на FastAPI",
    version="1.0.0",
    redoc_url=None,
)

app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})
