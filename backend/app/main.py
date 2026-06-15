from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine, Base
from .routers import patients

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="GuMED Medical Data Platform",
    description="REST API for the UCI Heart Disease dataset",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(patients.router, prefix="/api/v1", tags=["patients"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
