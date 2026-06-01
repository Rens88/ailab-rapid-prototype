---
name: standalone-html-planner
description: Use when asked to build or refactor a standalone HTML app generated from local structured data, especially for map-plus-timeline planners, itinerary viewers, route comparison tools, or small interactive dashboards that should work without a framework build step.
---

# Standalone HTML Planner

Build the app as a generator, not as hand-edited HTML.

The pattern from this repo is:

- one canonical source model
- one script that validates and normalizes that model
- one inline HTML template with CSS and JavaScript
- one or two generated standalone pages with different interaction levels

Use this skill when the goal is a shareable HTML artifact that opens directly in a browser and stays easy to regenerate from editable data files.

## Default architecture

Prefer this file layout unless the repo already has a better local convention:

```text
data/
  ideas.csv
  itineraries.csv
  itinerary_items.csv
  trip.csv
scripts/
  generate_<app>.py
dist/
  viewer.html
  constructor.html
```

Rules:

- Keep source data outside the HTML. Spreadsheet-friendly CSV is a good default.
- Normalize everything into one JSON object in the generator before rendering.
- Generate output files into `dist/`; do not treat them as the source of truth.
- Keep the generator deterministic and strict about validation.

## Data modeling heuristics

Favor fewer entity types.

In this design, everything that can appear in a route or timeline is the same kind of item. Do not immediately split the model into separate stop, leg, note, and route-segment systems unless the product actually needs that complexity.

Good default:

- a primary item table for things the user is planning
- an itinerary table for named route options
- an ordered join table for itinerary membership and per-itinerary duration/notes

If travel needs to appear in the same sequence as stops, model travel as another item type instead of inventing a second planner layer.

## Generator workflow

The generator should do four things:

1. Read structured source files.
2. Validate required fields, dates, numeric ranges, uniqueness, and ordering rules.
3. Normalize rows into a single browser-ready JSON seed.
4. Inject that seed into an inline HTML template and write the final page(s).

Keep normalization in the generator, not in scattered browser code. The browser should receive a clean seed model that is ready to render.

## UI split

If the app has both a shareable endpoint and an editing workspace, split them into separate generated pages that share the same seed model.

Use this split:

- `viewer.html`: read-only, fast, safe to share
- `constructor.html`: local editing workspace with draft state and export helpers

Do not mix editing controls into the shared page unless the user explicitly wants one all-in-one tool. The split keeps the shareable surface smaller and harder to break.

## Interaction model

For this style of app, plain JavaScript is usually enough.

Prefer:

- a small number of top-level views such as `Map`, `Timeline`, and optionally `Export`
- DOM rendering from application state rather than server round-trips
- direct event listeners instead of a framework when the interaction surface is modest
- `localStorage` only for local draft state in the editable page

Useful interaction patterns from this design:

- itinerary selector with an "all items" mode
- clickable cards that focus map markers
- ordered markers when an itinerary is selected
- map/timeline dual views over the same underlying selection
- popup actions that add items into the current itinerary
- CSV export textareas generated from in-browser state

## Map and routing pattern

Use Leaflet when a lightweight map is enough.

Routing should degrade gracefully:

- draw a dashed straight fallback line immediately
- asynchronously request a routed line from an external service such as OSRM
- replace the fallback only if the request succeeds
- cache route results client-side for the current session

Do not make the whole app depend on routing availability. The map must remain useful when routing or tiles are unavailable.

If the app includes explicit travel paths from the source data, render them as dashed overlays distinct from computed road routes.

## Timeline pattern

Use a second representation of the exact same itinerary state instead of inventing a different model for the timeline.

Good defaults:

- compute item start and end dates in the generator or in one small browser utility
- render a day-axis timeline for the selected itinerary
- show duration, category, and lightweight notes directly on each block
- keep timeline ordering consistent with map marker ordering

The point is scanability, not calendar-grade scheduling.

## HTML, CSS, and JS conventions

Prefer one inline template when the final artifact must stay self-contained.

Keep the browser code organized by responsibility:

- boot and state loading
- shell rendering
- view rendering
- map rendering
- timeline rendering
- editing actions
- export helpers
- small utility functions

Styling rules from this design:

- use CSS variables for palette, borders, shadows, and semantic colors
- make the header and controls compact on mobile
- use a split layout that collapses cleanly to one column
- make cards and markers reflect item category or tag color

## Validation rules worth preserving

When adapting this pattern, validate the domain rules before generating HTML.

Examples from this design:

- IDs must be unique
- itinerary membership order must be unique per itinerary
- dates must be valid ISO dates
- latitude and longitude must be in range
- durations must be positive integers
- itinerary total duration must not exceed its declared limit
- sequence-specific item roles must be enforced when the domain depends on them

If notes are user-editable, sanitize them before embedding them in HTML. Allow only a tiny safe subset if rich text is needed.

## When to stay simple

Choose this pattern over a framework app when most of these are true:

- the app is mostly read-only or lightly editable
- regeneration from local files is acceptable
- the data volume is small to moderate
- offline-ish sharing matters more than live collaboration
- the interaction model fits in a few views and a few hundred lines of JavaScript

Do not use this pattern by default for heavy multi-user editing, authentication, large datasets, or highly stateful workflows that need a real backend.

## Delivery checklist

When implementing this skill in another repo:

1. Define the smallest workable source schema.
2. Write one generator that validates and normalizes the schema.
3. Generate one seed JSON object for the browser.
4. Build one inline HTML template with minimal external dependencies.
5. Separate shared viewing from local editing if both are needed.
6. Add graceful map and routing fallback.
7. Keep export or round-trip paths tied to the source schema.
8. Regenerate the HTML instead of manually patching generated output.
