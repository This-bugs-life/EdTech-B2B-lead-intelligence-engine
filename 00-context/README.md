# 00 — Context

> **What?** The engagement background, problem statement, and scope boundary.
>
> **Why?** Context is the precondition for credible architecture. Every design decision in this PoC traces back to the problem framing established here.
>
> **What breaks?** Scope without a defined problem boundary expands indefinitely. This section exists to hold the boundary.
>
> **What learned?** The client's core issue was not a technology problem — it was a data transport problem being treated as a synthesis problem. Fixing the wrong layer first is the most common failure mode in AI automation engagements.

---

## Engagement Overview

**Type:** Proof of Concept (PoC)
**Domain:** B2B SaaS — HR/L&D sector — Revenue Operations
**Scope:** Lead intelligence architecture — design, governance, and proof of value

## The Problem

A B2B SaaS company in the HR/L&D sector had built its revenue pipeline on a learner management platform — a system designed for content delivery, not lead intelligence.

The result:
- Lead data moved manually between siloed tools
- No deterministic lead scoring logic
- No audit trail for data provenance
- SDR time consumed by information movement, not qualification

## What This Engagement Does Not Solve

- CMS platform decoupling — deferred (requires CPO sign-off, separate initiative)
- Intelligence Vault implementation — Phase 2
- Historical data migration — out of scope

## Scope Boundary

This PoC delivers: architecture design, governance model, proof-of-value metrics, and a pre-production specification ready for Phase 1 provisioning.

It does not deliver: running code, a live database, or a production-ready deployment.
