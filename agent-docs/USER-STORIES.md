# User Stories
## EquInnoLab — Prestatiesport Portal · AI Layer
Version 2.0 · May 2026

Priority: Must / Should / Could / Won't · Estimate: S / M / L / XL

---

## 1. Actors

**Sport Scientist** — Primary operator of the Holistic Report Generator. Computer or iPad. Full access to all AnalysisData records for their organisation. Reviews, edits, and publishes all AI-generated reports.

**Coach** — Primary user of the Coach Sparring Bot. Smartphone. Sees aggregated pattern-level insights for assigned riders. Cannot modify AnalysisData records directly.

**Rider (subject)** — Subject whose data is analysed. User records with `type="rider"`. Must give GDPR consent before data is passed to any AI call.

**Admin / DPO** — Manages user accounts, consent records, organisation settings, and data retention. Has audit access to all AI calls.

---

## 2. Epic Overview

| Epic | Title | Sub-product | Status |
|---|---|---|---|
| E-01 | Data ingestion & context assembly | Both | Original |
| E-02 | Holistic Report Generator | Sub-A | Original |
| E-03 | Coach Sparring Bot | Sub-B | Original |
| E-04 | Human review & publish workflow | Sub-A | Original |
| E-05 | GDPR consent & data governance | Both | Original |
| E-06 | Longitudinal performance tracking | Both | Original |
| E-07 | Goal & training scale management | Sub-B | Original |
| E-08 | Training plans & periodization | Sub-A | New — codebase |
| E-09 | Reports management | Sub-A | New — codebase |
| E-10 | Activity & schedule tracking | Sub-B | New — codebase |
| E-11 | Scientific Library & RAG | Both | New |

---

## 3. E-01 — Data Ingestion & Context Assembly

**US-01 [Must] [M]**
As a sport scientist, I want to retrieve all AnalysisData records for a given Analysis session, so that I can assemble a complete data context for the Report Generator without manual data wrangling.

**US-02 [Must] [S]**
As a sport scientist, I want to see which test_types have complete vs. incomplete data for a session, so that I know which analyses can be included in the report before I generate.

**US-03 [Must] [M]**
As a sport scientist, I want to validate that measurement JSON conforms to the expected schema for each test_type, so that I can trust the AI model receives well-formed input.

**US-04 [Must] [M]**
As an engineer, I want to query the Questionnaire record for home-mode Analysis sessions, so that home-mode OMSAT-3 and subjective data is included in the AI context alongside lab measurements.

---

## 4. E-02 — Holistic Report Generator

**US-05 [Must] [XL]**
As a sport scientist, I want to generate a holistic performance report from a completed Analysis session, so that I can provide the coach and rider with a data-grounded, narrative performance summary within 10 minutes.

**US-06 [Should] [M]**
As a sport scientist, I want to select which test_types to include in a report before generating, so that I can exclude incomplete or low-quality tests without regenerating the whole report.

**US-07 [Must] [M]**
As a sport scientist, I want to receive a warning when the AI model expresses low confidence on a specific finding, so that I know which parts of the report need extra scrutiny before I publish.

**US-08 [Should] [L]**
As a sport scientist, I want to see the raw data interpretation step separately from the narrative synthesis step, so that I can verify the AI's data reading before I accept its coaching narrative (P-07).

---

## 5. E-03 — Coach Sparring Bot

**US-09 [Must] [XL]**
As a coach, I want to ask a natural language question about a rider's recent performance pattern, so that I get a data-grounded answer in under 30 seconds without navigating the full portal.

**US-10 [Should] [L]**
As a coach, I want to ask the bot to compare two time periods for a rider's metric, so that I can spot whether a training block is working.

**US-11 [Must] [M]**
As a coach, I want to receive an escalation message when the bot cannot answer reliably, so that I am not misled by a hallucinated answer.

**US-12 [Could] [M]**
As a coach, I want to view the Sparring Bot's conversation history for a rider, so that I can recall what I already asked.

---

## 6. E-04 — Human Review & Publish Workflow

**US-13 [Must] [L]**
As a sport scientist, I want to review and edit an AI-generated report before publishing, so that I can correct any errors before the coach sees the output.

**US-14 [Should] [M]**
As a sport scientist, I want to add comments to specific report sections before publishing, so that I can annotate my reasoning for edits.

