"""
Team DNA — KNVB
Phase 2: Streamlit prototype for opponent analysis.

Pipeline: load data → anonymise → table-to-text → LLM → parse → de-anonymise → report
Real LLM calls require OPENAI_API_KEY in the environment; without it the app runs in demo mode.
"""

from __future__ import annotations

import os
import re
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False


# ── paths ──────────────────────────────────────────────────────────────────
DATA_PATH = Path(__file__).resolve().parent / "example-data" / "knvb_opponents.csv"

# ── constants ──────────────────────────────────────────────────────────────
SECTION_TITLES = [
    "Speelstijlsamenvatting",
    "Sterktes per spelfase",
    "Zwaktes per spelfase",
    "Tactische aandachtspunten",
    "Datalimitaties en aanbevelingen voor aanvullende analyse",
]

UNAVAIL = (
    "Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. "
    "Aanbeveling: aanvullen via video-analyse."
)

DISCLAIMER = (
    "Bevindingen zijn gebaseerd op event data en bedoeld als startpunt voor verdere analyse. "
    "Het professionele oordeel van de scout blijft leidend."
)

# ── system prompt (condensed from agent-docs/PROMPTS.md) ──────────────────
SYSTEM_PROMPT = """Je bent een data-analist die professionele scouts van een nationale voetbalbond ondersteunt bij wedstrijdvoorbereiding.

Je ontvangt geanonimiseerde event data en aggregaatstatistieken van de meest recente wedstrijden van TEAM_A.

Genereer een analyserapport in het Nederlands met precies deze vijf secties, in deze volgorde:
1. Speelstijlsamenvatting
2. Sterktes per spelfase
3. Zwaktes per spelfase
4. Tactische aandachtspunten
5. Datalimitaties en aanbevelingen voor aanvullende analyse

VERPLICHTE REGELS — wijk hier nooit van af:
- Elke claim is herleidbaar naar de aangeleverde data. Gebruik nooit externe kennis over TEAM_A.
- Elke bewering krijgt een bronvermelding: (Bron: YYYY-MM-DD (TEAM_X)[, ...])
- Bij ontbrekende onderbouwing schrijf je exact: "Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse."
- Alle vijf secties zijn altijd aanwezig, ook als ze de onbeschikbaarheidsmelding bevatten.
- Elke sectietitel direct gevolgd door de datadekkingindicator: [Hoog], [Middel] of [Laag].
- Gebruik uitsluitend labels (TEAM_A, TEAM_B, SPELER_01 …) — nooit echte namen.
- Tactische aandachtspunten als observaties ("Uit de data blijkt…"), nooit als adviezen.
- Maximaal 3–5 bevindingen per sectie.

OUTPUTFORMAAT:
## [Sectietitel] [Indicator]

[Bevinding]
(Bron: ...)
"""

