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
BUILD_DIR = ROOT / "build"
DEFAULT_OUTPUT = BUILD_DIR / "example.html"


CANVAS_FIELDS = {
    "gebruikerContext": "Gebruikerscontext",
    "takenDoelen": "Taken en doelen",
    "huidigProces": "Huidig proces",
    "pijnpunten": "Pijnpunten",
    "aiMogelijkheden": "AI-kansen",
    "databronnen": "Databronnen",
    "datakwaliteit": "Datakwaliteit",
    "productDienst": "Productvorm",
    "waardecreatie": "Waardecreatie",
    "ethiekPrivacy": "Ethiek en privacy",
    "kritischeAannames": "Kritische aannames",
    "succesMetrics": "Succesmetingen",
    "tijdlijnTeam": "Tijdlijn en team",
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
        "projectName": str(canvas.get("projectName", "Workshopprototype")),
        "organisation": str(canvas.get("organisation", "Workshopteam")),
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


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "prototype"


def next_versioned_output(build_dir: Path, stem: str) -> Path:
    pattern = re.compile(rf"^{re.escape(stem)}-v(\d+)\.html$")
    next_version = 1

    for path in build_dir.glob(f"{stem}-v*.html"):
        match = pattern.match(path.name)
        if not match:
            continue
        next_version = max(next_version, int(match.group(1)) + 1)

    return build_dir / f"{stem}-v{next_version:02d}.html"


def default_output_path(
    canvas_path: Path, canvas: dict[str, Any], requested_name: str | None
) -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    if requested_name:
        return next_versioned_output(BUILD_DIR, slugify(requested_name))

    if canvas_path.resolve() == DEFAULT_CANVAS.resolve():
        return DEFAULT_OUTPUT

    project_name = str(canvas.get("projectName", "")).strip()
    if project_name:
        return next_versioned_output(BUILD_DIR, slugify(project_name))

    return next_versioned_output(BUILD_DIR, slugify(canvas_path.stem))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a standalone workshop HTML prototype."
    )
    parser.add_argument("--canvas", type=Path, default=DEFAULT_CANVAS)
    parser.add_argument("--skill", type=Path, default=DEFAULT_SKILL)
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Recognizable base name for generated build files, for example 'team-planner'.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Explicit output path. If omitted, the default example is written to build/example.html and custom runs are versioned in build/.",
    )
    args = parser.parse_args()

    canvas = load_json(args.canvas)
    skill = extract_skill_summary(args.skill)
    model = normalize_canvas(canvas, skill)
    output_path = args.output or default_output_path(args.canvas, canvas, args.name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(model), encoding="utf-8")
    print(f"Wrote {output_path}")


