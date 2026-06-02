# Product Constitution
## EquInnoLab — Prestatiesport Portal · AI Layer
Version 2.0 · May 2026

---

## 1. Purpose & Scope

This constitution governs the AI layer of the EquInnoLab Prestatiesport Portal. It is the single source of truth that overrides any conflicting decision made elsewhere.

Two AI sub-products share one codebase and one data model:

- **Sub-product A — Holistic Report Generator**: used by sport scientists (computer or iPad) to turn raw AnalysisData into a structured, human-editable performance report.
- **Sub-product B — Coach Sparring Bot**: used by coaches (smartphone) to answer pattern-level questions about a rider's session history within 30 seconds.

---

## 2. Product Overview

### Sub-product A — Holistic Report Generator

Actor: Sport scientist (computer or iPad).

The Report Generator reads all completed `AnalysisData` records for a given Analysis session, interprets the measurement data in their `data` JSONField, and produces a structured, traceable, human-editable report. **No report is ever published without explicit human sign-off (P-02).**

#### Canonical test_type inventory

| test_type (frontend) | Backend string | Subject | Mode | Status |
|---|---|---|---|---|
| pct | pct | Rider | Lab | Active |
| flexchair | flexchair | Rider | Lab | Active |
| mental | mental | Rider | Lab/Home | Active |
| riderNutrition | rider_nutrition | Rider | Lab | Placeholder |
| horseHeartRate | horseHeartRate | Horse | Lab | Active |
| lactate | lactate | Horse | Lab | Active |
| conformation | conformation | Horse | Lab | Active |
| nutrition | nutrition | Horse | Lab | Placeholder |
| kinematicFreeMovement | kinematicFreeMovement | Horse | Lab | Active |
| kinematicInHand | kinematicInHand | Horse | Lab | Active |
| gaits | gaits | Horse | Lab | Legacy |
| seatBalance | seatBalance | Combination | Lab | Active |
| combination | biomechanical | Combination | Lab | Active |
| teamHeartRate | ridden_hr | Combination | Lab | Active |
| competitionProtocol | competition_protocol | Combination | Lab | Active |
| jumpingCompetition | jumpingCompetition | Combination | Lab | Active |

### Sub-product B — Coach Sparring Bot

Actor: Coach (smartphone, primary device).

The Sparring Bot answers natural-language questions from coaches about longitudinal performance patterns. Every response must complete in under 30 seconds (P-06). It escalates to the sport scientist when confidence is low (P-08).

### Shared Data Model

Both sub-products read from the same Django database. Coaches and sport scientists see only riders within their own organisation.

---

## 3. Governing Principles

These eleven principles are non-negotiable.

### 3.1 Welfare & Safety

**P-01 Horse welfare above performance optimisation**
No AI output may recommend loads or targets that prioritise performance metrics over horse welfare. When data suggests welfare risk (e.g. elevated lactate without recovery data), the system must flag the concern before presenting performance insight.

**P-02 Four-eyes review — AI never publishes autonomously**
Every AI-generated output that reaches a coach, rider, or external party must first be reviewed and approved by a qualified sport scientist. Bypassing the review step is not permitted, even in the MVP.

**P-03 Traceable claims — every insight has a source**
Every factual claim must cite the specific `AnalysisData` record, test_type, and data field that supports it. Calibrated uncertainty is preferred over unsupported assertions.

**P-04 Contradictory literature must be surfaced**
When literature is genuinely divided on a topic, the AI must present the leading positions rather than picking one.

### 3.2 Data Integrity & Privacy

**P-05 Subject-data isolation — rider and horse data stay separate**
Rider-only health data must never be merged with horse-only medical data unless a combination analysis has been explicitly requested and consented to. Each AI call must be scoped to a single `subject_type` or an explicit combination.

**P-09 GDPR consent gate before any AI call**
No personal data may be passed to an external AI model without explicit, logged AVG/GDPR consent. The system must refuse the AI call if consent is missing or withdrawn.

**P-10 Development environment gate**
AI calls against real rider or horse data are only permitted in production. Dev and staging environments must use synthetic dummy data only.

### 3.3 Explainability & Trust

**P-07 Split explainability — one output per reasoning layer**
Data interpretation (reading raw measurement data from the JSONField) and narrative synthesis (coaching language) must be separable and independently inspectable.

**P-08 Refuse and escalate rather than hallucinate**
When the AI does not have sufficient data to answer reliably, it must say so explicitly and escalate to the sport scientist. The minimum data threshold before a trend claim is valid must be defined per test_type.

### 3.4 Infrastructure & Compliance

