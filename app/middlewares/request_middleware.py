# =============================================
# middlewares/request_middleware.py - Middleware global
# =============================================

import time
import uuid
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("device_systems")
logging.basicConfig(level=logging.INFO)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que:
    - Mide el tiempo de respuesta de cada petición.
    - Agrega cabeceras X-Process-Time, X-App-Name y X-Request-ID.
    - Registra método, ruta y código de estado de cada petición.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Propaga el Request-ID si ya viene en la petición, o genera uno nuevo
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])

        response = await call_next(request)

        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"{request.method} {request.url.path} - "
            f"status={response.status_code} - "
            f"time={process_time:.4f}s - "
            f"request_id={request_id}"
        )

        return response