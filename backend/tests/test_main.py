from fastapi.testclient import TestClient
from backend.main import app
import pytest

client = TestClient(app)

# Szerver fut-e
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running", "docs_url": "/docs"}

# Valós adat lekérése (HUN)
def test_get_hun_data():
    response = client.get("/api/dashboard/HUN")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "HUN"
    assert "metrics" in data

# hibás országkód (Paraméterezett)
@pytest.mark.parametrize("bad_code", ["XYZ", "123", "NONEXISTENT"])
def test_404_error(bad_code):
    response = client.get(f"/api/dashboard/{bad_code}")
    assert response.status_code == 404