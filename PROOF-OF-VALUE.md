---
project: B2B Lead Intelligence Engine (PoC)
domain: HR/L&D SaaS — Revenue Operations
status: PoC — Pre-Production Design
version: 1.2
last-updated: 2026-05-08
classification: portfolio-public
---

# Proof of Value — Autonomous Lead Intelligence Engine

## The Problem

B2B pipeline built on a learner management platform.

Data transport and data synthesis were being treated as the same problem.
They aren't.

The result: manual copy-paste across siloed tools. No deterministic lead
scoring. SDR time consumed by information movement, not intelligence.

The system needed a fixed foundation before AI could add value.
This engagement fixes the foundation.

---

## The Architecture

**Bifurcated directory design:**

`/raw-staging/` -> Claude Code agent -> `/wiki/`

Raw data lands in `/raw-staging/` as an immutable dump. The agent
processes, classifies, and writes synthesised intelligence to `/wiki/`.
No direct database writes. API-only upstream interaction via AE-ready
flag state change.

**Hot MD Cache:**
A ~1,000-word Markdown file maintained at vault root. 30-day rolling
window. AE-ready leads only. Floor: 10 leads minimum. Ceiling: 1,000
words hard cap. Estimated token reduction: ~95% vs. full-vault RAG
retrieval.

**Knowledge base:** Obsidian vault — local-first, offline-capable,
Markdown-native. Confirmed net-new stack addition.

---

## Privacy Protocol

Three-tier data classification:

| Tier | Classification | Handling |
|------|---------------|----------|
| Green | Public data — verified business information | Fully automated |
| Amber | Semi-public — enriched or scraped with consent ambiguity | Automated ingestion / manual enrichment review gate |
| Red | Sensitive — private comms, contractual data | Manual CLI only / air-gapped |

**Edge case rules:**
- LinkedIn DM exports → Amber regardless of content
- All PDFs → Amber regardless of source
- Ambiguous signals → Amber is default

---

## Structural Safeguards

**Weekly Linting Protocol:**
Automated scan targeting:
- Contradictions (entity ID anchors as primary de-duplication key)
- Orphaned wiki pages with no upstream source
- Stale claims (Last AE Activity field overrides date-based staleness logic)

Lint output writes to `/lint-reports/` → human review trigger →
notification dispatch. Human arbitration required before any stale-claim
removal.

**Recursive Loop Prevention:**
Claude Code `.claude/` session logs + cloud sync daemon = infinite
self-summarisation loop. Pre-deployment mitigation: `.no-sync` provisioned
for `.claude/` and `/scripts/` before first cloud sync activation.
Obsidian Sync requires a separate exclusion configuration.

**Cloud Sync Exclusion Matrix:**

| Path | Sync Status |
|------|------------|
| `/raw-staging/` | Excluded |
| `/wiki/` | Permitted post-review |
| `/hot-cache.md` | Permitted post-review |
| `/.claude/` | Excluded |
| `/scripts/` | Excluded |
| `/lint-reports/` | Excluded |

---

## Proof of Value

**Industry benchmark:** 75–90 SDR-minutes per lead (manual qualification)
**Post-implementation target:** 10–15 SDR-minutes per lead
**Recovered capacity:** 200–250 hours/month at 200 leads/month volume

**AE intelligence quality:**
Structured wiki profile with verified entity anchors vs. bare CRM entry
with no enrichment lineage.

**Token efficiency:**
~95% reduction in LLM context overhead via Hot MD Cache vs.
full-vault RAG retrieval on every query.

---

## Risk Register

| ID | Risk | Status |
|----|------|--------|
| R-01 | Recursive loop via OS cloud sync daemon | Pre-deployment provisioning |
| R-02 | Obsidian net-new stack component | Closed |
| R-03 | Lint report output triggers detection loop | Pre-deployment provisioning |
| R-04 | `index.md` race condition on concurrent writes | Pre-deployment provisioning |
| R-05 | Linting misses semantic contradictions | Pre-deployment provisioning |
| R-06 | Linting results go unreviewed | Pre-deployment provisioning |
| R-07 | Stale-claim false positive deletion | Pre-deployment provisioning |
| R-08 | Misclassified data reaching external API | Pre-deployment provisioning |
| R-09 | Social platform DM export misclassified as Green | Pre-deployment provisioning |
| R-10 | Hot MD Cache empty at launch | Pre-deployment provisioning |
| R-11 | CMS decoupling scope creep | Closed — CPO sign-off confirmed |
| R-12 | Intelligence Vault scope confusion | Closed — Phase 2 declared |

**Zero open design risks. All remaining risks are pre-deployment provisioning tasks.**

---

## Phase 2 — Intelligence Vault

Scoped as a Phase 2 deliverable.

Locally managed repository for proprietary business logic and sensitive
operational data. Not part of this PoC. Architecture decisions deferred
to Phase 2 engagement.

---

## Human-in-the-Loop Commitment

AI synthesises. Humans arbitrate truth and security.

Every operational state change — data tier reclassification, AE-ready
flag promotion, lint-triggered deletion, upstream CRM write — requires
a human decision trigger.

The system has no autonomous write authority.