# ── embedded mock reports (demo mode — no API key required) ───────────────
_MOCK: dict[str, str] = {
    "Engeland": """\
## Speelstijlsamenvatting [Hoog]

TEAM_A speelt met een hoge pressing in de aanvalsfase: gemiddeld PPDA van 6.2 over de selectie, wat duidt op agressieve druk in de opbouwfase van de tegenstander.
(Bron: 2025-04-04 (TEAM_B), 2025-03-22 (TEAM_C), 2025-03-19 (TEAM_D))

De aanval verloopt primair via de rechterflank: 42% van de aanvallen wordt langs de rechterzijde opgebouwd. De linkerflank is beduidend minder actief (22%).
(Bron: 2025-03-22 (TEAM_C), 2024-11-14 (TEAM_E), 2024-10-10 (TEAM_F), 2024-10-07 (TEAM_G))

Verdedigend hanteert TEAM_A een middelhoog blok bij gelijkstand of voorsprong, en schakelt naar een laag blok bij achterstand. Omschakeling na balwinst is direct en verticaal.
(Bron: 2025-04-04 (TEAM_B), 2024-10-10 (TEAM_F), 2024-10-07 (TEAM_G))

## Sterktes per spelfase [Hoog]

**Aanvallende opbouw**
Sterke rechterflank met frequente overlap: gemiddeld 18 gecombineerde flankacties per wedstrijd. Hoog aankomstpercentage dieptebal rechts (68%).
(Bron: 2025-03-22 (TEAM_C), 2025-03-19 (TEAM_D), 2024-11-14 (TEAM_E))

**Verdedigende organisatie**
Sterk defensief blok in de eigen helft: gemiddeld 4.2 key interceptions per wedstrijd. Effectief in luchtduels bij standaardsituaties (74% gewonnen).
(Bron: 2025-04-04 (TEAM_B), 2025-03-22 (TEAM_C), 2024-10-10 (TEAM_F))

**Standaardsituaties**
Bovengemiddelde doelgevaarcreatie via corners: gemiddeld 2.1 schoten binnen de 16-meter per standaardsituatieserie.
(Bron: 2025-04-04 (TEAM_B), 2024-10-07 (TEAM_G))

## Zwaktes per spelfase [Middel]

*Conclusies zijn indicatief — data gedeeltelijk incompleet voor 2 van 6 wedstrijden.*

**Aanvallende opbouw**
Beperkte variatie via de linkerflank: slechts 22% van de aanvallen. Lage succesrate bij combinaties door het midden (34%).
(Bron: 2025-04-04 (TEAM_B), 2025-03-22 (TEAM_C), 2025-03-19 (TEAM_D), 2024-10-07 (TEAM_G))

**Omschakeling aanval→verdediging**
Verhoogd risico bij hoog balbezit: gemiddeld 2.8 tegenaanvallen toegestaan per wedstrijd wanneer balbezit boven 65%.
(Bron: 2025-04-04 (TEAM_B), 2024-11-14 (TEAM_E), 2024-10-10 (TEAM_F))

## Tactische aandachtspunten [Middel]

*Conclusies zijn indicatief; gebaseerd op patronen uit 4 volledig gedocumenteerde wedstrijden.*

Uit de data blijkt dat TEAM_A kwetsbaar is voor vroeg hoge druk op de linkercentrale verdediger: gemiddeld 3.1 balverliezen per 90 minuten op die positie in de opbouwfase.
(Bron: 2025-03-22 (TEAM_C), 2025-03-19 (TEAM_D), 2024-11-14 (TEAM_E))

Uit de data blijkt dat TEAM_A bij ingooien in de eigen helft regelmatig ruimte biedt achter de verdedigingslinie: 6 van 14 geanalyseerde ingooien resulteerden in een gevaarlijke situatie.
(Bron: 2025-04-04 (TEAM_B), 2024-10-10 (TEAM_F))

## Datalimitaties en aanbevelingen voor aanvullende analyse [Laag]

Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse.

Pressing-statistieken per zone ontbreken voor 2 van 6 wedstrijden. Individuele spelersprestaties zijn niet beschikbaar voor dit rapport.
""",

    "Italië": """\
## Speelstijlsamenvatting [Middel]

*Analyse gebaseerd op 4 beschikbare wedstrijden.*

TEAM_A toont een gedisciplineerde verdedigende basishouding met een compact laag blok. Na balwinst zoekt de ploeg snel de diepte via lange ballen op de aanvallers.
(Bron: 2025-03-26 (TEAM_B), 2025-03-23 (TEAM_C), 2024-11-15 (TEAM_D))

Aanvallend is er een sterke nadruk op balbehoud in de opbouwfase, maar beperkte creativiteit in de laatste linie: gemiddeld 2.8 clear chances per wedstrijd.
(Bron: 2025-03-23 (TEAM_C), 2024-11-15 (TEAM_D), 2024-10-14 (TEAM_E))

## Sterktes per spelfase [Middel]

*Gebaseerd op 3 van 4 wedstrijden; gedeeltelijk incompleet.*

**Verdedigende organisatie**
Sterk georganiseerd laag blok: gemiddeld slechts 1.8 tegenaanvallen toegestaan per wedstrijd. Hoog percentage gewonnen tackles in de defensieve helft (70%).
(Bron: 2025-03-26 (TEAM_B), 2024-11-15 (TEAM_D), 2024-10-14 (TEAM_E))

**Standaardsituaties verdedigend**
Effectief in het verdedigen van corners: slechts 1 tegendoelpunt uit standaardsituaties in de geselecteerde wedstrijden.
(Bron: 2025-03-26 (TEAM_B), 2025-03-23 (TEAM_C))

## Zwaktes per spelfase [Middel]

*Conclusies zijn indicatief op basis van 4 wedstrijden.*

**Aanvallende opbouw**
Beperkte doelgevaarcreatie vanuit lopende aanvallen: gemiddeld 2.8 clear chances per 90 minuten — ondergemiddeld voor WK-kwalificatieniveau.
(Bron: 2025-03-26 (TEAM_B), 2025-03-23 (TEAM_C), 2024-11-15 (TEAM_D))

## Tactische aandachtspunten [Laag]

Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse.

Onvoldoende wedstrijddata beschikbaar voor het identificeren van betrouwbare tactische patronen.

## Datalimitaties en aanbevelingen voor aanvullende analyse [Laag]

Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse.

Slechts 4 wedstrijden beschikbaar. Pressing-statistieken per zone ontbreken geheel. Spelersdata incompleet voor 2 van 4 wedstrijden.
""",

    "Armenië": """\
## Speelstijlsamenvatting [Laag]

*Analyse gebaseerd op slechts 2 wedstrijden — bevindingen zijn speculatief.*

Op basis van de beschikbare data hanteert TEAM_A een defensief georiënteerde basishouding met een laag blok. Aanvallend is de data onvoldoende om betrouwbare patronen te identificeren.
(Bron: 2025-03-23 (TEAM_B), 2025-03-20 (TEAM_C))

## Sterktes per spelfase [Laag]

Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse.

Onvoldoende wedstrijddata (2 wedstrijden) voor het identificeren van sterktes per spelfase.

## Zwaktes per spelfase [Laag]

Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse.

Onvoldoende wedstrijddata (2 wedstrijden) voor het identificeren van zwaktes per spelfase.

## Tactische aandachtspunten [Laag]

Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse.

Onvoldoende data voor het formuleren van betrouwbare tactische aandachtspunten.

## Datalimitaties en aanbevelingen voor aanvullende analyse [Laag]

Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse.

Slechts 2 wedstrijden beschikbaar. Alle event-datatypes zijn incompleet. Video-analyse wordt sterk aanbevolen als aanvulling voor wedstrijdvoorbereiding.
""",
}


