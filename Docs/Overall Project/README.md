# EcoFarm_Human - Documentation Index

Welcome! This folder contains project documentation to help developers, testers, and stakeholders get started with the EcoFarm_Human MVP.

## Docs Index
- `architecture-overview.md` - MVP architecture and component overview.
- `modular-architecture.md` - Repo structure and module design; run instructions.
- `deployment-guide.md` - Hosting options, Render steps, GitHub Actions samples.
- `render-setup.md` - Render service setup and GitHub secrets guide for CI/CD.
- `onboarding.md` - Developer onboarding instructions (no Docker required).
- `supabase-setup.md` - Step-by-step Supabase setup with PostGIS & migrations.
- `ai-models-and-usage.md` - AI provider integration choices and cost & caching guidance.
- `tamilnadu-data-sources.md` - Public data sources and scraping strategy for Tamil Nadu.
- `api-contracts.md` - Endpoint samples and schema examples (OpenAPI samples).
- `sprint-plan.md` - 3-sprint plan with deliverables & acceptance criteria.
- `testing-strategy.md` - Unit/integration/contract and E2E test strategy.
- `runbook.md` - Operational runbook and incident response.
- `data-privacy-and-risk.md` - Data handling, privacy & retention policies.
 - `ai-models-and-usage.md` - AI provider integration choices and cost & caching guidance.

## Quick Start
- Review `onboarding.md` to set up dev environment.
- Follow `supabase-setup.md` to create your Supabase project and enable PostGIS.
- Run a service: `uvicorn services.farms.main:app --reload --port 8002` (set env variables first).
- Open the Swagger UI: `http://localhost:8002/docs` for the running service.

## Contribution & Updates
- Update docs when you change deployment flows or service contracts.
- Create PRs for code & doc changes and keep docs in sync with any API change.

## Contact
- If you need help, add a comment in the `README.md` or open an issue in the repo.

