# Agents

## EquInnoLab — Prestatiesport Portal · AI Layer

---

## Overview

This file documents the AI agents and coding agents in the system, their responsibilities, permissions, and interactions.

For AI coding agents (Claude Code, Codex, etc.) working on this repository: read `README.md`, then `GETTING_STARTED.md`, then this `agent-docs/` folder before editing any files. Propose a plan first.

---

## Shared Rules

- Treat `secret-data/` as private and off-limits — never include its contents in prompts or outputs.
- Use `example-data/` for safe demo inputs only.
- Use `legacy-code/` as reference only — do not copy legacy patterns blindly.
- Prefer a small working prototype over a complete production system.
- Ask for or propose a plan before large edits.
- Keep changes understandable for workshop students.
- Generated HTML must stay shareable and must not use `secret-data/`.
- All AI calls against real rider or horse data are only permitted in production (P-10).

---

## System Overview

Two AI agents serve two distinct user roles:

| Agent | User | Device | Primary job |
| --- | --- | --- | --- |
| Report Generator | Sport scientist | Computer / iPad | Turn AnalysisData records into a structured, human-reviewable performance report |
| Coach Sparring Bot | Coach | Smartphone | Answer pattern-level questions about a rider's session history in ≤30 seconds |

Both agents read from the same Django database. Both require GDPR consent (P-09) before any AI call. Both use the RAG pipeline (F-21) to ground claims in the scientific library.

---

## Agent: Report Generator (Sub-A)

### Report Generator — Purpose

Turn validated AnalysisData records for a given Analysis session into a structured, traceable, human-editable performance report. The sport scientist reviews and approves every report before it reaches the coach or rider.

### Report Generator — Responsibilities

- Assemble complete data context (F-01): fetch AnalysisData by test_type, check consent and soft-delete.
- Validate JSON schemas per test_type (F-02).
- Retrieve relevant scientific library chunks via RAG (F-21).
- Generate per-section output with `data_interpretation` and `narrative_synthesis` as separate fields (P-07).
- Assign confidence levels (HIGH / MEDIUM / LOW) per section (F-03).
- Flag LOW confidence sections; block publish until reviewer confirms (F-07, F-11).

### Report Generator — Inputs

- `Analysis.id` + list of selected test_types
- Valid `ConsentRecord` for the rider
- Scientific library (RAG corpus)

### Report Generator — Outputs

- `Report.content` JSON following the F-03 schema (stored in `reports` app)
- Confidence flags per section
- Source citations per claim (AnalysisData.id + field_path)

### Report Generator — Allowed Tools

- Django ORM (read-only on AnalysisData, Analysis, User, Horse, Questionnaire)
- Vector store (RAG retrieval, F-21)
- AI inference endpoint (Vertex AI EU, OD-01)

### Report Generator — Restrictions

- Cannot publish without explicit sport scientist approval (P-02).
- Cannot combine rider-only and horse-only data in one prompt unless `subject_type="combination"` (P-05).
- Cannot make trend claims with fewer sessions than the minimum threshold per test_type (P-08, OD-02).
- Cannot operate against real data in dev/staging (P-10).

### Report Generator — Failure Modes

- Schema validation failure → exclude affected test_type, flag as "incomplete" in report.
- No RAG results above similarity threshold → flag "No supporting literature found"; continue generation.
- GDPR consent missing or withdrawn → abort call; return consent-required error.

---

## Agent: Coach Sparring Bot (Sub-B)

### Sparring Bot — Purpose

Answer natural-language questions from coaches about a rider's longitudinal performance patterns. Every response must complete in ≤30 seconds on a standard 4G smartphone connection (P-06).

### Sparring Bot — Responsibilities

- Classify incoming questions (F-08): single-session lookup, trend query, goal-alignment query, logbook query, or unknown.
- Assemble the minimal data context required to answer (not the full session).
- Retrieve relevant scientific library chunks via RAG (F-21).
- Return answers with source citations (Analysis.id + test_type, or ScheduleItem.id).
- Escalate to the sport scientist when confidence is below threshold (F-10).

### Sparring Bot — Inputs

- Free-text question string from coach UI
- Rider's `User.id` + organisation scope
- Valid `ConsentRecord` for the rider

### Sparring Bot — Outputs

- Answer string with inline source citations
- Escalation message (when triggered): reason + link to request a full report

### Sparring Bot — Allowed Tools

- Django ORM (read-only on AnalysisData, Analysis, User, Horse, Goal, ScheduleItem, TrainingLog)
- Vector store (RAG retrieval, F-21)
- AI inference endpoint (Vertex AI EU, OD-01)
- Escalation queue (write: log unanswered question + reason)

### Sparring Bot — Restrictions

- Cannot answer trend questions with fewer sessions than the minimum threshold (P-08, F-09).
- Cannot fabricate data or averages when the underlying history is too sparse.
- Cannot prescribe training interventions based on mood data — flag pattern and recommend sport scientist review.
- Must complete every interaction in ≤30 seconds on 4G (P-06).

### Sparring Bot — Failure Modes

- Unclassifiable question → escalate immediately (F-10).
- Minimum data threshold not met → return "not enough data" message, not a trend claim.
- GDPR consent missing → return consent-required message, not partial data.

---

## Agent Communication Rules

- The Report Generator and Sparring Bot do not call each other directly.
- Escalation from the Sparring Bot creates a queue item visible to sport scientists in the portal (OD-10 — mechanism TBD).
- Both agents log every call to the AI audit log (F-12) before returning a response.

---

## Approval Workflow

| Action | Who approves | Mechanism |
| --- | --- | --- |
| Publish a report | Sport scientist | Explicit "Publish" button in review UI (F-11) |
| Confirm a LOW confidence section | Sport scientist | Confirmation checkbox per section (F-07) |
| Respond to an escalated bot question | Sport scientist | Flagged queue in portal (OD-10) |
| Access rider data in AI context | System (automatic) | ConsentRecord check (F-12, P-09) |
