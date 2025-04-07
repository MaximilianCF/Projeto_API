# app/middleware/logging.py

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round((time.time() - start_time) * 1000, 2)
        method = request.method
        path = request.url.path
        status = response.status_code
        user_agent = request.headers.get("user-agent", "unknown")
        print(
            f"{method} {path} - Status: {status} - Tempo: {duration}ms - User-Agent: {user_agent}"
        )
        return response
