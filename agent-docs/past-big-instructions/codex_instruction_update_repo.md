# Codex Instruction – Update `ailab-rapid-prototype`

You are working in the repository `Rens88/ailab-rapid-prototype`.

## Goal

Update this repository into a clearer, lightweight workshop template for AI-assisted rapid prototyping.

Keep the template simple. Do not over-engineer.

The repo should help students move from:

idea → agent planning docs → empty clickable prototype → functional prototype

---

# Important context

- The `agent-docs/` architecture is intentional. Do not remove or simplify it away.
- Students have already been introduced to creating their own agent constitution, prompts, memory, architecture notes, and related planning docs.
- The template should explicitly instruct students to replace or adapt the provided `agent-docs/` with their own already-generated docs.
- `legacy-code/` or `legacy-prototype/` is reference material:
  old code/patterns that agents can inspect and imitate, not production code to copy blindly.
- Keep both dependency paths visible:
  - simple beginner path: `requirements.txt`
  - modern optional path: `pyproject.toml`

---

# Tasks

## 1. Add `GETTING_STARTED.md`

Create a human-readable step-by-step setup guide for students.

It should include:
- clone or create the repo
- open the repo in VS Code
- create a local Python virtual environment named `.venv`
- activate `.venv`
- install dependencies using `requirements.txt`
- mention the optional `pyproject.toml` route
- create a Docker Sandbox with Codex
- recommend branch mode:

```bash
sbx create --branch ai-feature codex .
```

- run the sandbox:

```bash
sbx run <sandbox-name>
```

- explain that students should review Git changes manually
- explain that the sandbox does not replace the local venv
- include a step where students insert or adapt their own generated `agent-docs/` materials

Keep this file practical, friendly, and checklist-like.

---

## 2. Add `WORKSHOP-CHECKLIST.md`

Create an afvinkbare workshop checklist.

Use phases:

- Phase 0: Local setup
- Phase 1: Add / adapt agent docs
- Phase 2: Create empty clickable shell
- Phase 3: Ask the agent to inspect legacy/reference code
- Phase 4: Upgrade toward a functional app
- Phase 5: Test with users and capture feedback

Include checkboxes.

Make it clear that students should first ask the agent to inspect and plan before letting it edit files.

---

## 3. Add root-level `AGENTS.md`

Create a short instruction file for AI coding agents.

It should tell agents:
- first read `README.md`
- then read `GETTING_STARTED.md`
- then inspect `agent-docs/`
- treat `secret-data/` as private and off-limits
- use `example-data/` for demos
- use `legacy-code/` or `legacy-prototype/` only as reference
- do not copy legacy code blindly
- prefer a small working prototype over a complete production system
- ask for or propose a plan before large edits
- keep changes understandable for workshop students

---

## 4. Update `.codexignore`

Add sensible defaults:

```gitignore
secret-data/
.venv/
.env
*.env
__pycache__/
.pytest_cache/
.ruff_cache/
.mypy_cache/
.ipynb_checkpoints/
.DS_Store
Thumbs.db
```

Do not ignore `example-data/`.

---

## 5. Improve or create `requirements.txt`

Use `requirements.txt` as the beginner-friendly install path.

If the project does not yet need many dependencies, keep it minimal.

Include at least the dependencies needed for the functional app phase if applicable, for example:

```text
streamlit
pandas
```

Do not add unnecessary libraries.

---

## 6. Clean up `pyproject.toml`

Make sure `pyproject.toml` is formatted readably across multiple lines.

Keep it as the optional modern Python project configuration.

Do not make the project overly complex.

---

## 7. Create Phase 1 prototype shell

Create:

```text
prototype-shell/
└── index.html
```

This should be a standalone HTML file.

Requirements:
- no backend
- no build step
- mobile-friendly
- easily shareable
- fake a sense of interaction
- use mocked/example content
- demonstrate one simple end-to-end user journey
- include a small feedback or “was this useful?” interaction
- keep styling inline or self-contained

This is not meant to be a real app. It is a clickable concept prototype.

---

## 8. Create Phase 2 functional app scaffold

Create:

```text
app.py
```

Use Streamlit unless there is a strong reason not to.

Requirements:
- minimal runnable app
- load example/mock data if available
- show a simple interaction
- include visible context/evidence behind output
- include a placeholder for collecting feedback
- keep code readable for students

Also update docs so students understand:
- `prototype-shell/index.html` is Phase 1
- root-level `app.py` is Phase 2

---

## 9. Update `README.md`

Keep the README concise.

It should explain:
- purpose of the repo
- intended workshop flow
- folder structure
- difference between:
  - `agent-docs/`
  - `prototype-shell/`
  - `app.py`
  - `example-data/`
  - `secret-data/`
  - `legacy-code/` or `legacy-prototype/`
- link to `GETTING_STARTED.md`
- link to `WORKSHOP-CHECKLIST.md`

Do not remove the planning-first philosophy. Strengthen it.

---

## 10. Preserve intentional existing structure

Do not delete `agent-docs/`.

Do not remove existing useful planning docs such as:
- `CONSTITUTION.md`
- `FEATURES.md`
- `USER-STORIES.md`
- `PROMPTS.md`
- `MEMORY.md`
- `ARCHITECTURE.md`
- `AGENTS.md` inside `agent-docs/`

Only edit them if needed to align terminology or add references to the new two-phase prototype flow.

---

## 11. Validate

After editing:
- show the final folder structure
- verify `prototype-shell/index.html` exists
- verify `app.py` exists
- verify `GETTING_STARTED.md` exists
- verify `WORKSHOP-CHECKLIST.md` exists
- verify `.codexignore` contains private-data exclusions
- if possible, run a basic syntax check on Python files

---

# Expected outcome

A simple, generic workshop starter repo that teaches students:

1. how to initialize the project,
2. how to bring in their own agent docs,
3. how to create a quick standalone HTML shell,
4. how to evolve that into a small functional app,
5. how to use AI agents safely and deliberately.

---

# Additional note

The repository currently references both:
- `legacy-code/`
- `legacy-prototype/`

Normalize this naming or explicitly support both consistently throughout the repo and documentation.
umentation.
