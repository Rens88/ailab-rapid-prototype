# Agents

## Overview

This file documents the agents that exist in the system and explains their responsibilities, permissions, and interactions.

In multi-agent systems, this file becomes essential because it:
- prevents role confusion,
- clarifies delegation,
- documents tool access,
- and helps developers debug orchestration issues.

Each agent should have:
- a clear purpose,
- defined inputs/outputs,
- allowed tools,
- and operational constraints.

---

# System Overview

Describe how agents cooperate inside the system.

---

# Shared Rules

- Agents must log important actions
- Agents cannot bypass approval systems
- Agents should avoid duplicate work
- Agents should treat root-level `app.py` as the intended Phase 2 Streamlit app location
- A small placeholder working app in `app.py` is acceptable for this workshop template
- Agents should prefer updating `generate_standalone_html.py` or safe source inputs for Phase 1 instead of editing deliverable HTML directly
- Agents may run `generate_standalone_html.py` to regenerate the richer Phase 1 output in `build/`
- Agents should not hand-write the generated `.html` deliverable itself
- Agents should use standardized Phase 1 navigation with these top-level buttons in this exact order: `Uitdaging`, `Aannames`, `Interactieve Demo`, `Wat kan er misgaan?`, and `Next Steps`
- Agents may add subpages or tabs only inside `Interactive Demo` when the use case needs them
- Agents should derive those pages from the provided documents and ask the user for clarification if important content is missing
- Generated HTML should stay shareable and should not use `secret-data/`
- Agents should generate user-facing output in Dutch by default unless the user asks for another language
- Agents should make the `Interactieve Demo` control visually distinct from the other top-level navigation buttons
- Agents should place `Bronnen` under a top-right options-style button with three horizontal lines instead of including it in the main button sequence
- Agents should omit a prominent `Skill: ...` badge unless the user explicitly asks for it, or hide it behind an optional control
- After generating a first version, agents should ask about theme colors, logos in `assets/`, and whether more interaction should be added to `Interactieve Demo`

---

# Agent: PlannerAgent

## Purpose

Describe the role of the planner.

## Responsibilities

- Break goals into tasks
- Prioritize work
- Delegate tasks

## Inputs

- User goals
- Previous task results

## Outputs

- Task plans
- Execution instructions

## Allowed Tools

- Search API
- Memory Retrieval

## Restrictions

- Cannot execute shell commands

## Failure Modes

- Infinite planning loops
- Overly large task trees

---

# Agent: ExecutorAgent

## Purpose

Describe the execution agent.

## Responsibilities

- Execute approved actions
- Generate code
- Run workflows

## Inputs

- Approved tasks

## Outputs

- Results
- Logs
- Artifacts

## Allowed Tools

- Shell
- Python Runtime
- APIs

## Restrictions

- Requires approval for destructive actions

## Failure Modes

- Tool retries
- Partial execution

---

# Agent Communication Rules

Describe:
- message format,
- task handoff,
- retries,
- escalation logic.

---

# Approval Workflow

Document:
- when humans must approve,
- critical actions,
- rollback procedures.

---

# Future Agents

Placeholder for future agent definitions.
