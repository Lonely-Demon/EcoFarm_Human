import pytest
from fastapi.testclient import TestClient
from services.ai_recs.main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def sample_weather():
    return {"hourly": {"temperature_2m": [28, 29, 30]}, "timezone": "UTC"}

@pytest.fixture
def sample_soil():
    return {"properties": {"phh2o": {"mean": 6.0}}}

@patch('services.ai_recs.routers.fetch_weather')
@patch('services.ai_recs.routers.fetch_soil')
def test_recommendations(mock_soil, mock_weather, sample_soil, sample_weather):
    mock_weather.return_value = sample_weather
    mock_soil.return_value = sample_soil

    resp = client.post('/ai/rec/', json={"lat":12.9, "lon":80.2, "preferred_crops": ["tomato"]})
    assert resp.status_code == 200
    data = resp.json()
    assert 'recommendations' in data
    assert isinstance(data['recommendations'], list)
    # Top recommendation should be tomato due to preference and matching pH
    assert data['recommendations'][0]['crop'] == 'tomato'