#!/usr/bin/env python3
"""Compile a non-promoting illustration guide from existing World Engine records."""
import hashlib
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COLORS = ['#8ea0b4', '#b1bd8b', '#c4bc74', '#c7996a', '#719e8e', '#6b9d9c', '#8ab5c5']


def project(position):
    """Identical to audience-site/src/experience.js projectPoint, in its 1000x700 viewBox."""
    x, y = position
    return {'x': 90 + float(x) * 8.2, 'y': 650 - float(y) * 5.8}


def compile_matrix():
    sources = {}

    def read(relative):
        path = ROOT / relative
        raw = path.read_bytes()
        sources[relative] = {'path': relative, 'sha256': hashlib.sha256(raw).hexdigest()}
        return json.loads(raw)

    locations = read('world/data/locations.json')['locations']
    regions = read('world/data/physical_zones.json')['regions']
    routes = read('world/data/routes.json')['routes']
    state = read('world/data/current_world_state.json')
    for relative in ['world/production/CANONICAL_WORLD_PLATE_SPATIAL_BLUEPRINT_V1.md',
                     'world/production/CANONICAL_WORLD_PLATE_SPATIAL_QA_V1.md']:
        sources[relative] = {'path': relative, 'sha256': hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()}
    source_script = 'productions/audience-site/src/experience.js'
    sources[source_script] = {'path': source_script, 'sha256': hashlib.sha256((ROOT / source_script).read_bytes()).hexdigest()}
    region_by_id = {r['id']: r for r in regions}
    anchors = []
    for number, location in enumerate(locations, 1):
        location_id = location['id']
        card_path = f'world/location-control-plane/locations/{location_id}/CARD.json'
        packet_path = f'world/production/visual-packets/{location_id}.json'
        card = read(card_path) if (ROOT / card_path).is_file() else {}
        packet = read(packet_path) if (ROOT / packet_path).is_file() else {}
        region = region_by_id[location['physical_zone_id']]
        involved_routes = [r['id'] for r in routes if location_id in [r['from'], *(r.get('via_location_ids') or ([r['via_location_id']] if r.get('via_location_id') else [])), r['to']]]
        anchors.append({
            'number': number, 'id': location_id, 'label': location['name'],
            'canonStatus': location.get('canon_status'),
            'abstractPosition': location['abstract_position'],
            'overlayPoint': project(location['abstract_position']),
            'svgPoint': {axis: (40 if axis == 'x' else 220) + value * 1.25 for axis, value in project(location['abstract_position']).items()},
            'regionId': region['id'], 'regionLabel': region['name'],
            'regionalEnvironment': region['environment'],
            'landmarks': location.get('persistent_landmarks', []),
            'routeIds': involved_routes,
            'baseState': location.get('current_state', []),
            'authoritativeState': state['locations'].get(location_id, []),
            'stateAsOf': state.get('as_of'),
            'ordinaryActivities': packet.get('world', {}).get('ordinary_inhabitants', []),
            'features': card.get('addressable_feature_handles', []),
            'sourcePaths': ['world/data/locations.json', 'world/data/physical_zones.json', 'world/data/routes.json', 'world/data/current_world_state.json'] + ([card_path] if card else []) + ([packet_path] if packet else []),
            'review': {'sourceBinding': 'PENDING', 'biome': 'PENDING', 'landmarks': 'PENDING', 'routes': 'PENDING', 'desktop': 'PENDING', 'phone': 'PENDING'},
        })
    return {
        'schemaVersion': 1, 'status': 'COMPOSITION_GUIDE__NOT_FINAL_ART__NO_CANON_PROMOTION',
        'coordinateSpace': 'schemin-local-v1 (abstract, non-metric)',
        'projection': {'viewBox': [0, 0, 1000, 700], 'x': '90 + x * 8.2', 'y': '650 - y * 5.8', 'svgTranslate': [40, 220], 'svgScale': 1.25},
        'warning': 'Region rectangles are abstract source extents, not coastlines, political borders, surveyed land parcels or terrain masks. Route strokes are connections, not travel-distance claims. This guide does not authorize new permanent scenery.',
        'regions': regions, 'routes': routes, 'anchors': anchors,
        'sources': [sources[k] for k in sorted(sources)],
    }


