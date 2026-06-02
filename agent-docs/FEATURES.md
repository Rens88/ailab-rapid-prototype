# Feature Specifications
## EquInnoLab — Prestatiesport Portal · AI Layer
Version 2.2 · May 2026

---

## Feature Index

| ID | Title | Epic | Priority |
|---|---|---|---|
| F-01 | AI context assembler (data ingestion) | E-01 | Must |
| F-02 | JSON schema validator per test_type | E-01 | Must |
| F-03 | Report output format & structure | E-02 | Must |
| F-04 | Holistic Report Generator — rider analyses | E-02 | Must |
| F-05 | Holistic Report Generator — horse analyses | E-02 | Must |
| F-06 | Holistic Report Generator — combination analysis | E-02 | Should |
| F-07 | Low-confidence flagging & explainability panels | E-02 | Must |
| F-08 | Coach Sparring Bot — question handler | E-03 | Must |
| F-09 | Coach Sparring Bot — longitudinal trend engine | E-03 | Should |
| F-10 | Coach Sparring Bot — escalation handler | E-03 | Must |
| F-11 | Human review & publish workflow | E-04 | Must |
| F-12 | GDPR consent gate & audit log | E-05 | Must |
| F-13 | Longitudinal performance dashboard | E-06 | Should |
| F-14 | Goal-alignment engine | E-07 | Should |
| F-15 | Training plan AI draft generator | E-08 | Should |
| F-16 | Lactate & ridden heart rate analysis | E-02 | Should |
| F-17 | Kinematic in-hand analysis (Noran AI) | E-02 | Should |
| F-18 | Jumping competition analysis | E-02 | Should |
| F-19 | Competition video & protocol analysis | E-02 | Should |
| F-20 | Activity & logbook context enrichment | E-10 | Should |
| F-21 | RAG pipeline — scientific literature retrieval | E-11 | Must |
| F-22 | Scientific library curation workflow | E-11 | Should |
| F-23 | Schedule generation — day-by-day training tables | E-08 | Should |

---

## F-01 AI Context Assembler — Data Ingestion
Epic: E-01 · Priority: Must

Assembles the complete input context for any AI call by fetching and validating all relevant `AnalysisData` records, the Questionnaire (home-mode), and metadata from Analysis, User, and Horse models.

**Behaviour**
- Given an `Analysis.id` and a list of requested test_types, fetches all `AnalysisData` records where `test_type` is in the list and `deleted=False`.
- Fetches `Analysis.user`, `Analysis.horse`, `Analysis.mode`, `Analysis.subject_type`, `Analysis.session_type` for context metadata.
- For `mode="home"`, fetches the linked `Questionnaire.responses` JSONField.
- Returns a structured context object with sections: metadata, rider_data, horse_data, questionnaire (if applicable).

**Edge cases**
- `AnalysisData.data` is null → mark test_type as "incomplete" and exclude from AI prompt.
- `Analysis.deleted=True` → refuse context assembly and return error.
- Rider has no GDPR consent → refuse and return consent-required error (P-09).
- `subject_type="horse"` → rider_data section is omitted (P-05).

**Acceptance criteria**
- Context assembly completes in <5 seconds for a session with 10 test_types.
- No `AnalysisData` record with `deleted=True` appears in the context.
- GDPR check is performed before any data is assembled.

---

## F-02 JSON Schema Validator per test_type
Epic: E-01 · Priority: Must

Validates each `AnalysisData.data` payload against the canonical JSON schema for its test_type before passing it to any AI model. Prevents hallucinations caused by malformed input.

**Acceptance criteria**
- Schema validation is performed for every test_type before the AI call is made.
- A missing required field produces a human-readable error naming the field and test_type.
- Validation failure for one test_type does not abort validation of others.
- Schema definitions are stored as versioned JSON Schema files, not hardcoded.

---

## F-03 Report Output Format & Structure
Epic: E-02 · Priority: Must

Defines the canonical structure of an AI-generated Report and the content schema stored in `Report.content` (JSONField).

**Report structure**
```json
{
  "metadata": { "analysis_id", "session_date", "subject_type", "sport_scientist_id", "generated_at", "model_used", "test_types_included" },
  "sections": [{ "test_type", "data_interpretation", "narrative_synthesis", "confidence_level", "sources": [{"analysis_data_id", "field_path"}], "flags": [] }],
  "overall_summary": { "key_findings", "recommendations", "open_questions" },
  "review_metadata": { "reviewed_by", "reviewed_at", "published_at", "edits_made" }
}
```

**Confidence levels**
- HIGH: ≥3 sessions, schema valid, no normative benchmark gaps.
- MEDIUM: 1–2 sessions, or one missing benchmark, no schema errors.
- LOW: <1 full session, schema errors present, or AI uncertainty in output.

