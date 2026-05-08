# 03 — Governance

> **What?** Privacy classification protocol, Human-in-the-Loop (HITL) gates, Weekly Linting Protocol, and cloud sync exclusion matrix.
>
> **Why?** An autonomous pipeline without governance is a liability, not an asset. The governance layer defines what the system is allowed to do without human authorisation, and what it is explicitly not.
>
> **What breaks?** Three failure modes were identified before deployment:
> - **Recursive loops:** Claude Code session logs + cloud sync daemon = infinite self-summarisation. Mitigated by `.no-sync` pre-deployment provisioning.
> - **Knowledge deprecation:** LLMs don't unlearn — stale claims persist until actively removed. Mitigated by Weekly Linting Protocol with human arbitration.
> - **Data misclassification:** A social platform DM export misclassified as Green data reaches the automated pipeline. Mitigated by Amber-default rule.
>
> **What learned?** Governance is most expensive when retrofitted. Every protocol in this section was designed into the architecture before implementation, not added after the first incident.

---

## Privacy Classification

| Tier | Data Type | Handling |
|------|-----------|----------|
| Green | Public, verified business information | Fully automated |
| Amber | Semi-public / consent ambiguity | Automated ingestion / manual enrichment review gate |
| Red | Private comms, contractual data | Manual CLI only / air-gapped |

**Edge case rules:**
- LinkedIn DM exports → Amber
- All PDFs → Amber regardless of source
- Ambiguous signals → Amber (conservative default)

## Human-in-the-Loop Gates

The system has no autonomous write authority. Every operational state change — data tier reclassification, AE-ready flag promotion, lint-triggered deletion, upstream CRM write — requires a human decision trigger.

AI synthesises. Humans arbitrate truth and security.

## Weekly Linting Protocol

Automated scan targeting:
1. Contradictions (entity ID anchors as primary de-duplication key)
2. Orphaned wiki pages with no upstream source
3. Stale claims (Last AE Activity field overrides date-based staleness logic)

Output: `/lint-reports/` → human review trigger → notification → arbitration required before any deletion.

## Cloud Sync Exclusion Matrix

| Path | Status |
|------|--------|
| `/raw-staging/` | Excluded |
| `/wiki/` | Permitted post-review |
| `/hot-cache.md` | Permitted post-review |
| `/.claude/` | Excluded |
| `/scripts/` | Excluded |
| `/lint-reports/` | Excluded |
