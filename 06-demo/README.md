# 06 — Demo

> **What?** A live audio walkthrough of the autonomous lead intelligence architecture, recorded during the engagement.
>
> **Why?** Architecture documentation describes a system. A live demo shows one being reasoned about in real time. The gap between those two things is where technical credibility is established or lost.
>
> **What breaks?** A demo without timestamps is difficult to navigate. A demo without an accompanying written summary is inaccessible to anyone who can't listen to audio. Both are documented below.
>
> **What learned?** The most technically revealing moment in the recording was not a design decision — it was a failure mode being identified in real time. The recursive loop risk (Claude Code session logs + cloud sync daemon) was surfaced and resolved during the live session, not in a post-hoc document. That's what makes it evidence.

---

## Demo Recording

**Status:** External hosting pending.

The live audio demo will be hosted externally via Loom or YouTube (unlisted) with timestamp markers. Link to be added here on upload.

**Key topics covered:**
- Bifurcated directory design walkthrough
- Hot MD Cache rationale and sizing constraints
- Markdown vs. vector RAG decision
- Three risk categories identified in real time:
  - Privacy Paradox (data classification edge cases)
  - Knowledge Deprecation (LLMs as probabilistic aggregators that don't unlearn)
  - Recursive Loops (Claude Code session logs + cloud sync daemon)
- Tools demonstrated: Claude Code, Obsidian, Gemini Flash API

## Timestamp Guide

*To be populated on external upload.*

| Timestamp | Topic |
|-----------|-------|
| — | Introduction and problem framing |
| — | Bifurcated directory design |
| — | Hot MD Cache sizing rationale |
| — | Three risk categories |
| — | Governance protocol walkthrough |

---

*Audio file excluded from repository (binary). See `.gitignore` for exclusion rule.*