# ── data ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_opponents() -> pd.DataFrame:
    if not DATA_PATH.exists():
        return pd.DataFrame(columns=[
            "opponent_name", "match_date", "match_opponent", "competition",
            "result", "possession_pct", "ppda", "right_flank_pct", "left_flank_pct",
            "clear_chances", "interceptions", "tackle_pct",
            "transitions_conceded", "set_piece_shots", "data_complete",
        ])
    df = pd.read_csv(DATA_PATH, parse_dates=["match_date"])
    return df


# ── pipeline ───────────────────────────────────────────────────────────────
def build_mapping(opponent_name: str, matches: pd.DataFrame) -> dict[str, str]:
    """Map real names to anonymous labels. TEAM_A = the opponent being analysed."""
    mapping: dict[str, str] = {opponent_name: "TEAM_A"}
    for i, opp in enumerate(matches["match_opponent"].unique(), start=2):
        mapping[opp] = f"TEAM_{chr(64 + i)}"  # TEAM_B, TEAM_C, …
    return mapping


def table_to_text(matches: pd.DataFrame, mapping: dict[str, str]) -> str:
    """Convert per-match stats to anonymised text for the LLM."""
    n = len(matches)
    n_complete = int(matches["data_complete"].sum())

    def avg(col: str) -> float:
        return matches[col].mean()

    complete_src = f"{n_complete} van {n} volledig gedocumenteerde wedstrijden"

    lines = ["WEDSTRIJDOVERZICHT (bronset voor deze analyse):"]
    for _, row in matches.sort_values("match_date", ascending=False).iterrows():
        anon_opp = mapping.get(row["match_opponent"], row["match_opponent"])
        lines.append(
            f"- {row['match_date'].strftime('%Y-%m-%d')}: TEAM_A – {anon_opp}, "
            f"{row['competition']}, {row['result']}"
        )

    lines += [
        "",
        f"EVENTDATA EN STATISTIEKEN — TEAM_A (geaggregeerd over {n} wedstrijden):",
        "",
        "AANVALLENDE OPBOUW:",
        f"- Gemiddeld balbezit: {avg('possession_pct'):.0f}%  (Bron: alle wedstrijden)",
        f"- Pressing intensiteit PPDA (lager = hogere druk): {avg('ppda'):.1f}  (Bron: alle wedstrijden)",
        f"- Aanvallen via rechterflank: {avg('right_flank_pct'):.0f}%  (Bron: {complete_src})",
        f"- Aanvallen via linkerflank: {avg('left_flank_pct'):.0f}%  (Bron: {complete_src})",
        f"- Clear chances gecreëerd per wedstrijd: {avg('clear_chances'):.1f}  (Bron: alle wedstrijden)",
        "",
        "VERDEDIGENDE ORGANISATIE:",
        f"- Key interceptions per wedstrijd: {avg('interceptions'):.1f}  (Bron: alle wedstrijden)",
        f"- Tackle succespercentage defensieve helft: {avg('tackle_pct'):.0f}%  (Bron: alle wedstrijden)",
        f"- Tegenaanvallen toegestaan per wedstrijd: {avg('transitions_conceded'):.1f}  (Bron: alle wedstrijden)",
        "",
        "STANDAARDSITUATIES:",
        f"- Schoten per standaardsituatieserie: {avg('set_piece_shots'):.1f}  (Bron: {complete_src})",
        "",
        "DATADEKKING:",
        f"- Volledig gedocumenteerde wedstrijden: {n_complete} van {n}",
    ]

    if n_complete < n:
        missing = n - n_complete
        lines.append(
            f"- Ontbrekende data: flankaanval-details en zone-pressing statistieken "
            f"ontbreken voor {missing} wedstrijd{'en' if missing > 1 else ''}"
        )

    return "\n".join(lines)


