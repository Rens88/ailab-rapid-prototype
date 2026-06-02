# Architecture

## EquInnoLab — Prestatiesport Portal · AI Layer

---

## Overview

The AI layer sits on top of an existing Django/Vue portal. It does not replace the portal's data model — it reads from it. The architecture was locked after codebase analysis on 19 May 2026. See `CONSTITUTION.md` for authoritative technical decisions (TC-01 through TC-10).

---

## High-Level Architecture

```text
Coach (smartphone)          Sport Scientist (computer/iPad)
       |                               |
  Sparring Bot UI              Report Generator UI
       |                               |
  ─────────────── AI Gateway ────────────────
       |                               |
  Question Handler            Context Assembler (F-01)
  Trend Engine (F-09)         Schema Validator (F-02)
  Escalation Handler (F-10)   Report Generator (F-04/05/06)
       |                               |
  ─────────────── RAG Pipeline (F-21) ────────────────
                     |
            Scientific Library
            (vector store, EU GCP)
                     |
  ─────────────── Django ORM ──────────────────
                     |
         PostgreSQL — AnalysisData (JSON-in-DB)
         Analysis · User · Horse · Goal
         Questionnaire · ScheduleItem · TrainingLog
         Report · ReportComment · ConsentRecord
```

---

## Key Architectural Constraints

**TC-01 JSON-in-DB**: All measurement data is in `AnalysisData.data` (JSONField). No normalised measurement tables. The AI layer queries by `test_type` string and parses the JSON payload.

**TC-03 No Rider model**: Riders are `User` records with `type="rider"`. Rider-horse combinations are implicit via `Analysis.user` + `Analysis.horse` FKs.

**TC-04 Soft-delete**: All queries must filter `deleted=False`.

**TC-07 RAG**: Every AI generation call retrieves relevant chunks from the scientific library before generating. The scientific library is a live retrieval corpus, not a static reference.

---

## Request Flow

### Report Generator (Sub-A)

1. Sport scientist selects an Analysis session and test_types to include.
2. Context Assembler (F-01) fetches all `AnalysisData` records, checks GDPR consent (F-12), checks soft-delete.
3. Schema Validator (F-02) validates each `data` JSONField.
4. RAG pipeline (F-21) retrieves top-k scientific library chunks for each test_type.
5. AI model generates report sections with data_interpretation + narrative_synthesis per test_type.
6. Report is stored as `Report.content` (JSONField) with status="draft".
7. Sport scientist reviews in the review UI (F-11): edits, confirms LOW confidence sections, clicks Publish.
8. Published report becomes visible to coach and rider via the portal.

### Sparring Bot (Sub-B)

1. Coach submits a natural language question.
2. Question Handler (F-08) classifies the question type.
3. Minimal data context is assembled (not the full session).
4. RAG pipeline retrieves relevant scientific chunks.
5. AI model generates answer with source citations.
6. If confidence is below threshold → Escalation Handler (F-10) fires instead.
7. Total time: ≤30 seconds on 4G (P-06).

---

## Components

### AI Gateway

Entry point for all AI calls. Enforces:

- GDPR consent check (P-09) before any data is fetched
- Environment gate (P-10): real data only in production
- Subject-data isolation routing (P-05): rider-only, horse-only, or combination calls

### Context Assembler (F-01)

Fetches and structures `AnalysisData` records into a typed context object. Returns metadata, rider_data, horse_data, and questionnaire sections. Handles home-mode `Questionnaire.responses`.

### Schema Validator (F-02)

Validates each `AnalysisData.data` payload against versioned JSON Schema files per test_type. Validation failure for one test_type does not abort others.

### RAG Pipeline (F-21)

- Embeds query strings derived from test_type, subject_type, and detected deficits.
- Retrieves top-k=5 chunks by cosine similarity from the vector store.
- Norm-table chunks use value-range lookup, not semantic similarity.
- Injects retrieved chunks into the system prompt under a "Scientific context" header.
- If no chunk meets the minimum similarity threshold, flags "No supporting literature found."

### Report Generator (F-04 / F-05 / F-06)

Calls the AI model with the assembled context and retrieved scientific chunks. Produces sections with `data_interpretation` and `narrative_synthesis` as separate fields (P-07). Assigns confidence levels (HIGH / MEDIUM / LOW) per section (F-03).

### Review & Publish Workflow (F-11)

Enforces P-02 (four-eyes review). Status machine: draft → in-review → published. A LOW confidence section blocks publishing until the sport scientist explicitly confirms it.

---

## Data Models (key fields relevant to AI layer)

```python
# AnalysisData
#   test_type  str   canonical identifier (frontend string, TC-06)
#   data       JSON  all measurement values for the test_type (TC-01)
#   deleted    bool  must filter deleted=False (TC-04)

# Analysis
#   user         FK  → User (rider, TC-03)
#   horse        FK  → Horse
#   mode         str "lab" | "home"
#   subject_type str "rider" | "horse" | "combination"

# User
#   type  str  "rider" | "coach" | "sport_scientist" | "admin"

# Questionnaire
#   responses  JSON  OMSAT-3 and other home-mode answers (TC-05)

# Report
#   content  JSON  structured report following F-03 schema
#   status   str   draft | in-review | published | rejected | archived

# ConsentRecord
#   user_id          FK
#   granted_at       datetime
#   withdrawn_at     datetime (nullable)
#   consent_version  str
```

---

## Security Considerations

- **P-09 / F-12**: No AI call proceeds without a valid `ConsentRecord` for the rider. Consent withdrawal takes effect immediately.
- **P-10**: Dev/staging environments use synthetic dummy data only. Environment detection is automatic (Django `settings.DEBUG`).
- **P-11**: All AI inference, embedding, and vector storage runs within GCP EU regions. Vertex AI is the preferred inference platform.
- Audit log is append-only — no UPDATE or DELETE on audit records.

---

## Open Architecture Decisions

See `CONSTITUTION.md` Section 5 (Open Decisions): OD-01, OD-02, OD-04, OD-08, OD-09, OD-10, OD-11.

Critical path for MVP: **OD-01** (model platform) and **OD-09** (consent capture UI) must be resolved before the first production AI call.
