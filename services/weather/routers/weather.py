from fastapi import APIRouter, HTTPException, Depends
import httpx
from common.config import settings
from common.db import get_db
from sqlalchemy.orm import Session
from services.weather import crud

router = APIRouter()

@router.get('/')
async def get_weather(lat: float, lon: float, provider: str = 'auto', db: Session = Depends(get_db)):
    # Query Open-Meteo
    try:
        # Check cache first
        cached = crud.get_cached_weather(db, lat, lon)
        if cached and (provider == 'auto' or provider == cached.provider):
            return {"provider": cached.provider, "data": cached.payload, "cached_at": str(cached.cached_at)}

        # Try Open-Meteo if provider is auto or open-meteo
        if provider == 'auto' or provider == 'open-meteo':
            url = f"{settings.OPEN_METEO_URL}/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=30)
            if r.status_code == 200:
                payload = r.json()
                crud.save_weather_cache(db, 'open-meteo', lat, lon, payload)
                return {"provider": "open-meteo", "data": payload}

        # Fall back to NASA POWER if available
        if provider == 'auto' or provider == 'nasa-power':
            # Example NASA POWER query (daily TMAX/TMIN) - adjust to actual endpoint parameters
            nasa_url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MAX,T2M_MIN&community=AG&latitude={lat}&longitude={lon}&format=JSON"
            async with httpx.AsyncClient() as client:
                r2 = await client.get(nasa_url, timeout=30)
            if r2.status_code == 200:
                payload = r2.json()
                crud.save_weather_cache(db, 'nasa-power', lat, lon, payload)
                return {"provider": "nasa-power", "data": payload}

        raise HTTPException(status_code=500, detail="Failed to fetch weather from available providers")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
