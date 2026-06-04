# Getting Started

This is the human guide for this repository. If you are a participant, start here.

## 1. Clone Repository

### Low-tech:

- [ ] Go to [Rens88/ailab-rapid-prototype](https://github.com/Rens88/ailab-rapid-prototype) and download the `.zip` file.
- [ ] Or ask your agent, for example Claude Code, to clone [Rens88/ailab-rapid-prototype](https://github.com/Rens88/ailab-rapid-prototype) for you:
```text
Clone https://github.com/Rens88/ailab-rapid-prototype into a new local folder for me and tell me where you put it.
```
- [ ] (optional) Open the repository folder in VS Code.

### High-tech:

- [ ] Clone the repository with Git.

```bash
git clone https://github.com/Rens88/ailab-rapid-prototype
cd ailab-rapid-prototype
```

- [ ] (optional) Open the repository folder in VS Code.

```bash
code .
```

## 2. Create `.venv` and Install Requirements

### Low-tech:

- [ ] Ask your agent to create a local `.venv`, activate it, and install the requirements for you:
```text
Please create a local .venv in this repository, install the requirements from requirements.txt.
```
- [ ] Ask your agent to use the Python generator code to create the standalone HTML:
```text
Please use the Python file generate_standalone_html.py in this repository to generate the standalone HTML for me, and tell me which HTML file was created in build/.
```
- [ ] Or ask the agent to verify that `python generate_standalone_html.py` can run:
```
Check whether python generate_standalone_html.py runs successfully.
```

### High-tech:

- [ ] Create a local virtual environment.

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

- [ ] Install the dependencies.

```bash
pip install -r requirements.txt
```

- [ ] Generate the default standalone HTML example.

```bash
python generate_standalone_html.py
```

- [ ] If you prefer not to activate the virtual environment first, run the generator directly with the Python executable inside `.venv`.

On macOS or Linux:

```bash
.venv/bin/python generate_standalone_html.py
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe generate_standalone_html.py
```

- [ ] Open [build/example.html](build/example.html) in your browser and check that the generated example works.

---
---
Congratulations!
You've (hopefully) managed to create the default standalone-html. Check out [build/example.html](build/example.html) in your favorite browser.
You're now ready to get started with your own standalone-html for your use-case.

## 3. Copy Homework Into `agent-docs/`

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
- [ ] Add any additional homework files your workshop needs.

## 4. Start The Workshop With A Startup Prompt

- [ ] Paste this prompt into your agent:
```text
Start the workshop. First read README.md. Then read AGENTS.md at the repo root and every file in agent-docs/. Treat legacy-code/ as reference only and do not copy it. Generate user-facing output in Dutch by default unless I ask for another language. For Phase 1, do not create a standalone HTML file directly. Instead, update generate_standalone_html.py or safe source inputs and generate outputs into build/. After that, summarize the project setup and propose a small plan for a Phase 1 generator-based prototype before editing any files.
```

## 5. Build Phase 1

Phase 1 is the focus of AI-lab session 3 on June 4, 2026. Phase 2 belongs to the next AI-lab session.

- [ ] Use your agent to iterate different versions of your standalone HTML for Phase 1.
- [ ] Ask for mocked or example content only.
- [ ] Ask for one clickable end-to-end journey and a small feedback interaction.
- [ ] Ask the agent to generate each version into `build/` with a recognizable sequential filename:

```text
Build a small Phase 1 clickable prototype by updating generate_standalone_html.py or safe source inputs. Do not create a standalone HTML deliverable directly. Use mocked or example content only. Generate the user-facing output in Dutch by default. Make sure there is one clickable end-to-end journey and a small feedback interaction. Use these default buttons in this exact order: `Uitdaging`, `Aannames`, `Interactieve Demo`, `Wat kan er misgaan?`, `Next Steps`. Make the `Interactieve Demo` button stand out visually. Put `Bronnen` under a top-right options-like button with three horizontal lines instead of in the main button sequence, and omit or hide any visible `Skill: ...` badge. Generate the result into build/ with a recognizable sequential filename such as build/team-planner-v01.html. After generating the first version, ask me whether I want to adapt the color theme and/or add logos from assets/, ask which 2 to 5 HEX colors I like, ask which logo files you should process, and then ask whether I want more interaction on the `Interactieve Demo` page and what I want to add first. Before doing any Phase 2 work, stop and ask me to confirm.
```

- [ ] If the prototype is ready and you think about Phase 2, stop first and confirm that you really want to move into the next session's work.

---

NOTE: To generate the standalone html, either ask your agent to do this for you, or call `generate_standalone.html` using Python and your virtual environment.

## 6. Build Phase 2

This is for next week's AI-lab session and only for participants who are done iterating on their Phase 1 product.

- [ ] Ask your agent whether you are really done iterating on Phase 1 before starting Phase 2:

```text
Before we start Phase 2, check whether my Phase 1 prototype is stable enough to stop iterating for now. If not, tell me to stay in Phase 1. If yes, propose a minimal Phase 2 plan in app.py.
```

- [ ] Before building the app, provide the agent with any fake or example data it can use for Phase 2.
- [ ] Keep all Phase 2 data in `example-data/`.
- [ ] If you do not have suitable fake data yet, ask the agent to generate code that synthesizes it and saves it into `example-data/`.
- [ ] Ask for a minimal functional app in `app.py`.
- [ ] Build or adapt root-level `app.py`.
- [ ] Keep it minimal and readable.
- [ ] Use public fake or example data from `example-data/`.
- [ ] Add one meaningful interaction.
- [ ] Show the context or evidence behind the output.

Suggested prompt:

```text
We are ready for Phase 2. First check whether Phase 1 is stable enough to stop iterating for now. Then inspect example-data/ and use any fake or example data you find there. If needed, generate code that synthesizes additional fake data and save it into example-data/. Generate the user-facing app in Dutch by default unless I ask for another language. After that, build a minimal readable app in app.py with one meaningful interaction and visible context behind the output.
```

---
NOTE: To run the app:

Low-tech:

- [ ] Ask your agent to run the app for you and tell you how to open it:

```text
Please run the Phase 2 app for me and tell me which local URL I should open in my browser.
```

High-tech:

- [ ] Run the app locally when you are ready.

```bash
streamlit run app.py
```

## 7. Final Check

### Low-tech:

- [ ] Ask your agent for a short summary of what changed:

```text
Please give me a short summary of what changed, list which files were edited, and confirm that secret-data/ was not used.
```

- [ ] Open the changed files and skim them yourself.
- [ ] Check that `secret-data/` was not used.

### High-tech:

- [ ] Review the changed files carefully.
- [ ] Keep `secret-data/` private.
- [ ] Use `example-data/` for safe demo inputs.
- [ ] Make sure the prototype is understandable enough to hand in or share.
