# Agent Instructions

This file is the root-level instruction set for any agent working in this repository.

## Read Order

1. Read `README.md` first.
2. Read this file.
3. Read all files in `agent-docs/` before proposing implementation work.
4. Treat files in `agent-docs/past-big-instructions/` as historical context only if they conflict with the current root-level guidance.

## Repository Boundaries

1. Treat `secret-data/` as private and off-limits.
2. Use `example-data/` for demos, mocked inputs, and safe test data.
3. Treat `legacy-code/` as reference material only.
4. Do not copy legacy code blindly.

## Prototype Strategy

1. Prefer a small working prototype over a complete production system.
2. Keep changes understandable for workshop students.
3. Treat root-level `generate_standalone_html.py` as the main Phase 1 implementation path.
4. Do not create or maintain Phase 1 by directly editing a standalone HTML deliverable.
5. Generate Phase 1 HTML artifacts into `build/`.
6. Treat `build/example.html` as the default generated example artifact.
7. Treat user-specific Phase 1 artifacts as generated outputs named with recognizable sequential filenames such as `build/team-planner-v01.html`, `build/team-planner-v02.html`, and so on.
8. Treat root-level `app.py` as the intended Phase 2 Streamlit app location.
9. It is OK for `app.py` to be a small placeholder working app.
10. For Phase 1 standalone HTML, use standardized navigation with these default top-level buttons in this exact order: `Uitdaging`, `Aannames`, `Interactieve Demo`, `Wat kan er misgaan?`, and `Next Steps`.
11. Only `Interactieve Demo` may contain additional subpages or tabs when the use case genuinely needs them.
12. By default, generate user-facing output in Dutch for both Phase 1 and Phase 2 unless the user explicitly asks for another language.
13. In Phase 1, make the `Interactieve Demo` navigation item visually distinct from the other top-level buttons.
14. In Phase 1, keep source links and canvas references visually secondary by placing them under a top-right options-style button with three horizontal lines, not inside the main button sequence.
15. Do not show a prominent visible skill badge such as `Skill: workshop-html-prototype` unless the user explicitly wants it; omit it or hide it behind an optional control.

The intended flow is:

```text
idea -> agent planning docs -> Phase 1 clickable shell -> Phase 2 functional app
```

## Working Style

1. Ask for or propose a plan before large edits.
2. Inspect the existing repo structure before implementing.
3. For Phase 1, update generator code or source data and then run `generate_standalone_html.py` to regenerate the artifact into `build/`.
4. Agents may run the generator script to create HTML outputs, but should not write the generated `.html` deliverable directly by hand.
5. When moving into Phase 2, keep the app minimal and readable.
6. If the date is June 4, 2026 or earlier and the user seems ready to move into Phase 2, explicitly confirm that they want to continue even though Phase 2 belongs to the next AI-lab session.
7. Build the Phase 1 page structure from the provided `agent-docs/`, example data, and safe references. If the material is too thin or ambiguous, ask the user for clarification instead of inventing extra pages.
8. After generating a first version, ask whether the user wants to adapt the color theme and/or add logos. Mention that logos can be added in `assets/`, ask for 2 to 5 preferred HEX colors, and ask which logo files should be processed.
9. After that, ask whether the user wants more interaction on the `Interactieve Demo` page and what they want to add first.
