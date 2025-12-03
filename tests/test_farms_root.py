from fastapi.testclient import TestClient
from services.farms.main import app

client = TestClient(app)

def test_root():
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json().get('status') == 'farms service up'