**P-11 EU-resident GCP-native AI — all data stays in Europe**
All AI inference, data storage, and logging must run within GCP EU regions. Vertex AI (EU region) is the preferred inference platform.

**P-06 30-second phone rule for the Sparring Bot**
Every Sparring Bot interaction must complete within 30 seconds on a standard 4G smartphone connection. This is a hard UX constraint, not a target.

---

## 4. Technical Architecture Decisions

Locked after codebase analysis on 19 May 2026. These supersede any contradictory assumptions in earlier spec documents.

**TC-01 JSON-in-DB architecture — all measurement data in AnalysisData.data**
Every measurement value is stored in the `data` JSONField on `AnalysisData`. The AI layer must read measurement data by querying `AnalysisData` by `test_type` string and parsing the JSON payload.

**TC-02 RideType enum is 0–7 (not 0–4)**
WALK=0, TROT=1, CANTER_LEFT=2, CANTER_RIGHT=3, JUMP=4, PACE=5, PIAFFE=6, HALT=7.

**TC-03 Riders are User records — no separate Rider model**
Riders are `User` records with `type="rider"`. Rider-horse relationships are implicit via `Analysis.user` and `Analysis.horse` FKs.

**TC-04 Soft-delete via BaseDateTrackedModel**
AI queries must filter on `deleted=False`.

**TC-05 Questionnaire 1-to-1 with home-mode Analysis**
For `mode="home"`, home-mode mental/subjective data must be read from `Questionnaire.responses`, not `AnalysisData`.

**TC-06 test_type string is the authoritative analysis identifier**
Use the exact test_type strings from `_TEST_CONFIGS`. Historical aliases must not appear in new AI code.

**TC-07 RAG architecture — scientific library is the retrieval corpus**
The AI layer uses Retrieval-Augmented Generation. Before generating any output, the system retrieves the most relevant chunks from the scientific library via semantic similarity search.

**TC-08 Scientific library taxonomy — four-dimension tagging**
(1) Subject: rider/horse/combination; (2) Analysis type: maps to test_type string; (3) Scope: normative/mechanistic/intervention/diagnostic; (4) Application: general/norm-table/protocol/exercise-prescription.

**TC-09 Frontend/backend test_type naming discrepancies**
- "riderNutrition" = "rider_nutrition" (backend)
- "teamHeartRate" = "ridden_hr" (backend)
- "competitionProtocol" = "competition_protocol" (backend)
- "combination" = "biomechanical" (backend)

Frontend test_type string (in `AnalysisData.test_type`) is always authoritative.

**TC-10 seatBalance and combination share an identical data schema**
Both use the same Noran AI JSON structure; differentiated only by marker set (rider-only vs. rider+horse).

---

## 5. Open Decisions

| ID | Status | Description | Owner |
|---|---|---|---|
| OD-01 | OPEN | Which AI model platform and inference endpoint (Vertex AI model/version)? | Engineering lead + CTO |
| OD-02 | OPEN | Minimum dataset size per test_type before a trend claim is valid? | Sport scientist + data scientist |
| OD-03 | RESOLVED | Rider-horse combinations identified via Analysis.user + Analysis.horse FKs (TC-03) | Engineering |
| OD-04 | OPEN | How to handle a horse that changes owner (data-transfer consent workflow)? | Product owner + legal |
| OD-05 | RESOLVED | All eight RideType values in scope (TC-02) | Engineering |
| OD-06 | RESOLVED | Report content stored in Report.content JSONField (TC-01) | Engineering |
| OD-07 | PARTIALLY RESOLVED | Report.content schema and review workflow exist but not yet specced for AI use | Sport scientist + engineering |
| OD-08 | OPEN | Which equine performance norms for benchmarking — store in DB, pass from frontend, or embed in prompt? | Sport scientist lead |
| OD-09 | OPEN | How is AVG/GDPR consent captured and stored at User level? | DPO + engineering |
| OD-10 | OPEN | Escalation path mechanism for Sparring Bot (in-app, email, or queue)? | Product owner + sport scientist |
| OD-11 | OPEN | Can rider kinematics be aggregated across sessions on different horses? | Sport scientist + data scientist |

---

## 6. Document History

| Version | Date | Summary |
|---|---|---|
| 1.0 | 12 May 2026 | Initial spec from 10-round interview with Maurice Fierloos |
| 2.0 | 19 May 2026 | Codebase grounding: locked TC-01–06, resolved OD-03/05/06, added new test_types |
| 2.1 | 19 May 2026 | Added TC-07 (RAG), TC-08 (taxonomy), OD-11 (multi-horse rider kinematics) |
| 2.2 | 20 May 2026 | Full codebase audit of Vue Test components: added canonical test_type table, TC-09, TC-10 |
