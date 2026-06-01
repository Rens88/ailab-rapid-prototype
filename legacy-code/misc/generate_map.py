#!/usr/bin/env python3
"""Generate lean standalone trip idea and itinerary tools from CSV data."""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
from datetime import date, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_DIR = ROOT / "dist"

COMMITMENTS = {"booked", "intended", "wish"}
TRAVEL_ROLES = {"start", "stop-over", "end"}
TRAVEL_TYPES = {"flight", "train", "bus", "ferry", "car"}
DATE_FMT = "%Y-%m-%d"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required CSV file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path} must include a header row.")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def require_text(row: dict[str, str], field: str, *, context: str) -> str:
    value = row.get(field, "").strip()
    if not value:
        raise ValueError(f"{context} requires '{field}'.")
    return value


def optional_text(row: dict[str, str], field: str) -> str:
    return row.get(field, "").strip()


def parse_float(row: dict[str, str], field: str, *, context: str) -> float:
    value = require_text(row, field, context=context)
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{context} field '{field}' must be numeric.") from error
    return number


def parse_optional_int(row: dict[str, str], field: str, *, context: str) -> int | None:
    value = optional_text(row, field)
    if not value:
        return None
    return parse_positive_int(value, context=f"{context} field '{field}'")


def parse_required_int(row: dict[str, str], field: str, *, context: str) -> int:
    return parse_positive_int(require_text(row, field, context=context), context=f"{context} field '{field}'")


def parse_positive_int(value: str, *, context: str) -> int:
    try:
        number = int(float(value))
    except ValueError as error:
        raise ValueError(f"{context} must be a positive integer.") from error
    if number < 1:
        raise ValueError(f"{context} must be a positive integer.")
    return number


