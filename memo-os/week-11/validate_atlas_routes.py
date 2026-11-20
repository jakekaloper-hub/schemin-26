#!/usr/bin/env python3
"""Week11 story-room Atlas route and venue-preflight check (not visual approval).

No permanent LOC state, route, jurisdiction or environmental reference is changed.
Checks current source map topology; weather/rights/renderer/venue sublocations stay held.
"""
import hashlib
import json
from collections import deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROUTES = REPO / "world/data/routes.json"
EXPECTED_ROUTE_BLOB = "da418245708c1f9d2128775df0ce7d26e7eeaa18"

JOURNEYS = [
    ("HMB -> neutral bridge", "LOC-BELT-KEEPER-KEEP", "LOC-BRIDGE-MOUNTAIN-LAKE"),
    ("DK -> neutral bridge", "LOC-DK-HIGHLAND-STRONGHOLD", "LOC-BRIDGE-MOUNTAIN-LAKE"),
    ("El Niño -> Slob camp", "LOC-STORM-BOWL", "LOC-SLOB-FOOTHILL-CAMP"),
    ("Chili -> ObiWan base", "LOC-CHILI-STABLE", "LOC-TRADE-JEDI-MOUNTAIN-BASE"),
    ("Red Leopards -> TDS domain", "LOC-RED-RUINS", "LOC-TDS-WATERFALL-TEMPLE"),
    ("Chins -> Mud Dogs swamp", "LOC-CHINS-ROAD-COMMONS", "LOC-MUD-DOGS-SWAMP"),
    ("LLC -> Duckhook domain", "LOC-LLC-BOARDROOM", "LOC-COUNTRY-CLUB-JACKSON"),
]

CARD_EXPECTATIONS = [
    ("LOC-BRIDGE-MOUNTAIN-LAKE", "PROVISIONAL_CANON", "REG-UPPER-VALLEYS"),
    ("LOC-TDS-WATERFALL-TEMPLE", "PERMANENT_CANON", "REG-SOUTHERN-WETLANDS"),
    ("LOC-COUNTRY-CLUB-JACKSON", "PERMANENT_CANON", "REG-SOUTHERN-WETLANDS"),
    ("LOC-PITTSYS-BOOK", "PROVISIONAL_CANON", "REG-CENTRAL-BASIN"),
]

def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def build_graph(routes):
    graph = {}
    for r in routes:
        seq = [r["from"], *(r.get("via_location_ids") or []), r["to"]]
        for a, b in zip(seq, seq[1:]):
            graph.setdefault(a, []).append((b, r["id"]))
            if not r.get("one_way", False):
                graph.setdefault(b, []).append((a, r["id"]))
    return graph

def trace(graph, origin, destination):
    queue = deque([(origin, [])])
    seen = {origin}
    while queue:
        current, history = queue.popleft()
        if current == destination:
            return history
        for next_location, route_id in graph.get(current, []):
            if next_location not in seen:
                seen.add(next_location)
                queue.append((next_location, [*history, (route_id, next_location)]))
    return None

def main(root=REPO):
    data = (root / "world/data/routes.json").read_bytes()
    if blob_sha(data) != EXPECTED_ROUTE_BLOB:
        print("FAIL: World Engine route source revision changed; review and repin")
        return 1
    parsed = json.loads(data)
    graph = build_graph(parsed["routes"])
    passed = 0
    for name, origin, venue in JOURNEYS:
        path = trace(graph, origin, venue)
        if path is None:
            print("FAIL", name, "no path")
        else:
            passed += 1
            print("PASS", name, " | ".join(x[0] for x in path))
    for id_, canon, zone in CARD_EXPECTATIONS:
        f = root / "world/location-control-plane/locations" / id_ / "CARD.json"
        obj = json.loads(f.read_text(encoding="utf-8"))
        if (obj.get("location_id"), obj.get("canon_status"),
            obj.get("physical_zone", {}).get("id")) != (id_, canon, zone):
            print("FAIL", id_, "location identity/canon/zone changed")
            return 1
    print(f"ROUTE_GATE: {passed}/{len(JOURNEYS)} connected (topology only)")
    print("VENUE_HOLD: bridge is provisional; Duckhook non-golf 11-year site unverified")
    print("PITTSYS_HOLD: Central Basin Book record conflicts with Commissioner TDS-waterfall placement")
    print("VISUAL_HOLD: Atlas environment bytes/canon, dynamic weather and property rights unapproved")
    return 0 if passed == len(JOURNEYS) else 1

if __name__ == "__main__":
    raise SystemExit(main())
