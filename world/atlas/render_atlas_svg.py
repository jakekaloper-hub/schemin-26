#!/usr/bin/env python3
"""Render a deterministic schematic Schemin Atlas SVG.

This is a QA renderer: abstract coordinates only, no claim of final art direction.
"""

from pathlib import Path
import json
import html

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "world" / "data"
OUT = ROOT / "world" / "atlas" / "prototypes" / "SCHEMIN_ATLAS_V1_SCHEMATIC.svg"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main():
    zones = load("physical_zones.json")["regions"]
    divisions = {d["id"]: d for d in load("divisions.json")["divisions"]}
    locs = load("locations.json")["locations"]
    routes = load("routes.json")["routes"]
    loc_by_id = {l["id"]: l for l in locs}

    width, height = 1000, 1000
    def sx(x): return 50 + x * 9
    def sy(y): return 950 - y * 9

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="50" y="35" font-size="22" font-family="serif">Schemin Atlas V1 — schematic / abstract coordinates</text>'
    ]

    # Physical zones: outlines only to keep the prototype neutral.
    for z in zones:
        xmin,ymin,xmax,ymax = z["abstract_bounds"]
        x=sx(xmin); y=sy(ymax); w=(xmax-xmin)*9; h=(ymax-ymin)*9
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#777" stroke-dasharray="6 4"/>')
        parts.append(f'<text x="{x+5}" y="{y+16}" font-size="11" font-family="sans-serif">{html.escape(z["name"])}</text>')

    # Routes.
    for r in routes:
        a=loc_by_id[r["from"]].get("abstract_position")
        b=loc_by_id[r["to"]].get("abstract_position")
        if not a or not b: continue
        parts.append(f'<line x1="{sx(a[0])}" y1="{sy(a[1])}" x2="{sx(b[0])}" y2="{sy(b[1])}" stroke="#555" stroke-width="2"/>')

    # Locations, labelled with division initial when applicable.
    for l in locs:
        p=l.get("abstract_position")
        if not p: continue
        div = l.get("division_id")
        marker = {"DIV-BURGERS":"B","DIV-WINGS":"W","DIV-PIZZA":"P"}.get(div,"N")
        parts.append(f'<circle cx="{sx(p[0])}" cy="{sy(p[1])}" r="5" fill="#222"/>')
        label=f'{marker}: {l["name"]}'
        parts.append(f'<text x="{sx(p[0])+8}" y="{sy(p[1])-7}" font-size="10" font-family="sans-serif">{html.escape(label)}</text>')

    parts.append('</svg>')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUT)

if __name__ == "__main__":
    main()
