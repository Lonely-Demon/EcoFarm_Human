# API Contracts (OpenAPI Samples)

This file documents the minimal set of core APIs for the MVP. These are example payloads and responses for FastAPI endpoints; use FastAPI's generated OpenAPI as the canonical source.

Notes:
- Each service will have its own OpenAPI/Swagger docs (e.g., `http://localhost:8002/docs`).
- For cross-service contract tests, export OpenAPI JSON and publish in `Docs/Overall Project/api_contract_schemas/`.

---

## Auth Service
- POST /auth/register
  - Request:
    ```json
    {
      "email": "farmer@example.com",
      "password": "securepassword",
      "name": "Ramu",
      "phone": "+919876543210",
      "language": "ta"
    }
    ```
  - Response (201):
    ```json
    {
      "id": "uuid",
      "email": "farmer@example.com",
      "name": "Ramu",
      "token": "<jwt>"
    }
    ```

- POST /auth/login
  - Request:
    ```json
    { "email":"farmer@example.com", "password":"securepassword" }
    ```
  - Response (200):
    ```json
    { "token": "<jwt>", "refresh_token": "<refresh>" }
    ```

---

## Users / Profile
- GET /user/profile
  - Auth required (Bearer token)
  - Response:
    ```json
    {
      "id": "uuid",
      "name": "Ramu",
      "email": "farmer@example.com",
      "phone": "+919876543210",
      "language": "ta",
      "created_at": "2025-12-01T12:34:56Z"
    }
    ```

- PUT /user/profile
  - Request: same object as above (name/phone/language update permitted)
  - Response: (200) updated profile

---

## Farms & Sectors
- POST /farms
  - Request:
    ```json
    {
      "name":"My Farm",
      "geom": {
        "type":"Polygon",
        "coordinates": [[[80.0, 12.5], [80.1, 12.5], [80.1, 12.6], [80.0, 12.6], [80.0, 12.5]]] 
      }
    }
    ```
  - Response: (201)
    ```json
    {
      "id": "uuid",
      "name": "My Farm",
      "area": 1.23,
      "geom": {...},
      "created_at": "..."
    }
    ```

- POST /farms/{farm_id}/sectors
  - Request: polygon & metadata
  - Response: (201) sector created

- GET /farms/{id}
  - Response includes farm with sector list and GeoJSON fields

---

## Weather Service (Aggregator)
- GET /weather?lat=12.5&lon=80.0
  - Response:
    ```json
    {
      "provider": "open-meteo",
      "location": {"latitude":12.5,"longitude":80},
      "current": {"temp_c":28.3, "wind_kph":12.0, "humidity":80},
      "forecast": [{"date":"2025-12-03","temp_max":29,"temp_min":25}]
    }
    ```

---

## Market Price Service
- GET /market/prices?location=Tamil%20Nadu&crop_id=tomato
  - Response (200):
    ```json
    {
      "crop_id":"tomato",
      "market":"Chennai Mandi",
      "price": 18.0,
      "unit":"KG",
      "collected_at":"2025-12-01T06:00:00Z",
      "source":"eNAM"
    }
    ```

---

## AI Planting Recommendation
- POST /ai/planting-recommendation
  - Input:
    ```json
    {
      "farm_id":"uuid",
      "sector_id":"uuid",
      "budget":50000,
      "preferred_crops":["tomato","brinjal"],
      "time_horizon_months":6
    }
    ```
  - Response (200):
    ```json
    {
      "recommendations":[
        {"crop":"tomato","score":0.9,"rationale":"Good market price & soil compatibility"},
        {"crop":"brinjal","score":0.7,"rationale":"Moderate market interest"}
      ],
      "created_at":"2025-12-01T12:00:00Z"
    }
    ```

---

## AI Disease Detection
- POST /ai/diagnose
  - Content-Type: multipart/form-data (image: file, metadata: JSON)
  - Input: image and optional sector_id
  - Response (200):
    ```json
    {
      "diagnosis": "Leaf Blight",
      "confidence": 0.87,
      "actions": [
         "See guidance: https://.../blight-gid",
         "Consider removing affected leaves"
      ],
      "provider":"huggingface",
      "inference_time_ms":342
    }
    ```

---

## Tasks & Records
- POST /tasks
  - Input: task details (title, due_date, sector_id, assigned_to, recurrence)
  - Response: created task

- POST /records
  - Input: type (planting|harvest|expense), sector_id, data
  - Response: (201) stored

---

## Notes
- All endpoints require a Bearer token except `POST /auth/register` & `POST /auth/login`.
- Use GeoJSON geometry for all sector/farm spatial fields.
- Use pagination for listing endpoints when required (limit & offset or cursor).
- Add `X-Request-ID` header in requests for traceability across modules.

---

## Next steps
- Export OpenAPI specs from FastAPI services and store them in `Docs/Overall Project/api_contract_schemas` for contract testing.
- Implement JSON schema test harness in CI for contracts.

---

## AI Recommendations (Service: `ai_recs`)
- POST /ai/rec/
  - Request example (JSON):
    ```json
    {
      "lat": 12.9,
      "lon": 80.2,
      "budget": 50000,
      "preferred_crops": ["tomato","brinjal"],
      "time_horizon_months": 6
    }
    ```
  - Response (200):
    ```json
    {
      "recommendations": [
         {"crop":"tomato","score":0.92,"rationale":"pH 6.0 within range; preferred crop; mean temp within threshold"},
         {"crop":"brinjal","score":0.67,"rationale":"pH 6.0 within range; mean temp marginal"}
      ]
    }
    ```
