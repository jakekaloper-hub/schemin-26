"""Check Week 11 folio navigation and flag refreshed sheets for relettering after a copy edit."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from zipfile import BadZipFile, ZipFile

DESK = Path(__file__).resolve().parent
PNG_DESK = "WEEK11_FOLIO_OG_COMPARISON"
ATLAS_DESK = "WEEK11_LOCATION_DESK"
REHEARSAL = "OPEN_BOARD_PAGE_REHEARSAL.md"
REFRESHED_FOLIOS = {"F12", "F13", "F14", "F21", "F22"}


def direction_digest(section, row):
    """Track the artist's source and the approved wording printed in the comparison."""
    # Navigation can change independently of the manuscript and printed instructions.
    body = section.split("\n[On the board]", 1)[0].strip()
    content = [body, row["week11_direction"], row["week11_acceptance_test"]]
    return hashlib.sha256("\n".join(content).encode()).hexdigest()


def validate(pack):
    manuscript = (DESK / REHEARSAL).read_text()
    pieces = re.split(r'<a id="folio-(\d{2})"></a>', manuscript)
    sections = dict(zip(pieces[1::2], pieces[2::2]))
    numbers = [f"{n:02d}" for n in range(1, 36)]
    if pieces[1::2] != numbers:
        raise ValueError("Expected 35 unique, ordered rehearsal anchors")
    png = json.loads((DESK / f"{PNG_DESK}.json").read_text())
    atlas = json.loads((DESK / f"{ATLAS_DESK}.json").read_text())
    png_text = (DESK / f"{PNG_DESK}.md").read_text()
    atlas_text = (DESK / f"{ATLAS_DESK}.md").read_text()
    selected = json.loads((DESK / "W11_POST_MNF_ALL_35_FOLIO_SELECTED_CUTS_2026-11-24.json").read_text())
    lettering = (DESK / selected["reader_lettering"]).read_text()
    reader_parts = re.split(r"^## (F\d{2}) · [^\n]+\n", lettering, flags=re.MULTILINE)
    folios = selected["folios"]
    if reader_parts[1::2] != [f"F{nn}" for nn in numbers] or len(folios) != len(numbers):
        raise ValueError("Reader lettering and selection must contain 35 ordered folios")
    reader = dict(zip(reader_parts[1::2], reader_parts[2::2], strict=True))
    if reader["F02"].strip() != folios[1]["updated_copy"]:
        raise ValueError("F02: Opening Drive lettering differs from the selected result")
    source = json.loads((DESK / "W11_POST_MNF_FLAIM_ESPN_SOURCE_2026-11-24.json").read_text())
    rows = []
    for game in source["week11"]["matchups"]:
        away, home = game["away"], game["home"]
        rows.append(f"| {away['name']} | {away['score']:.2f} | {home['name']} | {home['score']:.2f} |")
    printed = [line.replace("’", "'").replace("**", "") for line in reader["F04"].splitlines() if line.startswith("| ")]
    if sorted(printed[2:]) != sorted(rows):
        raise ValueError("F04: printed visitor/home scores differ from the final ESPN games")
    expected_members = []
    for nn, row, place, cut in zip(numbers, png["folios"], atlas["folios"], folios, strict=True):
        folio = "F" + nn
        if row["folio"] != folio or place["folio"] != folio or cut["folio"] != folio:
            raise ValueError(f"{folio}: folio IDs disagree")
        if not (cut["updated_copy"] == row["post_mnf_selected_cut"] == place["post_mnf_selected_story_cut"]):
            raise ValueError(f"{folio}: selected production cut differs between desks")
        rehearsal_target = f"{REHEARSAL}#folio-{nn}"
        for name, anchor, register in [(PNG_DESK, "compare", png_text), (ATLAS_DESK, "atlas", atlas_text)]:
            target = f"{name}.md#{anchor}-{nn}"
            if f"]({target})" not in sections[nn]:
                raise ValueError(f"{folio}: missing desk link {target}")
            table_row = next((line for line in register.splitlines() if f'id="{anchor}-{nn}"' in line), "")
            if f"]({rehearsal_target})" not in table_row:
                raise ValueError(f"{folio}: desk row does not return to its commission")
        for active, frozen in [(row["rehearsal_source"], row["capture_rehearsal_source"]),
                               (place["folio_source"], place["capture_folio_source"])]:
            if (active != png["sources"]["current_rehearsal"] + "#folio-" + nn
                    or active == frozen or not frozen.endswith("/" + rehearsal_target)):
                raise ValueError(f"{folio}: current and historical sources do not resolve separately")
        if folio in REFRESHED_FOLIOS and not all(
            row.get(field) for field in ("instruction_source", "instruction_digest", "week11_direction")
        ):
            raise ValueError(f"{folio}: missing evidence for refreshed instructions")
        if "instruction_source" in row and direction_digest(sections[nn], row) != row["instruction_digest"]:
            raise ValueError(f"{folio}: commission or printed instructions changed; reopen this comparison")
        member = row["comparison_pack_member"]
        if not member.startswith(f"Folios/{folio}-") or not member.endswith(".png"):
            raise ValueError(f"{folio}: wrong comparison pack member {member}")
        expected_members.append(member)
        if pack is not None:
            if hashlib.sha256(pack.read(member)).hexdigest() != row["comparison_sheet_sha256"]:
                raise ValueError(f"{folio}: comparison PNG does not match the register")
    if pack is not None:
        expected = [*expected_members, "Week-11-Folio-Contact-Sheet.png"]
        if sorted(pack.namelist()) != sorted(expected) or pack.testzip() is not None:
            raise ValueError("Incorrect archive contents or damaged ZIP")
    return len(sections)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", type=Path, help="optional private Week 11 comparison ZIP")
    args = parser.parse_args()
    try:
        if args.pack:
            with ZipFile(args.pack) as archive:
                count = validate(archive)
        else:
            count = validate(None)
    except (ValueError, KeyError, OSError, BadZipFile) as exc:
        sys.exit(str(exc))
    print(f"{count} Week 11 folio routes validated" + ("; 35 private PNGs matched" if args.pack else ""))