def parse_date_value(value: str, *, context: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{context} must be an ISO date in YYYY-MM-DD format.") from error


def split_pipe(value: str) -> list[str]:
    return [part.strip() for part in value.split("|") if part.strip()]


def parse_lat_lon(lat: float, lon: float, *, context: str) -> None:
    if not -90 <= lat <= 90:
        raise ValueError(f"{context} latitude is out of range: {lat}")
    if not -180 <= lon <= 180:
        raise ValueError(f"{context} longitude is out of range: {lon}")


def parse_path(value: str, *, context: str) -> list[dict[str, Any]]:
    if not value:
        return []
    points: list[dict[str, Any]] = []
    for index, raw_point in enumerate(split_pipe(value), start=1):
        label = ""
        coords = raw_point
        if "@" in raw_point:
            label, coords = raw_point.rsplit("@", 1)
            label = label.strip()
        if "," not in coords:
            raise ValueError(f"{context} path point {index} must look like Label@lat,lon.")
        raw_lat, raw_lon = [part.strip() for part in coords.split(",", 1)]
        try:
            lat = float(raw_lat)
            lon = float(raw_lon)
        except ValueError as error:
            raise ValueError(f"{context} path point {index} must contain numeric lat/lon.") from error
        parse_lat_lon(lat, lon, context=f"{context} path point {index}")
        points.append({"label": label, "lat": lat, "lon": lon})
    return points


def sanitize_notes(value: str) -> str:
    """Allow a tiny HTML subset while keeping CSV notes safe for sharing."""
    escaped = html.escape(value, quote=False)
    allowed = ("b", "strong", "i", "em", "br", "p", "ul", "ol", "li")
    for tag in allowed:
        escaped = escaped.replace(f"&lt;{tag}&gt;", f"<{tag}>")
        escaped = escaped.replace(f"&lt;/{tag}&gt;", f"</{tag}>")
        escaped = escaped.replace(f"&lt;{tag}/&gt;", f"<{tag}>")
        escaped = escaped.replace(f"&lt;{tag} /&gt;", f"<{tag}>")
    return escaped.replace("\n", "<br>")


def normalize_idea(row: dict[str, str], *, index: int) -> dict[str, Any]:
    context = f"ideas.csv row {index}"
    idea_id = require_text(row, "id", context=context)
    title = require_text(row, "title", context=context)
    commitment = require_text(row, "commitment", context=context).lower()
    if commitment not in COMMITMENTS:
        raise ValueError(f"{context} commitment must be one of: {', '.join(sorted(COMMITMENTS))}.")

    primary_tag = require_text(row, "primary_tag", context=context).lower()
    tags = [primary_tag]
    for tag in split_pipe(optional_text(row, "tags")):
        normalized_tag = tag.lower()
        if normalized_tag not in tags:
            tags.append(normalized_tag)

    lat = parse_float(row, "lat", context=context)
    lon = parse_float(row, "lon", context=context)
    parse_lat_lon(lat, lon, context=context)

    min_duration = parse_optional_int(row, "min_duration_days", context=context)
    duration = parse_optional_int(row, "duration_days", context=context)
    people = split_pipe(optional_text(row, "people"))
    notes = optional_text(row, "notes")

    idea: dict[str, Any] = {
        "id": idea_id,
        "title": title,
        "commitment": commitment,
        "primary_tag": primary_tag,
        "tags": tags,
        "lat": lat,
        "lon": lon,
        "min_duration_days": min_duration,
        "duration_days": duration or min_duration or 1,
        "people": people,
        "notes": notes,
        "notes_html": sanitize_notes(notes),
    }

    if primary_tag != "travel":
        return idea

    role = require_text(row, "travel_role", context=context).lower()
    if role not in TRAVEL_ROLES:
        raise ValueError(f"{context} travel_role must be one of: {', '.join(sorted(TRAVEL_ROLES))}.")
    travel_type = require_text(row, "travel_type", context=context).lower()
    if travel_type not in TRAVEL_TYPES:
        raise ValueError(f"{context} travel_type must be one of: {', '.join(sorted(TRAVEL_TYPES))}.")

    idea.update(
        {
            "travel_role": role,
            "travel_type": travel_type,
            "from_label": require_text(row, "from_label", context=context),
            "via_labels": split_pipe(optional_text(row, "via_labels")),
            "to_label": require_text(row, "to_label", context=context),
            "travel_path": parse_path(optional_text(row, "travel_path"), context=context),
        }
    )
    return idea


def normalize_itinerary(row: dict[str, str], *, index: int) -> dict[str, Any]:
    context = f"itineraries.csv row {index}"
    start_date = parse_date_value(require_text(row, "start_date", context=context), context=context)
    end_date_text = optional_text(row, "end_date")
    end_date = parse_date_value(end_date_text, context=context) if end_date_text else None
    duration_days = parse_optional_int(row, "duration_days", context=context)
    if end_date is None and duration_days is None:
        raise ValueError(f"{context} requires either 'end_date' or 'duration_days'.")
    if end_date is not None and end_date < start_date:
        raise ValueError(f"{context} end_date must be on or after start_date.")

    return {
        "id": require_text(row, "id", context=context),
        "name": require_text(row, "name", context=context),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat() if end_date else "",
        "duration_days": duration_days,
        "summary": optional_text(row, "summary"),
        "items": [],
    }


def normalize_trip(data_dir: Path) -> dict[str, Any]:
    meta_rows = read_csv_rows(data_dir / "trip.csv")
    meta = meta_rows[0] if meta_rows else {}

    ideas: list[dict[str, Any]] = []
    idea_lookup: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(read_csv_rows(data_dir / "ideas.csv"), start=2):
        idea = normalize_idea(row, index=index)
        if idea["id"] in idea_lookup:
            raise ValueError(f"Duplicate idea id '{idea['id']}'.")
        ideas.append(idea)
        idea_lookup[idea["id"]] = idea

    itineraries: list[dict[str, Any]] = []
    itinerary_lookup: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(read_csv_rows(data_dir / "itineraries.csv"), start=2):
        itinerary = normalize_itinerary(row, index=index)
        if itinerary["id"] in itinerary_lookup:
            raise ValueError(f"Duplicate itinerary id '{itinerary['id']}'.")
        itineraries.append(itinerary)
        itinerary_lookup[itinerary["id"]] = itinerary

    seen_orders: set[tuple[str, int]] = set()
    for index, row in enumerate(read_csv_rows(data_dir / "itinerary_items.csv"), start=2):
        context = f"itinerary_items.csv row {index}"
        itinerary_id = require_text(row, "itinerary_id", context=context)
        if itinerary_id not in itinerary_lookup:
            raise ValueError(f"{context} references unknown itinerary '{itinerary_id}'.")
        idea_id = require_text(row, "idea_id", context=context)
        if idea_id not in idea_lookup:
            raise ValueError(f"{context} references unknown idea '{idea_id}'.")
        item_order = parse_required_int(row, "item_order", context=context)
        key = (itinerary_id, item_order)
        if key in seen_orders:
            raise ValueError(f"{context} duplicates item_order {item_order} in itinerary '{itinerary_id}'.")
        seen_orders.add(key)

        duration = parse_required_int(row, "duration_days", context=context)
        idea = idea_lookup[idea_id]
        minimum = idea.get("min_duration_days")
        if minimum and duration < minimum:
            raise ValueError(f"{context} duration is shorter than the idea minimum duration.")
        itinerary_lookup[itinerary_id]["items"].append(
            {
                "order": item_order,
                "idea_id": idea_id,
                "duration_days": duration,
                "note": optional_text(row, "note"),
            }
        )

    for itinerary in itineraries:
        itinerary["items"].sort(key=lambda item: item["order"])
        validate_itinerary(itinerary, idea_lookup)
        attach_dates(itinerary)

    return {
        "title": meta.get("title") or "Trip planner",
        "subtitle": meta.get("subtitle") or "",
        "description": meta.get("description") or "",
        "ideas": ideas,
        "itineraries": itineraries,
    }


def validate_itinerary(itinerary: dict[str, Any], idea_lookup: dict[str, dict[str, Any]]) -> None:
    context = f"itinerary '{itinerary['id']}'"
    items = itinerary["items"]
    if len(items) < 2:
        raise ValueError(f"{context} must include at least a start travel idea and an end travel idea.")

    ideas = [idea_lookup[item["idea_id"]] for item in items]
    first = ideas[0]
    last = ideas[-1]
    if first["primary_tag"] != "travel" or first.get("travel_role") != "start":
        raise ValueError(f"{context} must start with a travel idea whose travel_role is 'start'.")
    if last["primary_tag"] != "travel" or last.get("travel_role") != "end":
        raise ValueError(f"{context} must end with a travel idea whose travel_role is 'end'.")
    for idea in ideas[1:-1]:
        if idea["primary_tag"] == "travel" and idea.get("travel_role") != "stop-over":
            raise ValueError(f"{context} can only use stop-over travel ideas between start and end.")

    total_days = sum(item["duration_days"] for item in items)
    max_days = itinerary.get("duration_days")
    if itinerary.get("end_date"):
        start = parse_date_value(itinerary["start_date"], context=context)
        end = parse_date_value(itinerary["end_date"], context=context)
        date_limit = (end - start).days + 1
        max_days = min(max_days, date_limit) if max_days else date_limit
    if max_days and total_days > max_days:
        raise ValueError(f"{context} uses {total_days} days, which exceeds its {max_days}-day limit.")
    itinerary["total_days"] = total_days


def attach_dates(itinerary: dict[str, Any]) -> None:
    cursor = parse_date_value(itinerary["start_date"], context=f"itinerary '{itinerary['id']}'")
    for item in itinerary["items"]:
        start = cursor
        end = cursor + timedelta(days=item["duration_days"] - 1)
        item["start_date"] = start.isoformat()
        item["end_date"] = end.isoformat()
        cursor = end + timedelta(days=1)


def render_html(trip: dict[str, Any], *, mode: str) -> str:
    data = json.dumps(trip, ensure_ascii=True, indent=2)
    title = html.escape(trip["title"], quote=True)
    subtitle = html.escape(trip["subtitle"], quote=True)
    app_title = f"{title} - {mode.title()}"
    template = HTML_TEMPLATE
    template = template.replace("__APP_TITLE__", app_title)
    template = template.replace("__TRIP_JSON__", data)
    template = template.replace("__MODE__", mode)
    return template


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate lean trip viewer and constructor HTML files.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="Folder containing trip.csv and data CSV files.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Folder for generated HTML files.")
    args = parser.parse_args()

    trip = normalize_trip(args.data_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    viewer_path = args.output_dir / "viewer.html"
    constructor_path = args.output_dir / "constructor.html"
    viewer_path.write_text(render_html(trip, mode="viewer"), encoding="utf-8")
    constructor_path.write_text(render_html(trip, mode="constructor"), encoding="utf-8")
    print(f"Wrote {viewer_path}")
    print(f"Wrote {constructor_path}")


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__APP_TITLE__</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f4ef;
      --panel: #fffdf8;
      --ink: #1f2a25;
      --muted: #647067;
      --line: #d8d2c6;
      --accent: #0b6b5d;
      --accent-2: #c45528;
      --travel: #245b9d;
      --wish: #8a6f28;
      --booked: #0b6b5d;
      --shadow: 0 16px 44px rgba(35, 42, 36, 0.13);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: "Aptos", "Segoe UI", sans-serif;
      line-height: 1.4;
    }
    button, input, select, textarea {
      font: inherit;
    }
    button {
      border: 1px solid var(--line);
      background: var(--panel);
      color: var(--ink);
      border-radius: 7px;
      padding: 0.58rem 0.8rem;
      cursor: pointer;
    }
    button:hover { border-color: var(--accent); }
    button.primary {
      background: var(--accent);
      border-color: var(--accent);
      color: white;
    }
    button:disabled {
      opacity: 0.45;
      cursor: not-allowed;
    }
    header.app-header {
      padding: 1rem clamp(1rem, 3vw, 2rem);
      border-bottom: 1px solid var(--line);
      background: rgba(255, 253, 248, 0.88);
      position: sticky;
      top: 0;
      z-index: 900;
      backdrop-filter: blur(12px);
      transition: padding 160ms ease;
    }
    header.app-header.is-collapsed {
      padding-top: 0.45rem;
      padding-bottom: 0.45rem;
    }
    .header-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }
    .header-title {
      min-width: 0;
    }
    h1, h2, h3, p { margin-top: 0; }
    h1 {
      margin-bottom: 0.15rem;
      font-size: clamp(1.35rem, 4vw, 2rem);
      letter-spacing: 0;
      transition: font-size 160ms ease;
    }
    .app-header.is-collapsed h1 {
      font-size: 1rem;
      margin-bottom: 0;
    }
    .subtitle {
      margin: 0;
      color: var(--muted);
      font-size: 0.95rem;
    }
    .app-header.is-collapsed .subtitle {
      display: none;
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
      justify-content: flex-end;
    }
    .header-toggle {
      width: 2.25rem;
      height: 2.25rem;
      padding: 0;
      display: inline-grid;
      place-items: center;
      font-weight: 800;
    }
    .tabs {
      display: flex;
      gap: 0.35rem;
      flex-wrap: wrap;
    }
    .tabs button[aria-pressed="true"] {
      background: var(--ink);
      border-color: var(--ink);
      color: white;
    }
    .sub-tabs {
      margin: 0 0 0.75rem;
    }
    main {
      padding: clamp(0.75rem, 2vw, 1.25rem);
    }
    .view { display: none; }
    .view.active { display: block; }
    .viewer-controls {
      display: flex;
      gap: 0.6rem;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 0.75rem;
    }
    .viewer-controls select {
      min-height: 2.45rem;
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 0.5rem;
      background: white;
      color: var(--ink);
      min-width: min(100%, 22rem);
    }
    .split {
      display: grid;
      grid-template-columns: minmax(300px, 390px) minmax(0, 1fr);
      min-height: calc(100vh - 110px);
      gap: 1rem;
    }
    .split.overview-hidden {
      grid-template-columns: 1fr;
    }
    .split.overview-hidden .overview-panel {
      display: none;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      min-width: 0;
    }
    .sidebar {
      padding: 1rem;
      overflow: auto;
      max-height: calc(100vh - 130px);
    }
    .map {
      min-height: calc(100vh - 130px);
      border-radius: 8px;
      overflow: hidden;
    }
    .toolbar {
      display: flex;
      gap: 0.5rem;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 0.75rem;
    }
    .toolbar select, .toolbar input {
      min-height: 2.45rem;
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 0.5rem;
      background: white;
      color: var(--ink);
    }
    .idea-card, .timeline-item {
      border: 1px solid var(--line);
      border-left: 5px solid var(--idea-color, var(--line));
      border-radius: 8px;
      padding: 0.75rem;
      background: white;
      margin-bottom: 0.65rem;
    }
    .idea-card.is-selected {
      border-color: var(--accent);
      box-shadow: inset 0 0 0 1px var(--accent);
    }
    .idea-card[role="button"] {
      cursor: pointer;
    }
    .idea-card[role="button"]:focus {
      outline: 3px solid rgba(11, 107, 93, 0.28);
      outline-offset: 2px;
    }
    .idea-card h3, .timeline-item h3 {
      margin-bottom: 0.25rem;
      font-size: 1rem;
    }
    .meta {
      color: var(--muted);
      font-size: 0.86rem;
      margin-bottom: 0.4rem;
    }
    .pills {
      display: flex;
      gap: 0.35rem;
      flex-wrap: wrap;
      margin: 0.45rem 0;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      background: #ebe4d5;
      color: #3e453f;
      padding: 0.16rem 0.5rem;
      font-size: 0.78rem;
    }
    .pill.booked { background: #d8ede5; color: #134d42; }
    .pill.intended { background: #dbe7f4; color: #234d78; }
    .pill.wish { background: #f3e4bc; color: #705317; }
    .notes {
      color: #38433c;
      font-size: 0.92rem;
      margin: 0.35rem 0 0;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 0.5rem;
      margin-bottom: 0.75rem;
    }
    .stat {
      background: #efe9dc;
      border-radius: 8px;
      padding: 0.65rem;
    }
    .stat span {
      display: block;
      color: var(--muted);
      font-size: 0.76rem;
    }
    .stat strong { font-size: 1.05rem; }
    .timeline {
      display: grid;
      gap: 0.55rem;
    }
    .timeline-item {
      display: grid;
      grid-template-columns: 4.8rem minmax(0, 1fr);
      gap: 0.75rem;
      align-items: start;
    }
    .timeline-date {
      color: var(--accent);
      font-weight: 700;
      font-size: 0.86rem;
    }
    .item-controls {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      flex-wrap: nowrap;
      margin-top: 0.45rem;
    }
    .duration-inline {
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      white-space: nowrap;
      color: var(--muted);
      font-weight: 700;
    }
    .duration-inline input {
      width: 3.2rem;
      min-height: 2rem;
      padding: 0.25rem 0.35rem;
      text-align: center;
    }
    .icon-button {
      width: 2rem;
      height: 2rem;
      display: inline-grid;
      place-items: center;
      padding: 0;
      font-weight: 800;
      line-height: 1;
    }
    .day-timeline {
      display: grid;
      grid-template-columns: 7.4rem minmax(0, 1fr);
      gap: 1rem;
      padding: clamp(0.75rem, 2vw, 1.2rem);
      overflow-x: auto;
    }
    .day-axis, .day-lanes {
      display: grid;
      grid-auto-rows: 34px;
    }
    .day-axis {
      border-right: 1px solid var(--line);
      padding-right: 0.75rem;
    }
    .day-tick {
      color: var(--muted);
      font-weight: 700;
      font-size: 0.82rem;
      border-top: 1px solid rgba(100, 112, 103, 0.18);
      padding-top: 0.35rem;
      white-space: nowrap;
    }
    .day-tick.weekend {
      color: #a23616;
    }
    .day-lanes {
      position: relative;
      min-width: 540px;
    }
    .day-lanes::before {
      content: "";
      position: absolute;
      inset: 0 auto 0 0;
      width: 3px;
      background: #bfc8d3;
      border-radius: 999px;
    }
    .timeline-block {
      margin-left: 1.25rem;
      border-left: 6px solid var(--idea-color, var(--accent));
      border-radius: 7px;
      padding: 0.65rem 0.8rem;
      background: var(--idea-soft, #dfe8f2);
      box-shadow: inset 0 0 0 1px rgba(36, 91, 157, 0.08);
      overflow: hidden;
    }
    .timeline-block.travel {
      background: var(--idea-soft, #e5e7eb);
      border-left-color: var(--idea-color, var(--travel));
    }
    .timeline-block h3 {
      margin: 0 0 0.25rem;
      font-size: 1rem;
    }
    .timeline-block .duration {
      float: right;
      color: #98420e;
      font-weight: 800;
      margin-left: 0.5rem;
    }
    .empty-state {
      padding: 1rem;
      color: var(--muted);
    }
    .builder-mode {
      display: none;
    }
    .builder-mode.active {
      display: block;
    }
    .popup-add-form {
      display: grid;
      gap: 0.45rem;
      margin-top: 0.65rem;
    }
    .popup-add-form label {
      margin: 0;
    }
    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0.6rem;
    }
    label {
      display: grid;
      gap: 0.25rem;
      color: var(--muted);
      font-size: 0.83rem;
      margin-bottom: 0.6rem;
    }
    input, select, textarea {
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 0.55rem;
      background: white;
      color: var(--ink);
      min-width: 0;
    }
    textarea {
      min-height: 6rem;
      resize: vertical;
    }
    .export-box {
      width: 100%;
      min-height: 9rem;
      font-family: "Cascadia Mono", Consolas, monospace;
      font-size: 0.78rem;
      white-space: pre;
    }
    .marker-dot {
      width: 1.2rem;
      height: 1.2rem;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: white;
      background: var(--accent);
      border: 2px solid white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.25);
      font-size: 0.65rem;
      font-weight: 700;
    }
    .marker-dot.travel { background: var(--travel); }
    .marker-dot.unused { background: #9a958b; }
    .hidden { display: none !important; }
    @media (max-width: 820px) {
      .header-row { align-items: flex-start; flex-direction: column; }
      .header-actions { justify-content: flex-start; }
      .app-header.is-collapsed .header-row {
        flex-direction: row;
        align-items: center;
      }
      .split { grid-template-columns: 1fr; }
      .sidebar { max-height: none; }
      .map { min-height: 58vh; }
      .stats { grid-template-columns: 1fr; }
      .timeline-item { grid-template-columns: 1fr; }
      .form-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header class="app-header" id="appHeader">
    <div class="header-row">
      <div class="header-title">
        <h1 id="appTitle"></h1>
        <p class="subtitle" id="appSubtitle"></p>
      </div>
      <div class="header-actions">
        <nav class="tabs" id="tabs"></nav>
        <button class="header-toggle" id="headerToggle" type="button" aria-label="Collapse header" title="Collapse header">^</button>
      </div>
    </div>
  </header>
  <main id="app"></main>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const MODE = "__MODE__";
    const SEED = __TRIP_JSON__;
    const storageKey = "clean-trip-constructor-v1";
    const headerStorageKey = "clean-trip-header-collapsed-v1";
    const clone = (value) => JSON.parse(JSON.stringify(value));
    let state = loadState();
    let maps = {};
    let layers = {};
    let routeRenderVersions = {};
    let routeCache = new Map();
    let viewerMarkers = new Map();
    let constructorIdeaMarkers = new Map();
    let pendingLatLng = null;
    let pendingMarker = null;

    const $ = (selector, root = document) => root.querySelector(selector);
    const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
    const escapeHTML = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[char]));
    const fmtDate = (value) => value ? new Date(value + "T00:00:00").toLocaleDateString(undefined, { month: "short", day: "numeric" }) : "";
    const isTravel = (idea) => idea?.primary_tag === "travel";
    const ideaById = (id) => state.ideas.find((idea) => idea.id === id);
    const itineraryById = (id) => state.itineraries.find((itinerary) => itinerary.id === id);
    const splitPipe = (value) => String(value || "").split("|").map((part) => part.trim()).filter(Boolean);
    const tagPalette = {
      travel: "#245b9d",
      city: "#2563eb",
      friends: "#2f6ab3",
      nature: "#16845b",
      tramping: "#15803d",
      beach: "#0e7490",
      mountains: "#6d4fc2",
      sightseeing: "#b45309",
      family: "#c2410c",
      food: "#be123c",
      camping: "#5f6f52"
    };

    boot();

    function boot() {
      $("#appTitle").textContent = SEED.title || "Trip planner";
      $("#appSubtitle").textContent = SEED.subtitle || "";
      initializeHeaderToggle();
      if (MODE === "constructor") {
        renderConstructorShell();
      } else {
        renderViewerShell();
      }
    }

    function initializeHeaderToggle() {
      const collapsed = localStorage.getItem(headerStorageKey) === "true";
      setHeaderCollapsed(collapsed);
      $("#headerToggle").addEventListener("click", () => {
        setHeaderCollapsed(!$("#appHeader").classList.contains("is-collapsed"));
        localStorage.setItem(headerStorageKey, String($("#appHeader").classList.contains("is-collapsed")));
        setTimeout(() => Object.values(maps).forEach((map) => map.invalidateSize()), 180);
      });
    }

    function setHeaderCollapsed(collapsed) {
      $("#appHeader").classList.toggle("is-collapsed", collapsed);
      const toggle = $("#headerToggle");
      toggle.textContent = collapsed ? "v" : "^";
      toggle.setAttribute("aria-label", collapsed ? "Expand header" : "Collapse header");
      toggle.title = collapsed ? "Expand header" : "Collapse header";
    }

    function loadState() {
      if (MODE !== "constructor") {
        return clone(SEED);
      }
      try {
        const stored = JSON.parse(localStorage.getItem(storageKey) || "");
        if (stored?.ideas?.length && stored?.itineraries) {
          return stored;
        }
      } catch (error) {
        console.warn("No saved constructor state", error);
      }
      return clone(SEED);
    }

    function saveState() {
      if (MODE === "constructor") {
        localStorage.setItem(storageKey, JSON.stringify(state));
      }
    }

    function renderViewerShell() {
      $("#tabs").innerHTML = `
        <button type="button" data-view="map" aria-pressed="true">Map</button>
        <button type="button" data-view="timeline" aria-pressed="false">Timeline</button>
      `;
      $("#app").innerHTML = `
        <div class="viewer-controls">
          <select id="viewerItinerarySelect"></select>
          <button class="map-only-control" type="button" id="toggleOverviewButton">Hide overview</button>
          <label class="map-only-control"><input id="showUnusedIdeas" type="checkbox"> Show unused ideas</label>
        </div>
        <section class="view active" id="mapView">
          <div class="split" id="viewerMapLayout">
            <aside class="panel sidebar overview-panel" id="viewerOverview"></aside>
            <div class="panel map" id="viewerMap"></div>
          </div>
        </section>
        <section class="view" id="timelineView">
          <div class="panel" id="viewerTimeline"></div>
        </section>
      `;
      bindTabs();
      initMap("viewerMap");
      renderViewerOptions();
      renderViewer();
      syncViewerControls();
      $("#viewerItinerarySelect").addEventListener("change", renderViewer);
      $("#showUnusedIdeas").addEventListener("change", renderViewer);
      $("#toggleOverviewButton").addEventListener("click", toggleOverview);
    }

    function renderConstructorShell() {
      $("#tabs").innerHTML = `
        <button type="button" data-view="ideas" aria-pressed="true">Ideas</button>
        <button type="button" data-view="itinerary" aria-pressed="false">Itinerary</button>
        <button type="button" data-view="export" aria-pressed="false">Export</button>
      `;
      $("#app").innerHTML = `
        <section class="view active" id="ideasView">
          <div class="split">
            <aside class="panel sidebar">
              <form id="ideaForm">
                <div class="form-grid">
                  <label>Title<input name="title" required></label>
                  <label>Commitment<select name="commitment"><option>intended</option><option>booked</option><option>wish</option></select></label>
                  <label>Main tag<input name="primary_tag" required placeholder="tramping"></label>
                  <label>Extra tags<input name="tags" placeholder="friends|camping"></label>
                  <label>Latitude<input name="lat" type="number" step="any" required></label>
                  <label>Longitude<input name="lon" type="number" step="any" required></label>
                  <label>Minimum days<input name="min_duration_days" type="number" min="1"></label>
                  <label>Default days<input name="duration_days" type="number" min="1"></label>
                </div>
                <label>People<input name="people" placeholder="Anika|Jess"></label>
                <label>Notes<textarea name="notes"></textarea></label>
                <details>
                  <summary>Travel fields</summary>
                  <div class="form-grid">
                    <label>Role<select name="travel_role"><option value=""></option><option>start</option><option>stop-over</option><option>end</option></select></label>
                    <label>Type<select name="travel_type"><option value=""></option><option>flight</option><option>train</option><option>bus</option><option>ferry</option><option>car</option></select></label>
                    <label>From<input name="from_label"></label>
                    <label>To<input name="to_label"></label>
                  </div>
                  <label>Via labels<input name="via_labels" placeholder="Singapore|Auckland"></label>
                  <label>Path<input name="travel_path" placeholder="AMS@52.3105,4.7683|SIN@1.3644,103.9915"></label>
                </details>
                <div class="toolbar">
                  <button class="primary" type="submit">Save idea</button>
                  <button id="useCurrentLatLng" type="button">Use current lon/lat</button>
                </div>
              </form>
              <div id="constructorIdeasList"></div>
            </aside>
            <div class="panel map" id="constructorIdeasMap"></div>
          </div>
        </section>
        <section class="view" id="itineraryView">
          <div class="tabs sub-tabs" id="builderViewTabs">
            <button type="button" data-builder-view="map" aria-pressed="true">Map</button>
            <button type="button" data-builder-view="timeline" aria-pressed="false">Timeline</button>
          </div>
          <div class="builder-mode active" id="builderMapMode">
            <div class="split">
              <aside class="panel sidebar">
                <div class="toolbar">
                  <select id="builderItinerarySelect"></select>
                  <button id="newItineraryButton" type="button">New itinerary</button>
                </div>
                <form id="itineraryForm">
                  <label>Name<input name="name" required></label>
                  <div class="form-grid">
                    <label>Start date<input name="start_date" type="date" required></label>
                    <label>Duration days<input name="duration_days" type="number" min="1"></label>
                  </div>
                  <label>End date<input name="end_date" type="date"></label>
                  <button class="primary" type="submit">Save itinerary</button>
                </form>
                <div class="stats" id="builderStats"></div>
                <div class="timeline" id="builderTimeline"></div>
              </aside>
              <div class="panel map" id="builderMap"></div>
            </div>
          </div>
          <div class="builder-mode" id="builderTimelineMode">
            <div class="panel" id="builderDayTimeline"></div>
          </div>
        </section>
        <section class="view" id="exportView">
          <div class="split">
            <aside class="panel sidebar">
              <h2>CSV export</h2>
              <p class="meta">These are the three source files for the generator.</p>
              <button class="primary" id="refreshExport" type="button">Refresh export</button>
            </aside>
            <div class="panel sidebar">
              <label>ideas.csv<textarea class="export-box" id="ideasCsv" readonly></textarea></label>
              <label>itineraries.csv<textarea class="export-box" id="itinerariesCsv" readonly></textarea></label>
              <label>itinerary_items.csv<textarea class="export-box" id="itemsCsv" readonly></textarea></label>
            </div>
          </div>
        </section>
      `;
      bindTabs();
      initMap("constructorIdeasMap", { click: handleConstructorMapClick });
      initMap("builderMap");
      $("#ideaForm").addEventListener("submit", saveIdeaFromForm);
      $("#useCurrentLatLng").addEventListener("click", usePendingLatLng);
      $("#newItineraryButton").addEventListener("click", createItinerary);
      $("#builderItinerarySelect").addEventListener("change", renderItineraryBuilder);
      $("#itineraryForm").addEventListener("submit", saveItineraryFromForm);
      $("#refreshExport").addEventListener("click", renderExports);
      bindBuilderViewTabs();
      renderConstructorIdeas();
      renderItineraryBuilder();
      renderExports();
    }

    function bindTabs() {
      $$("#tabs button").forEach((button) => {
        button.addEventListener("click", () => {
          $$("#tabs button").forEach((entry) => entry.setAttribute("aria-pressed", String(entry === button)));
          $$(".view").forEach((view) => view.classList.remove("active"));
          const target = $("#" + button.dataset.view + "View");
          if (target) target.classList.add("active");
          syncViewerControls();
          setTimeout(() => Object.values(maps).forEach((map) => map.invalidateSize()), 80);
        });
      });
    }

    function bindBuilderViewTabs() {
      $$("#builderViewTabs button").forEach((button) => {
        button.addEventListener("click", () => {
          $$("#builderViewTabs button").forEach((entry) => entry.setAttribute("aria-pressed", String(entry === button)));
          $$(".builder-mode").forEach((view) => view.classList.remove("active"));
          const target = $("#builder" + capitalize(button.dataset.builderView) + "Mode");
          if (target) target.classList.add("active");
          setTimeout(() => maps.builderMap?.invalidateSize(), 80);
        });
      });
    }

    function capitalize(value) {
      return String(value || "").slice(0, 1).toUpperCase() + String(value || "").slice(1);
    }

    function syncViewerControls() {
      if (MODE !== "viewer") {
        return;
      }
      const activeView = $("#tabs button[aria-pressed='true']")?.dataset.view || "map";
      $$(".map-only-control").forEach((element) => {
        element.hidden = activeView !== "map";
      });
    }

    function initMap(id, options = {}) {
      const el = $("#" + id);
      if (!el || maps[id]) return maps[id];
      const map = L.map(id, { scrollWheelZoom: true }).setView([-41.2, 172.8], 5);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: "&copy; OpenStreetMap"
      }).addTo(map);
      if (options.click) map.on("click", options.click);
      maps[id] = map;
      layers[id] = L.layerGroup().addTo(map);
      return map;
    }

    function renderViewerOptions() {
      const options = [`<option value="">No itinerary - all ideas</option>`]
        .concat(state.itineraries.map((itinerary) => `<option value="${escapeHTML(itinerary.id)}">${escapeHTML(itinerary.name)}</option>`));
      $("#viewerItinerarySelect").innerHTML = options.join("");
    }

    function selectedViewerItinerary() {
      const id = $("#viewerItinerarySelect")?.value || "";
      return id ? itineraryById(id) : null;
    }

    function renderViewer() {
      const itinerary = selectedViewerItinerary();
      renderViewerOverview(itinerary);
      renderViewerMap(itinerary);
      renderViewerTimeline(itinerary);
    }

    function toggleOverview() {
      const layout = $("#viewerMapLayout");
      const hidden = !layout.classList.contains("overview-hidden");
      layout.classList.toggle("overview-hidden", hidden);
      $("#toggleOverviewButton").textContent = hidden ? "Show overview" : "Hide overview";
      setTimeout(() => maps.viewerMap?.invalidateSize(), 80);
    }

    function renderViewerOverview(itinerary) {
      const panel = $("#viewerOverview");
      if (!itinerary) {
        panel.innerHTML = `
          <div class="stats">${simpleStatsHTML(state.ideas)}</div>
          ${state.ideas.map((idea) => ideaCard(idea)).join("")}
        `;
        return;
      }
      const items = itineraryItems(itinerary);
      const usedIds = new Set(items.map((item) => item.idea.id));
      const unused = $("#showUnusedIdeas")?.checked ? state.ideas.filter((idea) => !usedIds.has(idea.id)) : [];
      panel.innerHTML = `
        <h2>${escapeHTML(itinerary.name)}</h2>
        <div class="stats">${statsHTML(itinerary, items)}</div>
        ${items.map((item) => ideaCard(item.idea, { selected: true, focusable: true })).join("")}
        ${unused.length ? `<h3>Not included</h3>${unused.map((idea) => ideaCard(idea, { focusable: true })).join("")}` : ""}
      `;
      bindOverviewFocusLinks();
    }

    function renderViewerMap(itinerary) {
      if (!itinerary) {
        drawIdeasMap("viewerMap", state.ideas);
        return;
      }
      const items = itineraryItems(itinerary);
      const usedIds = new Set(items.map((item) => item.idea.id));
      const unused = $("#showUnusedIdeas")?.checked ? state.ideas.filter((idea) => !usedIds.has(idea.id)) : [];
      drawItineraryMap("viewerMap", items, unused);
    }

    function renderViewerTimeline(itinerary) {
      const timeline = $("#viewerTimeline");
      if (!itinerary) {
        timeline.innerHTML = `<div class="empty-state">Select an itinerary to see the day-by-day timeline.</div>`;
        return;
      }
      timeline.innerHTML = renderDayTimeline(itinerary, itineraryItems(itinerary));
    }

    function ideaCard(idea, options = {}) {
      const selected = options.selected ? " is-selected" : "";
      const action = options.action ? `<div class="toolbar">${options.action}</div>` : "";
      const focusAttrs = options.focusable ? ` role="button" tabindex="0" data-focus-idea="${escapeHTML(idea.id)}"` : "";
      const style = ideaStyle(idea);
      return `
        <article class="idea-card${selected}" style="${style}"${focusAttrs}>
          <h3>${escapeHTML(idea.title)}</h3>
          <div class="meta">${escapeHTML(locationText(idea))}</div>
          <div class="pills">
            <span class="pill ${escapeHTML(idea.commitment)}">${escapeHTML(idea.commitment)}</span>
            <span class="pill">${escapeHTML(idea.primary_tag)}</span>
            ${isTravel(idea) ? `<span class="pill">${escapeHTML(idea.travel_type)} ${escapeHTML(idea.travel_role)}</span>` : ""}
          </div>
          ${idea.people?.length ? `<div class="meta">Meet: ${escapeHTML(idea.people.join(", "))}</div>` : ""}
          ${idea.notes_html ? `<p class="notes">${idea.notes_html}</p>` : ""}
          ${action}
        </article>
      `;
    }

    function ideaStyle(idea) {
      const color = tagColor(idea);
      return `--idea-color: ${color}; --idea-soft: ${softColor(color)};`;
    }

    function tagColor(ideaOrTag) {
      const tag = typeof ideaOrTag === "string"
        ? ideaOrTag
        : String(ideaOrTag?.primary_tag || ideaOrTag?.tags?.[0] || "").trim().toLowerCase();
      if (tagPalette[tag]) {
        return tagPalette[tag];
      }
      let hash = 0;
      for (const char of tag || "idea") {
        hash = ((hash << 5) - hash + char.charCodeAt(0)) | 0;
      }
      const hue = Math.abs(hash) % 360;
      return hslToHex(hue, 56, 38);
    }

    function softColor(hex) {
      const { r, g, b } = hexToRgb(hex);
      return `rgba(${r}, ${g}, ${b}, 0.14)`;
    }

    function hexToRgb(hex) {
      const normalized = String(hex || "#64748b").replace("#", "");
      const value = parseInt(normalized.length === 3
        ? normalized.split("").map((part) => part + part).join("")
        : normalized, 16);
      return {
        r: (value >> 16) & 255,
        g: (value >> 8) & 255,
        b: value & 255
      };
    }

    function hslToHex(h, s, l) {
      s /= 100;
      l /= 100;
      const k = (n) => (n + h / 30) % 12;
      const a = s * Math.min(l, 1 - l);
      const f = (n) => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
      return `#${[f(0), f(8), f(4)].map((value) => Math.round(255 * value).toString(16).padStart(2, "0")).join("")}`;
    }

    function bindOverviewFocusLinks() {
      $$("[data-focus-idea]", $("#viewerOverview")).forEach((card) => {
        const focus = () => focusViewerIdea(card.dataset.focusIdea);
        card.addEventListener("click", focus);
        card.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            focus();
          }
        });
      });
    }

    function focusViewerIdea(ideaId) {
      const marker = viewerMarkers.get(ideaId);
      const idea = ideaById(ideaId);
      const map = maps.viewerMap;
      if (!marker || !idea || !map) {
        return;
      }
      map.flyTo([idea.lat, idea.lon], Math.max(map.getZoom(), 10), { duration: 0.65 });
      marker.openPopup();
    }

    function locationText(idea) {
      if (isTravel(idea)) {
        const via = idea.via_labels?.length ? ` via ${idea.via_labels.join(", ")}` : "";
        return `${idea.from_label || ""} to ${idea.to_label || ""}${via}`;
      }
      return `${Number(idea.lat).toFixed(4)}, ${Number(idea.lon).toFixed(4)}`;
    }

    function itineraryItems(itinerary) {
      return [...(itinerary.items || [])]
        .sort((a, b) => Number(a.order) - Number(b.order))
        .map((item) => ({ ...item, idea: ideaById(item.idea_id) }))
        .filter((item) => item.idea);
    }

    function statsHTML(itinerary, items) {
      const totalDays = items.reduce((sum, item) => sum + Number(item.duration_days || 1), 0);
      const km = estimateKm(items);
      return `
        <div class="stat"><span>Days</span><strong>${totalDays}</strong></div>
        <div class="stat"><span>All km</span><strong>${Math.round(km.all)}</strong></div>
        <div class="stat"><span>Stop km</span><strong>${Math.round(km.stops)}</strong></div>
      `;
    }

    function simpleStatsHTML(ideas) {
      const travelCount = ideas.filter(isTravel).length;
      return `
        <div class="stat"><span>Ideas</span><strong>${ideas.length}</strong></div>
        <div class="stat"><span>Stops</span><strong>${ideas.length - travelCount}</strong></div>
        <div class="stat"><span>Travel</span><strong>${travelCount}</strong></div>
      `;
    }

    function renderDayTimeline(itinerary, items) {
      if (!items.length) {
        return `<div class="empty-state">This itinerary has no items yet.</div>`;
      }
      const start = parseLocalDate(itinerary.start_date);
      const lastItemEnd = items[items.length - 1]?.end_date;
      const durationEnd = itinerary.duration_days ? formatLocalDate(addDays(start, Number(itinerary.duration_days) - 1)) : "";
      const end = parseLocalDate(itinerary.end_date || durationEnd || lastItemEnd || itinerary.start_date);
      const dayCount = Math.max(1, daysBetween(start, end) + 1);
      const rowStyle = `grid-template-rows: repeat(${dayCount}, 34px)`;
      const ticks = Array.from({ length: dayCount }, (_, index) => {
        const day = addDays(start, index);
        const weekend = day.getDay() === 0 || day.getDay() === 6 ? " weekend" : "";
        return `<div class="day-tick${weekend}">${escapeHTML(dayLabel(day))}</div>`;
      }).join("");
      const blocks = items.map((item, index) => {
        const idea = item.idea;
        const itemStart = parseLocalDate(item.start_date);
        const itemEnd = parseLocalDate(item.end_date);
        const startLine = daysBetween(start, itemStart) + 1;
        const endLine = daysBetween(start, itemEnd) + 2;
        const classes = `timeline-block${isTravel(idea) ? " travel" : ""}`;
        return `
          <article class="${classes}" style="grid-row: ${startLine} / ${endLine}; ${ideaStyle(idea)}">
            <span class="duration">${Number(item.duration_days || 1)} day${Number(item.duration_days || 1) === 1 ? "" : "s"}</span>
            <h3>${index + 1}. ${escapeHTML(idea.title)}</h3>
            <div class="pills">
              <span class="pill ${escapeHTML(idea.commitment)}">${escapeHTML(idea.commitment)}</span>
              <span class="pill">${escapeHTML(idea.primary_tag)}</span>
              ${isTravel(idea) ? `<span class="pill">${escapeHTML(idea.travel_type)} ${escapeHTML(idea.travel_role)}</span>` : ""}
            </div>
            ${idea.people?.length ? `<div class="meta">Meet: ${escapeHTML(idea.people.join(", "))}</div>` : ""}
            ${item.note ? `<p class="notes">${escapeHTML(item.note)}</p>` : ""}
            ${idea.notes_html ? `<p class="notes">${idea.notes_html}</p>` : ""}
          </article>
        `;
      }).join("");
      return `
        <div class="day-timeline">
          <div class="day-axis" style="${rowStyle}">${ticks}</div>
          <div class="day-lanes" style="${rowStyle}">${blocks}</div>
        </div>
      `;
    }

    function parseLocalDate(value) {
      const [year, month, day] = String(value || "").split("-").map(Number);
      return new Date(year, month - 1, day);
    }

    function addDays(value, days) {
      const next = new Date(value);
      next.setDate(next.getDate() + days);
      return next;
    }

    function formatLocalDate(value) {
      const year = value.getFullYear();
      const month = String(value.getMonth() + 1).padStart(2, "0");
      const day = String(value.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    }

    function daysBetween(start, end) {
      const ms = Date.UTC(end.getFullYear(), end.getMonth(), end.getDate())
        - Date.UTC(start.getFullYear(), start.getMonth(), start.getDate());
      return Math.round(ms / 86400000);
    }

    function dayLabel(day) {
      return day.toLocaleDateString(undefined, { month: "short", day: "2-digit", weekday: "short" });
    }

    function drawIdeasMap(mapId, ideas) {
      const map = maps[mapId];
      const layer = layers[mapId];
      if (!map || !layer) return;
      routeRenderVersions[mapId] = (routeRenderVersions[mapId] || 0) + 1;
      if (mapId === "viewerMap") {
        viewerMarkers = new Map();
      }
      if (mapId === "constructorIdeasMap") {
        constructorIdeaMarkers = new Map();
      }
      layer.clearLayers();
      const bounds = [];
      ideas.forEach((idea) => {
        const marker = addIdeaMarker(layer, idea, { popup: ideaCard(idea) });
        if (mapId === "viewerMap") {
          viewerMarkers.set(idea.id, marker);
        }
        if (mapId === "constructorIdeasMap") {
          constructorIdeaMarkers.set(idea.id, marker);
        }
        bounds.push([idea.lat, idea.lon]);
        addTravelPath(layer, idea);
      });
      fitBounds(map, bounds);
    }

    function drawItineraryMap(mapId, items, unused = []) {
      const map = maps[mapId];
      const layer = layers[mapId];
      if (!map || !layer) return;
      if (mapId === "viewerMap") {
        viewerMarkers = new Map();
      }
      layer.clearLayers();
      const bounds = [];
      items.forEach((item, index) => {
        const idea = item.idea;
        const marker = addIdeaMarker(layer, idea, { order: index + 1, popup: ideaCard(idea, { selected: true }) });
        if (mapId === "viewerMap") {
          viewerMarkers.set(idea.id, marker);
        }
        bounds.push([idea.lat, idea.lon]);
        addTravelPath(layer, idea);
      });
      drawItineraryRoutes(mapId, layer, items);
      unused.forEach((idea) => {
        const marker = addIdeaMarker(layer, idea, { unused: true, popup: ideaCard(idea) });
        if (mapId === "viewerMap") {
          viewerMarkers.set(idea.id, marker);
        }
        bounds.push([idea.lat, idea.lon]);
        addTravelPath(layer, idea);
      });
      fitBounds(map, itineraryTravelFocusBounds(items) || bounds);
    }

    function itineraryTravelFocusBounds(items) {
      if (!items.length) {
        return null;
      }
      const firstTravel = items.find((item) => isTravel(item.idea) && item.idea.travel_role === "start")?.idea;
      const lastTravel = [...items].reverse().find((item) => isTravel(item.idea) && item.idea.travel_role === "end")?.idea;
      const points = [];
      travelFocusPoint(firstTravel, "to").forEach((point) => points.push(point));
      travelFocusPoint(lastTravel, "from").forEach((point) => points.push(point));
      return points.length >= 2 ? points : null;
    }

    function travelFocusPoint(idea, endpoint) {
      if (!idea || !isTravel(idea)) {
        return [];
      }
      const path = Array.isArray(idea.travel_path) ? idea.travel_path : [];
      if (path.length) {
        const point = endpoint === "to" ? path[path.length - 1] : path[0];
        return [[point.lat, point.lon]];
      }
      return [[idea.lat, idea.lon]];
    }

    function drawItineraryRoutes(mapId, layer, items) {
      const version = (routeRenderVersions[mapId] || 0) + 1;
      routeRenderVersions[mapId] = version;
      for (let index = 0; index < items.length - 1; index += 1) {
        const from = items[index].idea;
        const to = items[index + 1].idea;
        if (!from || !to || isTravel(from) || isTravel(to)) {
          continue;
        }
        drawRoadRoute(mapId, layer, from, to, version);
      }
    }

    function drawRoadRoute(mapId, layer, from, to, version) {
      const fallback = L.polyline([[from.lat, from.lon], [to.lat, to.lon]], {
        color: tagColor(from),
        weight: 3,
        opacity: 0.45,
        dashArray: "5 7"
      }).addTo(layer);
      routeLatLngs(from, to)
        .then((latLngs) => {
          if (routeRenderVersions[mapId] !== version) {
            return;
          }
          layer.removeLayer(fallback);
          L.polyline(latLngs, {
            color: tagColor(from),
            weight: 4,
            opacity: 0.78
          }).addTo(layer);
        })
        .catch(() => {});
    }

    async function routeLatLngs(from, to) {
      const key = `${from.lon},${from.lat};${to.lon},${to.lat}`;
      if (routeCache.has(key)) {
        return routeCache.get(key);
      }
      const url = `https://router.project-osrm.org/route/v1/driving/${key}?overview=full&geometries=geojson`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Route request failed: ${response.status}`);
      }
      const data = await response.json();
      const coordinates = data?.routes?.[0]?.geometry?.coordinates;
      if (!Array.isArray(coordinates) || coordinates.length < 2) {
        throw new Error("Route response did not include a line.");
      }
      const latLngs = coordinates.map(([lon, lat]) => [lat, lon]);
      routeCache.set(key, latLngs);
      return latLngs;
    }

    function addIdeaMarker(layer, idea, options = {}) {
      const className = `marker-dot ${isTravel(idea) ? "travel" : ""} ${options.unused ? "unused" : ""}`;
      const label = options.order ? String(options.order) : (isTravel(idea) ? "T" : "");
      const marker = L.marker([idea.lat, idea.lon], {
        icon: L.divIcon({ className: "", html: `<span class="${className}" style="background: ${tagColor(idea)}">${escapeHTML(label)}</span>`, iconSize: [24, 24], iconAnchor: [12, 12] })
      }).addTo(layer);
      if (options.popup) marker.bindPopup(options.popup, { maxWidth: 320 });
      return marker;
    }

    function addTravelPath(layer, idea) {
      if (!isTravel(idea) || !idea.travel_path?.length) return;
      const points = idea.travel_path.map((point) => [point.lat, point.lon]);
      if (points.length > 1) {
        L.polyline(points, { color: tagColor(idea), weight: 3, dashArray: "7 8", opacity: 0.8 }).addTo(layer);
      }
    }

    function fitBounds(map, points) {
      if (!points.length) return;
      map.fitBounds(L.latLngBounds(points), { padding: [26, 26], maxZoom: 10 });
    }

    function estimateKm(items) {
      let all = 0;
      let stops = 0;
      for (let index = 0; index < items.length - 1; index += 1) {
        all += distanceKm(items[index].idea, items[index + 1].idea);
      }
      items.forEach((item) => {
        if (isTravel(item.idea) && item.idea.travel_path?.length > 1) {
          all += pathKm(item.idea.travel_path);
        }
      });
      const stopIdeas = items.map((item) => item.idea).filter((idea) => !isTravel(idea));
      for (let index = 0; index < stopIdeas.length - 1; index += 1) {
        stops += distanceKm(stopIdeas[index], stopIdeas[index + 1]);
      }
      return { all, stops };
    }

    function pathKm(points) {
      let total = 0;
      for (let index = 0; index < points.length - 1; index += 1) {
        total += haversine(points[index].lat, points[index].lon, points[index + 1].lat, points[index + 1].lon);
      }
      return total;
    }

    function distanceKm(a, b) {
      return haversine(a.lat, a.lon, b.lat, b.lon);
    }

    function haversine(lat1, lon1, lat2, lon2) {
      const rad = Math.PI / 180;
      const dLat = (lat2 - lat1) * rad;
      const dLon = (lon2 - lon1) * rad;
      const s1 = Math.sin(dLat / 2);
      const s2 = Math.sin(dLon / 2);
      const a = s1 * s1 + Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * s2 * s2;
      return 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    }

    function renderConstructorIdeas() {
      $("#constructorIdeasList").innerHTML = state.ideas.map((idea) => ideaCard(idea, { focusable: true })).join("");
      drawIdeasMap("constructorIdeasMap", state.ideas);
      bindConstructorIdeaFocusLinks();
    }

    function bindConstructorIdeaFocusLinks() {
      $$("[data-focus-idea]", $("#constructorIdeasList")).forEach((card) => {
        const focus = () => focusConstructorIdea(card.dataset.focusIdea);
        card.addEventListener("click", focus);
        card.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            focus();
          }
        });
      });
    }

    function focusConstructorIdea(ideaId) {
      const marker = constructorIdeaMarkers.get(ideaId);
      const idea = ideaById(ideaId);
      const map = maps.constructorIdeasMap;
      if (!marker || !idea || !map) {
        return;
      }
      map.flyTo([idea.lat, idea.lon], Math.max(map.getZoom(), 10), { duration: 0.65 });
      marker.openPopup();
    }

    function handleConstructorMapClick(event) {
      pendingLatLng = event.latlng;
      if (pendingMarker) {
        pendingMarker.remove();
      }
      pendingMarker = L.circleMarker(pendingLatLng, { radius: 9, color: "#c45528", weight: 3, fillOpacity: 0.2 }).addTo(maps.constructorIdeasMap);
    }

    function usePendingLatLng() {
      if (!pendingLatLng) return;
      const form = $("#ideaForm");
      form.elements.lat.value = pendingLatLng.lat.toFixed(6);
      form.elements.lon.value = pendingLatLng.lng.toFixed(6);
    }

    function saveIdeaFromForm(event) {
      event.preventDefault();
      const form = event.currentTarget;
      const title = form.elements.title.value.trim();
      const primaryTag = form.elements.primary_tag.value.trim().toLowerCase();
      const lat = Number(form.elements.lat.value);
      const lon = Number(form.elements.lon.value);
      if (!Number.isFinite(lat) || !Number.isFinite(lon) || lat < -90 || lat > 90 || lon < -180 || lon > 180) {
        alert("Every idea needs a valid latitude and longitude.");
        return;
      }
      if (primaryTag === "travel") {
        const hasTravelFields = form.elements.travel_role.value
          && form.elements.travel_type.value
          && form.elements.from_label.value.trim()
          && form.elements.to_label.value.trim();
        if (!hasTravelFields) {
          alert("Travel ideas need role, type, from, and to.");
          return;
        }
      }
      const idea = {
        id: slug(title),
        title,
        commitment: form.elements.commitment.value,
        primary_tag: primaryTag,
        tags: [primaryTag, ...splitPipe(form.elements.tags.value).map((tag) => tag.toLowerCase())].filter((value, index, arr) => value && arr.indexOf(value) === index),
        lat,
        lon,
        min_duration_days: numberOrNull(form.elements.min_duration_days.value),
        duration_days: numberOrNull(form.elements.duration_days.value) || numberOrNull(form.elements.min_duration_days.value) || 1,
        people: splitPipe(form.elements.people.value),
        notes: form.elements.notes.value.trim(),
        notes_html: escapeHTML(form.elements.notes.value.trim()).replace(/\n/g, "<br>")
      };
      if (primaryTag === "travel") {
        Object.assign(idea, {
          travel_role: form.elements.travel_role.value,
          travel_type: form.elements.travel_type.value,
          from_label: form.elements.from_label.value.trim(),
          via_labels: splitPipe(form.elements.via_labels.value),
          to_label: form.elements.to_label.value.trim(),
          travel_path: parsePathInput(form.elements.travel_path.value)
        });
      }
      const existing = state.ideas.findIndex((entry) => entry.id === idea.id);
      if (existing >= 0) {
        state.ideas[existing] = idea;
      } else {
        state.ideas.push(idea);
      }
      saveState();
      form.reset();
      renderConstructorIdeas();
      renderItineraryBuilder();
      renderExports();
    }

    function parsePathInput(value) {
      return splitPipe(value).map((raw) => {
        const [labelPart, coordsPart = labelPart] = raw.includes("@") ? raw.split("@") : ["", raw];
        const [lat, lon] = coordsPart.split(",").map(Number);
        return { label: labelPart.trim(), lat, lon };
      }).filter((point) => Number.isFinite(point.lat) && Number.isFinite(point.lon));
    }

    function createItinerary() {
      const id = `itinerary-${Date.now().toString(36)}`;
      state.itineraries.push({ id, name: "New itinerary", start_date: new Date().toISOString().slice(0, 10), end_date: "", duration_days: 14, summary: "", items: [] });
      saveState();
      renderItineraryBuilder(id);
    }

    function renderItineraryBuilder(preferredId = null, options = {}) {
      const select = $("#builderItinerarySelect");
      select.innerHTML = state.itineraries.map((itinerary) => `<option value="${escapeHTML(itinerary.id)}">${escapeHTML(itinerary.name)}</option>`).join("");
      if (preferredId) select.value = preferredId;
      const itinerary = itineraryById(select.value) || state.itineraries[0];
      if (!itinerary) return;
      select.value = itinerary.id;
      const form = $("#itineraryForm");
      form.elements.name.value = itinerary.name || "";
      form.elements.start_date.value = itinerary.start_date || "";
      form.elements.duration_days.value = itinerary.duration_days || "";
      form.elements.end_date.value = itinerary.end_date || "";
      const items = itineraryItems(itinerary);
      $("#builderStats").innerHTML = statsHTML(itinerary, items);
      $("#builderTimeline").innerHTML = items.map((item, index) => builderTimelineItemHTML(itinerary, item, index)).join("");
      $("#builderDayTimeline").innerHTML = renderDayTimeline(itinerary, items);
      drawBuilderMap(itinerary, items, options);
    }

    function saveItineraryFromForm(event) {
      event.preventDefault();
      const itinerary = itineraryById($("#builderItinerarySelect").value);
      if (!itinerary) return;
      const form = event.currentTarget;
      itinerary.name = form.elements.name.value.trim();
      itinerary.start_date = form.elements.start_date.value;
      itinerary.duration_days = numberOrNull(form.elements.duration_days.value);
      itinerary.end_date = form.elements.end_date.value;
      refreshItemDates(itinerary);
      saveState();
      renderItineraryBuilder(itinerary.id);
      renderExports();
    }

    function builderTimelineItemHTML(itinerary, item, index) {
      return `
        <article class="timeline-item" style="${ideaStyle(item.idea)}">
          <div class="timeline-date">${index + 1}<br>${escapeHTML(fmtDate(item.start_date))}</div>
          <div>
            <h3>${escapeHTML(item.idea.title)}</h3>
            <div class="item-controls" aria-label="Itinerary item controls">
              <span class="duration-inline">
                <input type="number" min="1" value="${Number(item.duration_days || 1)}" data-duration-index="${index}" aria-label="Duration days" title="Duration in days">
                <span>days</span>
              </span>
              <button class="icon-button" type="button" data-move-index="${index}" data-direction="-1" aria-label="Move up" title="Move this idea earlier">&uarr;</button>
              <button class="icon-button" type="button" data-move-index="${index}" data-direction="1" aria-label="Move down" title="Move this idea later">&darr;</button>
              <button class="icon-button" type="button" data-remove-index="${index}" aria-label="Remove" title="Remove this idea from the itinerary">&times;</button>
            </div>
          </div>
        </article>
      `;
    }

    function drawBuilderMap(itinerary, items, options = {}) {
      const layer = layers.builderMap;
      const map = maps.builderMap;
      if (!layer || !map) return;
      const preservedView = options.mapView || null;
      layer.clearLayers();
      const selectedIds = new Set(items.map((item) => item.idea_id));
      const bounds = [];
      items.forEach((item) => addTravelPath(layer, item.idea));
      drawItineraryRoutes("builderMap", layer, items);
      state.ideas.forEach((idea) => {
        const order = items.findIndex((item) => item.idea_id === idea.id);
        const marker = addIdeaMarker(layer, idea, {
          order: order >= 0 ? order + 1 : null,
          unused: !selectedIds.has(idea.id),
          popup: ideaCard(idea, { action: builderAddActionHTML(idea) })
        });
        bounds.push([idea.lat, idea.lon]);
        marker.on("popupopen", () => {
          setTimeout(() => {
            const popup = marker.getPopup()?.getElement();
            const button = popup?.querySelector("[data-add-next]");
            if (!button) {
              return;
            }
            button.addEventListener("click", () => {
              const durationInput = popup.querySelector("[data-add-duration]");
              const duration = numberOrNull(durationInput?.value) || idea.duration_days || idea.min_duration_days || 1;
              addIdeaToItinerary(itinerary, button.dataset.addNext, duration);
            });
          }, 0);
        });
      });
      if (preservedView) {
        map.setView(preservedView.center, preservedView.zoom, { animate: false });
      } else {
        fitBounds(map, itineraryTravelFocusBounds(items) || bounds);
      }
      bindTimelineControls(itinerary);
    }

    function builderAddActionHTML(idea) {
      const duration = idea.duration_days || idea.min_duration_days || 1;
      return `
        <div class="popup-add-form">
          <label>Days
            <input type="number" min="1" value="${Number(duration)}" data-add-duration="${escapeHTML(idea.id)}">
          </label>
          <button type="button" data-add-next="${escapeHTML(idea.id)}">Add as next stop</button>
        </div>
      `;
    }

    function bindTimelineControls(itinerary) {
      $$("[data-duration-index]").forEach((input) => input.addEventListener("change", () => {
        itinerary.items[Number(input.dataset.durationIndex)].duration_days = Math.max(1, Number(input.value || 1));
        refreshItemDates(itinerary);
        saveState();
        renderItineraryBuilder(itinerary.id);
        renderExports();
      }));
      $$("[data-move-index]").forEach((button) => button.addEventListener("click", () => {
        const index = Number(button.dataset.moveIndex);
        const target = index + Number(button.dataset.direction);
        if (target < 0 || target >= itinerary.items.length) return;
        [itinerary.items[index], itinerary.items[target]] = [itinerary.items[target], itinerary.items[index]];
        normalizeOrders(itinerary);
        refreshItemDates(itinerary);
        saveState();
        renderItineraryBuilder(itinerary.id);
        renderExports();
      }));
      $$("[data-remove-index]").forEach((button) => button.addEventListener("click", () => {
        itinerary.items.splice(Number(button.dataset.removeIndex), 1);
        normalizeOrders(itinerary);
        refreshItemDates(itinerary);
        saveState();
        renderItineraryBuilder(itinerary.id);
        renderExports();
      }));
    }

    function addIdeaToItinerary(itinerary, ideaId, durationDays = null) {
      const idea = ideaById(ideaId);
      if (!idea) return;
      const mapView = currentMapView("builderMap");
      itinerary.items.push({ order: itinerary.items.length + 1, idea_id: idea.id, duration_days: durationDays || idea.duration_days || idea.min_duration_days || 1, note: "" });
      refreshItemDates(itinerary);
      saveState();
      renderItineraryBuilder(itinerary.id, { mapView });
      renderExports();
    }

    function currentMapView(mapId) {
      const map = maps[mapId];
      return map ? { center: map.getCenter(), zoom: map.getZoom() } : null;
    }

    function normalizeOrders(itinerary) {
      itinerary.items.forEach((item, index) => item.order = index + 1);
    }

    function refreshItemDates(itinerary) {
      normalizeOrders(itinerary);
      let cursor = itinerary.start_date ? new Date(itinerary.start_date + "T00:00:00") : new Date();
      itinerary.items.forEach((item) => {
        item.start_date = cursor.toISOString().slice(0, 10);
        cursor.setDate(cursor.getDate() + Number(item.duration_days || 1) - 1);
        item.end_date = cursor.toISOString().slice(0, 10);
        cursor.setDate(cursor.getDate() + 1);
      });
    }

    function numberOrNull(value) {
      const number = Number(value);
      return Number.isFinite(number) && number > 0 ? number : null;
    }

    function slug(value) {
      return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || `idea-${Date.now().toString(36)}`;
    }

    function renderExports() {
      $("#ideasCsv").value = toCsv(["id","title","commitment","primary_tag","tags","lat","lon","min_duration_days","people","notes","travel_role","from_label","via_labels","to_label","travel_type","travel_path","duration_days"], state.ideas.map((idea) => ({
        ...idea,
        tags: (idea.tags || []).filter((tag) => tag !== idea.primary_tag).join("|"),
        people: (idea.people || []).join("|"),
        via_labels: (idea.via_labels || []).join("|"),
        travel_path: (idea.travel_path || []).map((point) => `${point.label ? point.label + "@" : ""}${point.lat},${point.lon}`).join("|")
      })));
      $("#itinerariesCsv").value = toCsv(["id","name","start_date","end_date","duration_days","summary"], state.itineraries);
      const rows = [];
      state.itineraries.forEach((itinerary) => (itinerary.items || []).forEach((item, index) => rows.push({
        itinerary_id: itinerary.id,
        item_order: index + 1,
        idea_id: item.idea_id,
        duration_days: item.duration_days,
        note: item.note || ""
      })));
      $("#itemsCsv").value = toCsv(["itinerary_id","item_order","idea_id","duration_days","note"], rows);
    }

    function toCsv(headers, rows) {
      const line = (values) => values.map((value) => {
        const text = String(value ?? "");
        return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
      }).join(",");
      return [line(headers), ...rows.map((row) => line(headers.map((header) => row[header])))].join("\n");
    }
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
