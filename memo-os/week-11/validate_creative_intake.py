#!/usr/bin/env python3
"""Week 11 typed-source / Founder-answer integrity gate. Stdlib only.

This tests a fixed November 20 provisional snapshot, not post-MNF scoring.
It does not grant independent Umpire acceptance, Story Lock, Page Lock, or release.
Changes to either locked reference fixture require explicit audited repinning.
"""
import argparse
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

W11 = Path("memo-os/week-11")
FOUND = W11 / "FOUNDER_CREATIVE_INTERVIEW_58_RESPONSES_2026-11-20.md"
REF = W11 / "FOUNDER_NORMALIZED_REFERENCE_2026-11-20.json"
SRC = W11 / "WEEK11_TEST_SOURCE_RECEIPT_2026-11-20.json"
SYN = W11 / "FOUNDER_STORY_ROOM_SYNTHESIS_2026-11-20.md"
MATRIX = W11 / "PRODUCTION_STORY_DEPENDENCY_MATRIX_2026-11-20.md"
INDEX = W11 / "_INDEX.md"
EXPECTED_GIT_BLOBS = {
    str(REF): "638395e239946c186a33a602f3338bba449abb6c",
    str(SRC): "a2ffc1c8bfee329e2dd68d6c838914e9974667e3",
}
EXPECTED_SECTIONS = {"G": 6, "S": 6, "O": 6, "R": 6, "M": 6,
                     "D": 6, "W": 5, "F": 4, "P": 7, "I": 6}
ALIASES = {1: "ObiWan", 2: "Red Leopards", 3: "Slob", 4: "LLC",
           5: "DK", 6: "Three Dreaded Snake", 7: "Chili", 8: "HMB",
           9: "El Niño", 10: "Mud Dogs", 11: "Seven Deadly Chins",
           12: "Duckhook"}

def git_blob_sha(content: bytes):
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()

def money(value):
    try:
        return Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return Decimal("NaN")

def parse_answers(text):
    rows = []
    for m in re.finditer(r"^- \*\*([A-Z]\d{2})\*\* — (.+)$", text, re.MULTILINE):
        fields = m.group(2).split("; **Commissioner text:** ", 1)
        rows.append({"id": m.group(1),
                     "selection": fields[0],
                     "note": fields[1] if len(fields) == 2 else ""})
    return rows

