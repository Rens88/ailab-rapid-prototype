# AI Lab Rapid Prototype

## Overview

This repository is a planning-first workshop template for students who use AI coding agents to move from a real-world idea to a rapid prototype.

The goal is not a production system. The goal is a small, understandable prototype that makes an idea concrete enough to test with real people.

The intended flow is:

```text
idea -> agent planning docs -> Phase 1 clickable shell -> Phase 2 functional app
```

---

# Workshop Flow

1. Adapt the planning files in `agent-docs/` for your own idea.
2. Ask the agent to inspect and plan before it edits files.
3. Build a Phase 1 clickable shell in `prototype-shell/index.html`.
4. Optionally regenerate a richer Phase 1 artifact with `generate_standalone_html.py`.
5. Upgrade the most useful flow into a Phase 2 Streamlit app in `app.py`.
6. Test with users and capture what changed in `agent-docs/MEMORY.md`.

Start small. Prefer one complete journey over many unfinished features.

---

# Key Files

- `GETTING_STARTED.md`: setup steps for VS Code, Python, Codex sandbox, and local review.
- `WORKSHOP-CHECKLIST.md`: phase-by-phase workshop checklist.
- `AGENTS.md`: root-level instructions for AI coding agents.
- `agent-docs/`: planning materials for constitution, prompts, memory, architecture, features, and user stories.
- `prototype-shell/index.html`: Phase 1 standalone clickable concept prototype.
- `generate_standalone_html.py`: root-level placeholder generator for a richer standalone HTML artifact.
- `dist/index.html`: generated Phase 1 HTML output. Regenerate it instead of treating it as the source of truth.
- `app.py`: Phase 2 minimal functional Streamlit scaffold. It is OK for this root file to be a small placeholder working app.
- `example-data/`: public, safe demo inputs.
- `secret-data/`: private working data; keep this out of agent context and git history.
- `legacy-code/`: old reference implementation and patterns agents can inspect but should not copy blindly.

---

# Run The Prototypes

Open the Phase 1 shell directly in a browser:

```text
prototype-shell/index.html
```

Run the Phase 2 app after installing dependencies:

```bash
streamlit run app.py
```

Regenerate the richer Phase 1 standalone HTML artifact:

```bash
python generate_standalone_html.py
```

---

# Folder Structure

```text
AGENTS.md
GETTING_STARTED.md
WORKSHOP-CHECKLIST.md
agent-docs/
app.py
assets/
dist/
example-data/
generate_standalone_html.py
legacy-code/
prototype-shell/
secret-data/
```

---

# Important Documentation

- `GETTING_STARTED.md`
- `WORKSHOP-CHECKLIST.md`
- `agent-docs/AGENTS.md`
- `agent-docs/ARCHITECTURE.md`
- `agent-docs/CONSTITUTION.md`
- `agent-docs/FEATURES.md`
- `agent-docs/MEMORY.md`
- `agent-docs/PROMPTS.md`
- `agent-docs/USER-STORIES.md`

---

# Current Scope

This template intentionally keeps the application surface small. A minimal placeholder Streamlit app in root-level `app.py` is welcome because it gives students a simple, conventional place to start. Keep it readable and easy to replace as the prototype matures.
