from fastapi.testclient import TestClient
from services.farms.main import app

client = TestClient(app)

def test_create_farm_requires_payload():
    resp = client.post('/farms', json={})
    assert resp.status_code == 422