def validate(root: Path, quiet=False):
    checks = []
    def check(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    required = (FOUND, REF, SRC, SYN, MATRIX, INDEX,
                Path("memo-os/week-9/WEEK_9_WEEK_10_PROVIDER_EVIDENCE_2026-11-20.json"))
    missing = [str(p) for p in required if not (root / p).is_file()]
    if missing:
        if not quiet: print("FAIL required inputs missing: " + ", ".join(missing))
        return 1

    raw = {p: (root / p).read_bytes() for p in required}
    founder, synthesis, matrix, index = [raw[p].decode("utf-8")
                                        for p in (FOUND, SYN, MATRIX, INDEX)]
    reference, fixture = [json.loads(raw[p]) for p in (REF, SRC)]
    provider = json.loads(raw[Path(fixture["source_path"])])

    for filename, pin in EXPECTED_GIT_BLOBS.items():
        check("trusted input pinned " + filename, git_blob_sha(raw[Path(filename)]) == pin)

    check("Founder source blob binding",
          git_blob_sha(raw[FOUND]) == reference["transcription_source_git_blob_sha"])
    check("source ESPN normalized blob binding",
          git_blob_sha(raw[Path(fixture["source_path"])]) == fixture["source_git_blob_sha"])
    check("captured provider identity",
          str(provider.get("league_id")) == str(fixture["league_id"]) == "1417621"
          and provider.get("season") == fixture["season"] == 2026
          and provider.get("observation_date") == "2026-11-20"
          and fixture.get("week") == 11)
    check("fixture explicitly provisional",
          fixture.get("scope") == "PROVISIONAL_CAPTURE_NO_FACT_LOCK"
          and fixture.get("ffhub_nov18", {}).get("status") == "NOT_REVERIFIED")

    actual = parse_answers(founder)
    baseline = reference.get("answers", [])
    check("58 unique Founder IDs and ten section counts",
          len(actual) == len(baseline) == 58
          and len({x["id"] for x in actual}) == 58
          and all(sum(x["id"].startswith(k) for x in actual) == n
                  for k, n in EXPECTED_SECTIONS.items()))
    check("all 58 exact normalized selections and free-text values",
          actual == baseline, "compared against separately pinned normalized transcript, not chat byte-for-byte")
    check("Owner G01 strategic control preserved",
          any(x["id"] == "G01" and x["selection"] == "Strategic control over the Commonwealth"
              for x in actual) and "strategic" in synthesis.lower())
    check("Founder boundary and family constraints preserved",
          "Exclude family matters" in founder
          and "household/new-baby elements out" in synthesis)
    check("Commissioner absent except note",
          "The Commissioner role must not exist except in the Commissioner's Note" in founder
          and "no diegetic commissioner character" in synthesis.lower())
    check("Island after Week14",
          "after Week 14" in synthesis
          and "not entered" in synthesis)
    check("GOTW inherited W10 bridge",
          "W10-P35" in synthesis and "LOC-BRIDGE-MOUNTAIN-LAKE" in synthesis
          and "no first strike" in synthesis.lower())
    check("Slob inherited W10 weather",
          "W10-P33" in synthesis and "LOC-SLOB-FOOTHILL-CAMP" in matrix)

    matches = provider["week11_matchups"]["matchups"]
    expected = fixture["matchups"]
    check("six provider matches, twelve distinct owners and UNDECIDED",
          len(matches) == len(expected) == 6
          and len({i for v in matches for i in (v["home"]["teamId"], v["away"]["teamId"])}) == 12
          and all(v["winner"] == "UNDECIDED" for v in matches))
    current = [
        {"home_id": m["home"]["teamId"], "home_name": m["home"]["teamName"],
         "home_current_points": money(m["home"]["currentPoints"]),
         "away_id": m["away"]["teamId"], "away_name": m["away"]["teamName"],
         "away_current_points": money(m["away"]["currentPoints"]),
         "winner": m["winner"]}
        for m in matches
    ]
    fixture_normalized = [{**m, "home_current_points": money(m["home_current_points"]),
                           "away_current_points": money(m["away_current_points"])}
                          for m in expected]
    check("six source-to-fixture exact matchup values",
          current == fixture_normalized)
    expected_scoreline = "; ".join(
        f'{ALIASES[m["home_id"]]} {money(m["home_current_points"]):.2f}–'
        f'{ALIASES[m["away_id"]]} {money(m["away_current_points"]):.2f}'
        for m in expected)
    check("six exact matrix live scorelines",
          expected_scoreline in matrix, "snapshot capture remains provisional")

    duck = next(m for m in expected if m["home_id"] == 12)
    chili = next(m for m in expected if m["away_id"] == 7)
    scoring = {x["player"]: x for x in fixture["scored_starters_secondary_flaim_detail"]}
    check("individual starter receipt team alignment",
          scoring["C.J. Stroud"]["team_id"] == duck["home_id"]
          and money(scoring["C.J. Stroud"]["points"]) == money(duck["home_current_points"])
          and scoring["Jonathan Taylor"]["team_id"] == duck["away_id"]
          and money(scoring["Jonathan Taylor"]["points"]) == money(duck["away_current_points"])
          and scoring["David Montgomery"]["team_id"] == chili["away_id"]
          and money(scoring["David Montgomery"]["points"]) == money(chili["away_current_points"])
          and all(x["started"] for x in scoring.values()))
    for player, pattern in {
        "C.J. Stroud": r"C\.J\. Stroud contributed \*\*([0-9]+\.[0-9]+) started Thursday points",
        "Jonathan Taylor": r"Jonathan Taylor ([0-9]+\.[0-9]+)",
        "David Montgomery": r"David Montgomery ([0-9]+\.[0-9]+) points",
    }.items():
        found = re.search(pattern, matrix)
        check("matrix/player point value " + player,
              bool(found and money(found.group(1)) == money(scoring[player]["points"])))

    house = fixture["pittsys_board"]
    keys = [f'{x["home_id"]}-{x["away_id"]}' for x in expected]
    status_keys = house["posted"] + house["off_board"] + house["unspecified"]
    check("Pittsy six-way exhaustive non-invented classification",
          len(house["posted"]) == 3 and len(house["off_board"]) == 2
          and len(house["unspecified"]) == 1
          and sorted(keys) == sorted(status_keys)
          and len(set(status_keys)) == 6)
    check("missing Mud/Chins house status explicit",
          house["unspecified"] == ["10-11"]
          and "HOUSE_BOARD_STATUS_UNSPECIFIED" in matrix
          and "not OFF BOARD" in matrix)
    check("Nov18 FFHub unverified in live copy",
          "NOT_REVERIFIED" in matrix
          and "November 18" in matrix)
    check("separate Road to Seven project",
          "Issue #319" in matrix and "separate isolated seven-PNG special" in matrix)

    for k in range(1, 7):
        segment = re.search(rf"^### W11-G0{k} —(.*?)(?=^### W11-G0[1-6] —|^## Issue-wide)",
                            matrix, re.MULTILINE | re.DOTALL)
        check(f"match {k} has win/loss and unresolved branches",
              bool(segment and segment.group(1).count("**If ") == 3
                   and re.search(r"\*\*If (?:tie|tie/undecided|tie/unknown)", segment.group(1))))
    check("no fixed page count and no final approval",
          "no folio counts" in matrix and "NO PAGE OR STORY LOCK" in matrix)
    check("index links to all governing input files",
          all(x in index for x in
              (FOUND.name, SYN.name, MATRIX.name,
               "INDEPENDENT_RED_TEAM_AUDIT_2026-11-20.md")))
    passed = sum(ok for _, ok, _ in checks)
    if not quiet:
        for name, ok, detail in checks:
            print(("PASS" if ok else "FAIL") + " " + name +
                  (" — " + detail if detail else ""))
        print(f"RESULT {passed}/{len(checks)} PASS; {len(checks)-passed} FAIL")
        print("Scope: pinned normalized/source-fixture integrity only; no independent source-provider or visual release authorization.")
    return 0 if passed == len(checks) else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    raise SystemExit(validate(args.root))
