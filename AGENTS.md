# Agent Instructions

This repository is a lightweight workshop template for AI-assisted rapid prototyping.

When working here:

1. Read `README.md` first.
2. Read `GETTING_STARTED.md` next.
3. Inspect `agent-docs/` before proposing implementation work.
4. Treat `secret-data/` as private and off-limits.
5. Use `example-data/` for demos, mocked inputs, and safe test data.
6. Treat `legacy-code/` as reference material only.
7. Do not copy legacy code blindly.
8. Prefer a small working prototype over a complete production system.
9. Treat root-level `app.py` as the intended Phase 2 Streamlit app location.
10. It is OK for `app.py` to be a placeholder working app; keep it small, readable, and easy to replace.
11. Treat `generate_standalone_html.py` as the placeholder Phase 1 HTML generator.
12. Generated `dist/index.html` is an output artifact; prefer updating the generator or source data.
13. Ask for or propose a plan before large edits.
14. Keep changes understandable for workshop students.

The intended flow is:

```text
idea -> agent planning docs -> Phase 1 clickable shell -> Phase 2 functional app
```
