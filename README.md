# EdTech B2B Lead Intelligence Engine — PoC

> Autonomous lead qualification and knowledge synthesis for a B2B EdTech revenue operation.

## What This Is

A proof-of-concept architecture for an autonomous lead intelligence system designed for a B2B SaaS company operating in the HR/L&D sector. Built to replace a manual, siloed lead qualification workflow with a deterministic data pipeline, AI-assisted synthesis layer, and human-in-the-loop governance model.

This repository documents the full engagement lifecycle: problem framing, discovery, architectural design, governance protocols, and proof of value.

**Status:** Pre-production design confirmed. Implementation pending Phase 1 provisioning.

---

## The Problem in One Line

The client's B2B pipeline was built on a learner management platform — a system designed for content delivery, not revenue intelligence. Lead data was being manually moved between tools with no scoring logic, no audit trail, and no way to surface AE-ready signals at scale.

---

## Architecture at a Glance

```
[Inbound Triggers]
      |
      v
[/raw-staging/]  <--- Immutable dump. No processing here.
      |
      v
[Claude Code Agent]  <--- Classify -> Synthesise -> Write
      |
      +---> [/wiki/]          <- Structured lead profiles
      +---> [/hot-cache.md]   <- ~1,000-word AE-ready index
      +---> [Upstream CRM]    <- API-only writes, AE-ready flag only
```

Three-tier privacy classification governs every record:

| Tier | Type | Handling |
|------|------|----------|
| Green | Public, verified | Fully automated |
| Amber | Consent ambiguity | Automated ingestion / manual enrichment review |
| Red | Private comms / contracts | Manual CLI only, air-gapped |

---

## Repository Structure

| Directory | Contents |
|-----------|----------|
| [`00-context/`](00-context/) | Engagement background, problem statement, scope |
| [`01-discovery/`](01-discovery/) | Discovery questionnaire, Five Whys, root cause analysis |
| [`02-architecture/`](02-architecture/) | Technical architecture, bifurcated directory design, Hot MD Cache |
| [`03-governance/`](03-governance/) | Privacy protocol, HITL gates, linting, cloud sync exclusion |
| [`04-evidence/`](04-evidence/) | Proof of value metrics, benchmarks, efficiency projections |
| [`05-brief/`](05-brief/) | Executive brief evolution, stakeholder communication |
| [`06-demo/`](06-demo/) | Live demo recording, walkthrough notes |
| [`assets/`](assets/) | Architecture diagrams, screenshots |
| [`PROOF-OF-VALUE.md`](PROOF-OF-VALUE.md) | Full proof-of-value document |
| [`DECISION-LOG.md`](DECISION-LOG.md) | Architectural decision record |

---

## Proof of Value — Key Numbers

| Metric | Before | After (Projected) |
|--------|--------|-------------------|
| SDR time per lead | 75-90 min (industry benchmark) | 10-15 min |
| Capacity recovered | — | 200-250 hrs/month at 200 leads |
| LLM token overhead | Full-vault RAG per query | ~95% reduction via Hot MD Cache |

---

## Design Principles

This engagement applied five principles from the Proof-of-Value OS:

1. **Comprehension over generation** — understand the system before automating it
2. **Explanation as native artifact** — every decision ships with its reasoning
3. **Transactions over credentials** — the work is the evidence
4. **Work in the open** — this repository is the deliverable
5. **Ship proof with work** — metrics, risks, and failure modes documented from day one

---

## Stack

- **Claude Code** — AI agent layer (synthesis, classification)
- **Obsidian** — local-first Markdown knowledge base
- **Gemini Flash API** — supporting LLM layer
- **n8n / Zapier** — inbound trigger automation
- **GitHub** — version control and portfolio surface

---

## Status & Scope

**In scope (PoC):** Architecture, governance model, directory structure, agent behaviour spec, Hot MD Cache design, privacy protocol, HITL gates.

**Phase 2 (out of scope):** Intelligence Vault — locally managed repository for proprietary business logic and sensitive operational data. Architecture deferred.

**Classification:** `portfolio-public` — all client-identifying details anonymised.
