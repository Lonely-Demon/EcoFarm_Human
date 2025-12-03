from fastapi.testclient import TestClient
from services.auth.main import app

client = TestClient(app)

def test_register_requires_email_password():
    resp = client.post('/auth/register', json={})
    assert resp.status_code == 422
