# Features

## Overview

This file describes the user-facing capabilities that the first prototype should demonstrate.

For this workshop, the first version should be a rapid, somewhat-interactive, easily-shareable prototype. The goal is not production completeness. The goal is to make the idea concrete enough that other people can react to it.

The first prototype should:
- show one complete end-to-end journey,
- use realistic example or mocked inputs,
- expose enough context to make the output believable,
- and make feedback collection easy.

---

# Prototype Goal

Create a self-contained prototype that can be opened locally or shared quickly with other people.

Recommended characteristics:
- minimal setup,
- no required backend for the first version,
- a clear start state,
- a visible transformation from input to output,
- and a fast way to try a second scenario.

---

# Core Features

## Feature 1: Guided Starting Point

- Explain the problem being solved in plain language
- Make it obvious who the prototype is for
- Provide a single clear call to action to begin

## Feature 2: Example Input Or Demo Scenario

- Let the user start from sample data, prefilled inputs, or a default scenario
- Ensure the full flow works even when the tester brings no data
- Reduce setup friction during a workshop or stakeholder demo

## Feature 3: Simple User Input

- Let the user enter or select a small number of realistic inputs
- Focus on the inputs that most strongly affect the outcome
- Avoid long forms or implementation-heavy setup

## Feature 4: Scenario Selection Or Filtering

- Let the user choose one case, record, persona, or situation to inspect
- Support narrowing the scope before generating an output
- Make the selected context visible to the user

## Feature 5: Transparent Output Context

- Show the evidence, assumptions, or summary that drives the result
- Make the prototype auditable enough that a tester can challenge it
- Help the builder explain what the system is basing its answer on

## Feature 6: First Generated Result

- Produce a concrete recommendation, draft, analysis, or next step
- Make the result specific enough that a tester can agree, disagree, or refine it
- Prefer outputs that feel useful rather than technically impressive

## Feature 7: Steering And Iteration

- Let the user adjust the emphasis or request a second version
- Support rapid experimentation without restarting the whole flow
- Demonstrate that the product can adapt to user intent

## Feature 8: Feedback Capture

- Include a lightweight way to record reactions
- Examples: a short form, thumbs up or down, confidence rating, or follow-up question
- Make feedback collection part of the prototype rather than a separate activity

---

# Nice-To-Have Features

- Mobile-friendly layout
- Scenario compare view
- Example data autofill
- Exportable summary or screenshot-friendly output
- Visible disclaimer when parts of the flow are mocked

---

# Out Of Scope For The First Prototype

- Authentication
- Production integrations
- Full data pipelines
- Robust permissions
- Long-running agent workflows
- Perfect visual polish

---

# Success Criteria

- A new person can understand the concept within a few minutes
- The prototype demonstrates a full journey from input to output
- The prototype is easy to share without developer help
- The output is concrete enough to attract useful criticism
- Feedback from early users clearly informs the next build step
