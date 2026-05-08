# 02 — Architecture

> **What?** The bifurcated directory design, Hot MD Cache specification, and agent behaviour model for the autonomous lead intelligence engine.
>
> **Why?** Architecture decisions at this stage are more consequential than code. A poorly designed data flow cannot be patched at the implementation layer — it has to be redesigned. This section is where the structural choices are made and their rationale recorded.
>
> **What breaks?** Single-directory designs with no staging layer lose audit trail integrity. Full-vault RAG on every query at 200+ profiles generates prohibitive token overhead. Direct DB writes from AI agents create unauditable mutation surfaces.
>
> **What learned?** The most important architectural constraint was not technical — it was epistemic. LLMs don't unlearn. Any synthesised intelligence written to the wiki becomes a claim that persists until actively contradicted. The Weekly Linting Protocol exists because of this. Knowledge deprecation is a first-class risk, not an afterthought.

---

## System Architecture

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

## Bifurcated Directory Design

`/raw-staging/` is an immutable data dump. Nothing is processed here. The Claude Code agent reads from staging and writes synthesised output to `/wiki/`. The separation creates a clean audit boundary.

## Hot MD Cache

A ~1,000-word Markdown file at vault root. Updated on each agent processing cycle. Contains only AE-ready leads from the last 30 days.

**Constraints:**
- Floor: 10 leads minimum
- Ceiling: 1,000 words hard cap
- Window: 30-day rolling
- Inclusion criteria: AE-ready flag = true

**Rationale:** ~95% token reduction vs. full-vault RAG retrieval. AEs query current-cycle leads, not historical records. The cache makes the common case fast without sacrificing the full wiki for edge cases.

## Level 4 AI Framework

- **Deterministic routing** — data movement follows fixed rules, no LLM involvement
- **LLMs restricted to** — unstructured data parsing, wiki profile synthesis, proposal drafting
- **No direct DB writes** — all upstream CRM interaction via API only
- **AE-ready flag** — the only trigger for upstream state change

---

*See [`PROOF-OF-VALUE.md`](../PROOF-OF-VALUE.md) for the full architectural specification.*
