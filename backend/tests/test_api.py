import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_list_patients():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

@pytest.mark.asyncio
async def test_list_patients_with_filter():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients?target=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(p["target"] == 1 for p in data)

@pytest.mark.asyncio
async def test_get_patient_by_id():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["age"] == 50

@pytest.mark.asyncio
async def test_get_patient_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients/99999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_stats_summary():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] == 3
    assert data["heart_disease_positive"] == 2
    assert data["heart_disease_negative"] == 1

@pytest.mark.asyncio
async def test_pagination():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
