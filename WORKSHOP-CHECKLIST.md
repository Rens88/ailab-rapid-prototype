# Workshop Checklist

## Phase 0: Local Setup

- [ ] Clone or create the repository.
- [ ] Open the repository in VS Code.
- [ ] Create `.venv`.
- [ ] Activate `.venv`.
- [ ] Install dependencies with `pip install -r requirements.txt`.
- [ ] Confirm you can run Python from the activated environment.
- [ ] Create a Codex sandbox with `sbx create --branch ai-feature codex .`.
- [ ] Run the sandbox with `sbx run <sandbox-name>`.

## Phase 1: Add / Adapt Agent Docs

- [ ] Open `agent-docs/`.
- [ ] Replace or adapt the template docs with your own generated materials.
- [ ] Keep private data and secrets out of `agent-docs/`.
- [ ] Ask the agent to read `README.md`, `GETTING_STARTED.md`, and `agent-docs/`.
- [ ] Ask the agent to inspect and plan before letting it edit files.
- [ ] Review the agent's plan against your intended prototype scope.

## Phase 2: Create Empty Clickable Shell

- [ ] Build or adapt `prototype-shell/index.html`.
- [ ] Optionally run `python generate_standalone_html.py` to create `dist/index.html`.
- [ ] Keep it standalone and shareable.
- [ ] Use mocked or example content.
- [ ] Demonstrate one simple end-to-end journey.
- [ ] Add a small feedback or "was this useful?" interaction.
- [ ] Test it on desktop and mobile widths.
- [ ] Treat generated HTML as output; update the generator or source data when regenerating.

## Phase 3: Ask The Agent To Inspect Legacy / Reference Code

- [ ] Ask the agent to inspect `legacy-code/` as reference material.
- [ ] Ask for a short summary of useful patterns before implementation.
- [ ] Confirm the agent is not copying legacy code blindly.
- [ ] Decide which patterns should move into the new prototype.

## Phase 4: Upgrade Toward A Functional App

- [ ] Build or adapt root-level `app.py`.
- [ ] Keep `app.py` as a small placeholder working app until the prototype needs more structure.
- [ ] Load safe example data from `example-data/`.
- [ ] Add one meaningful interaction.
- [ ] Show the context, assumptions, or evidence behind the output.
- [ ] Add a placeholder for collecting user feedback.
- [ ] Run the app with `streamlit run app.py`.

## Phase 5: Test With Users And Capture Feedback

- [ ] Show the clickable shell or Streamlit app to at least one real user.
- [ ] Watch where the flow is confusing.
- [ ] Capture feedback in `agent-docs/MEMORY.md`.
- [ ] Update `agent-docs/FEATURES.md` or `agent-docs/USER-STORIES.md` if the scope changes.
- [ ] Review Git changes manually before committing.
