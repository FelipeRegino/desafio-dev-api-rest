import time
import logging

import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import holder, dock_account, transaction_history

logger = logging.getLogger("uvicorn.error")
app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, ex: StarletteHTTPException):
    logger.error(f"Failed to complete request - {ex}")
    return JSONResponse(content={"message": ex.detail}, status_code=ex.status_code)

@app.middleware("http")
async def middleware(request: Request, call_next):
    logger.info(f"Request started [{request.method} {request.url.path}]")
    try:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"Request finished [{request.method} {request.url.path}] - process_time={str(process_time)}")
        return response
    except Exception as ex:
        logger.critical(f"Internal server error - {ex}")
        return JSONResponse(content={"message": "Internal server error"}, status_code=500)

app.include_router(holder.router)
app.include_router(dock_account.router)
app.include_router(transaction_history.router)

if __name__ == '__main__':
    config = uvicorn.Config("http_server:app", port=8000, log_level="debug")
    server = uvicorn.Server(config)
    server.run()