**US-15 [Should] [M]**
As a sport scientist, I want to reject a report and trigger regeneration with a different test_type selection, so that I can correct a poor report without losing the original draft.

---

## 7. E-05 — GDPR Consent & Data Governance

**US-16 [Must] [L]**
As a rider, I want to give or withdraw my consent for my data to be used in AI analysis, so that I retain control over how my personal data is processed (AVG/GDPR right).

**US-17 [Must] [L]**
As an admin / DPO, I want to view an audit log of all AI calls made against rider data, so that I can demonstrate GDPR compliance.

**US-18 [Should] [L]**
As an admin / DPO, I want to respond to a data subject access request by exporting all AI outputs related to a rider, so that I can fulfil GDPR Article 15 obligations.

---

## 8. E-06 — Longitudinal Performance Tracking

**US-19 [Should] [L]**
As a sport scientist, I want to view a longitudinal summary of a rider's performance across all sessions, so that I can identify long-term development trends before generating a periodic report.

**US-20 [Should] [M]**
As a coach, I want to ask the Sparring Bot for a trend over the last N weeks for a specific metric, so that I can track whether a training intervention is producing measurable improvement.

---

## 9. E-07 — Goal & Training Scale Management

**US-21 [Should] [L]**
As a coach, I want to ask the Sparring Bot whether a rider's recent results are aligned with their active goal, so that I get an AI opinion on goal-progress.

**US-22 [Could] [M]**
As a coach, I want to see which SWOT items from a rider's goal are supported by recent analysis data.

---

## 10. E-08 — Training Plans & Periodization

**US-23 [Should] [XL]**
As a sport scientist, I want to generate a training plan recommendation based on session analysis data and the rider's active goal, so that I have an AI-drafted starting point rather than starting from scratch.

**US-24 [Could] [XL]**
As a sport scientist, I want to generate a periodization overview (macro-cycle) aligned with the rider's competition calendar.

**US-25 [Could] [M]**
As a coach, I want to ask the Sparring Bot whether the current training week aligns with the approved periodization plan.

---

## 11. E-09 — Reports Management

**US-26 [Must] [S]**
As a sport scientist, I want to view all reports for a rider in chronological order, so that I have a complete audit trail.

**US-27 [Must] [M]**
As a sport scientist, I want to share a published report with the coach and rider via the portal.

**US-28 [Must] [M]**
As an admin / DPO, I want to archive or delete a report at the request of the data subject, so that I can fulfil GDPR Article 17 (right to erasure) obligations.

---

## 12. E-10 — Activity & Schedule Tracking

**US-29 [Should] [S]**
As a coach, I want to ask the Sparring Bot how many training sessions a rider completed in a given period, so that I can quickly check session adherence.

**US-30 [Should] [M]**
As a sport scientist, I want to see TrainingLog entries for a rider as context when generating a report, so that I can include subjective wellbeing data alongside objective measurements.

**US-31 [Could] [M]**
As a coach, I want to ask the Sparring Bot about a rider's mood and horse wellbeing trends from the logbook.

---

## 13. E-11 — Scientific Library & RAG

**US-32 [Should] [M]**
As a sport scientist, I want to upload a scientific document and tag it across the four taxonomy dimensions, so that the AI system can retrieve relevant literature during report generation and every AI claim can be traced to a specific source.

**US-33 [Should] [S]**
As a sport scientist, I want to mark a library document as retired so that outdated literature is excluded from future AI retrievals.

**US-34 [Could] [M]**
As a sport scientist, I want to see a dashboard showing which documents are in the library, how recently they were updated, and how often they have been retrieved.

**US-35 [Must] [L]**
As a system, I want to retrieve the most relevant scientific library chunks and inject them into the AI prompt before generating any report section or Sparring Bot answer, so that every AI-generated claim is grounded in retrieved evidence (P-03).

**US-36 [Should] [M]**
As a sport scientist, I want to see which scientific sources the AI retrieved and used when generating each section of a report, so that I can verify the scientific basis before publishing.

---

## 14. Priority Matrix (MVP scope)

Must stories: US-01–05, US-07, US-09, US-11, US-13, US-16, US-17, US-26, US-27, US-28, US-35
