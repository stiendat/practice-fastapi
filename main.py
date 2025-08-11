from fastapi import FastAPI
from src.api.main_router import router as main_router
from src.utils.observability_utils import PrometheusMiddleware, metrics, setting_otlp
import uvicorn
import asyncio
import sys
import logging


app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name="fastapi-app")
app.add_route("/metrics", metrics)
setting_otlp(app, "fastapi-app", "tempo:4317")
app.include_router(main_router)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000)