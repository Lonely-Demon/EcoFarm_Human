import pytest
from fastapi.testclient import TestClient
from services.weather.main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def sample_weather_json():
    return {"hourly": {"temperature_2m": [25, 26, 27]}, "timezone": "UTC"}

@patch('services.weather.routers.httpx.AsyncClient.get')
def test_weather_cache_and_fallback(mock_get, sample_weather_json):
    # Simulate open-meteo response
    class MockResp:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json = json_data
        def json(self):
            return self._json

    async def fake_get(url, timeout=30):
        # Return a successful open-meteo response
        return MockResp(200, sample_weather_json)

    mock_get.side_effect = fake_get

    resp = client.get('/weather?lat=12.9&lon=80.2')
    assert resp.status_code == 200
    body = resp.json()
    assert body.get('provider') == 'open-meteo'
    assert 'data' in body

    # Call again to ensure cache returns (no errors)
    resp2 = client.get('/weather?lat=12.9&lon=80.2')
    assert resp2.status_code == 200
    assert resp2.json().get('provider') == 'open-meteo'

*** End Patch