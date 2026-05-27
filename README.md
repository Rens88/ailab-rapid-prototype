# AI App Workshop Template

## Overview

This repository is a planning-first template for workshop participants who use AI tools such as Codex or Claude Code to go from a real-world idea to a rapid prototype.

The intended first milestone is not a production-grade app. It is a somewhat-interactive, easily-shareable prototype that makes the idea concrete enough to test with real people.

This template separates:
- planning documents in `agent-docs/`,
- safe demo inputs in `example-data/`,
- private working data in `secret-data/`,
- shared visual assets in `assets/`,
- and one reference implementation in `legacy-prototype/`.

---

# First Deliverable

For most participants, the best first artifact is a self-contained HTML prototype.

Recommended constraints:
- one `index.html` or `prototype.html` entry point,
- optional static assets only,
- mocked or example data instead of real integrations,
- one complete end-to-end flow from input to output,
- and one built-in way to collect feedback.

Why this works well in a workshop:
- almost no setup friction,
- easy to regenerate with AI assistance,
- easy to share by file or simple static hosting,
- and it forces attention onto the user journey before infrastructure.

---

# What To Borrow From `legacy-prototype/`

The reference prototype is currently a Streamlit app, not a template to copy literally. The useful patterns to reuse are:
- start from sample data so a demo always works,
- let the user select or narrow the scenario,
- show the evidence or context behind the output,
- generate a first result quickly,
- and let the user steer or refine that result.

---

# Working Rhythm

1. Define the problem and first prototype scope in `agent-docs/FEATURES.md` and `agent-docs/USER-STORIES.md`.
2. Record constraints and guardrails in `agent-docs/CONSTITUTION.md`.
3. Capture prompting strategy in `agent-docs/PROMPTS.md`.
4. Build the first prototype with example or mocked data.
5. Show it to real users and capture what changed in `agent-docs/MEMORY.md`.

---

# Folder Structure

```text
agent-docs/
assets/
example-data/
secret-data/
legacy-prototype/
```

Notes:
- `agent-docs/` contains planning and operating documents for AI-assisted building.
- `example-data/` is for synthetic or safely shareable demo data.
- `secret-data/` is for real or private data and should stay out of git except for its `readme.md`.
- `legacy-prototype/` is an example reference implementation and may be removed before distributing this template.

---

# Important Documentation

- `agent-docs/AGENTS.md`
- `agent-docs/ARCHITECTURE.md`
- `agent-docs/CONSTITUTION.md`
- `agent-docs/FEATURES.md`
- `agent-docs/MEMORY.md`
- `agent-docs/PROMPTS.md`
- `agent-docs/USER-STORIES.md`

---

# Current Scope

This template intentionally avoids committing real application code at the repository root.

Use it to frame the problem, generate a first prototype, and decide what deserves a real implementation next.
