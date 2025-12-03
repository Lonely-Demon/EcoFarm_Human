# Architecture Overview

This document summarizes the architectural approach for the EcoFarm_Human MVP focusing on a modular backend-first FastAPI stack and Supabase for cloud DB/storage.

## Goals
- Backend-first approach: FastAPI modular services, each independently runnable.
- Minimal local tooling and no Docker required locally; services are run with `uvicorn` for local dev and deployed to a lightweight host via GitHub Actions.
- Use Supabase (Postgres + PostGIS) for data and storage.
- Use public free data sources for weather and soil data (Open-Meteo, NASA POWER, SoilGrids, government APIs), and pre-trained public models for inference (Hugging Face primary, OpenRouter fallback).

## Components
- `services/` - folder with each service (auth, users, farms, weather, market, ai_recs, disease_detection, tasks_records, streamlit_demo).
- `common/` - shared code (database connection, models, utilities, configuration loader).
- `Docs/` - documentation assets and runbook.
- `tests/` - unit & integration tests.

## Data Flow (high level)
1. Client/Streamlit -> Auth Service: JWT-based tokens or Supabase Auth.
2. Client -> Farm Service: CRUD for farms (GeoJSON saved in Postgres + PostGIS).
3. Client -> Weather Service -> external providers (Open-Meteo, NASA POWER) + cache -> return forecast.
4. Client -> AI Recommendation Service -> fetch soil/weather/market for region -> return ranked crop suggestions.
5. Client -> Disease Detection Service -> upload image -> inference via Hugging Face -> return label/confidence.

## Design Choices
- Modular monolith: each service is an independent FastAPI app (single code repo), ensuring services can be run independent of each other.
- Supabase for DB + Auth + Storage; avoids local Docker and reduces infra overhead.
- Streamlit used only for local QA/demos.

## Notes
- Focus on Tamil Nadu (India) regional datasets and localized recommendations. This will guide the choice of public datasets and market sources.
- Marketplace and community features are excluded from MVP per project goals.
