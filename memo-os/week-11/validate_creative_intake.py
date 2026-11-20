#!/usr/bin/env python3
"""Deterministic Week 11 creative-intake consistency checks (not publication QA).

Run at repository root:
    python3 memo-os/week-11/validate_creative_intake.py
Run elsewhere:
    python3 validate_creative_intake.py --root /path/to/schemin-26

No external API, renderer, provider, artwork, or authorial judgments are certified.
"""
import argparse
import re
from pathlib import Path

REL = Path("memo-os/week-11")
EXPECTED = {"G": 6, "S": 6, "O": 6, "R": 6, "M": 6,
            "D": 6, "W": 5, "F": 4, "P": 7, "I": 6}


def validate(root: Path):
    files = {
        "founder": REL / "FOUNDER_CREATIVE_INTERVIEW_58_RESPONSES_2026-11-20.md",
        "synthesis": REL / "FOUNDER_STORY_ROOM_SYNTHESIS_2026-11-20.md",
        "matrix": REL / "PRODUCTION_STORY_DEPENDENCY_MATRIX_2026-11-20.md",
        "index": REL / "_INDEX.md",
    }
    missing = [str(path) for path in files.values() if not (root / path).is_file()]
    if missing:
        raise FileNotFoundError("Missing required files: " + ", ".join(missing))
    txt = {name: (root / path).read_text(encoding="utf-8") for name, path in files.items()}
    f, s, m, i = (txt[x] for x in ("founder", "synthesis", "matrix", "index"))
    checks = []

    def check(name, good, evidence=""):
        checks.append((name, bool(good), evidence))

    ids = re.findall(r"^- \*\*([A-Z]\d{2})\*\* —", f, re.M)
    check("58 distinct answers", len(ids) == 58 and len(set(ids)) == 58, f"{len(ids)} total / {len(set(ids))} unique")
    counts = {p: sum(x.startswith(p) for x in ids) for p in EXPECTED}
    check("all 10 answer sections", counts == EXPECTED, str(counts))
    check("Founder source is creative, not Fact Lock", "NOT FACT LOCK" in f and "not independent historical verification" in f)
    check("GOTW W10-P35 bridge source", "W10-P35" in s and "LOC-BRIDGE-MOUNTAIN-LAKE" in s and "no first strike" in s.lower())
    check("Slob W10-P33 source", "W10-P33" in s and "LOC-SLOB-FOOTHILL-CAMP" in m)
    match_ids = re.findall(r"^### W11-G0([1-6]) —", m, re.M)
    check("six distinct match dossiers", sorted(match_ids) == list("123456"), str(match_ids))
    for k in range(1, 7):
        z = re.search(rf"^### W11-G0{k} —(.*?)(?=^### W11-G0[1-6] —|^## Issue-wide)", m, re.M | re.S)
        check(f"match {k}: distinct outcome forks", bool(z and z.group(1).count("**If ") >= 2 and ("**If tie" in z.group(1) or "tie" in z.group(1).lower())))
    for name in ("D0nkey K0ng", "His Majesty's Blood", "Slob on my Dobb", "El Niño", "ObiWan Jacoby", "Chili", "Red Leopards", "Three Dreaded Snake", "Seven Deadly Chins", "Mud Dogs", "Dr. Duckhook", "The LLC"):
        check("team covered: " + name, name in m)
    candidates = s.split("**Seven Inklings / production-room candidates", 1)
    sporting = candidates[1].split("**Preliminary recommendation", 1)[0] if len(candidates) > 1 else ""
    check("seven sporting concepts", len(re.findall(r"^[1-7]\. ", sporting, re.M)) == 7)
    check("Pittsy's Nov19 board: 3 posted + 2 off", all(x in m for x in ("three posted games", "two explicitly off-board", "Issue #323")))
    check("Road to Seven separate", "Issue #319" in m and "separate isolated seven-PNG special" in m)
    check("Postseason island timing", "after Week 14" in s and "not entered" in s)
    check("Commissioner character restricted", "no diegetic commissioner character" in s.lower() and "Commissioner's Note" in s)
    check("Mud Dogs outcome contingent", "If Mud wins" in m and "If Chins wins" in m and "no Cancún" in m)
    check("Duckhook non-golf venue unresolved", "NOT a golf course" in s and "NOT YET FOUND" in m)
    check("Nov18 FFHub attribution explicitly withheld", "NOT_REVERIFIED" in m and "November 18" in m)
    check("No predetermined page count", "No fixed pages" in s and "no folio counts" in m)
    check("No fake consultant approval", "No actual Tim Veil human attendance" in s and "No authenticated external person" in m)
    check("Index resolves source and synthesis", all(x in i for x in ("FOUNDER_CREATIVE_INTERVIEW_58_RESPONSES_2026-11-20.md", "FOUNDER_STORY_ROOM_SYNTHESIS_2026-11-20.md", "PRODUCTION_STORY_DEPENDENCY_MATRIX_2026-11-20.md")))

    for name, good, evidence in checks:
        print(("PASS" if good else "FAIL") + " " + name + (f" — {evidence}" if evidence else ""))
    passed = sum(g for _, g, _ in checks)
    print(f"RESULT {passed}/{len(checks)} PASS; {len(checks) - passed} FAIL")
    print("Scope: documentary consistency only; independent Umpire, sports Fact Lock, page/visual QA and publication remain separate.")
    return 0 if passed == len(checks) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = ap.parse_args()
    raise SystemExit(validate(args.root))


if __name__ == "__main__":
    main()
