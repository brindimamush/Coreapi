import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("api.timing")

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        logger.info(
            f"{request.method} {request.url.path} {response.status_code}",
            extra={
                "request_id": getattr(request.state, "request_id", None),
                "duration_ms": round(duration * 1000, 2),
            },
        )
        response.headers["X-Response-Time"] = str(round(duration * 1000))
        return response