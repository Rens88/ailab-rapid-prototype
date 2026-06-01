# Getting Started

Use this guide as a practical setup checklist for the workshop.

## 1. Get The Repository

- [ ] Clone this repository, or create your own repository from the workshop template.

```bash
git clone <your-repo-url>
cd ailab-rapid-prototype
```

- [ ] Open the folder in VS Code.

```bash
code .
```

## 2. Create A Local Python Environment

The sandbox is useful for agent work, but it does not replace your local Python virtual environment. Keep a local `.venv` for running and testing the app yourself.

- [ ] Create a virtual environment named `.venv`.

```bash
python -m venv .venv
```

- [ ] Activate it on macOS or Linux.

```bash
source .venv/bin/activate
```

- [ ] Or activate it on Windows PowerShell.

```powershell
".venv\Scripts\Activate"
```

- [ ] Install the beginner-friendly dependencies.

```bash
pip install -r requirements.txt
```

Optional modern route:

```bash
pip install -e .
```

The optional route uses `pyproject.toml`. For most workshop participants, `requirements.txt` is the clearest path.

## 3. Add Or Adapt Your Agent Docs

- [ ] Open `agent-docs/`.
- [ ] Replace or adapt the provided planning files with the materials you already generated for your own idea.
- [ ] Keep the same rough structure so agents know where to look:
  - `CONSTITUTION.md`
  - `FEATURES.md`
  - `USER-STORIES.md`
  - `PROMPTS.md`
  - `MEMORY.md`
  - `ARCHITECTURE.md`
  - `AGENTS.md`

Before asking an agent to edit files, ask it to inspect `README.md`, `GETTING_STARTED.md`, and `agent-docs/`, then propose a small plan.

## 4. Create A Docker Sandbox With Codex

Use branch mode so agent changes are isolated from your main branch.

- [ ] Create the sandbox.

```bash
sbx create --branch ai-feature codex .
```

- [ ] Run the sandbox.

```bash
sbx run <sandbox-name>
```

- [ ] In the sandbox, ask the agent to inspect and plan before it edits files.

Example prompt:

```text
Read README.md, GETTING_STARTED.md, and agent-docs/. Then inspect legacy-code/ as reference only. Propose a small plan for a Phase 1 clickable prototype before editing files.
```

## 5. Build In Two Phases

- [ ] Phase 1 (AI-lab session 3): start with `prototype-shell/index.html`.
  - Standalone HTML.
  - No backend.
  - Mocked or example content.
  - One clickable end-to-end journey.
  - A small feedback interaction.
  - Optional generator path: run `python generate_standalone_html.py` to write `dist/index.html`.

- [ ] Phase 2 (AI-lab session 4): evolve into root-level `app.py`.
  - Minimal Streamlit app.
  - It may be a placeholder working app.
  - Uses public example data from `example-data/`.
  - Shows context or evidence behind its output.
  - Keeps the code readable for students.

## 6. Review Git Changes Manually

- [ ] Review every changed file before committing.

```bash
git status
git diff
```

- [ ] Check that private data stayed out of git.
- [ ] Keep `secret-data/` private.
- [ ] Use `example-data/` for safe demo inputs.
