# AI Models and Usage

This document details the recommended AI providers and how to integrate pre-trained models in the backend.

## High-level approach
- Use **Hugging Face** inference API as the primary inference provider for image & text models.
- Use **OpenRouter** or another provider as a fallback if Hugging Face rate limits or paid quotas are exceeded.
- Avoid hosting large GPU instances in the MVP to reduce costs; rely on inference APIs with a limited number of calls and caching.
- Provide a wrapper service that standardizes inference calls, caches outputs, and stores metadata for retraining.

## Example inference flow
1. Client uploads an image to a `disease_detection` endpoint.
2. Service uploads raw image to Supabase Storage and stores a reference in `disease_reports` table.
3. Service calls the Hugging Face inference endpoint with the image (or calls a wrapper microservice if you want to support multiple providers).
4. The wrapper caches the result in `disease_reports` (result JSON + confidence) and returns the result to the client.
5. If the result is not confident (below threshold), the UI returns a 'low-confidence' message and suggests manual actions or local extension contact.

## Providers & use
- **Hugging Face**: Primary; many image classification models available; can be used via `requests` or `httpx` with `Authorization: Bearer <api-key>`.
- **OpenRouter**: Backup LLM provider for text prompts; fallback if HF rated out or model unavailable.
- **Other**: Vertex AI, OpenAI (beta) - both are paid but can be considered for higher-scale production.

## Sample Python (image inference with HF)
```python
import httpx

HF_API_URL = "https://api-inference.huggingface.co/models/<owner/model-name>"
HF_TOKEN = os.environ['HUGGING_FACE_API_KEY']

async with httpx.AsyncClient() as client:
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Accept": "application/json"
    }
    files = {"file": open("leaf.jpg", "rb")}
    r = await client.post(HF_API_URL, headers=headers, files=files, timeout=60)
    result = r.json()

# store result and return
```

## Prompting & LLM guidance (Gemini-style prompts)
- For general-purpose LLMs (Gemini-like), use clear system prompts to define role and constraints. Example:
```text
SYSTEM: You are a helpful agronomic assistant. Return concise recommendations for crop and pest management in Tamil Nadu, India. Use local weather & soil indexes and provide confidence levels.
```
- Always store system and user prompts for traceability and debugging.
- Avoid exposing sensitive data in prompts (e.g. user PII) and mask such data before sending to remote inference.

## Caching & Cost Control
- Cache inference results for identical inputs to avoid repeated calls.
- Limit the number of calls with per-user or per-farm quotas.
- Store inference metadata (provider, model name, token cost if available) for billing/tracking.

## Offline/Edge Considerations
- If running local/edge model is later possible, the wrapper should support toggling a local model for inference to reduce costs and latency.

## Logging & Retraining
- Keep user feedback loop: allow users to flag incorrect inferences for manual review.
- Build minimal labeling pipeline: store flagged images & labels for future fine-tuning.

## Rate Limits & Fallback
- If Hugging Face rejects calls or reaches rate limits, fallback to OpenRouter or return an informative error to the user telling them to try again.
