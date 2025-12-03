from fastapi import APIRouter, Depends, HTTPException
from services.ai_recs import schemas, crud
from common.db import get_db
from sqlalchemy.orm import Session
import httpx
from common.config import settings

router = APIRouter()

# Minimal static crop profiles (for MVP) - ideally be in DB or a YAML file
CROP_PROFILES = {
    "tomato": {"ph_min": 5.5, "ph_max": 6.8, "max_temp": 35},
    "brinjal": {"ph_min": 5.0, "ph_max": 7.0, "max_temp": 36},
    "millet": {"ph_min": 5.5, "ph_max": 7.5, "max_temp": 42},
}

async def fetch_weather(lat: float, lon: float):
    url = f"{settings.OPEN_METEO_URL}/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=30)
    return r.json() if r.status_code == 200 else None

async def fetch_soil(lat: float, lon: float):
    # Use SoilGrids for basic soil pH - example GET request (SoilGrids API needs parameterized URL)
    url = f"https://rest.soilgrids.org/query?lon={lon}&lat={lat}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=30)
    return r.json() if r.status_code == 200 else None

@router.post('/', response_model=schemas.RecommendationResponse)
async def recommend(payload: schemas.RecommendationRequest, db: Session = Depends(get_db)):
    if not payload.lat or not payload.lon:
        raise HTTPException(status_code=400, detail='lat & lon required')

    # Fetch weather & soil - if fetch fails, continue gracefully
    weather = await fetch_weather(payload.lat, payload.lon)
    soil = await fetch_soil(payload.lat, payload.lon)

    # Basic heuristic: favor crops with matching pH and temp
    recommendations = []
    ph = None
    try:
        # SoilGrids returns many layers; use 0-5cm pH if available
        ph = soil.get('properties', {}).get('phh2o', {}).get('mean', None) if soil else None
    except Exception:
        ph = None

    # Extract mean temperature from weather (hourly first value)
    mean_temp = None
    try:
        temps = weather.get('hourly', {}).get('temperature_2m', []) if weather else []
        if temps:
            mean_temp = sum(temps) / len(temps)
    except Exception:
        mean_temp = None

    for crop, profile in CROP_PROFILES.items():
        score = 0.0
        rationale_pieces = []
        # pH match
        if ph is not None:
            if profile['ph_min'] <= ph <= profile['ph_max']:
                score += 0.5
                rationale_pieces.append(f"pH {ph} within {profile['ph_min']}-{profile['ph_max']}")
            else:
                # penalty proportionally
                score += max(0, 0.2 - abs((ph - (profile['ph_min'] + profile['ph_max'])/2)) / 10)
                rationale_pieces.append(f"pH {ph} outside ideal range")
        else:
            rationale_pieces.append('No soil pH data')

        # Temperature match
        if mean_temp is not None:
            if mean_temp <= profile['max_temp']:
                score += 0.4
                rationale_pieces.append(f"mean temp {mean_temp:.1f}C <= max {profile['max_temp']}")
            else:
                rationale_pieces.append(f"mean temp {mean_temp:.1f}C > max {profile['max_temp']}")

        # Budget & preferences bump
        if payload.preferred_crops and crop in payload.preferred_crops:
            score += 0.2
            rationale_pieces.append('Preferred crop')

        # normalize
        score = min(1.0, score)
        recommendations.append({
            'crop': crop,
            'score': round(score, 2),
            'rationale': '; '.join(rationale_pieces)
        })

    # Sort by score desc
    recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)

    # Save result in DB
    try:
        saved = crud.save_recommendation(db, payload.dict(), {'recommendations': recommendations})
    except Exception:
        saved = None

    return {'recommendations': recommendations}
