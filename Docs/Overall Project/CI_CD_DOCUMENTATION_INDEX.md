# CI/CD Documentation Index

**Last Updated:** December 2, 2025  
**Status:** ✅ Ready for Implementation

## Quick Links

### 🚀 Getting Started
1. **[CI_CD_ENHANCEMENTS_SUMMARY.md](./CI_CD_ENHANCEMENTS_SUMMARY.md)** - Overview of all changes (START HERE)
2. **[GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md)** - Configure GitHub secrets step-by-step
3. **[PRE_LAUNCH_CHECKLIST.md](./PRE_LAUNCH_CHECKLIST.md)** - Validation checklist before going live

### 📖 Reference Documentation
- **[render-setup.md](./render-setup.md)** - Render integration and deployment details
- **[SYNTHETIC_CHECKS_RUNBOOK.md](./SYNTHETIC_CHECKS_RUNBOOK.md)** - Incident response guide

---

## What's New

### Three Major Improvements Implemented

#### 1. **Sentry Release Tagging** 
   - Automatically tags each deployment with GitHub SHA
   - All deploy workflows updated (7 files)
   - **No configuration needed** - runs automatically

#### 2. **Slack Alerting**
   - Rich notifications for synthetic health checks
   - Color-coded status (🟢 pass / 🔴 fail / 🟠 partial)
   - Links to workflow logs
   - **Requires:** `SLACK_WEBHOOK` GitHub secret

#### 3. **GitHub Issues Escalation**
   - Auto-creates issue on 2+ consecutive failures
   - Updates single issue per incident (no spam)
   - Labels: `synthetic-check-failure`, `urgent`
   - **No configuration needed** - runs automatically

---

## Implementation Checklist

### Phase 1: Setup (30 mins)
- [ ] Read [CI_CD_ENHANCEMENTS_SUMMARY.md](./CI_CD_ENHANCEMENTS_SUMMARY.md)
- [ ] Follow [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) to add 11 secrets
- [ ] Create GitHub labels: `synthetic-check-failure`, `urgent`

### Phase 2: Validation (15 mins)
- [ ] Complete [PRE_LAUNCH_CHECKLIST.md](./PRE_LAUNCH_CHECKLIST.md)
- [ ] Run manual workflow trigger: `gh workflow run synthetic-checks.yml`
- [ ] Verify Slack notification arrives
- [ ] Check Render deployment worked

### Phase 3: Team Training (20 mins)
- [ ] Review [SYNTHETIC_CHECKS_RUNBOOK.md](./SYNTHETIC_CHECKS_RUNBOOK.md) with team
- [ ] Set up on-call rotation
- [ ] Configure Slack channel alerts

### Phase 4: Go Live
- [ ] All checkboxes above complete ✅
- [ ] Team confident with runbook
- [ ] Make first production deploy
- [ ] Monitor next synthetic check run

---

## Document Guide

| Document | Purpose | Audience | Time |
|----------|---------|----------|------|
| [CI_CD_ENHANCEMENTS_SUMMARY.md](./CI_CD_ENHANCEMENTS_SUMMARY.md) | What changed and why | Everyone | 10 min |
| [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) | How to configure secrets | DevOps / Admin | 15 min |
| [PRE_LAUNCH_CHECKLIST.md](./PRE_LAUNCH_CHECKLIST.md) | Verify everything works | DevOps / QA | 30 min |
| [SYNTHETIC_CHECKS_RUNBOOK.md](./SYNTHETIC_CHECKS_RUNBOOK.md) | How to handle failures | On-call Engineers | 15 min |
| [render-setup.md](./render-setup.md) | Architecture & deployment | Everyone | 15 min |

---

## Key Features at a Glance

### Sentry Release Tagging
```yaml
# Automatic - happens before every deploy
SENTRY_RELEASE = github.sha (e.g., "a1b2c3d...")
```
✅ No setup needed  
✅ Automatic on every deploy  
✅ Improves error tracking accuracy

### Slack Notifications
```
Every 6 hours, after synthetic checks run:
[Slack message with status, colors, and links]
```
✅ Requires `SLACK_WEBHOOK` secret  
✅ Optional (checks continue if webhook fails)  
✅ Rich formatting with colors

### GitHub Issues
```
On 2+ consecutive failures:
[Automatic GitHub Issue created with details and links]
```
✅ Requires labels (created manually first time)  
✅ Single issue per incident (updates existing)  
✅ Labeled for easy filtering

---

## Secrets Required

Add these 11 GitHub secrets (see [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) for details):

1. `RENDER_API_KEY` - Render API token
2. `RENDER_SERVICE_ID_FARMS` - Service ID
3. `RENDER_SERVICE_ID_AUTH` - Service ID
4. `RENDER_SERVICE_ID_AI_RECS` - Service ID
5. `RENDER_SERVICE_ID_FARMS_STAGING` - Service ID
6. `RENDER_SERVICE_ID_AUTH_STAGING` - Service ID
7. `RENDER_SERVICE_ID_AI_RECS_STAGING` - Service ID
8. `RENDER_SERVICE_ID_WEATHER_STAGING` - Service ID
9. `SLACK_WEBHOOK` - Slack webhook URL (optional)
10. `STAGING_BASE_URL` - Staging domain
11. `PROD_BASE_URL` - Production domain

---

## Workflows Updated

### Deploy Workflows (All 7)
```
Before Deploy:
✅ Run tests
✅ Set SENTRY_RELEASE via Render API
✅ Trigger deployment
```

### Synthetic Checks
```
Every 6 hours:
✅ Check /healthz (both envs)
✅ Check /weather (both envs)
✅ Check /ai/rec (both envs)
✅ Send Slack notification
✅ Create/update GitHub Issue if failing
```

---

## Troubleshooting

### Slack not working?
→ See [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) → Troubleshooting → "Slack notifications not arriving"

### Sentry not tracking releases?
→ Verify `SENTRY_DSN` is set in Render service environment

### GitHub Issue not creating?
→ Create labels manually: `synthetic-check-failure`, `urgent`

### Need more help?
→ See [SYNTHETIC_CHECKS_RUNBOOK.md](./SYNTHETIC_CHECKS_RUNBOOK.md) → Troubleshooting section

---

## Next Steps

1. **Read:** [CI_CD_ENHANCEMENTS_SUMMARY.md](./CI_CD_ENHANCEMENTS_SUMMARY.md) (5 min)
2. **Setup:** [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) (15 min)
3. **Validate:** [PRE_LAUNCH_CHECKLIST.md](./PRE_LAUNCH_CHECKLIST.md) (30 min)
4. **Go Live:** Deploy with confidence! 🚀

---

## Questions?

**For setup questions:** See [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md)  
**For deployment questions:** See [render-setup.md](./render-setup.md)  
**For incident response:** See [SYNTHETIC_CHECKS_RUNBOOK.md](./SYNTHETIC_CHECKS_RUNBOOK.md)  
**For verification:** See [PRE_LAUNCH_CHECKLIST.md](./PRE_LAUNCH_CHECKLIST.md)  
**For overview:** See [CI_CD_ENHANCEMENTS_SUMMARY.md](./CI_CD_ENHANCEMENTS_SUMMARY.md)

---

**Status:** ✅ Ready for implementation  
**Target Launch:** This week  
**Estimated Setup Time:** 1-2 hours total
