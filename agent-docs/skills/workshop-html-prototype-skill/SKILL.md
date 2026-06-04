---
name: workshop-html-prototype
description: Use when asked to create, refactor, or review a standalone HTML concept prototype for an AI Impact Lab or rapid-prototyping workshop. Best for turning use-case canvases, agent-docs, user stories, legacy-code references, and example data into a mobile-friendly, shareable, no-build HTML demo that communicates the problem, users, intended workflow, mocked interaction, evidence, assumptions, feedback, and next steps without requiring a backend or framework.
---

# Workshop HTML Prototype

Create a generator-first standalone HTML concept prototype for workshop participants.

The prototype is not meant to be a production app. It is a shareable, mobile-friendly conversation artifact that helps users, coaches, scientists, analysts, and stakeholders quickly understand and test the shape of a use case before building a functional app.

Use this skill when the goal is to turn a workshop use-case canvas, `agent-docs/`, user stories, legacy-code references, or example data into a simple clickable HTML prototype.

## Core principle

Build a small, believable prototype generator before building the real app.

The generated HTML should:
- open directly in a browser
- require no backend
- require no build step
- be easy to share
- work reasonably on mobile
- fake interaction where needed
- make assumptions visible
- invite feedback
- default to Dutch unless the user explicitly asks for another language

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

build/
  example.html

generate_standalone_html.py
```

Treat `agent-docs/` as intentional workshop input. Students may already have generated their own constitution, architecture notes, memory, prompts, feature list, and user stories. Do not remove this structure.

Treat `legacy-code/` or `legacy-prototype/` as reference material only. Extract patterns and domain cues, but do not copy old implementation blindly.

Never use `secret-data/` for a shareable HTML prototype.

## Standard prototype structure

Use this standardized navigation structure unless the user explicitly asks for a different structure.
In the generated UI, use these default top-level buttons in this exact order: `Uitdaging`, `Aannames`, `Interactieve Demo`, `Wat kan er misgaan?`, and `Next Steps`.

1. **Uitdaging**
   - What problem is this prototype about?
   - Who is affected?
   - What situation, workflow, or decision makes this worth solving?

2. **Aannames**
   - Which assumptions are most important to test first?
   - Which parts are still uncertain, fragile, or dependent on better data?
   - What evidence from the provided documents supports or weakens those assumptions?

3. **Interactieve Demo**
   - The main fake interaction.
   - Let the user select a context, option, athlete, team, group, location, scenario, or mock dataset.
   - Show a generated result, advice, dashboard card, report snippet, or planning overview.
   - This is the only top-level page that may contain additional subpages or tabs when the use case genuinely needs them.

4. **Wat kan er misgaan?**
   - List important risks and failure modes.
   - Include data quality, privacy, adoption, representativeness, validation, and model limitations where relevant.
   - Make it explicit what could break trust or make the prototype unusable in practice.

5. **Next Steps**
   - What should be tested, validated, or built next?
   - Mention missing data, user feedback, integration needs, privacy checks, and the bridge toward a functional app.

Do not expand this into many top-level pages by default. Keep the top-level navigation tight and consistent.
Build these pages from the provided documents, example data, and safe references. If the source material is incomplete or ambiguous, ask the user for clarification instead of inventing extra sections.

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

Use plain HTML, CSS, and JavaScript in the generated artifact unless there is a strong reason not to.

Preferred patterns:
- tab or step navigation
- simple cards
- mock selectors
- generated summary panel
- expandable evidence section
- clickable feedback buttons
- local-only state in JavaScript
- a visually distinct `Interactieve Demo` navigation control so the main demo stands out
- a top-right options-style button with three horizontal lines that contains `Bronnen`

For this workshop template, prefer five top-level tabs or subpages matching the standardized structure above.
Only add deeper navigation inside `Interactive Demo` when the use case truly needs multiple demo modes.

Do not add heavy libraries unless necessary. Avoid external dependencies when the file should be easy to share offline.

## HTML conventions

Prefer a simple generator that writes a single self-contained HTML file into `build/`.

Use:
- inline CSS
- inline JavaScript
- accessible semantic HTML
- responsive layout
- readable text
- clear visual hierarchy
- enough fake content to make the use case concrete

Do not show a prominent `Skill: workshop-html-prototype` label in the UI by default.
If the skill metadata is useful, hide it behind an optional control instead of giving it a fixed top-right badge.

Keep the generator code understandable for workshop students.
Do not treat a generated HTML file as the source of truth.

## Data handling

When using data:
- prefer small mocked datasets embedded in the HTML
- or load from `example-data/` if the generator needs it
- do not use private or sensitive data
- clearly label mock data as mock/example data

In this workshop template, the generator is the preferred Phase 1 path:

```text
generate_standalone_html.py
build/
  example.html
  team-planner-v01.html
  team-planner-v02.html
```

Treat everything in `build/` as generated output. Update the generator or safe source data when the page needs to change.
Use recognizable sequential filenames for user-specific versions.

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

This skill covers Phase 1: the standalone clickable shell generated from code.

Do not turn it into a Streamlit, Dash, or backend app unless explicitly asked.

If the user wants the next step, recommend a separate Phase 2 implementation:
- root-level `app.py`
- Streamlit or similar
- real data loading
- functional interactions
- validation and feedback capture

The Phase 1 HTML should make the intended interface and product logic clear enough that Phase 2 can be built deliberately.

## After the first version

After generating the first Phase 1 version, ask the user:
- whether they want to adapt the color theme and/or add logos
- to name 2 to 5 preferred HEX colors
- which logo files in `assets/` should be processed
- whether they want more interaction on the `Interactieve Demo` page
- what they would like to add first

## Delivery checklist

Before finishing, verify that the prototype:
1. Opens as a generated standalone HTML file.
2. Uses the standardized five-part navigation, unless the user explicitly asked for something else.
3. Works on mobile-sized screens.
4. Includes a fake but believable interaction.
5. Shows data/evidence behind the output.
6. Lists assumptions and risks.
7. Includes a feedback interaction.
8. Avoids private or secret data.
9. Is simple enough for workshop participants to understand.
10. Can be used as input for a later functional app.
