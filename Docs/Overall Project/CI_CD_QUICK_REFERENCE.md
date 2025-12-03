# CI/CD Quick Reference Card

**Print this or bookmark for easy access!**

---

## 📋 Workflow Triggers

| Workflow | Trigger | What Happens |
|----------|---------|--------------|
| deploy-farms.yml | Push to `main` | Tests → Set Sentry Release → Deploy |
| deploy-auth.yml | Push to `main` | Tests → Set Sentry Release → Deploy |
| deploy-ai-recs.yml | Push to `main` | Tests → Set Sentry Release → Deploy |
| deploy-farms-staging.yml | Push to `dev` | Tests → Set Sentry Release → Deploy |
| deploy-auth-staging.yml | Push to `dev` | Tests → Set Sentry Release → Deploy |
| deploy-ai-recs-staging.yml | Push to `dev` | Tests → Set Sentry Release → Deploy |
| deploy-weather-staging.yml | Push to `dev` | Tests → Set Sentry Release → Deploy |
| synthetic-checks.yml | Every 6 hours (manual: `gh workflow run synthetic-checks.yml`) | Check endpoints → Slack → GitHub Issue |

---

## 🔔 Alert Indicators

### Slack Message Color Coding
- 🟢 **GREEN** - All checks passed ✅
- 🔴 **RED** - Checks failed ❌
- 🟠 **ORANGE** - Partial (one env up, one down) ⚠️

### GitHub Issue Labels
- `synthetic-check-failure` - Synthetic check failed
- `urgent` - High priority

---

## 🚨 When Checks Fail

### What You'll See
1. **Slack Message** - Immediate notification (red colored)
2. **GitHub Issue** - Created after 2nd consecutive failure

### How to Respond
1. Click Slack link → View workflow logs
2. Identify which endpoint failed (healthz, weather, ai/rec)
3. Check if it's staging, production, or both
4. See [SYNTHETIC_CHECKS_RUNBOOK.md](./SYNTHETIC_CHECKS_RUNBOOK.md) for next steps

### Common Fixes
| Error | Likely Cause | Action |
|-------|--------------|--------|
| `503` or `Connection refused` | Service crashed | Restart in Render dashboard |
| `404` | Endpoint missing | Check if code changed |
| `500` | Code error | Check logs in Render or Sentry |
| `Timeout` | Service too slow | Check CPU/memory in Render |

---

## 🔐 Important Secrets

| Secret | Status | Used For |
|--------|--------|----------|
| RENDER_API_KEY | ✅ Required | Deploy & Sentry tagging |
| RENDER_SERVICE_ID_* (8 total) | ✅ Required | Target services |
| SLACK_WEBHOOK | 🟡 Optional | Notifications |
| STAGING_BASE_URL | ✅ Required | Health checks |
| PROD_BASE_URL | ✅ Required | Health checks |

**See [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) for setup instructions**

---

## 🔍 Quick Diagnostics

### Check Synthetic Checks Status
```bash
gh run list --workflow=synthetic-checks.yml --limit=5
```

### View Latest Deployment
```bash
gh run list --workflow=deploy-farms.yml --limit=1
```

### Manually Trigger Checks (for testing)
```bash
gh workflow run synthetic-checks.yml
```

### Check Service Health Manually
```bash
curl https://api.example.com/healthz
curl https://staging-api.example.com/healthz
```

---

## 📞 Who to Contact

| Issue | Contact |
|-------|---------|
| Deploy failing | DevOps / Platform team |
| Synthetic check failing | On-call engineer |
| Slack not working | DevOps (check webhook) |
| GitHub Issue not creating | Create labels, then check |
| Sentry not tracking | Check SENTRY_DSN in Render |

---

## 🔗 Important Links

- [CI/CD Documentation Index](./CI_CD_DOCUMENTATION_INDEX.md) - Start here
- [GitHub Secrets Setup](./GITHUB_SECRETS_SETUP.md) - Configure secrets
- [Synthetic Checks Runbook](./SYNTHETIC_CHECKS_RUNBOOK.md) - Incident response
- [Pre-Launch Checklist](./PRE_LAUNCH_CHECKLIST.md) - Validation
- [Render Setup](./render-setup.md) - Architecture overview

---

## ⚡ One-Minute Workflows

### Make a Deploy
```bash
git add .
git commit -m "feature: add new feature"
git push origin main  # Triggers deploy
# Check GitHub Actions for status
```

### Test Synthetic Checks
```bash
gh workflow run synthetic-checks.yml
# Wait 2 minutes, check Slack for notification
```

### Check Service Health
```bash
curl -i https://api.example.com/healthz
curl -i https://staging-api.example.com/healthz
```

### View Deployment Logs
```bash
gh run list --workflow=deploy-farms.yml --limit=1
gh run view <RUN_ID> --log
```

---

## ❌ Disabled Features

- Sentry Release Tagging: Set Render env var automatically
- Slack Notifications: Send to #alerts or custom channel
- GitHub Issues: Create on 2+ consecutive failures

**To disable any feature:** Comment out in workflow YAML files (see [CI_CD_ENHANCEMENTS_SUMMARY.md](./CI_CD_ENHANCEMENTS_SUMMARY.md))

---

## ✅ Status Checks

### Green Light (Ready)
- ✅ All GitHub secrets configured
- ✅ Slack webhook working
- ✅ GitHub labels exist
- ✅ Health endpoints responding
- ✅ Last 3 checks passed

### Yellow Light (Caution)
- ⚠️ 1 failed check (watch next run)
- ⚠️ Slack webhook not tested
- ⚠️ One secret missing (but optional)

### Red Light (Blocked)
- ❌ Required secret missing
- ❌ Health endpoints returning 500+
- ❌ 2+ consecutive check failures
- ❌ Recent deploy failing

---

## 📊 Typical Workflow Timeline

```
Push to main
    ↓ (1 sec)
Workflow starts
    ↓ (2 min)
Tests run
    ↓ (30 sec)
Sentry release tagged
    ↓ (10 sec)
Deploy triggered on Render
    ↓ (2-5 min)
Render builds and deploys
    ↓ (1 min)
Service restarts
    ↓ (30 sec)
Deployment complete ✅
```

**Total Time:** ~8-10 minutes

---

## 📖 Reading Order

1. **First time:** Read [CI_CD_ENHANCEMENTS_SUMMARY.md](./CI_CD_ENHANCEMENTS_SUMMARY.md) (10 min)
2. **Setting up:** Follow [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) (15 min)
3. **Before going live:** Complete [PRE_LAUNCH_CHECKLIST.md](./PRE_LAUNCH_CHECKLIST.md) (30 min)
4. **On-call duty:** Bookmark [SYNTHETIC_CHECKS_RUNBOOK.md](./SYNTHETIC_CHECKS_RUNBOOK.md)
5. **Quick lookup:** Use this card!

---

**Last Updated:** December 2, 2025  
**Status:** ✅ Ready for Production
