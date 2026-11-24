"""Replay the five record-only examples and the Burgers hypothetical at Week 11."""
import json
from decimal import Decimal
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
# Each tuple contains the six hypothetical winners for that week, in any order.
EXAMPLES = {
    "A": ((1, 10, 2, 3, 4, 9), (10, 6, 3, 7, 9, 11), (6, 10, 7, 3, 11, 9)),
    "B": ((1, 10, 2, 3, 4, 9), (1, 5, 3, 2, 9, 4), (1, 10, 12, 3, 8, 9)),
    "C": ((5, 6, 2, 7, 4, 9), (10, 6, 3, 2, 9, 11), (6, 5, 7, 2, 11, 9)),
    "D": ((5, 6, 2, 7, 4, 11), (10, 6, 12, 2, 8, 11), (6, 5, 7, 2, 11, 9)),
    "E": ((1, 10, 2, 3, 4, 11), (10, 6, 3, 7, 8, 4), (6, 10, 7, 3, 11, 4)),
}
# (winner, loser); actual Weeks 2–4, cross-read against the pinned ESPN snapshot.
EARLY_BURGERS = [(10, 1), (5, 6), (1, 6), (5, 10), (1, 5), (6, 10)]
# (winner, winner score, loser, loser score); hypothetical Weeks 12–14.
LATE_BURGERS = [
    [(1, 120, 5, 100), (10, 200, 6, 100)],
    [(10, 200, 1, 100), (6, 120, 5, 100)],
    [(1, 120, 6, 100), (10, 200, 5, 100)],
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def record_only_field(wins, divisions, places):
    """Try every division tie outcome. Require the same seven-team field for all."""
    candidates = []
    for members in divisions:
        best = max(wins[team] for team in members)
        candidates.append([team for team in members if wins[team] == best])
    wildcards = places - len(divisions)
    fields = set()
    for champions in product(*candidates):
        others = sorted(set(wins).difference(champions), key=wins.get, reverse=True)
        assert wins[others[wildcards - 1]] > wins[others[wildcards]], "wild card tie"
        fields.add(tuple(sorted((*champions, *others[:wildcards]))))
    assert len(fields) == 1, "qualification depends on division tiebreak"
    return set(fields.pop())


def check_mud(standings, fixtures, burgers):
    wins = {team: standings[team]["record"][0] for team in burgers}
    points = {team: Decimal(str(standings[team]["points_for"])) for team in burgers}
    head_to_head = list(EARLY_BURGERS)
    for week, games in zip(fixtures, LATE_BURGERS):
        assert {pair for pair in week if pair <= burgers} == {
            frozenset((w, l)) for w, _, l, _ in games
        }
        for winner, high, loser, low in games:
            assert high > low
            wins[winner] += 1
            points[winner] += high
            points[loser] += low
            head_to_head.append((winner, loser))
    assert set(wins.values()) == {6}
    for team in burgers:
        for rival in burgers - {team}:
            assert sum({w, l} == {team, rival} for w, l in head_to_head) == 2
    mini = {team: sum(w == team for w, _ in head_to_head) for team in burgers}
    assert mini == {1: 4, 5: 2, 6: 2, 10: 4}
    assert sum((w, l) == (10, 1) for w, l in head_to_head) == 2
    assert points[10] > max(v for t, v in points.items() if t != 10)
    return points


def main():
    source = load(HERE / "W11_POST_MNF_FLAIM_ESPN_SOURCE_2026-11-24.json")
    rest = load(HERE / "W11_WEEK13_14_REMAINING_ESPN_SCHEDULE_2026-11-24.json")
    canon = load(ROOT / "canon/league.json")
    assert canon["playoff_teams"] == 7 and canon["regular_season_weeks"] == 14
    divisions = {
        d["name"]: set(d["member_team_ids_2026"])
        for d in load(ROOT / "world/data/divisions.json")["divisions"]
    }
    standings = {t["team_id"]: t for t in source["standings"]["teams"]}
    assert len(standings) == 12 and all(sum(t["record"]) == 11 for t in standings.values())
    assert len(divisions) == 3 and set.union(*divisions.values()) == set(standings)
    fixtures = [[frozenset((g["home"]["team_id"], g["away"]["team_id"]))
                 for g in source["week12"]["fixtures"]]]
    for key in ("week13", "week14"):
        fixtures.append([frozenset((g["home_id"], g["away_id"])) for g in rest["weeks"][key]])
    for week in fixtures:
        assert len(week) == 6 and set.union(*(set(p) for p in week)) == set(standings)
    qualifies, misses = set(), set()
    for label, winners in EXAMPLES.items():
        wins = {team: row["record"][0] for team, row in standings.items()}
        for week, selections in zip(fixtures, winners):
            assert len(set(selections)) == 6
            for game in week:
                picked = game.intersection(selections)
                assert len(picked) == 1
                wins[next(iter(picked))] += 1
        field = record_only_field(wins, divisions.values(), canon["playoff_teams"])
        qualifies.update(field)
        misses.update(set(standings) - field)
        print(label, ", ".join(standings[t]["team"] for t in sorted(field)))
    assert qualifies == set(standings) - {10} and misses == set(standings)
    points = check_mud(standings, fixtures, divisions["Burgers"])
    print("Burgers hypothetical final points for:", dict(sorted(points.items())))
    print("12 qualification examples; 12 miss examples.")


if __name__ == "__main__":
    main()
