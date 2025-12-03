# EcoFarm Documentation Index

Welcome! Use this index to navigate the documentation. All docs are organized by purpose.

---

## 📋 Getting Started (Read These First)

Start here if you're new to the project or setting it up for the first time.

- **[PRE_SETUP_RENDER_GITHUB.md](01_Getting_Started/PRE_SETUP_RENDER_GITHUB.md)** — Create GitHub repo and 8 Render services *(pre-requisite)*
- **[GITHUB_SECRETS_SETUP.md](01_Getting_Started/GITHUB_SECRETS_SETUP.md)** — Add secrets to GitHub for CI/CD (Render API key, service IDs, URLs, etc.)
- **[SOLO_SETUP_GUIDE.md](01_Getting_Started/SOLO_SETUP_GUIDE.md)** — Complete setup guide for solo developers (5 steps)
- **[PRE_LAUNCH_CHECKLIST.md](01_Getting_Started/PRE_LAUNCH_CHECKLIST.md)** — Validation checklist before first deploy

### Quick Path
1. Read **PRE_SETUP_RENDER_GITHUB.md** (create GitHub repo + Render services)
2. Read **GITHUB_SECRETS_SETUP.md** (add secrets)
3. Read **SOLO_SETUP_GUIDE.md** (complete setup)
4. Use **PRE_LAUNCH_CHECKLIST.md** before first deploy

---

## 🔄 CI/CD Documentation

Everything about GitHub Actions, Sentry release tagging, Slack alerts, and GitHub Issues escalation.

- **[CI_CD_QUICK_REFERENCE.md](02_CI_CD/CI_CD_QUICK_REFERENCE.md)** — One-page cheat sheet for common CI/CD tasks
- **[CI_CD_ENHANCEMENTS_SUMMARY.md](02_CI_CD/CI_CD_ENHANCEMENTS_SUMMARY.md)** — What changed: Sentry tagging, Slack alerts, GitHub Issues escalation
- **[CI_CD_DOCUMENTATION_INDEX.md](02_CI_CD/CI_CD_DOCUMENTATION_INDEX.md)** — Detailed CI/CD architecture & workflow
- **[SYNTHETIC_CHECKS_RUNBOOK.md](02_CI_CD/SYNTHETIC_CHECKS_RUNBOOK.md)** — How to monitor, debug, and respond to synthetic checks

---

## 🏗️ Architecture

Design decisions, API contracts, and system overview.

- **[architecture-overview.md](03_Architecture/architecture-overview.md)** — High-level system design
- **[modular-architecture.md](03_Architecture/modular-architecture.md)** — Service-based architecture & inter-service communication
- **[api-contracts.md](03_Architecture/api-contracts.md)** — API endpoints & request/response schemas

---

## ⚙️ Operations & Runbooks

Deployment, monitoring, and troubleshooting guides.

- **[deployment-guide.md](04_Operations/deployment-guide.md)** — How to deploy services (manual & automated)
- **[render-setup.md](04_Operations/render-setup.md)** — Render configuration & environment variables
- **[supabase-setup.md](04_Operations/supabase-setup.md)** — Database & Auth setup
- **[monitoring.md](04_Operations/monitoring.md)** — Monitoring, logging, and alerting
- **[runbook.md](04_Operations/runbook.md)** — General operational runbook

---

## 📚 Reference Material

Research, data sources, and technical references.

- **[ai-models-and-usage.md](05_Reference/ai-models-and-usage.md)** — AI/ML models and integration
- **[testing-strategy.md](05_Reference/testing-strategy.md)** — Testing frameworks and approach
- **[data-privacy-and-risk.md](05_Reference/data-privacy-and-risk.md)** — Privacy & security considerations
- **[tamilnadu-data-sources.md](05_Reference/tamilnadu-data-sources.md)** — Regional data sources for Tamil Nadu
- **[sprint-plan.md](05_Reference/sprint-plan.md)** — Development sprint roadmap

---

## 🗂️ Archive

Completed reports, research docs, and historical reference (PDFs + TXT variants).

- Old research documents (tech stack, MVP considerations, etc.)
- Completion reports & team announcements
- Historical onboarding docs

---

## Quick Navigation

**I'm deploying for the first time:**
→ Start with [01_Getting_Started/](01_Getting_Started/)

**I need to troubleshoot a failed deploy:**
→ Check [02_CI_CD/SYNTHETIC_CHECKS_RUNBOOK.md](02_CI_CD/SYNTHETIC_CHECKS_RUNBOOK.md)

**I need to understand the system design:**
→ Read [03_Architecture/](03_Architecture/)

**I need to run operations (logs, monitoring, etc.):**
→ See [04_Operations/](04_Operations/)

**I'm looking for reference material:**
→ Check [05_Reference/](05_Reference/)

---

**Last Updated:** December 3, 2025
