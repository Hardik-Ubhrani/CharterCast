import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "PORTWISE AI Backend")
VERSION = os.getenv("VERSION", "0.1.0")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "https://chartercastm.vercel.app",
]
CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "")
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_RAW.split(",") if origin.strip()]
for default_origin in DEFAULT_CORS_ORIGINS:
    if default_origin not in CORS_ORIGINS:
        CORS_ORIGINS.append(default_origin)

from contextlib import asynccontextmanager
from backend.models.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB
    init_db()
    yield

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Intelligent Freight Forecasting Model & Decision Engine for Bulk Cargo Chartering",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Timing & Logging Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if DEBUG else "An unexpected error occurred. Please check request parameters.",
            "path": request.url.path
        }
    )

# Include Routers
from backend.api.health import router as health_router
from backend.api.forecast import router as forecast_router
from backend.api.vessel import router as vessel_router
from backend.api.risk import router as risk_router
from backend.api.scenario import router as scenario_router
from backend.api.analyze import router as analyze_router
from backend.api.freight import router as freight_router
from backend.api.trade_route import router as trade_route_router

app.include_router(health_router, prefix="/api")
app.include_router(forecast_router, prefix="/api")
app.include_router(vessel_router, prefix="/api")
app.include_router(risk_router, prefix="/api")
app.include_router(scenario_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(freight_router, prefix="/api")
app.include_router(trade_route_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": f"Welcome to {APP_NAME} API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host=host, port=port, reload=DEBUG)
