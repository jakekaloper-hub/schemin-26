#!/usr/bin/env python3
"""Deterministically render Phase 3 structural environment plates from active World Engine data."""
from __future__ import annotations
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "world" / "data"
OUT = ROOT / "world" / "environment-references" / "plates"

def load(name):
    return json.loads((DATA / name).read_text())

def esc(value):
    return html.escape(str(value), quote=False)

def line(arr, y, label):
    text = " • ".join(str(x) for x in (arr or [])) or "NONE"
    return f'<text x="80" y="{y}" font-family="sans-serif" font-size="22">{esc(label)}: {esc(text)}</text>'

def render(location, zone, state):
    current = state.get("locations", {}).get(location["id"], location.get("current_state", []))[:3]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
<rect width="1600" height="900" fill="#f3efe4"/>
<rect x="50" y="50" width="1500" height="800" fill="none" stroke="#111" stroke-width="4"/>
<text x="80" y="115" font-family="serif" font-size="44" font-weight="700">{esc(location["name"])}</text>
<text x="80" y="155" font-family="sans-serif" font-size="20">{esc(location["id"])} • STRUCTURAL REFERENCE V1 • NOT CINEMATIC ART</text>
<line x1="80" y1="180" x2="1520" y2="180" stroke="#111" stroke-width="2"/>
{line([zone["name"]],230,"PHYSICAL ZONE")}
{line(zone["environment"]["terrain"],275,"TERRAIN")}
{line(zone["environment"]["climate"],320,"CLIMATE")}
{line(location.get("persistent_landmarks",[])[:4],365,"LANDMARKS")}
{line(location.get("access_route_ids",[])[:4],410,"ACCESS")}
{line(current,455,"CURRENT STATE")}
<text x="80" y="525" font-family="sans-serif" font-size="24" font-weight="700">SPATIAL ANCHOR</text>
<circle cx="290" cy="665" r="100" fill="none" stroke="#111" stroke-width="3"/>
<text x="240" y="672" font-family="sans-serif" font-size="18">LOC CORE</text>
<line x1="390" y1="665" x2="640" y2="665" stroke="#111" stroke-width="3"/>
<text x="455" y="645" font-family="sans-serif" font-size="18">ROUTE APPROACH</text>
<rect x="670" y="585" width="280" height="160" fill="none" stroke="#111" stroke-width="3"/>
<text x="710" y="670" font-family="sans-serif" font-size="18">LANDMARK FIELD</text>
<path d="M980 745 Q1180 520 1480 610" fill="none" stroke="#111" stroke-width="3"/>
<text x="1120" y="545" font-family="sans-serif" font-size="18">HORIZON / ZONE CONTINUITY</text>
<text x="80" y="810" font-family="sans-serif" font-size="18">RULE: preserve geography, landmarks, route logic, and state. Camera/weather may vary. Generated scenery does not create canon.</text>
</svg>
'''

def main():
    locations = load("locations.json")["locations"]
    zones = {x["id"]: x for x in load("physical_zones.json")["regions"]}
    state = load("current_world_state.json")
    for location in locations:
        target = OUT / location["id"] / "STRUCTURAL_PLATE.svg"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(location, zones[location["physical_zone_id"]], state))
    print(f"rendered {len(locations)} structural plates")

if __name__ == "__main__":
    main()
