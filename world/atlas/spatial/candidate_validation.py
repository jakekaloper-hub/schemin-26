"""Read-only validation of candidate geometry; does not promote geography."""
import json
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "central_basin_candidate_v1.json"
ANCHORS = {"LOC-LEAGUE-CHAMBER", "LOC-LEAGUE-ARCHIVE", "LOC-PITTSYS-BOOK"}
INTERMEDIATES = {"LOC-DK-MUD-HILL", "LOC-SOUTHERN-SPEEDWAY"}


def validate_candidate(data: dict) -> list[str]:
    errors = []
    if data.get("status") != "DERIVED_SYNTHETIC_NOT_CANON":
        errors.append("INVALID_CANDIDATE_STATUS")
    crs = data.get("coordinate_reference", {})
    if crs.get("units") != "meters" or crs.get("real_distance_claim") is not False:
        errors.append("INVALID_COORDINATE_POLICY")
    if data.get("region_id") != "REG-CENTRAL-BASIN":
        errors.append("REGION_DRIFT")
    anchors = data.get("anchors", [])
    via = data.get("route_intermediates", [])
    if {x.get("location_id") for x in anchors} != ANCHORS:
        errors.append("ANCHOR_DRIFT")
    if {x.get("location_id") for x in via} != INTERMEDIATES:
        errors.append("INTERMEDIATE_DRIFT")
    coords = {}
    for item in anchors + via:
        xy, z = item.get("xy"), item.get("z")
        if not isinstance(xy, list) or len(xy) != 2 or any(type(v) not in (int, float) for v in xy) or type(z) not in (int, float):
            errors.append("INVALID_POINT_GEOMETRY")
        else:
            coords[item["location_id"]] = (xy[0], xy[1], z)
    if len(set(coords.values())) != len(coords):
        errors.append("COINCIDENT_LANDMARKS")
    expected = {
        "ROUTE-ARCHIVE-CHAMBER": ["LOC-LEAGUE-ARCHIVE", "LOC-LEAGUE-CHAMBER"],
        "ROUTE-BASIN-MARKET": ["LOC-LEAGUE-CHAMBER", "LOC-DK-MUD-HILL", "LOC-SOUTHERN-SPEEDWAY", "LOC-PITTSYS-BOOK"],
    }
    observed = {p.get("route_id"): p.get("locations") for p in data.get("paths", [])}
    if observed != expected:
        errors.append("ROUTE_TOPOLOGY_DRIFT")
    if any(any(x not in coords for x in path) for path in observed.values() if isinstance(path, list)):
        errors.append("ROUTE_LOCATION_MISSING")
    drain = data.get("synthetic_drainage", [])
    nodes = {n.get("id"): n for n in drain}
    if len(nodes) != len(drain) or not drain:
        errors.append("DRAINAGE_NODE_INVALID")
    for n in drain:
        child = n.get("downstream")
        if child is not None:
            if child not in nodes:
                errors.append("DRAINAGE_OUTLET_MISSING")
            elif n.get("z", -1) <= nodes[child].get("z", -1):
                errors.append("UPHILL_FLOW")
    for source in nodes:
        seen, node = set(), source
        while node is not None and node in nodes:
            if node in seen:
                errors.append("DRAINAGE_CYCLE")
                break
            seen.add(node)
            node = nodes[node].get("downstream")
    scenarios = data.get("scenarios", [])
    if len({x.get("date") for x in scenarios}) != len(scenarios) or len(scenarios) < 2:
        errors.append("INVALID_SEASONAL_SCENARIOS")
    if any(x.get("model_tag") != "HYPOTHETICAL" for x in scenarios):
        errors.append("IMPROPER_WEATHER_AUTHORITY")
    return sorted(set(errors))


def load_candidate() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))
