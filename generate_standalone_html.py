#!/usr/bin/env python3
"""Generate a standalone Phase 1 HTML prototype from a workshop canvas."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_CANVAS = ROOT / "legacy-code" / "misc" / "knltb-canvas-data.json"
DEFAULT_SKILL = (
    ROOT
    / "agent-docs"
    / "skills"
    / "workshop-html-prototype-skill"
    / "SKILL.md"
)
DEFAULT_OUTPUT = ROOT / "dist" / "index.html"


CANVAS_FIELDS = {
    "gebruikerContext": "Users & situation",
    "takenDoelen": "Tasks & goals",
    "huidigProces": "Current process",
    "pijnpunten": "Pain points",
    "aiMogelijkheden": "AI opportunities",
    "databronnen": "Data sources",
    "datakwaliteit": "Data quality",
    "productDienst": "Product shape",
    "waardecreatie": "Value creation",
    "ethiekPrivacy": "Ethics & privacy",
    "kritischeAannames": "Critical assumptions",
    "succesMetrics": "Success metrics",
    "tijdlijnTeam": "Timeline & team",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing canvas data: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def split_notes(value: str) -> list[str]:
    items: list[str] = []
    for raw_line in value.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        line = re.sub(r"^[-*]\s*", "", line)
        line = re.sub(r"^\d+[.)]\s*", "", line)
        items.append(line)
    return items


def first_items(value: str, limit: int) -> list[str]:
    return split_notes(value)[:limit]


def extract_skill_summary(path: Path) -> dict[str, str]:
    if not path.exists():
        return {
            "name": "workshop-html-prototype",
            "description": "Create a standalone HTML concept prototype for workshop use cases.",
        }

    text = path.read_text(encoding="utf-8")
    summary = {
        "name": "workshop-html-prototype",
        "description": "Create a standalone HTML concept prototype for workshop use cases.",
    }
    if text.startswith("---"):
        _, frontmatter, _ = text.split("---", 2)
        for line in frontmatter.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"')
            if key in summary and value:
                summary[key] = value
    return summary


def build_dashboard_cards(canvas: dict[str, Any]) -> list[dict[str, Any]]:
    goals = first_items(str(canvas.get("takenDoelen", "")), 6)
    pains = first_items(str(canvas.get("pijnpunten", "")), 6)
    quality = first_items(str(canvas.get("datakwaliteit", "")), 5)

    return [
        {
            "id": "planning",
            "title": "Planning groepen",
            "question": "Welke toernooien, events, testdagen en vakanties moeten zichtbaar zijn?",
            "signal": "Jaarplanning Groep 1/2: conceptueel volledig, overige groepen nog wisselend.",
            "mockScore": 68,
            "primaryAction": "Maak een gedeeld kwartaaloverzicht met ontbrekende invoer per groep.",
            "evidence": goals[:3] + pains[:1],
        },
        {
            "id": "presence",
            "title": "Aanwezigheid spelers & staf",
            "question": "Wie is wanneer op het NTC of extern aanwezig?",
            "signal": "Aanwezigheid staf wordt nog niet door iedereen bijgehouden.",
            "mockScore": 44,
            "primaryAction": "Start met weekniveau: staf, spelers, locatie en verantwoordelijke eigenaar.",
            "evidence": pains[1:3] + quality[:2],
        },
        {
            "id": "courts",
            "title": "Baanplanning NTC",
            "question": "Welke banen zijn bezet, vrij of mogelijk verhuurbaar?",
            "signal": "Baanplanning moet gekoppeld worden aan het bestaande afhangbord.",
            "mockScore": 57,
            "primaryAction": "Toon per week baanbezetting naast trainingsweken en verwachte aanwezigheid.",
            "evidence": goals[2:4] + quality[2:4],
        },
    ]


def normalize_canvas(canvas: dict[str, Any], skill: dict[str, str]) -> dict[str, Any]:
    sections = []
    for key, label in CANVAS_FIELDS.items():
        value = str(canvas.get(key, "")).strip()
        sections.append(
            {
                "key": key,
                "label": label,
                "items": split_notes(value),
                "raw": value,
            }
        )

    return {
        "projectName": str(canvas.get("projectName", "Workshop prototype")),
        "organisation": str(canvas.get("organisation", "Workshop team")),
        "date": str(canvas.get("date", "")),
        "skill": skill,
        "sections": sections,
        "dashboardCards": build_dashboard_cards(canvas),
        "feedbackPrompts": [
            "Helpt dit overzicht om sneller af te stemmen?",
            "Welke planning mist nog voor een echte test?",
            "Welke data moet eerst betrouwbaarder worden?",
        ],
    }


def render_html(model: dict[str, Any]) -> str:
    payload = json.dumps(model, ensure_ascii=False, indent=2)
    title = html.escape(f"{model['organisation']} {model['projectName']}", quote=True)
    return HTML_TEMPLATE.replace("__APP_TITLE__", title).replace(
        "__MODEL_JSON__", payload.replace("</", "<\\/")
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a standalone workshop HTML prototype."
    )
    parser.add_argument("--canvas", type=Path, default=DEFAULT_CANVAS)
    parser.add_argument("--skill", type=Path, default=DEFAULT_SKILL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    canvas = load_json(args.canvas)
    skill = extract_skill_summary(args.skill)
    model = normalize_canvas(canvas, skill)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(model), encoding="utf-8")
    print(f"Wrote {args.output}")


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__APP_TITLE__</title>
  <style>
    :root {
      --bg: #f3f7f4;
      --ink: #13211b;
      --muted: #5a6a61;
      --panel: #ffffff;
      --line: #cfd9d2;
      --field: #eef4f0;
      --accent: #007a5a;
      --accent-dark: #075842;
      --mint: #dceee6;
      --blue: #28658f;
      --yellow: #d4a51d;
      --red: #c84f39;
      --shadow: 0 18px 46px rgba(19, 33, 27, 0.12);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background:
        linear-gradient(120deg, rgba(0, 122, 90, 0.14), transparent 38%),
        linear-gradient(300deg, rgba(40, 101, 143, 0.13), transparent 35%),
        var(--bg);
      color: var(--ink);
      font-family: "Trebuchet MS", "Aptos", sans-serif;
      line-height: 1.45;
    }

    button, select, textarea { font: inherit; }

    .shell {
      width: min(1220px, calc(100% - 28px));
      margin: 0 auto;
      padding: 24px 0 44px;
    }

    header {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 20px;
      align-items: end;
      padding: 22px 0;
      border-bottom: 1px solid var(--line);
    }

    .eyebrow {
      margin: 0 0 8px;
      color: var(--accent-dark);
      font-size: 0.86rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    h1 {
      margin: 0;
      font-size: clamp(2rem, 7vw, 5.4rem);
      line-height: 0.94;
      letter-spacing: 0;
    }

    .skill-card {
      max-width: 360px;
      background: rgba(255, 255, 255, 0.78);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }

    .skill-card strong { display: block; margin-bottom: 6px; }
    .skill-card p { margin: 0; color: var(--muted); font-size: 0.94rem; }

    nav {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin: 18px 0;
    }

    nav button,
    .ghost,
    .feedback button {
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--ink);
      border-radius: 7px;
      padding: 9px 12px;
      cursor: pointer;
    }

    nav button[aria-pressed="true"],
    .primary {
      background: var(--accent);
      border-color: var(--accent);
      color: white;
    }

    .grid {
      display: grid;
      grid-template-columns: 390px minmax(0, 1fr);
      gap: 16px;
      align-items: start;
    }

    aside,
    .stage,
    .panel,
    .card {
      background: rgba(255, 255, 255, 0.86);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }

    aside {
      padding: 16px;
      position: sticky;
      top: 12px;
    }

    .stage {
      min-height: 620px;
      overflow: hidden;
    }

    .view {
      display: none;
      padding: 20px;
    }

    .view.active { display: block; }

    h2 {
      margin: 0 0 10px;
      font-size: clamp(1.45rem, 3vw, 2.35rem);
      line-height: 1.05;
      letter-spacing: 0;
    }

    h3 {
      margin: 0 0 8px;
      font-size: 1rem;
      letter-spacing: 0;
    }

    p { margin: 0 0 12px; color: var(--muted); }

    .selector {
      display: grid;
      gap: 10px;
      margin-bottom: 14px;
    }

    select,
    textarea {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: var(--field);
      color: var(--ink);
      padding: 10px;
    }

    textarea {
      min-height: 96px;
      resize: vertical;
    }

    .metric-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin: 16px 0;
    }

    .metric {
      background: var(--field);
      border-radius: 8px;
      padding: 12px;
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.78rem;
    }

    .metric strong {
      font-size: 1.55rem;
    }

    .cards {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin: 14px 0;
    }

    .card {
      box-shadow: none;
      padding: 14px;
      cursor: pointer;
    }

    .card.selected {
      border-color: var(--accent);
      box-shadow: inset 0 0 0 1px var(--accent);
    }

    .score {
      height: 9px;
      background: #dfe7e2;
      border-radius: 999px;
      overflow: hidden;
      margin-top: 10px;
    }

    .score span {
      display: block;
      height: 100%;
      width: var(--score);
      background: linear-gradient(90deg, var(--red), var(--yellow), var(--accent));
    }

    .output {
      border-top: 1px solid var(--line);
      margin-top: 18px;
      padding-top: 16px;
    }

    .evidence-list,
    .section-list {
      display: grid;
      gap: 8px;
      padding: 0;
      margin: 12px 0 0;
      list-style: none;
    }

    .evidence-list li,
    .section-list li {
      background: #f8fbf9;
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 10px;
    }

    .canvas-list {
      display: grid;
      gap: 10px;
    }

    .canvas-item {
      border-bottom: 1px solid var(--line);
      padding-bottom: 10px;
    }

    .canvas-item:last-child { border-bottom: 0; }
    .canvas-item button {
      width: 100%;
      text-align: left;
      border: 0;
      background: transparent;
      padding: 0;
      color: var(--ink);
      cursor: pointer;
    }
    .canvas-item small { color: var(--muted); }

    .roadmap {
      display: grid;
      gap: 12px;
      counter-reset: step;
    }

    .roadmap article {
      position: relative;
      padding: 14px 14px 14px 54px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdfb;
    }

    .roadmap article::before {
      counter-increment: step;
      content: counter(step);
      position: absolute;
      left: 14px;
      top: 14px;
      width: 28px;
      height: 28px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      background: var(--mint);
      color: var(--accent-dark);
      font-weight: 800;
    }

    .feedback {
      display: grid;
      gap: 12px;
    }

    .feedback-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .feedback button.selected {
      background: var(--mint);
      border-color: var(--accent);
    }

    .status {
      min-height: 22px;
      color: var(--accent-dark);
      font-weight: 700;
    }

    @media (max-width: 900px) {
      header,
      .grid {
        grid-template-columns: 1fr;
      }

      aside {
        position: static;
      }

      .cards,
      .metric-row {
        grid-template-columns: 1fr;
      }

      .stage {
        min-height: auto;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <div>
        <p class="eyebrow" id="eyebrow"></p>
        <h1 id="title"></h1>
      </div>
      <section class="skill-card">
        <strong id="skill-name"></strong>
        <p id="skill-description"></p>
      </section>
    </header>

    <nav aria-label="Prototype sections">
      <button type="button" data-view="overview" aria-pressed="true">Overview</button>
      <button type="button" data-view="demo" aria-pressed="false">Prototype Demo</button>
      <button type="button" data-view="evidence" aria-pressed="false">Data & Evidence</button>
      <button type="button" data-view="risks" aria-pressed="false">Assumptions</button>
      <button type="button" data-view="feedback" aria-pressed="false">Feedback</button>
      <button type="button" data-view="next" aria-pressed="false">Next Steps</button>
    </nav>

    <section class="grid">
      <aside>
        <h3>Canvas source</h3>
        <p>This page is generated from a workshop canvas and skill file. The interaction is mocked, but the evidence cards preserve the source thinking.</p>
        <div class="canvas-list" id="canvas-list"></div>
      </aside>

      <section class="stage">
        <section class="view active" id="overview"></section>
        <section class="view" id="demo"></section>
        <section class="view" id="evidence"></section>
        <section class="view" id="risks"></section>
        <section class="view" id="feedback"></section>
        <section class="view" id="next"></section>
      </section>
    </section>
  </main>

  <script id="seed" type="application/json">__MODEL_JSON__</script>
  <script>
    const model = JSON.parse(document.querySelector("#seed").textContent);
    const state = {
      selectedCard: model.dashboardCards[0].id,
      feedback: "",
      note: ""
    };

    const byKey = Object.fromEntries(model.sections.map((section) => [section.key, section]));

    function el(selector) {
      return document.querySelector(selector);
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
    }

    function list(items, className = "section-list") {
      if (!items || !items.length) {
        return `<p>No source notes yet.</p>`;
      }
      return `<ul class="${className}">${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
    }

    function renderShell() {
      el("#eyebrow").textContent = `${model.organisation} · ${model.date || "workshop canvas"}`;
      el("#title").textContent = model.projectName;
      el("#skill-name").textContent = `Skill: ${model.skill.name}`;
      el("#skill-description").textContent = model.skill.description;

      el("#canvas-list").innerHTML = model.sections.map((section) => `
        <article class="canvas-item">
          <button type="button" data-source="${section.key}">
            <strong>${escapeHtml(section.label)}</strong><br>
            <small>${section.items.length} source notes</small>
          </button>
        </article>
      `).join("");

      document.querySelectorAll("[data-source]").forEach((button) => {
        button.addEventListener("click", () => {
          showView("evidence");
          renderEvidence(button.dataset.source);
        });
      });
    }

    function renderOverview() {
      el("#overview").innerHTML = `
        <h2>From fragmented planning to one inspectable prototype</h2>
        <p>This generated shell turns the KNLTB canvas into a clickable concept: choose a planning dashboard, see a mocked recommendation, inspect the evidence, and capture feedback before building a real app.</p>
        <div class="metric-row">
          <div class="metric"><span>Canvas sections</span><strong>${model.sections.length}</strong></div>
          <div class="metric"><span>Mock dashboards</span><strong>${model.dashboardCards.length}</strong></div>
          <div class="metric"><span>Phase</span><strong>1</strong></div>
        </div>
        <div class="roadmap">
          <article><h3>Inspect the canvas</h3><p>Use the left panel to jump from source notes to evidence cards.</p></article>
          <article><h3>Try the fake dashboard</h3><p>Select a dashboard area and generate a first planning recommendation.</p></article>
          <article><h3>Collect reactions</h3><p>Use the feedback view to record whether the concept is useful enough for a Phase 2 app.</p></article>
        </div>
      `;
    }

    function selectedCard() {
      return model.dashboardCards.find((card) => card.id === state.selectedCard) || model.dashboardCards[0];
    }

    function renderDemo() {
      const card = selectedCard();
      el("#demo").innerHTML = `
        <h2>Prototype Demo</h2>
        <p>Select one planning surface and generate a mocked first output. This is deliberately static, but it should feel concrete enough to discuss with users.</p>
        <div class="selector">
          <label for="dashboard-select">Dashboard focus</label>
          <select id="dashboard-select">
            ${model.dashboardCards.map((item) => `<option value="${item.id}" ${item.id === card.id ? "selected" : ""}>${escapeHtml(item.title)}</option>`).join("")}
          </select>
        </div>
        <div class="cards">
          ${model.dashboardCards.map((item) => `
            <article class="card ${item.id === card.id ? "selected" : ""}" data-card="${item.id}">
              <h3>${escapeHtml(item.title)}</h3>
              <p>${escapeHtml(item.signal)}</p>
              <div class="score" aria-label="Mock readiness score"><span style="--score: ${item.mockScore}%"></span></div>
            </article>
          `).join("")}
        </div>
        <div class="output">
          <h3>${escapeHtml(card.question)}</h3>
          <p><strong>Mock recommendation:</strong> ${escapeHtml(card.primaryAction)}</p>
          <ul class="evidence-list">
            ${card.evidence.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </div>
      `;

      el("#dashboard-select").addEventListener("change", (event) => {
        state.selectedCard = event.target.value;
        renderDemo();
      });

      document.querySelectorAll("[data-card]").forEach((node) => {
        node.addEventListener("click", () => {
          state.selectedCard = node.dataset.card;
          renderDemo();
        });
      });
    }

    function renderEvidence(activeKey = "takenDoelen") {
      const section = byKey[activeKey] || byKey.takenDoelen;
      el("#evidence").innerHTML = `
        <h2>Data & Evidence</h2>
        <p>Generated-looking outputs should stay inspectable. These cards show which canvas notes support the mocked recommendation.</p>
        <div class="selector">
          <label for="evidence-select">Evidence source</label>
          <select id="evidence-select">
            ${model.sections.map((item) => `<option value="${item.key}" ${item.key === section.key ? "selected" : ""}>${escapeHtml(item.label)}</option>`).join("")}
          </select>
        </div>
        <h3>${escapeHtml(section.label)}</h3>
        ${list(section.items)}
      `;

      el("#evidence-select").addEventListener("change", (event) => {
        renderEvidence(event.target.value);
      });
    }

    function renderRisks() {
      const assumptions = byKey.kritischeAannames?.items || [];
      const privacy = byKey.ethiekPrivacy?.items || [];
      const quality = byKey.datakwaliteit?.items || [];
      el("#risks").innerHTML = `
        <h2>Assumptions & Risks</h2>
        <p>These are the checks to keep visible before turning the shell into a functional app.</p>
        <h3>Critical assumptions</h3>
        ${list(assumptions)}
        <h3>Data quality</h3>
        ${list(quality)}
        <h3>Ethics & privacy</h3>
        ${list(privacy)}
      `;
    }

    function renderFeedback() {
      el("#feedback").innerHTML = `
        <h2>Feedback</h2>
        <div class="feedback">
          <p>${escapeHtml(model.feedbackPrompts[0])}</p>
          <div class="feedback-row">
            ${["Useful", "Almost", "Not yet"].map((item) => `<button type="button" data-feedback="${item}" class="${state.feedback === item ? "selected" : ""}">${item}</button>`).join("")}
          </div>
          <label for="feedback-note">What should change before Phase 2?</label>
          <textarea id="feedback-note">${escapeHtml(state.note)}</textarea>
          <div class="status">${state.feedback ? `Captured: ${escapeHtml(state.feedback)}` : ""}</div>
        </div>
      `;

      document.querySelectorAll("[data-feedback]").forEach((button) => {
        button.addEventListener("click", () => {
          state.feedback = button.dataset.feedback;
          renderFeedback();
        });
      });
      el("#feedback-note").addEventListener("input", (event) => {
        state.note = event.target.value;
      });
    }

    function renderNext() {
      const timeline = byKey.tijdlijnTeam?.items || [];
      const metrics = byKey.succesMetrics?.items || [];
      el("#next").innerHTML = `
        <h2>Next Steps</h2>
        <p>Use the feedback from this generated shell to decide what belongs in the root-level Streamlit placeholder app.</p>
        <div class="roadmap">
          <article><h3>Validate the input format</h3><p>Agree how groups, staff, players and courts should be entered before building integrations.</p></article>
          <article><h3>Test one dashboard with users</h3><p>Start with the planning surface that creates the clearest coordination value.</p></article>
          <article><h3>Move to Phase 2</h3><p>Build the smallest working version in <code>app.py</code> after the HTML concept is clear.</p></article>
        </div>
        <h3>Timeline notes</h3>
        ${list(timeline)}
        <h3>Success metrics</h3>
        ${list(metrics)}
      `;
    }

    function showView(id) {
      document.querySelectorAll(".view").forEach((view) => {
        view.classList.toggle("active", view.id === id);
      });
      document.querySelectorAll("nav button").forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.view === id));
      });
      if (id === "demo") renderDemo();
      if (id === "evidence") renderEvidence();
      if (id === "risks") renderRisks();
      if (id === "feedback") renderFeedback();
      if (id === "next") renderNext();
    }

    document.querySelectorAll("nav button").forEach((button) => {
      button.addEventListener("click", () => showView(button.dataset.view));
    });

    renderShell();
    renderOverview();
    renderDemo();
    renderEvidence();
    renderRisks();
    renderFeedback();
    renderNext();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
