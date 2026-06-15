import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    """Test health endpoint"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_list_patients():
    """Test listing all patients"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["age"] == 50
    assert data[1]["target"] == 0

@pytest.mark.asyncio
async def test_list_patients_with_filter():
    """Test filtering by target (disease status)"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Filter for patients WITH disease
        response = await client.get("/api/v1/patients?target=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(p["target"] == 1 for p in data)

@pytest.mark.asyncio
async def test_get_patient_by_id():
    """Test getting a single patient by ID"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["age"] == 50
    assert data["sex"] == 1

@pytest.mark.asyncio
async def test_get_patient_not_found():
    """Test 404 for non-existent patient"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_get_stats_summary():
    """Test statistics endpoint"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/patients/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] == 3
    assert data["heart_disease_positive"] == 2
    assert data["heart_disease_negative"] == 1
    assert data["average_age"] == 50.0  # (50+35+65)/3 = 50.0

@pytest.mark.asyncio
async def test_pagination():
    """Test skip and limit parameters"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Get first patient only
        response = await client.get("/api/v1/patients?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1

@pytest.mark.asyncio
async def test_openapi_docs_available():
    """Test that OpenAPI docs are accessible"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/docs")
    assert response.status_code == 200
