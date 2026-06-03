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
2. Use the startup prompt in `GETTING_STARTED.md` so the agent inspects and plans before it edits files.
3. Build Phase 1 by updating `generate_standalone_html.py` and safe source inputs, not by hand-authoring a deliverable HTML file.
4. Generate Phase 1 artifacts into `build/`, with recognizable sequential filenames for user-specific versions.
5. Upgrade the most useful flow into a Phase 2 Streamlit app in `app.py`.
6. Test with users and capture what changed in `agent-docs/MEMORY.md`.

Start small. Prefer one complete journey over many unfinished features.

---

# Key Files

- `GETTING_STARTED.md`: the single human guide for setup, workshop flow, and startup prompts.
- `AGENTS.md`: the single root-level instruction file for agents working in this repo.
- `agent-docs/`: planning materials for constitution, prompts, memory, architecture, features, and user stories.
- `generate_standalone_html.py`: root-level Phase 1 generator. Update this or its safe source inputs instead of editing a built HTML deliverable directly.
- `build/example.html`: default generated Phase 1 example artifact.
- `build/`: generated Phase 1 HTML outputs, including recognizable sequential user-specific versions.
- `app.py`: Phase 2 minimal functional Streamlit scaffold. It is OK for this root file to be a small placeholder working app.
- `example-data/`: public, safe demo inputs.
- `secret-data/`: private working data; keep this out of agent context and git history.
- `legacy-code/`: old reference implementation and patterns agents can inspect but should not copy blindly.

---

# Run The Prototypes

Open the default generated Phase 1 example directly in a browser:

```text
build/example.html
```

Run the Phase 2 app after installing dependencies:

```bash
streamlit run app.py
```

Regenerate the richer Phase 1 standalone HTML artifact:

```bash
python generate_standalone_html.py
```

Generate a user-specific version with automatic sequential naming:

```bash
python generate_standalone_html.py --name team-planner
```

---

# Folder Structure

```text
AGENTS.md
GETTING_STARTED.md
agent-docs/
app.py
assets/
build/
example-data/
generate_standalone_html.py
legacy-code/
secret-data/
```

---

# Important Documentation

- `GETTING_STARTED.md`
- `AGENTS.md`
- `agent-docs/AGENTS.md`
- `agent-docs/ARCHITECTURE.md`
- `agent-docs/CONSTITUTION.md`
- `agent-docs/FEATURES.md`
- `agent-docs/MEMORY.md`
- `agent-docs/PROMPTS.md`
- `agent-docs/USER-STORIES.md`

---

# Current Scope

This template intentionally keeps the application surface small. Phase 1 should stay generator-first: update the generator or safe source inputs, then regenerate shareable HTML into `build/`. A minimal placeholder Streamlit app in root-level `app.py` is welcome for Phase 2 because it gives students a simple, conventional place to start. Keep it readable and easy to replace as the prototype matures.