def render_svg(matrix):
    esc = lambda value: html.escape(str(value), quote=True)
    by_id = {a['id']: a for a in matrix['anchors']}
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1400" width="2000" height="1400" role="img" aria-labelledby="title desc">',
           '<title id="title">Commonwealth atlas composition guide: 23 governed location anchors</title>',
           '<desc id="desc">Source-bound abstract region extents, 18 route chains, and 23 numbered locations. Not final artwork, a survey, or new canon.</desc>',
           '<rect width="2000" height="1400" fill="#171719"/>',
           '<style>text{font-family:Arial,sans-serif;fill:#eee8da}.fine{fill:#bfb8aa;font-size:18px}.small{font-size:14px}.region-label{font-size:17px;font-weight:bold;paint-order:stroke;stroke:#171719;stroke-width:4;stroke-linejoin:round}.point{fill:#17251f;stroke:#fff0bd;stroke-width:2}.route{fill:none;stroke:#f1d49b;stroke-width:2;stroke-dasharray:5 5}.anchor-label{font-size:12px;paint-order:stroke;stroke:#171719;stroke-width:3}.pending{fill:#e6b985}</style>',
           '<text x="40" y="58" font-size="34">SCHEMIN — ATLAS COMPOSITION GUIDE</text>',
           '<text x="40" y="98" class="fine">Existing geography first. All 23 anchors require individual source, biome, landmark, route and phone review.</text>',
           '<text x="40" y="134" class="fine">ABSTRACT / NON-METRIC • NOT FINAL ART • NO CANON PROMOTION • ALL VISUAL REVIEWS PENDING</text>',
           '<text x="40" y="177" class="fine">Map uses the exact audience-site projection. Region extents overlap; they are not coastlines or land boundaries.</text>',
           '<g id="map-frame" transform="translate(40 220) scale(1.25)">',
           '<rect width="1000" height="700" fill="#262824" stroke="#dfbf78"/>', '<g id="region-extents">']
    for color, region in zip(COLORS, matrix['regions']):
        left, south, right, north = region['abstract_bounds']
        top, bottom = project([left, north]), project([right, south])
        out.append(f'<rect data-region="{esc(region["id"])}" x="{top["x"]}" y="{top["y"]}" width="{bottom["x"]-top["x"]}" height="{bottom["y"]-top["y"]}" fill="{color}" fill-opacity=".18" stroke="{color}" stroke-dasharray="4 3"><title>{esc(region["name"])}</title></rect>')
    out.extend(['</g>', '<g id="route-chains">'])
    for route in matrix['routes']:
        ids = [route['from'], *(route.get('via_location_ids') or ([route['via_location_id']] if route.get('via_location_id') else [])), route['to']]
        points = ' '.join(f'{by_id[k]["overlayPoint"]["x"]},{by_id[k]["overlayPoint"]["y"]}' for k in ids)
        out.append(f'<polyline data-route="{esc(route["id"])}" points="{points}" class="route"><title>{esc(route["name"])}</title></polyline>')
    out.extend(['</g>', '<g id="anchor-points">'])
    for anchor in matrix['anchors']:
        p = anchor['overlayPoint']
        out.append(f'<g data-location="{esc(anchor["id"])}" transform="translate({p["x"]} {p["y"]})"><title>{esc(anchor["label"])}</title><circle r="15" class="point"/><text text-anchor="middle" y="5" font-size="14" font-weight="bold">{anchor["number"]}</text></g>')
    out.extend(['</g>', '<g id="optional-inline-labels" display="none">'])
    for anchor in matrix['anchors']:
        p = anchor['overlayPoint']
        out.append(f'<text x="{p["x"]+19}" y="{p["y"]+4}" class="anchor-label">{esc(anchor["label"])}</text>')
    out.extend(['</g>', '<text x="945" y="42" font-size="24">N ↑</text>', '</g>', '<g id="anchor-register">', '<text x="1340" y="200" font-size="24">FIXED LOCATION REGISTER</text>'])
    for anchor in matrix['anchors']:
        y = 239 + (anchor['number'] - 1) * 47
        out.append(f'<text x="1340" y="{y}" font-size="17">{anchor["number"]:02d} · {esc(anchor["label"])}</text><text x="1379" y="{y+19}" class="small" fill="#bfb8aa">{esc(anchor["regionLabel"])}</text>')
    out.extend(['</g>', '<g id="region-register">'])
    for i, (region, color) in enumerate(zip(matrix['regions'], COLORS)):
        y = 1140 + i * 30
        out.append(f'<rect x="40" y="{y-15}" width="16" height="16" fill="{color}"/><text x="69" y="{y}" font-size="18">{esc(region["name"])}</text>')
    out.extend(['</g>', '<text x="700" y="1160" class="fine">23 anchors • 18 route chains • 7 regional extents</text>', '<text x="700" y="1200" class="fine">JSON matrix contains landmarks, regional environments,</text>', '<text x="700" y="1230" class="fine">ordinary activities, authoritative state and source hashes.</text>', '<text x="700" y="1280" class="pending" font-size="19">No painted output passes by resemblance alone.</text>', '<text x="40" y="1370" class="fine">Toggle named SVG groups in a vector editor. Optional inline labels are hidden to avoid implying finished label placement.</text>', '</svg>'])
    return '\n'.join(out) + '\n'


