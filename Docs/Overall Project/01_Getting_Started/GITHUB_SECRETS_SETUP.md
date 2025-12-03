# GitHub Secrets Setup Checklist

This guide helps you configure all required secrets for the CI/CD pipelines to work properly.

## Quick Setup Steps

### 1. Navigate to Repository Settings
- Go to your GitHub repository
- Click **Settings** → **Secrets and variables** → **Actions**

### 2. Add Required Secrets

| Secret Name | Value | Source | Used By |
|---|---|---|---|
| `RENDER_API_KEY` | Your Render API key | [Render Dashboard](https://dashboard.render.com/api-tokens) | All deploy workflows |
| `RENDER_SERVICE_ID_FARMS` | Service ID for farms service | Render UI → ecofarm-farms → More → Service ID | deploy-farms.yml |
| `RENDER_SERVICE_ID_AUTH` | Service ID for auth service | Render UI → ecofarm-auth → More → Service ID | deploy-auth.yml |
| `RENDER_SERVICE_ID_FARMS_STAGING` | Service ID for staging farms | Render UI → ecofarm-farms-staging → More → Service ID | deploy-farms-staging.yml |
| `RENDER_SERVICE_ID_AUTH_STAGING` | Service ID for staging auth | Render UI → ecofarm-auth-staging → More → Service ID | deploy-auth-staging.yml |
| `RENDER_SERVICE_ID_AI_RECS_STAGING` | Service ID for staging AI recs | Render UI → ecofarm-ai-recs-staging → More → Service ID | deploy-ai-recs-staging.yml |
| `RENDER_SERVICE_ID_WEATHER_STAGING` | Service ID for staging weather | Render UI → ecofarm-weather-staging → More → Service ID | deploy-weather-staging.yml |
| `RENDER_SERVICE_ID_AI_RECS` | Service ID for AI recs service | Render UI → ecofarm-ai-recs → More → Service ID | deploy-ai-recs.yml |
| `SLACK_WEBHOOK` | Slack incoming webhook URL | [Create at Slack API](https://api.slack.com/apps) → Incoming Webhooks | synthetic-checks.yml |
| `STAGING_BASE_URL` | Staging environment base URL | Your staging domain (e.g., `https://staging-api.ecofarm.com`) | synthetic-checks.yml |
| `PROD_BASE_URL` | Production environment base URL | Your production domain (e.g., `https://api.ecofarm.com`) | synthetic-checks.yml |

### 3. Verify All Service IDs

To find a service ID in Render:
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on the service name
3. Click **More** → **Service ID**
4. Copy and paste into the GitHub secret

### 4. Test the Setup

**Option A: Manual Trigger**
```bash
# Trigger synthetic checks workflow manually
gh workflow run synthetic-checks.yml --repo your-org/your-repo
```

**Option B: Push and Watch**
```bash
# Make a small change and push to main to trigger deploy workflow
git commit --allow-empty -m "test: trigger CI/CD"
git push origin main
```

Then check:
- ✅ GitHub Actions tab → workflow status
- ✅ Slack channel → receives notification
- ✅ Render dashboard → deployment status

## What Each Workflow Does

### Deploy Workflows (deploy-*.yml)
- **Trigger**: Push to `main` (production) or `dev` (staging)
- **Steps**:
  1. Run tests
  2. Set Sentry release via Render API
  3. Trigger deployment on Render
- **Success Indicator**: Green checkmark in Actions tab + service deploys on Render

### Synthetic Checks (synthetic-checks.yml)
- **Trigger**: Every 6 hours (configurable in cron)
- **Steps**:
  1. Check staging endpoints
  2. Check production endpoints
  3. Send Slack notification
  4. Create GitHub Issue if 2+ consecutive failures
- **Success Indicator**: Slack message with ✅ PASSED status

## Troubleshooting

### Workflow fails with "401 Unauthorized"
→ Check `RENDER_API_KEY` is correct and has permission to manage services

### Slack notifications not arriving
→ Verify `SLACK_WEBHOOK` is valid (test in Slack app first)

### Synthetic checks failing but services are up
→ Verify `STAGING_BASE_URL` and `PROD_BASE_URL` are correct and accessible

### GitHub Issues not created
→ Check if `synthetic-check-failure` label exists in repo. If not, create it manually.

## Additional Configuration

### Creating Slack Webhook
1. Go to https://api.slack.com/apps
2. Create New App → From scratch
3. Choose your workspace
4. Go to **Incoming Webhooks** → Activate
5. Click **Add New Webhook to Workspace**
6. Select channel (e.g., #deploys or #alerts)
7. Copy webhook URL to `SLACK_WEBHOOK` secret

### Customizing Check Frequency
Edit `.github/workflows/synthetic-checks.yml`:
```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Change 6 to desired hours (0-23)
```

---
Once all secrets are configured, your CI/CD pipeline is ready to go!
