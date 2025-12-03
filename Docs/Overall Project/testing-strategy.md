# Testing Strategy

This document provides a test plan for unit, integration, contract, and E2E tests for the FastAPI modular backend.

## Goals
- Ensure APIs behave correctly and inter-service contracts remain intact.
- Validate AI inference errors, confidence values, and data flow.
- Prevent regressions with CI pipelines for each service.

## Testing Types
### Unit Tests
- Framework: `pytest` + `pytest-asyncio`
- Aim: isolate business logic; mock external calls using `pytest-mock`, `responses`, or `vcrpy`.
- Coverage target: 60–80% for MVP services.

### Integration Tests
- Use FastAPI's `TestClient` for each service.
- Integration tests run against a staging Supabase project (different DB & keys in CI).
- Include DB setup/teardown scripts and seed data.

### Contract (OpenAPI) Tests
- Export OpenAPI schemas JSON and run automated contract tests to ensure endpoints follow the expected schema.
- Tools: `schemathesis`, `prism` (or a small JSON schema checks script).

### E2E Tests
- Lightweight E2E tests using a combination of `pytest` + HTTP requests and Streamlit manual checks.
- Optionally include Playwright for UI testing if the Streamlit or eventual frontend interface is deployed.

### AI Model Tests
- Unit & integration tests for the inference wrapper; mock Hugging Face/OpenRouter responses.
- Confidence thresholds and assertions: ensure output structure & `confidence` field present.

## CI Integration (GitHub Actions)
- Each service has a GH Action workflow:
  - Steps on PR: install deps, lint, run unit tests, run contract tests.
  - Steps on merge to `main`: run integration tests against a `staging` Supabase project, run a smoke test; if passes, run deployment job to Render.

## Test Data
- Maintain small seed data sets for the staging DB.
- Use a separate Supabase project for staging & CI test runs if possible.

## Test Commands
- Local unit tests:
```powershell
pytest services/<service>/ -q
```
- Run integration tests locally with `DATABASE_URL` pointing to `staging` Supabase.

## Mocking External APIs
- For weather & market endpoints: use recorded responses with `vcrpy`.
- For Hugging Face: use mocked JSON responses for classification.

## Observability & Telemetry
- Tests should log `X-Request-ID` and `trace_id` for debugging in CI.

## Reporting
- Test coverage reports in GH Actions artifacts.
- Basic badge in README to show passing status & coverage.

## Additional Checks
- Linting & type checks (mypy) and static analysis on PR to keep code quality.
