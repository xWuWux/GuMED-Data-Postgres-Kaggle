import os

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/testdb",
)

from app.main import app
from app.database import Base, get_db
from app.models import HeartDisease


TEST_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/testdb",
)

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    async with TestSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        session.add_all(
            [
                HeartDisease(
                    id=1,
                    age=50,
                    sex=1,
                    cp=2,
                    trestbps=120,
                    chol=200,
                    fbs=0,
                    restecg=1,
                    thalach=160,
                    exang=0,
                    oldpeak=1.0,
                    slope=2,
                    ca=0,
                    thal=2,
                    target=1,
                ),
                HeartDisease(
                    id=2,
                    age=35,
                    sex=0,
                    cp=1,
                    trestbps=110,
                    chol=180,
                    fbs=0,
                    restecg=1,
                    thalach=170,
                    exang=0,
                    oldpeak=0.0,
                    slope=2,
                    ca=0,
                    thal=2,
                    target=0,
                ),
                HeartDisease(
                    id=3,
                    age=65,
                    sex=1,
                    cp=0,
                    trestbps=140,
                    chol=260,
                    fbs=1,
                    restecg=0,
                    thalach=130,
                    exang=1,
                    oldpeak=2.0,
                    slope=1,
                    ca=1,
                    thal=3,
                    target=1,
                ),
            ]
        )
        await session.commit()

    yield


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield async_client