def checklist(matrix):
    rows = ['# Atlas composition acceptance checklist', '', 'This is a production guide, not accepted cartography or new canonical authority. All reviews start pending.', '', 'Before generating final terrain: inspect the spatial blueprint, every linked location/visual packet and current state; resolve any source conflict explicitly. Preserve upstream status and non-metric coordinates. Region extents are not coastlines.', '', '## Per-anchor visual review', '', '| Anchor | Exact source binding | Regional biome | Required landmarks | Governed route connections | Desktop labels | Phone selection and labels |', '|---|---|---|---|---|---|---|']
    rows.extend(f'| {a["number"]:02d} {a["label"]} | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |' for a in matrix['anchors'])
    rows.extend(['', '## Whole composition', '', '- [ ] Every anchor matches its region and landmark requirements at its projected position.', '- [ ] No unapproved coastline, settlement, border, permanent landmark, distance or sovereignty claim is implied.', '- [ ] Every route preserves source order, including intermediate stops.', '- [ ] Current-state qualifiers survive: contested/unclaimed places are not depicted as newly owned sovereign territory.', '- [ ] A named region and recognizable place label remain available without hover.', '- [ ] Desktop and phone image/overlay transforms stay aligned through zoom, pan, selection, reload and return.', '- [ ] Phone hit areas are usable and labels do not collide; the location list remains available as an equivalent path.', '- [ ] Original output, derivatives, prompt, output hashes and source hashes are recorded.', '- [ ] Independent geographic and visual review references exact image bytes and records all defects.', '- [ ] Founder final visual judgment is separately recorded; no automatic promotion from a passing build.', '', 'Known regression examples: Alpine Wager must not lie over low green river valley; Country Club must not lie on an ocean inlet; the mountain-lake bridge must visibly retain its lake/bridge relationship.', ''])
    return '\n'.join(rows)


def main():
    matrix = compile_matrix()
    (HERE / 'ANCHOR_MATRIX.json').write_text(json.dumps(matrix, indent=2) + '\n')
    (HERE / 'COMPOSITION_GUIDE.svg').write_text(render_svg(matrix))
    (HERE / 'ACCEPTANCE_CHECKLIST.md').write_text(checklist(matrix))
    print(json.dumps({'anchors': len(matrix['anchors']), 'routes': len(matrix['routes']), 'regions': len(matrix['regions']), 'sources': len(matrix['sources']), 'status': matrix['status']}))


if __name__ == '__main__':
    main()
