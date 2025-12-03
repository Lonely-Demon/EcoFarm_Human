# Data Privacy & Risk

This document outlines data policies, PII handling, image retention, and key risk controls for the EcoFarm_Human MVP.

## Core Principles
- Minimize PII collection.
- Store images & PII only with user consent and allow deletion on request.
- Keep a record of model inferences for auditability but only store minimal metadata necessary to debug.
- Use secure channels for data transfer (TLS), and store secrets using GitHub Secrets and provider secret managers.

## Data Types & Handling
- Personal Data:
  - user email, phone, name: store only necessary fields; apply password hashing (bcrypt).
- Location Data:
  - farm polygons (geojson): store as geometry columns in PostGIS. Treat them as moderately sensitive.
- Image Data (disease photos):
  - Stored in Supabase Storage with private bucket; link to the `disease_reports` table via key.
  - Use signed URL for temporary access if displaying the image in a frontend.
  - Keep images for a limited time (30–90 days) unless user opts in to longer storage for training.
- Inference & Logs:
  - Store inference outputs, provider name, model name, timestamp, and a small context of the request. Avoid storing PII in inference prompts.

## Consent & Opt-in
- On first use of the `disease_detection` endpoint, explicitly ask for consent to store the image and use it to improve models.
- Use explicit checks and a short consent UI / API flag to log consent.

## Data Deletion (User Requests)
- Provide `DELETE /user/profile` (or data deletion endpoint) that removes PII and optionally references to images but carefully handle DB integrity constraints.
- For images, delete from Supabase Storage and remove metadata references from `disease_reports`.

## Retention & Anonymization
- Default: keep logs & images for 30 days; after which they are removed or anonymized.
- Anonymization: use a separate job to redact any PII references stored in logs or inference metadata.

## Access Control & Secrets
- Use `service_role` only on the server in GitHub Secrets or Render's secret store.
- Use RLS (Row-Level Security) policies in Supabase to ensure users only access their rows.

## Compliance & Regulations
- India: No widely required PII law like GDPR, but follow best practices for data security and not to export datasets without permission.
- GDPR / Privacy conscious: if you expect EU users, add 'Data Processing Agreement' and a clear policy.

## Risk Controls
- Model Risk (AI misdiagnosis): show confidence & caution; require manual review where confidence is low.
- Data Leakage Risk: do not include location or PII in prompts to inference providers; remove PII or hash it before external calls if possible.
- Cost/Abuse: limit inference calls per user; log usage, allow throttles to prevent runaway costs.

## Incident Response
- If a data leak is detected: disable keys, update or rotate affected secrets, investigate logs, notify stakeholders, and follow the deletion or mitigation steps.

## Monitoring & Audit
- Log who accessed what data and when (with `X-Request-ID`).
- Periodically audit Supabase storage and the database for stale images and sensitive PII.

## Developer Guidance
- Mask PII in any developer outputs in logs or error reports.
- Automate the monthly cleanup job that removes or anonymizes old items.

## Summary
- For MVP, maintain a conservative policy: store minimal PII, keep images behind private storage with consent, and provide clear deletion paths. This will meet practical privacy needs while enabling core features.