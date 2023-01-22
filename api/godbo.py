import asyncio
import json as JSON
import functools
import redis.asyncio as redis

from fastapi import FastAPI, APIRouter
from fastapi.responses import PlainTextResponse, JSONResponse, Response
from typing import Callable, Union

app = FastAPI()
router = APIRouter()
redis = redis.Redis(connection_pool=redis.ConnectionPool(host="godbo_redis", port=6379, db=0))

def handle_exception_and_continue(max_retries=5):
    def wrapper(func) -> Callable:
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as ex:

                    print(f"[!] Exception {ex} occurred in {func.__qualname__}")
                    retries += 1

                    if retries < max_retries:
                        await asyncio.sleep(0.5)
                        continue
                    else:
                        raise ex
        return inner
    return wrapper

@router.get("/", status_code=200)
@handle_exception_and_continue(max_retries=5)
async def apiroot(json: Union[str, None] = None):
    counter = await redis.incr("godbo")
    message = f"這是第{counter}次感恩讚嘆神BO."
    if json == "true":
        r = JSONResponse({"message": message, "godbo": counter}, status_code=200)
        r.headers["content-type"] = "application/json; charset=utf-8"
        return r
    elif not json or json == "false":
        r = PlainTextResponse(message, status_code=200)
        r.headers["content-type"] = "text/plain; charset=utf-8"
        return r
    else:
        return PlainTextResponse("Bad Request", status_code=418)

app.include_router(router)
