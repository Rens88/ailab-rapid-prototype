# Memory

## EquInnoLab — Prestatiesport Portal · AI Layer

---

## Overview

This file documents how memory works inside the AI layer of the Prestatiesport Portal. Memory affects personalization, context retention, planning quality, and long-term reliability.

The AI layer has **no persistent conversational memory between sessions** in the MVP. Each Report Generator call and each Sparring Bot interaction is stateless from the model's perspective. Longitudinal context is achieved by fetching historical `AnalysisData` records from the database — not by storing prior model outputs in a vector store.

---

## Memory Types

### Working Memory

Short-term context assembled per AI call.

#### Contents per Report Generator call

- All `AnalysisData` records for the selected test_types (from F-01 context assembler)
- `Analysis` metadata: session date, subject_type, mode
- `User` and `Horse` metadata
- `Questionnaire.responses` (home-mode sessions only)
- Retrieved RAG chunks (top-k=5 from the scientific library, F-21)
- Retrieved norm-table values (value-range lookup, TC-08)

#### Contents per Sparring Bot call

- Minimal dataset relevant to the classified question type (F-08)
- Retrieved RAG chunks relevant to the question
- For trend queries: the time-series data points for the queried test_type and metric (F-09)
- For goal queries: the active `Goal` record and mapped AnalysisData values (F-14)
- For logbook queries: `ScheduleItem` and `TrainingLog` records for the requested period (F-20)

#### Limits

- Context window management is the responsibility of the context assembler (F-01).
- If the assembled context exceeds the model's token limit, lower-priority sections are trimmed in this order: questionnaire data → logbook data → older sessions (keeping most recent).
- The trim decision and its reason are logged in the AI audit log (F-12).

---

### Episodic Memory

Prior interactions and session history, stored in the Django database — not in a model memory system.

#### What is stored

- All `AnalysisData` records per session (the primary longitudinal record)
- `Report` records with `Report.content` — every previously generated and published report
- `ReportComment` records — sport scientist annotations on past reports
- Sparring Bot conversation history (last 20 interactions per rider, per US-12)
- AI audit log entries (append-only, F-12)

#### What is NOT stored

- Raw model outputs beyond what is captured in `Report.content`
- Intermediate reasoning chains or chain-of-thought outputs
- Embeddings of past conversations (only the scientific library is embedded)

---

### Semantic Memory

Stable project knowledge, stored in the RAG scientific library.

#### Scientific library (TC-07, TC-08)

- Documents tagged across four dimensions: subject, analysis type, scope, application
- Norm-table documents stored as structured queryable rows (not text chunks)
- Managed via the curation workflow (F-22)
- Retrieved at call time via cosine similarity (F-21)

#### Normative benchmarks (OD-08 — open decision)

Currently computed in the Vue frontend. Until OD-08 is resolved, normative values are not stored in the database. The AI layer either receives pre-computed norm deltas as input, or they are embedded in the prompt as structured facts.

---

## Memory Lifecycle

1. **Creation**: AnalysisData is written by the Vue portal (lab or home mode).
2. **Assembly**: The context assembler (F-01) fetches relevant records at call time.
3. **Retrieval**: RAG pipeline (F-21) retrieves library chunks at call time.
4. **Storage**: Generated reports are stored in `Report.content` (JSONField).
5. **Expiration**: Records are soft-deleted (`deleted=True`) not physically removed. GDPR erasure requests are handled via admin soft-delete (US-28).

---

## Privacy & Security

- No rider or horse data is stored outside the EU (P-11).
- All AI calls require a valid `ConsentRecord` before any data is assembled (P-09).
- Consent withdrawal takes effect immediately: subsequent calls are refused.
- The AI audit log is append-only — no deletion or modification permitted (F-12).
- `secret-data/` in this repository is never included in any AI prompt or output.

---

## Memory Failures to Watch

- **Stale normative benchmarks (OD-08)**: if norms are embedded in prompts rather than fetched from a live source, they may silently become outdated as the sport science literature evolves.
- **Sparse session history leading to trend hallucination**: prevented by the minimum threshold enforcement in F-09 and P-08, but must be tested explicitly.
- **Context truncation losing critical test_types**: the trim order (above) prioritises objective measurement data over self-reported logbook data, but any truncation must be flagged in the output.
- **RAG retrieval returning irrelevant chunks**: if the scientific library has poor coverage for a test_type, the model may over-weight a loosely related chunk. The "No supporting literature found" flag (F-21) is the mitigation.

---

## Retention Policy

- `AnalysisData` and `Analysis` records: retained indefinitely unless the data subject requests erasure (GDPR Article 17, US-28).
- `Report` records: soft-deleted on data subject request; AI audit log entry for that report is retained (legal obligation).
- Sparring Bot conversation history: last 20 interactions per rider; items older than 90 days are archived and not shown by default (US-12).
- AI audit log: retained for the duration required by applicable data protection law (DPO responsibility).
