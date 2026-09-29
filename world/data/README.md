# Schemin World Data

This directory contains the machine-readable substrate for the Schemin World Engine.

## Authority model

Human-facing canon lives in governed Markdown and character control sources. Machine data mirrors accepted fields for validation and downstream consumers.

## Formats

- **JSON: single canonical machine-readable authority** for World Engine records and validation.
- YAML files in this directory that point to JSON are compatibility/supersession markers only; they must not become a second source of truth.
- GeoJSON-style geometry may be introduced for spatial QA, using **Schemin-local abstract coordinates**, not Earth latitude/longitude.
- Markdown: rationale, lore, provenance and governance.

## Mutation law

Renderers never write canon.

Only an approved mutation workflow may change:
- location state;
- route state;
- owner-domain state;
- division state;
- historical consequence.

Every mutation must include provenance.

## Abstract coordinate policy

Any `abstract_position` or `abstract_bounds` is:
- non-metric;
- non-Earth;
- for topology/relative layout only;
- not evidence of real-world mileage.

## Consumer contract

Memo OS, Novel OS and Atlas rendering must consume these same IDs rather than creating parallel location names.

## V1.1 additions

- `inhabitant_ontology.json` — population/singular/cohabitation status and El Niño manifestation modes.
- `encounter_venue_policy.json` — home-team and neutral-site venue rules.
- `living-novel/os/geography/world_travel_graph_v1.json` — hydrated travel graph derived from locations/routes.
