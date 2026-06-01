---
name: workshop-html-prototype
description: Use when asked to create, refactor, or review a standalone HTML concept prototype for an AI Impact Lab or rapid-prototyping workshop. Best for turning use-case canvases, agent-docs, user stories, legacy-code references, and example data into a mobile-friendly, shareable, no-build HTML demo that communicates the problem, users, intended workflow, mocked interaction, evidence, assumptions, feedback, and next steps without requiring a backend or framework.
---

# Workshop HTML Prototype

Create a standalone HTML concept prototype for workshop participants.

The prototype is not meant to be a production app. It is a shareable, mobile-friendly conversation artifact that helps users, coaches, scientists, analysts, and stakeholders quickly understand and test the shape of a use case before building a functional app.

Use this skill when the goal is to turn a workshop use-case canvas, `agent-docs/`, user stories, legacy-code references, or example data into a simple clickable HTML prototype.

## Core principle

Build a small, believable prototype shell before building the real app.

The HTML should:
- open directly in a browser
- require no backend
- require no build step
- be easy to share
- work reasonably on mobile
- fake interaction where needed
- make assumptions visible
- invite feedback

Do not over-engineer. Prefer clarity over completeness.

## Expected repository context

Prefer this layout when the repo does not already have a better convention:

```text
agent-docs/
  CONSTITUTION.md
  FEATURES.md
  USER-STORIES.md
  PROMPTS.md
  MEMORY.md
  ARCHITECTURE.md
  AGENTS.md

example-data/
  ...

legacy-code/ or legacy-prototype/
  ...

prototype-shell/
  index.html
```

Treat `agent-docs/` as intentional workshop input. Students may already have generated their own constitution, architecture notes, memory, prompts, feature list, and user stories. Do not remove this structure.

Treat `legacy-code/` or `legacy-prototype/` as reference material only. Extract patterns and domain cues, but do not copy old implementation blindly.

Never use `secret-data/` for a shareable HTML prototype.

## Standard prototype structure

Use this navigation structure unless the user asks for something else:

1. **Overview**
   - What problem is this prototype about?
   - What decision or workflow does it support?

2. **Users & Situation**
   - Who are the intended users?
   - When and where would they use it?
   - What do they need to accomplish?

3. **Current Process**
   - What happens today?
   - Where is the friction?
   - What is slow, fragmented, unclear, or hard to reproduce?

4. **Prototype Demo**
   - The main fake interaction.
   - Let the user select a context, option, athlete/team/group/location/scenario, or mock dataset.
   - Show a generated result, advice, dashboard card, report snippet, or planning overview.

5. **Data & Evidence**
   - Show which mocked or example data supposedly supports the output.
   - Include visible context behind the recommendation or result.
   - Make the prototype feel inspectable, not magical.

6. **Assumptions & Risks**
   - List the important assumptions.
   - Include data quality, privacy, adoption, representativeness, validation, and model limitations where relevant.

7. **Feedback**
   - Ask whether the output is useful.
   - Ask what is missing.
   - Include simple buttons or form-like controls, even if they only update the page locally.

8. **Next Steps**
   - What would need to be tested or built next?
   - Mention data access, validation with users, privacy checks, integration, and functional app development.

## Use-case adaptation

Adapt labels and examples to the domain, but keep the structure consistent.

Examples:
- Opponent analysis: select opponent, show strengths/weaknesses, data-backed evidence, scout feedback.
- Planning dashboard: select programme/week, show staff/player availability, court/resource planning, missing data.
- Training load analysis: select athlete/session/period, show internal and external load summary, key parameters, caveats.
- Location knowledge assistant: select venue/weather/course/class, show practical advice, observations, evidence, uncertainty.
- Reporting/chatbot assistant: select test profile or athlete/horse, show holistic interpretation, report snippet, coaching translation.

The standard pages should help every team explain:
- what they are building
- who it is for
- what input it uses
- what output it gives
- why the output should be trusted
- what still needs validation

## Interaction model

Use plain HTML, CSS, and JavaScript unless there is a strong reason not to.

Preferred patterns:
- tab or step navigation
- simple cards
- mock selectors
- generated summary panel
- expandable evidence section
- clickable feedback buttons
- local-only state in JavaScript

Do not add heavy libraries unless necessary. Avoid external dependencies when the file should be easy to share offline.

## HTML conventions

Prefer a single self-contained file:

```text
prototype-shell/index.html
```

Use:
- inline CSS
- inline JavaScript
- accessible semantic HTML
- responsive layout
- readable text
- clear visual hierarchy
- enough fake content to make the use case concrete

Keep the code understandable for workshop students.

## Data handling

When using data:
- prefer small mocked datasets embedded in the HTML
- or load from `example-data/` only if the user explicitly wants a generator
- do not use private or sensitive data
- clearly label mock data as mock/example data

If using a generator, keep it optional and simple:

```text
generate_standalone_html.py
dist/
  index.html
```

In this workshop template, `generate_standalone_html.py` may be used as a root-level placeholder generator. Treat `dist/index.html` as generated output and update the generator or source data when the page needs to change.

For most workshop cases, a single hand-editable `index.html` is enough.

## Evidence and explainability

Every generated-looking output should show at least some evidence.

Good evidence examples:
- source cards
- relevant input rows
- assumptions used
- confidence/uncertainty labels
- "why this was suggested" explanation
- "what the prototype does not know yet" note

This is especially important for sport, coaching, planning, health, performance, and athlete-related use cases.

## Privacy and safety

Never include real personal, medical, athlete, or confidential data unless the user explicitly confirms it is safe and appropriate.

For workshop prototypes:
- use fake names
- use mock data
- avoid sensitive details
- keep `secret-data/` out of scope
- make privacy assumptions visible in the prototype

## Relationship to Phase 2 apps

This skill covers Phase 1: the standalone clickable shell.

Do not turn it into a Streamlit, Dash, or backend app unless explicitly asked.

If the user wants the next step, recommend a separate Phase 2 implementation:
- root-level `app.py`
- Streamlit or similar
- real data loading
- functional interactions
- validation and feedback capture

The Phase 1 HTML should make the intended interface and product logic clear enough that Phase 2 can be built deliberately.

## Delivery checklist

Before finishing, verify that the prototype:
1. Opens as a standalone HTML file.
2. Has the standard sections or a deliberate subset.
3. Works on mobile-sized screens.
4. Includes a fake but believable interaction.
5. Shows data/evidence behind the output.
6. Lists assumptions and risks.
7. Includes a feedback interaction.
8. Avoids private or secret data.
9. Is simple enough for workshop participants to understand.
10. Can be used as input for a later functional app.
