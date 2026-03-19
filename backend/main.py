from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.executive_router import router as executive_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.debug_router import router as debug_router
from app.routers.products_router import router as products_router
from app.routers.insights_router import router as insights_router
from app.routers.analysis_router import router as analysis_router


app = FastAPI(
    title="Business Ops Analytics API",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
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