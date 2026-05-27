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
