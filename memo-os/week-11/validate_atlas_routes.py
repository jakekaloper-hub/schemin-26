#!/usr/bin/env python3
"""Week11 story-room Atlas route and venue-preflight check (not visual approval).

Checks route topology and joins each staged matchup to its cast, site and folios.
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

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def index_rows(rows, key):
    indexed = {row[key]: row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError(f"duplicate {key}")
    return indexed


def validate_cast(game, scene, receipt, owners, primaries):
    cast = index_rows(receipt["cast"], "character_id")
    sides = [game["home"], game["away"]]
    names = []
    expected = []
    for side in sides:
        owner = owners[side["teamId"]]
        char = owner["character_id"]
        member = cast[char]
        primary = primaries[char]
        staged = member["registered_primary"]
        if (member["owner"], member["team"]) != (owner["owner"], side["teamName"]):
            raise ValueError(f"{scene['matchup']} {char}: owner or fixture team mismatch")
        if (staged["expected_path"], staged["staged_sha256"]) != (
            primary["repository_path"], primary["expected_sha256"]
        ):
            raise ValueError(f"{scene['matchup']} {char}: registered primary reference mismatch")
        expected.append(char)
        names.append(f"{side['teamName']} ({char})")
    if (len(set(expected)) != 2 or sorted(scene["character_ids"]) != sorted(expected)
            or set(cast) != set(expected)):
        raise ValueError(f"{scene['matchup']}: expected exactly the two scheduled characters")
    return names


def validate_desk_location(scene, location, pages):
    staged = location["week11"]
    for field in ("matchup", "location_id", "sublocation_handle"):
        if staged[field] != scene[field]:
            raise ValueError(f"{scene['matchup']}: location desk disagrees on {field}")
    if sorted(staged["character_ids"]) != sorted(scene["character_ids"]):
        raise ValueError(f"{scene['matchup']}: location desk cast differs from scene")
    # An editorial insert or private interview can share the parent without using the public set.
    parent_folios = sorted(folio for folio, page in pages.items()
                           if scene["location_id"] in page["location_ids"])
    if sorted(location["folios"]) != parent_folios:
        raise ValueError(f"{scene['matchup']}: venue and page indexes disagree on folios")


def validate_scene_sites(root):
    weekly = root / "memo-os/week-11"
    desk = weekly / "preproduction"
    bindings = read_json(weekly / "sets/location-bindings.json")
    references = read_json(desk / "WEEK11_PRE_RENDER_REFERENCE_RECEIPT.json")
    snapshot = read_json(desk / "SUNDAY_2024_ET_SOURCE.json")
    if any((doc["season"], doc["week"]) != (2026, 11) for doc in (bindings, references)):
        raise ValueError("expected Week 11 of the 2026 season")
    # This fixed capture supplies the six fixture identities. It cannot settle a game.
    if (str(snapshot["league_id"]), snapshot["season"], snapshot["observed_at"]) != (
        "1417621", 2026, "2026-11-23T01:24:20.535441+00:00"
    ):
        raise ValueError("expected the November 22 8:24 p.m. Eastern fixture capture")
    games = index_rows(snapshot["week11_games"], "game")
    scenes = index_rows(bindings["matchups"], "matchup")
    receipts = index_rows(references["matchups"], "id")
    game_ids = {f"G{n:02d}" for n in range(1, 7)}
    scene_ids = {f"W11-{game}" for game in game_ids}
    if games.keys() != game_ids or scenes.keys() != scene_ids or receipts.keys() != scene_ids:
        raise ValueError("expected one fixture, scene and reference receipt per Week 11 matchup")
    # The direct scoreboard rows are [period, away ID, away points, home ID, home points, winner].
    pairs = [(g["away"]["teamId"], g["home"]["teamId"]) for g in games.values()]
    direct = [(away, home) for period, away, _, home, _, _ in snapshot["direct_espn"]["rows"]
              if period == 11]
    if sorted(pairs) != sorted(direct) or len({team for pair in pairs for team in pair}) != 12:
        raise ValueError("six distinct home/away pairs must agree with the direct scoreboard")
    owners = index_rows(read_json(root / "world/data/owner_domains.json")["domains"], "team_id")
    primaries = index_rows(read_json(root / "canon/characters/reference_sources_v1.json")["entries"],
                           "character_id")
    location_desk = read_json(desk / "WEEK11_LOCATION_DESK.json")
    pages = index_rows(location_desk["folios"], "folio")
    locations = index_rows(location_desk["locations"], "location_id")
    selected = {folio for folio, page in pages.items() if page["status"] == "SELECTED_SCENE_FEATURE"}
    used = set()
    control = root / "world/location-control-plane"
    registry = read_json(control / "registries/PARENT_SUBLOCATION_REGISTRY.json")
    by_handle = index_rows(registry["handles"], "handle_id")
    expected_venues = {venue for _, _, venue in JOURNEYS}
    if {row["location_id"] for row in scenes.values()} != expected_venues:
        raise ValueError("expected six Week 11 scenes covering all six venues")
    summary = []
    for game in sorted(games):
        matchup = f"W11-{game}"
        scene, receipt = scenes[matchup], receipts[matchup]
        venue, handle = scene["location_id"], scene["sublocation_handle"]
        if (venue, handle) != (receipt["venue"]["parent_id"], receipt["venue"]["feature"]):
            raise ValueError(f"{matchup}: site differs from its reference receipt")
        card = read_json(control / "locations" / venue / "CARD.json")
        features = index_rows(card["addressable_feature_handles"], "handle_id")
        if (by_handle[handle]["parent_location_id"] != venue or card["location_id"] != venue
                or handle not in features):
            raise ValueError(f"{matchup}: unresolved site {handle}")
        cast = validate_cast(games[game], scene, receipt, owners, primaries)
        validate_desk_location(scene, locations[venue], pages)
        folios = []
        for number in receipt["rehearsal_folios"]:
            if type(number) is not int:
                raise ValueError(f"{matchup}: expected a numeric rehearsal folio")
            folio = f"F{number:02d}"
            if folio not in selected or folio in used:
                raise ValueError(f"{matchup} {folio}: unselected or multiply assigned folio")
            page = pages[folio]
            if (page["location_ids"], page["selected_handle_ids"]) != ([venue], [handle]):
                raise ValueError(f"{matchup} {folio}: location desk and scene disagree")
            used.add(folio)
            folios.append(folio)
        if not folios:
            raise ValueError(f"{matchup}: no staged matchup folios")
        summary.append(f"PASS {matchup} | {' / '.join(cast)} | {handle} | {', '.join(folios)}")
    if used != selected:
        raise ValueError(f"selected matchup folios missing from receipts: {sorted(selected - used)}")
    return summary


def check_scene_sites(root):
    try:
        summary = validate_scene_sites(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL Week 11 scene bindings: {exc}")
        return False
    for line in summary:
        print(line)
    return True

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
    if not check_scene_sites(root):
        return 1
    print("SITE_GATE: 6/6 fixture, cast, site and folio assignments agree; bridge parent retains provisional status")
    print("PITTSYS_HOLD: Central Basin Book record conflicts with Commissioner TDS-waterfall placement")
    print("VISUAL_HOLD: Atlas environment bytes/canon, dynamic weather and property rights unapproved")
    print("Scope: preproduction assignments only. Renderer binding, likeness QA, final scores and release require separate evidence.")
    return 0 if passed == len(JOURNEYS) else 1

if __name__ == "__main__":
    raise SystemExit(main())
