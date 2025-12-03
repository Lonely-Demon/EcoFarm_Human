# AI Recommendations Service

This service provides simple, heuristic-based crop recommendations for a given (lat, lon) coordinate as an MVP.

Endpoints:
- `POST /ai/rec/` - body: lat, lon, budget, preferred_crops, time_horizon_months
  - Returns: list of ranked crop recommendations with scores and rationale

Important notes:
- For now this service uses `Open-Meteo` for weather and `SoilGrids` for soil. These are public data sources and ideal for MVP.
- This service caches recommendations in `ai_recommendations` DB table.
- Recommendations are basic heuristics; in Phase 2 we will plug in a proper ML model for better accuracy.