**Acceptance criteria**
- `data_interpretation` and `narrative_synthesis` are always separate fields — never merged.
- A report with any LOW confidence section cannot be published without reviewer confirmation.

---

## F-04 Holistic Report Generator — Rider Analyses
Epic: E-02 · Priority: Must

AI interpretation of rider-specific test_types (`subject_type="rider"`): pct, flexchair, mental, riderNutrition.

**Constraints**
- Rider test data is NEVER combined with horse test data in a single AI prompt (P-05) unless `subject_type="combination"`.
- Home-mode sessions include `Questionnaire.responses` as supplementary context, labelled "self-reported".

---

## F-05 Holistic Report Generator — Horse Analyses
Epic: E-02 · Priority: Must

AI interpretation of horse-specific test_types (`subject_type="horse"`): horseHeartRate, lactate, conformation, nutrition, kinematicFreeMovement, kinematicInHand. `gaits` is a legacy test_type — retained for historical records; new analyses use `kinematicFreeMovement`.

**Acceptance criteria**
- `gaits` section correctly handles all eight RideType values (WALK=0 through HALT=7).
- Horse welfare concern (P-01) is flagged when lactate values exceed the defined welfare threshold.
- Horse data is never mixed with rider health data in a single AI prompt (P-05).

---

## F-06 Holistic Report Generator — Combination Analysis
Epic: E-02 · Priority: Should

Generates reports for `subject_type="combination"`. Covers: seatBalance, combination (biomechanical), teamHeartRate (ridden_hr), competitionProtocol, jumpingCompetition.

This is the only feature where rider and horse data appear together in one AI prompt.

**Constraints**
- `subject_type` must be "combination" — system must refuse for rider-only or horse-only sessions.
- Consent must be present for both the rider (User) and horse owner.

---

## F-07 Low-Confidence Flagging & Explainability Panels
Epic: E-02 · Priority: Must

Implements P-07 (split explainability) and P-08 (refuse and escalate).

**Behaviour**
- Each report section has two panels: Data Interpretation and Narrative Synthesis.
- LOW confidence sections display a flag icon and a plain-language reason.
- A section with LOW confidence cannot be published without reviewer confirmation.
- When the Sparring Bot's confidence is below threshold, it triggers the escalation flow (F-10).

---

## F-08 Coach Sparring Bot — Question Handler
Epic: E-03 · Priority: Must

Core interaction engine. Accepts natural language questions from coaches and routes them to the appropriate data retrieval and AI call.

**Question classification rules**
- Single-session lookup: contains a specific date, session ID, or "last session"
- Trend query: contains "trend", "pattern", "over time", "last N weeks/months"
- Goal-alignment query: contains "goal", "target", "on track"
- Logbook query: contains "mood", "how many sessions", "training load"

**Acceptance criteria**
- 95% of questions classified correctly in unit tests covering 50 labelled examples.
- Response time ≤30 seconds measured from API call to response on 4G.
- Questions for riders without GDPR consent return a consent-required message.

---

## F-09 Sparring Bot — Longitudinal Trend Engine
Epic: E-03 · Priority: Should

Enables trend queries across multiple sessions. Enforces minimum data thresholds (OD-02).

**Minimum data thresholds (provisional)**
- lactate & ridden_hr: minimum 3 sessions before trend claim
- seatBalance & biomechanical: minimum 5 sessions
- kinematicFreeMovement: minimum 5 sessions
- gaits: minimum 3 sessions per RideType
- mental (OMSAT-3): minimum 2 sessions
- All other test_types: minimum 3 sessions

---

## F-10 Sparring Bot — Escalation Handler
Epic: E-03 · Priority: Must

Implements P-08. When the bot cannot answer reliably, it escalates to the sport scientist.

**Escalation triggers**
- AI confidence below threshold
- Question type is unclassifiable
- Minimum data threshold not met (F-09)
- Question touches a test_type that has no data for the rider
- Question asks for a recommendation that should come from a sport scientist

**Escalation behaviour**
- Bot responds: "I don't have enough data to answer this reliably."
- Response includes a direct link to request a full report from the sport scientist.
- Unanswered question and escalation reason are stored in a flagged queue visible to the sport scientist.
- Escalation is logged in the AI audit log (F-12).

---

## F-11 Human Review & Publish Workflow
Epic: E-04 · Priority: Must

Implements P-02 (four-eyes review). All Report state transitions are gated by explicit sport scientist action.

**Report status transitions**
- draft → in-review → published
- in-review → rejected (archived, new generation can be triggered)
- published → archived (admin action only)

**Constraints**
- No automated transition to "published" — human action always required.
- A report with any unconfirmed LOW confidence section cannot reach "published" state.

---

## F-12 GDPR Consent Gate & Audit Log
Epic: E-05 · Priority: Must

Implements P-09. Prevents any AI call from proceeding without logged consent.