def call_llm(opponent_name: str, data_text: str) -> str:
    """Return LLM-generated report text, or an embedded mock when no API key is set."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if _OPENAI_AVAILABLE and api_key:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": data_text},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    return _MOCK.get(opponent_name, _MOCK["Engeland"])


def parse_sections(raw: str, mapping: dict[str, str]) -> list[dict]:
    """Parse LLM output into sections and reverse-anonymise names."""
    reverse = {label: real for real, label in mapping.items()}

    # De-anonymise
    text = raw
    for label, real in reverse.items():
        text = text.replace(label, real)

    parts = re.split(r"^## ", text, flags=re.MULTILINE)

    # Parse failure guard: return all sections as unavailable
    if len(parts) <= 1:
        return [
            {"title": t, "indicator": "Laag", "body": UNAVAIL, "unavailable": True}
            for t in SECTION_TITLES
        ]

    sections: list[dict] = []
    for part in parts[1:]:
        lines = part.strip().split("\n")
        header = lines[0]
        m = re.match(r"^(.+?)\s+\[(Hoog|Middel|Laag)\]", header)
        title = m.group(1).strip() if m else header.strip()
        indicator = m.group(2) if m else "Laag"
        body = "\n".join(lines[1:]).strip()
        sections.append({
            "title": title,
            "indicator": indicator,
            "body": body,
            "unavailable": UNAVAIL.split(".")[0] in body,
        })

    # Inject unavailability placeholder for any missing required section
    present = {s["title"] for s in sections}
    for required in SECTION_TITLES:
        if not any(required in p for p in present):
            sections.append({
                "title": required,
                "indicator": "Laag",
                "body": UNAVAIL,
                "unavailable": True,
            })

    return sections


# ── HTML export ────────────────────────────────────────────────────────────
def build_report_html(
    opponent: str,
    matches: pd.DataFrame,
    sections: list[dict],
    generated_at: datetime,
) -> str:
    date_str = generated_at.strftime("%d %B %Y")
    iso_date = generated_at.strftime("%Y-%m-%d")

    badge_style = {
        "Hoog":   "background:#d4edda;color:#155724;border:1px solid #c3e6cb",
        "Middel": "background:#fff3cd;color:#856404;border:1px solid #ffeaa7",
        "Laag":   "background:#f8d7da;color:#721c24;border:1px solid #f5c6cb",
    }

    match_rows = "".join(
        f"<tr>"
        f"<td>{row['match_date'].strftime('%d %b %Y')}</td>"
        f"<td>{opponent} – {row['match_opponent']}</td>"
        f"<td>{row['competition']}</td>"
        f"<td>{row['result']}</td>"
        f"</tr>"
        for _, row in matches.sort_values("match_date", ascending=False).iterrows()
    )

    sections_html = ""
    for sec in sections:
        ind = sec["indicator"]
        badge = (
            f'<span style="display:inline-block;border-radius:999px;padding:2px 10px;'
            f'font-size:0.76rem;font-weight:600;{badge_style.get(ind, badge_style["Laag"])}">'
            f'{ind}</span>'
        )
        if sec["unavailable"]:
            body_html = (
                f'<p style="color:#721c24;font-style:italic;margin:0">{UNAVAIL}</p>'
            )
            extra = sec["body"].replace(UNAVAIL, "").strip()
            if extra:
                body_html += f'<p style="color:#6c757d;font-size:0.83rem;margin:8px 0 0">{extra}</p>'
            disclaimer_html = ""
        else:
            safe_body = sec["body"].replace("\n", "<br>")
            body_html = f'<div style="font-size:0.93rem;line-height:1.55">{safe_body}</div>'
            disclaimer_html = (
                f'<p style="font-size:0.78rem;color:#6c757d;font-style:italic;'
                f'border-top:1px solid #dee2e6;margin-top:12px;padding-top:8px 0 0">'
                f'{DISCLAIMER}</p>'
            )

        sections_html += f"""
        <div style="background:#fff;border:1px solid #dee2e6;border-radius:8px;margin-bottom:14px;overflow:hidden">
          <div style="padding:14px 18px 12px;border-bottom:1px solid #dee2e6;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap">
            <strong style="font-size:1rem;flex:1">{sec['title']}</strong>
            {badge}
          </div>
          <div style="padding:16px 18px">{body_html}{disclaimer_html}</div>
        </div>"""

    return f"""<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <title>Team DNA — {opponent}</title>
  <style>
    body {{font-family:Georgia,serif;color:#17211d;background:#f7f4ec;margin:0;padding:32px 40px;max-width:900px}}
    table {{width:100%;border-collapse:collapse;font-size:0.88rem}}
    td,th {{padding:7px 10px;border-bottom:1px solid #dee2e6;text-align:left}}
    th {{background:#f1eee6;font-weight:600}}
    @media print {{body{{background:#fff;padding:16px}}}}
  </style>
</head>
<body>
  <p style="font-size:0.82rem;color:#6c757d;margin-bottom:4px">Team DNA · Koninklijke Nederlandse Voetbalbond</p>
  <h1 style="font-size:2.2rem;margin:0 0 6px">{opponent}</h1>
  <p style="font-size:0.84rem;color:#6c757d;margin:0 0 20px">
    Gegenereerd op {date_str} · {len(matches)} wedstrijden geanalyseerd
  </p>

  <div style="background:#fff;border:1px solid #dee2e6;border-radius:8px;padding:14px 18px;margin-bottom:20px">
    <strong style="font-size:0.74rem;text-transform:uppercase;letter-spacing:.4px;color:#6c757d">Datadekking per sectie</strong>
    <div style="margin-top:8px;font-size:0.86rem;display:flex;gap:20px;flex-wrap:wrap">
      <span>🟢 <strong>Hoog</strong> — voldoende data voor een onderbouwde uitspraak</span>
      <span>🟡 <strong>Middel</strong> — beperkte data; conclusies zijn indicatief</span>
      <span>🔴 <strong>Laag</strong> — onvoldoende data; bevindingen zijn speculatief of ontbreken</span>
    </div>
  </div>

  <div style="background:#fff;border:1px solid #dee2e6;border-radius:8px;margin-bottom:14px;overflow:hidden">
    <div style="padding:14px 18px 12px;border-bottom:1px solid #dee2e6">
      <strong>Wedstrijdoverzicht</strong>
    </div>
    <div style="padding:16px 18px">
      <table>
        <tr><th>Datum</th><th>Wedstrijd</th><th>Competitie</th><th>Uitslag</th></tr>
        {match_rows}
      </table>
    </div>
  </div>

  {sections_html}

  <p style="font-size:0.78rem;color:#6c757d;margin-top:24px">
    TeamDNA_{opponent}_{iso_date} · Team DNA — Koninklijke Nederlandse Voetbalbond
  </p>
</body>
</html>"""


# ── indicator helpers ──────────────────────────────────────────────────────
_ICON = {"Hoog": "🟢", "Middel": "🟡", "Laag": "🔴"}


# ── screens ────────────────────────────────────────────────────────────────
def screen_select(df: pd.DataFrame) -> None:
    opponents = sorted(df["opponent_name"].unique().tolist()) if not df.empty else []

    col_form, col_info = st.columns([1, 1.6], gap="large")

    with col_form:
        opponent = st.selectbox("Tegenstander", ["— kies een team —"] + opponents)

        if opponent != "— kies een team —":
            n = len(df[df["opponent_name"] == opponent])
            complete = int(df[df["opponent_name"] == opponent]["data_complete"].sum())
            st.caption(f"{n} wedstrijden beschikbaar · {complete} volledig gedocumenteerd")

        go = st.button(
            "Start analyse →",
            type="primary",
            disabled=(opponent == "— kies een team —"),
        )

        demo_mode = not _OPENAI_AVAILABLE or not os.environ.get("OPENAI_API_KEY")
        if demo_mode:
            st.info(
                "**Demo modus** — geen `OPENAI_API_KEY` geconfigureerd. "
                "De app gebruikt vooraf gegenereerde voorbeelddata. "
                "Voeg de variabele toe aan je omgeving om de echte LLM in te schakelen.",
                icon="ℹ️",
            )

    with col_info:
        if opponent != "— kies een team —" and not df.empty:
            preview = (
                df[df["opponent_name"] == opponent]
                .sort_values("match_date", ascending=False)
                .assign(Datum=lambda d: d["match_date"].dt.strftime("%d %b %Y"))
                .rename(columns={
                    "match_opponent": "Tegenstander",
                    "competition": "Competitie",
                    "result": "Uitslag",
                })[["Datum", "Tegenstander", "Competitie", "Uitslag"]]
            )
            st.dataframe(preview, use_container_width=True, hide_index=True)
        else:
            st.markdown(
                "Selecteer een tegenstander om de analysepipeline te starten. "
                "Het systeem haalt automatisch de meest recente wedstrijden op, "
                "anonimiseert de data en genereert een gestructureerd rapport op basis van de event data."
            )

    if go and opponent != "— kies een team —":
        matches = df[df["opponent_name"] == opponent].copy().sort_values(
            "match_date", ascending=False
        )
        with st.status("Analyse wordt gegenereerd…", expanded=True) as status:
            st.write("Bezig met ophalen van data…")
            time.sleep(0.5)

            st.write("Bezig met verwerken & anonimiseren…")
            mapping = build_mapping(opponent, matches)
            data_text = table_to_text(matches, mapping)
            time.sleep(0.5)

            st.write("Rapport wordt gegenereerd…")
            raw = call_llm(opponent, data_text)
            time.sleep(0.4)

            st.write("Rapport gereed.")
            status.update(label="Rapport gereed ✓", state="complete")
            time.sleep(0.6)

        st.session_state.report = {
            "opponent": opponent,
            "matches": matches,
            "sections": parse_sections(raw, mapping),
            "generated_at": datetime.now(),
        }
        st.session_state.stage = "report"
        st.rerun()


def screen_report() -> None:
    r = st.session_state.report
    opponent: str = r["opponent"]
    matches: pd.DataFrame = r["matches"]
    sections: list[dict] = r["sections"]
    generated_at: datetime = r["generated_at"]

    html_bytes = build_report_html(opponent, matches, sections, generated_at).encode()
    filename = f"TeamDNA_{opponent}_{generated_at.strftime('%Y-%m-%d')}.html"

    # Top bar
    col_title, col_actions = st.columns([3, 1])
    with col_title:
        st.title(opponent)
        st.caption(
            f"Team DNA — KNVB · Gegenereerd op {generated_at.strftime('%d %B %Y')} "
            f"· {len(matches)} wedstrijden geanalyseerd"
        )
    with col_actions:
        st.download_button(
            "Exporteer rapport",
            data=html_bytes,
            file_name=filename,
            mime="text/html",
            type="primary",
            help="Download als HTML. Open in browser → Afdrukken → PDF om te exporteren.",
            key="export_top",
        )
        if st.button("← Nieuwe analyse", key="back_top"):
            st.session_state.stage = "select"
            st.session_state.report = None
            st.rerun()

    # Legend
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown("🟢 **Hoog** — voldoende data voor een onderbouwde uitspraak")
        c2.markdown("🟡 **Middel** — beperkte data; conclusies zijn indicatief")
        c3.markdown("🔴 **Laag** — onvoldoende data; bevindingen zijn speculatief of ontbreken")

    # Wedstrijdoverzicht
    with st.container(border=True):
        st.markdown("**Wedstrijdoverzicht** 🟢 Hoog")
        display = matches.assign(
            Datum=matches["match_date"].dt.strftime("%d %b %Y")
        ).rename(columns={
            "match_opponent": "Tegenstander",
            "competition": "Competitie",
            "result": "Uitslag",
        })[["Datum", "Tegenstander", "Competitie", "Uitslag"]]
        st.dataframe(display, use_container_width=True, hide_index=True)
        st.caption("Dit overzicht toont de bronset die door de hele analysepipeline is gebruikt.")

    # Report sections
    for sec in sections:
        icon = _ICON.get(sec["indicator"], "🔴")
        with st.container(border=True):
            st.markdown(f"**{sec['title']}** {icon} {sec['indicator']}")
            if sec["unavailable"]:
                st.warning(UNAVAIL, icon="⚠️")
                extra = sec["body"].replace(UNAVAIL, "").strip()
                if extra:
                    st.caption(extra)
            else:
                st.markdown(sec["body"])
                st.caption(f"*{DISCLAIMER}*")

    # Footer
    st.divider()
    col_footer, col_btn = st.columns([3, 1])
    col_footer.caption(
        f"TeamDNA_{opponent}_{generated_at.strftime('%Y-%m-%d')} · "
        "Team DNA — Koninklijke Nederlandse Voetbalbond"
    )
    col_btn.download_button(
        "Exporteer rapport",
        data=html_bytes,
        file_name=filename,
        mime="text/html",
        help="Download als HTML. Open in browser → Afdrukken → PDF om te exporteren.",
        key="export_bottom",
    )


# ── entry point ────────────────────────────────────────────────────────────
def main() -> None:
    st.set_page_config(
        page_title="Team DNA — KNVB",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    if "stage" not in st.session_state:
        st.session_state.stage = "select"
    if "report" not in st.session_state:
        st.session_state.report = None

    st.markdown(
        "<p style='color:#5e6a63;font-size:0.88rem;margin-bottom:0'>Team DNA · Koninklijke Nederlandse Voetbalbond</p>",
        unsafe_allow_html=True,
    )

    df = load_opponents()

    if st.session_state.stage == "select":
        st.header("Tegenstander analyse")
        screen_select(df)
    elif st.session_state.stage == "report" and st.session_state.report:
        screen_report()
    else:
        st.session_state.stage = "select"
        st.rerun()


if __name__ == "__main__":
    main()
