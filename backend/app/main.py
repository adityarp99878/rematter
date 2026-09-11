from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.db.database import init_db
    from app.config import get_settings
    settings = get_settings()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    init_db()
    if settings.DEMO_MODE:
        from app.db.seed import seed_database
        seed_database()
    yield


app = FastAPI(
    title="Material Rebirth AI",
    description="Agentic AI Marketplace for Circular Construction",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads AFTER creating the dir in lifespan
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

from app.api import materials, requirements, matches, pricing, logistics, impact, verification, transactions, dashboard, notifications

app.include_router(materials.router)
app.include_router(requirements.router)
app.include_router(matches.router)
app.include_router(pricing.router)
app.include_router(logistics.router)
app.include_router(impact.router)
app.include_router(verification.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)
app.include_router(notifications.router)


@app.get("/api/health")
def health():
    from app.config import get_settings
    return {"status": "healthy", "demo_mode": get_settings().DEMO_MODE}
