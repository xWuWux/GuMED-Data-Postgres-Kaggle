import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import Base, get_db
from app.models import HeartDisease

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/testdb"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def override_get_db():
    async with TestSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        test_patients = [
            HeartDisease(age=50, sex=1, cp=2, trestbps=130, chol=220,
                        fbs=0, restecg=0, thalach=140, exang=0,
                        oldpeak=1.5, slope=1, ca=0.0, thal=2.0, target=1),
            HeartDisease(age=35, sex=0, cp=1, trestbps=120, chol=180,
                        fbs=0, restecg=1, thalach=160, exang=0,
                        oldpeak=0.5, slope=2, ca=0.0, thal=3.0, target=0),
            HeartDisease(age=65, sex=1, cp=0, trestbps=140, chol=250,
                        fbs=1, restecg=0, thalach=120, exang=1,
                        oldpeak=2.5, slope=1, ca=1.0, thal=2.0, target=1),
        ]
        session.add_all(test_patients)
        await session.commit()
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def anyio_backend():
    return "asyncio"