HTML_TEMPLATE = r"""<!doctype html>
<html lang="nl">
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
      gap: 12px;
      align-items: start;
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

    .header-tools {
      display: flex;
      justify-content: flex-end;
    }

    .options-menu {
      position: relative;
    }

    .options-toggle {
      display: inline-grid;
      gap: 4px;
      width: 44px;
      min-height: 44px;
      padding: 10px 9px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.86);
      cursor: pointer;
      box-shadow: var(--shadow);
    }

    .options-toggle span {
      display: block;
      height: 2px;
      background: var(--ink);
      border-radius: 999px;
    }

    .options-toggle::-webkit-details-marker {
      display: none;
    }

    .options-panel {
      position: absolute;
      right: 0;
      top: calc(100% + 10px);
      width: min(340px, 80vw);
      padding: 14px;
      background: rgba(255, 255, 255, 0.96);
      border: 1px solid var(--line);
      border-radius: 10px;
      box-shadow: var(--shadow);
      z-index: 10;
    }

    .options-panel h3 {
      margin-bottom: 8px;
    }

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

    nav button[data-view="demo"] {
      background: #f4b860;
      border-color: #f4b860;
      color: #4b2a00;
      font-weight: 700;
    }

    nav button[data-view="demo"][aria-pressed="true"] {
      background: #d27b0d;
      border-color: #d27b0d;
      color: white;
    }

    .stage,
    .panel,
    .card {
      background: rgba(255, 255, 255, 0.86);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }

    .stage,
    .panel,
    .card {
      box-shadow: none;
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
      gap: 8px;
    }

    .canvas-item {
      border-bottom: 1px solid var(--line);
      padding-bottom: 8px;
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
      header {
        grid-template-columns: 1fr;
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
      <div class="header-tools">
        <details class="options-menu">
          <summary class="options-toggle" aria-label="Opties openen">
            <span></span>
            <span></span>
            <span></span>
          </summary>
          <div class="options-panel">
            <h3>Bronnen</h3>
            <p>Gegenereerd vanuit een workshopcanvas. De interactie is gemockt, maar de bronnotities blijven inspecteerbaar.</p>
            <div class="canvas-list" id="canvas-list"></div>
          </div>
        </details>
      </div>
    </header>

    <nav aria-label="Prototype-onderdelen">
      <button type="button" data-view="overview" aria-pressed="true">Uitdaging</button>
      <button type="button" data-view="risks" aria-pressed="false">Aannames</button>
      <button type="button" data-view="demo" aria-pressed="false">Interactieve Demo</button>
      <button type="button" data-view="evidence" aria-pressed="false">Wat kan er misgaan?</button>
      <button type="button" data-view="next" aria-pressed="false">Next Steps</button>
    </nav>

    <section class="stage">
      <section class="view active" id="overview"></section>
      <section class="view" id="demo"></section>
      <section class="view" id="evidence"></section>
      <section class="view" id="risks"></section>
      <section class="view" id="feedback"></section>
      <section class="view" id="next"></section>
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
        return `<p>Nog geen bronnotities.</p>`;
      }
      return `<ul class="${className}">${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
    }

    function renderShell() {
      el("#eyebrow").textContent = `${model.organisation} · ${model.date || "workshopcanvas"}`;
      el("#title").textContent = model.projectName;

      el("#canvas-list").innerHTML = model.sections.map((section) => `
        <article class="canvas-item">
          <button type="button" data-source="${section.key}">
            <strong>${escapeHtml(section.label)}</strong><br>
            <small>${section.items.length} bronnotities</small>
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
        <h2>Van losse planningsnotities naar een toetsbaar prototype</h2>
        <p>Deze gegenereerde shell vertaalt het KNLTB-canvas naar een klikbaar concept: kies een planningsonderdeel, bekijk een gemockt advies, inspecteer het bewijs en verzamel feedback voordat je een echte app bouwt.</p>
        <div class="metric-row">
          <div class="metric"><span>Canvassecties</span><strong>${model.sections.length}</strong></div>
          <div class="metric"><span>Mockdashboards</span><strong>${model.dashboardCards.length}</strong></div>
          <div class="metric"><span>Fase</span><strong>1</strong></div>
        </div>
        <div class="roadmap">
          <article><h3>Bekijk de uitdaging</h3><p>Gebruik de hoofdknoppen om snel van probleemdefinitie naar aannames en demo te gaan.</p></article>
          <article><h3>Test de demo</h3><p>Kies een dashboardonderdeel en genereer een eerste planningsadvies.</p></article>
          <article><h3>Open bronnen via opties</h3><p>Gebruik de knop met drie lijnen rechtsboven om bronnotities en onderbouwing te bekijken.</p></article>
        </div>
      `;
    }

    function selectedCard() {
      return model.dashboardCards.find((card) => card.id === state.selectedCard) || model.dashboardCards[0];
    }

    function renderDemo() {
      const card = selectedCard();
      el("#demo").innerHTML = `
        <h2>Interactieve Demo</h2>
        <p>Kies een planningsonderdeel en genereer een gemockte eerste output. Dit is bewust statisch, maar concreet genoeg om met gebruikers te bespreken.</p>
        <div class="selector">
          <label for="dashboard-select">Focus van het dashboard</label>
          <select id="dashboard-select">
            ${model.dashboardCards.map((item) => `<option value="${item.id}" ${item.id === card.id ? "selected" : ""}>${escapeHtml(item.title)}</option>`).join("")}
          </select>
        </div>
        <div class="cards">
          ${model.dashboardCards.map((item) => `
            <article class="card ${item.id === card.id ? "selected" : ""}" data-card="${item.id}">
              <h3>${escapeHtml(item.title)}</h3>
              <p>${escapeHtml(item.signal)}</p>
              <div class="score" aria-label="Mock gereedheidsscore"><span style="--score: ${item.mockScore}%"></span></div>
            </article>
          `).join("")}
        </div>
        <div class="output">
          <h3>${escapeHtml(card.question)}</h3>
          <p><strong>Gemockt advies:</strong> ${escapeHtml(card.primaryAction)}</p>
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
        <h2>Wat kan er misgaan?</h2>
        <p>Deze risico's en bewijskaarten laten zien waar het prototype kan stuklopen of waar extra onderbouwing nodig is.</p>
        <div class="selector">
          <label for="evidence-select">Kies een bron voor inspectie</label>
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
        <h2>Aannames</h2>
        <p>Dit zijn de controles die zichtbaar moeten blijven voordat deze shell een functionele app wordt.</p>
        <h3>Kritische aannames</h3>
        ${list(assumptions)}
        <h3>Datakwaliteit</h3>
        ${list(quality)}
        <h3>Ethiek en privacy</h3>
        ${list(privacy)}
      `;
    }

    function renderFeedback() {
      el("#feedback").innerHTML = `
        <h2>Feedback</h2>
        <div class="feedback">
          <p>${escapeHtml(model.feedbackPrompts[0])}</p>
          <div class="feedback-row">
            ${["Nuttig", "Bijna", "Nog niet"].map((item) => `<button type="button" data-feedback="${item}" class="${state.feedback === item ? "selected" : ""}">${item}</button>`).join("")}
          </div>
          <label for="feedback-note">Wat moet er veranderen voordat dit naar een app gaat?</label>
          <textarea id="feedback-note">${escapeHtml(state.note)}</textarea>
          <div class="status">${state.feedback ? `Vastgelegd: ${escapeHtml(state.feedback)}` : ""}</div>
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
        <p>Gebruik de feedback uit deze gegenereerde shell om te bepalen wat straks wel en niet in de root-level Streamlit-app hoort.</p>
        <div class="roadmap">
          <article><h3>Valideer de invoer</h3><p>Maak eerst afspraken over groepen, staf, spelers en banen voordat je koppelingen bouwt.</p></article>
          <article><h3>Test een dashboard met gebruikers</h3><p>Begin met het onderdeel dat de duidelijkste planningswaarde oplevert.</p></article>
          <article><h3>Ga pas daarna naar fase 2</h3><p>Bouw de kleinste werkende versie in <code>app.py</code> zodra het HTML-concept scherp genoeg is.</p></article>
        </div>
        <h3>Tijdlijnnotities</h3>
        ${list(timeline)}
        <h3>Succesmetingen</h3>
        ${list(metrics)}
        <h3>Feedback</h3>
        <div class="feedback">
          <p>${escapeHtml(model.feedbackPrompts[0])}</p>
          <div class="feedback-row">
            ${["Nuttig", "Bijna", "Nog niet"].map((item) => `<button type="button" data-feedback="${item}" class="${state.feedback === item ? "selected" : ""}">${item}</button>`).join("")}
          </div>
          <label for="feedback-note-next">Wat moet er veranderen voordat dit naar een app gaat?</label>
          <textarea id="feedback-note-next">${escapeHtml(state.note)}</textarea>
          <div class="status">${state.feedback ? `Vastgelegd: ${escapeHtml(state.feedback)}` : ""}</div>
        </div>
      `;

      document.querySelectorAll("[data-feedback]").forEach((button) => {
        button.addEventListener("click", () => {
          state.feedback = button.dataset.feedback;
          renderNext();
        });
      });
      el("#feedback-note-next").addEventListener("input", (event) => {
        state.note = event.target.value;
      });
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
