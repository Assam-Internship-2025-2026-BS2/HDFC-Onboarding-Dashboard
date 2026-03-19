import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.executive_router import router as executive_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.debug_router import router as debug_router
from app.routers.products_router import router as products_router
from app.routers.insights_router import router as insights_router
from app.routers.analysis_router import router as analysis_router


app = FastAPI(
    title="Business Ops Analytics API",
    version="1.0.0",
    docs_url="/docs",       
    redoc_url="/redoc",     
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
  
    "http://business-dashboard-alb-1108487393.ap-southeast-2.elb.amazonaws.com",
    "http://dugkfqqpvqc7l.cloudfront.net"
    "https://dugkfqqpvqc7l.cloudfront.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(executive_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(debug_router, prefix="/api/v1/debug", tags=["Debug"])
app.include_router(products_router, prefix="/api/v1/products", tags=["Products"])
app.include_router(insights_router, prefix="/api/v1/insights", tags=["Insights"])
app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["Analysis"])


@app.get("/")
def home():
    return {"message": "Business Ops API running"}


@app.get("/health")
def health():
    """
    Full health check:
      1. FastAPI is alive
      2. ClickHouse is reachable
      3. Target table exists and is queryable
    """
    health_status = {
        "status": "ok",
        "api": "ok",
        "clickhouse": "unknown",
        "table": "unknown",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    # Read connection config from environment variables
    host     = os.getenv("CLICKHOUSE_HOST", "localhost")
    port     = int(os.getenv("CLICKHOUSE_PORT", "8123"))
    database = os.getenv("CLICKHOUSE_DB", "business_ops")
    user     = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "")

    try:
        import clickhouse_connect

        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            database=database,
            username=user,
            password=password,
            connect_timeout=5,      # fail fast — don't block ALB
            send_receive_timeout=5
        )

        # Check 1: ClickHouse is alive
        ping_result = client.command("SELECT 1")
        if ping_result == 1:
            health_status["clickhouse"] = "ok"

        # Check 2: Target table exists and has data
        row_count = client.command(
            "SELECT count() FROM business_ops.dashboard_data"
        )
        health_status["table"] = f"ok ({row_count} rows)"

    except Exception as e:
        health_status["status"] = "degraded"
        health_status["clickhouse"] = "unreachable"
        health_status["table"] = "unknown"
        health_status["error"] = str(e)

        # Return 503 so ALB marks this task as unhealthy
        # when ClickHouse is down
        return JSONResponse(status_code=503, content=health_status)

    return JSONResponse(status_code=200, content=health_status)# test