**ConsentRecord fields**: `user_id`, `granted_at`, `withdrawn_at` (nullable), `consent_version`, `ip_address`.

**Audit log fields**: `timestamp`, `rider_user_id`, `analysis_id`, `test_types`, `ai_model_identifier`, `sport_scientist_user_id`, `call_type`, `response_status`.

**Acceptance criteria**
- The audit log is append-only — no UPDATE or DELETE permitted on audit records.

---

## F-13 Longitudinal Performance Dashboard
Epic: E-06 · Priority: Should

Visualises key metrics across sessions for sport scientists and coaches.

---

## F-14 Goal-Alignment Engine
Epic: E-07 · Priority: Should

Maps analysis data to the rider's active Goal record for goal-progress answers.

**Training scale tag mappings** (all six must be covered):
rhythm, relaxation, contact, impulsion, straightness, collection

---

## F-15 Training Plan AI Draft Generator
Epic: E-08 · Priority: Should

Generates a draft `TrainingPlan` record from analysis data and goal alignment. Does not share with the coach until sport scientist approves.

**Constraints**
- AI draft must not set specific intensity numbers (watts, km/h) without data from a lactate or pct test.
- Every recommendation cites the `AnalysisData` source that motivates it.

---

## F-16 Lactate & Ridden Heart Rate Analysis
Epic: E-02 · Priority: Should

NEW — added after codebase analysis.

**Lactate interpretation**: Computes LT1 and LT2 if sufficient steps. Flags steps where lactate > 4.0 mmol/L as welfare concern (P-01). Flags sessions with fewer than 4 steps as LOW confidence.

**Ridden heart rate interpretation**: Computes average HR per phase; flags phases with HR > 200 bpm.

---

## F-17 Kinematic In-Hand Analysis (Noran AI)
Epic: E-02 · Priority: Should

NEW — added after codebase analysis. Covers `kinematicInHand` test_type (horse led in hand, no rider).

---

## F-18 Jumping Competition Analysis
Epic: E-02 · Priority: Should

NEW — added after codebase analysis. Covers `jumpingCompetition` test_type.

Note: blocked from production until the `jumpingCompetition` JSON schema is confirmed in the codebase test suite.

---

## F-19 Competition Video & Protocol Analysis
Epic: E-02 · Priority: Should

NEW — added after codebase analysis. Covers `competition_video` and `competition_protocol` test_types.

In MVP, `competition_video` sections are marked "[video link only — not AI analysed]" in the report.

---

## F-20 Activity & Logbook Context Enrichment
Epic: E-10 · Priority: Should

NEW — added after codebase analysis. Enriches AI calls with `ScheduleItem` and `TrainingLog` data.

**Behaviour**
- `TrainingLog` data is always labelled "self-reported" in report output.
- A session with `stopped_early=True` produces a LOW confidence flag on all `AnalysisData` from that session.
- Mood trend (`ScheduleItem.mood` ≤2 for ≥3 consecutive sessions) triggers a wellbeing flag.

---

## F-21 RAG Pipeline — Scientific Literature Retrieval
Epic: E-11 · Priority: Must

Before generating any report section or Sparring Bot answer, the system queries the scientific library to retrieve the most relevant literature chunks (default top-k=5), which are injected into the AI prompt.

**Ingestion sub-pipeline**: documents are chunked into 300–600 token segments with 50-token overlap, embedded, and stored with taxonomy tags. Norm-table documents are stored in a structured queryable format.

**Acceptance criteria**
- For every AI generation call, at least one retrieval query is issued.
- If no chunk scores above minimum similarity threshold, output includes "No supporting literature found" note.
- Retrieval adds no more than 3 seconds to p95 generation call latency.

---

## F-22 Scientific Library Curation Workflow
Epic: E-11 · Priority: Should

Provides sport scientists with a workflow to add, tag, version, and retire literature in the RAG scientific library.

**Vocabulary**: Intensity language is discipline-appropriate — dressage plans use Maintenance/Moderate/High/Overload; showjumping plans use the same scale with discipline-specific exercise terminology.

---

## F-23 Schedule Generation — Day-by-Day Training Tables
Epic: E-08 · Priority: Should

Generates a day-by-day training schedule for a 6–8 week period covering both rider-as-athlete and horse, with coordinated intensity tracks.

**Periodization phases**: GPP → SPP → Competition → Transition

**Constraints**
- Must not schedule both rider and horse at Overload intensity on the same day without explicit sport scientist confirmation.
- Rider fitness metrics (pct, flexchair) are aggregated freely across horses; rider kinematic data (seatBalance, combination) is shown per horse separately (OD-11).

---

## MVP Release Checklist

Must-priority features: F-01, F-02, F-03, F-04, F-05, F-07, F-08, F-10, F-11, F-12, F-21

Must resolve before MVP: OD-01, OD-02, OD-09, OD-10
