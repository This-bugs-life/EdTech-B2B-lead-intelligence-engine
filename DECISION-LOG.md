---
project: EdTech B2B Lead Intelligence Engine
type: architectural-decision-record
version: 1.0
last-updated: 2026-05-08
classification: portfolio-public
---

# Decision Log — Autonomous Lead Intelligence Engine

Transactions over credentials. Every significant architectural decision is recorded here with its rationale, alternatives considered, and the signal that resolved it.

---

## D-01 — Bifurcated Directory Design

**Decision:** Separate `/raw-staging/` (immutable dump) from `/wiki/` (synthesised intelligence). No processing occurs in staging.

**Why:** Direct writes from inbound sources to a processed knowledge base create audit trail gaps. If an AI agent writes to the same location it reads from, there's no clean rollback point and no way to distinguish source-of-truth from derived output.

**Alternatives considered:** Single-directory approach with metadata flags. Rejected — too much reliance on flag integrity under concurrent writes.

**Resolution:** Bifurcated design. Staging is immutable by convention. Agent reads from staging, writes to wiki only.

---

## D-02 — Hot MD Cache Over Full-Vault RAG

**Decision:** Maintain a ~1,000-word Markdown file at vault root containing only AE-ready leads from the last 30 days, rather than running RAG over the full wiki on every query.

**Why:** Full-vault RAG at 200+ lead profiles generates excessive token overhead on every AE query. Most queries are about current-cycle leads, not historical records.

**Constraints:** Floor of 10 leads minimum. Ceiling of 1,000 words hard cap. 30-day rolling window. AE-ready flag required for inclusion.

**Alternatives considered:** Vector database with semantic search. Rejected for Phase 1 — introduces infrastructure complexity without proportional value gain at this volume. Revisit at Phase 2.

**Resolution:** Hot MD Cache confirmed. Projected ~95% token reduction vs. full-vault RAG.

---

## D-03 — Amber as Default Classification

**Decision:** When data tier is ambiguous, default to Amber (automated ingestion / manual enrichment review gate). Amber is not a soft Green.

**Why:** The cost of misclassifying Red data as Green (automated pipeline exposure) significantly outweighs the cost of misclassifying Green data as Amber (manual review delay). Asymmetric risk profile → conservative default.

**Edge cases locked:**
- LinkedIn DM exports → Amber regardless of content
- All PDFs → Amber regardless of source
- Any signal with consent ambiguity → Amber

**Resolution:** Amber-default confirmed. Encoded into agent classification logic.

---

## D-04 — API-Only Upstream Writes

**Decision:** No direct database writes. All upstream CRM interaction via API. Only the AE-ready flag state change triggers an upstream write.

**Why:** Direct DB writes from an AI agent create an unauditable mutation surface. API-only writes enforce a defined contract, maintain an audit trail, and allow rollback without database surgery.

**Resolution:** Level 4 AI framework applied. LLMs restricted to unstructured data parsing and proposal drafting. AE-ready flag is the only upstream trigger.

---

## D-05 — Obsidian as Knowledge Base

**Decision:** Add Obsidian as a net-new stack component for the local Markdown knowledge base layer.

**Why:** The client had no existing local-first Markdown tooling. Obsidian provides offline-capable, version-control-compatible knowledge management without cloud dependency. Consistent with the air-gap and cloud sync exclusion requirements.

**Risk at decision point:** Net-new stack addition — implementation complexity, onboarding overhead.

**Resolution:** Risk closed. Obsidian confirmed compatible with the bifurcated directory design and cloud sync exclusion matrix. Net-new stack addition accepted.

---

## D-06 — Intelligence Vault Deferred to Phase 2

**Decision:** The Intelligence Vault (locally managed repository for proprietary business logic and sensitive operational data) is explicitly out of scope for Phase 1 PoC.

**Why:** Including it in Phase 1 introduces scope ambiguity around what constitutes "sensitive operational data" and risks expanding the PoC beyond what can be delivered and validated in a single engagement cycle.

**Resolution:** Phase 2 declaration confirmed. No Intelligence Vault architecture decisions made in this document. Phase 2 engagement required before scoping.

---

## D-07 — CMS Decoupling Out of Scope

**Decision:** The client's CMS platform decoupling is not a Phase 1 deliverable. The intelligence engine operates alongside the existing CMS, not as a replacement for it.

**Why:** CMS decoupling is a platform-level decision requiring CPO sign-off and a separate technical roadmap. Conflating it with the lead intelligence PoC would create a scope dependency that cannot be resolved within this engagement.

**Resolution:** CPO sign-off confirmed. CMS decoupling scoped to a future initiative. Risk R-11 closed.
