"""Build an archival inventory and isolated, portable draft reading surface.

No publication registry, source manuscript or canon file is changed. Standard
library only; source text is HTML-escaped, never interpreted as executable HTML.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
MISSION = HERE.parent
ROOT = next(p for p in HERE.parents if (p / "SCHEMIN_26_PROJECT_MISSION.md").is_file())
BASELINE = "8fcb77191955f413fe970154d47632770f923055"
INVENTORY = MISSION / "inventory"
HARD_CANON = {
    "PROLOGUE_DRAFT_V1.md", "CHAPTER_01_THE_FIRST_ANSWER.md",
    "CHAPTER_02_WHAT_COMES_BACK.md", "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md",
}
LEGACY_READER_EXCLUDED = HARD_CANON - {"CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"}
# Explicit editorial order for these mission lanes, not filename inference.
SCENE_LANES = {
    "2015-jake-week1": (-3, "2015 Week 1 connected-account Jake candidate; user-attested identity plus Flaim continuity; no opponent identity"),
    "2015-jake-arc": (-2, "2015 Weeks 2–15 connected-account Jake candidate; user-attested identity plus Flaim continuity; no opponent identity"),
    "2016-jake-arc": (-1, "2016 connected-account Jake candidate; user-attested identity plus Flaim continuity; no opponent identity"),
    "2017-jake-turning": (0, "2017 selected connected-account Jake turning fixtures; Flaim event-level team-1 join; no opponent identity"),
    "2018-jake-breakwater": (1, "2018 connected-account Jake candidate; Flaim event-level team-1 join; no opponent identity"),
    "2024-title": (2, "2024 title aftermath only; no 2025 knowledge; event-scoped fictional identity support, raw human-owner UNKNOWN"),
    "2025-reckoning": (2, "2025 named postseason events only; no 2026 knowledge; event-scoped fictional identity support, raw human-owner UNKNOWN"),
    "2026": (3, "After Chapter III; before Week 4 results"),
    "2026-week4": (4, "Week 4 consequence lane"),
    "2026-week5": (5, "Week 5 consequence lane"),
    "2026-week6": (6, "Week 6 consequence lane; no Week 7 result"),
    "2026-week6-wetland": (7, "Same post-Week-6/pre-Week-7-result window; display order only, not proved temporal ordering of separate geographic events"),
}
EXPLICIT_LITERARY_FILES = ("2026-week5/A_DOOR_WIDE_ENOUGH_NONCANON.md",)
HISTORICAL_LANES = {"2015-jake-week1", "2015-jake-arc", "2016-jake-arc", "2017-jake-turning", "2018-jake-breakwater", "2024-title", "2025-reckoning"}
HISTORICAL_BINDING_AUDIT = MISSION / "evidence/HISTORICAL_BINDING_AUDIT_2022_2025.json"
CONNECTED_ACCOUNT_AUDIT = MISSION / "evidence/owner-extraction-audit/FLAIM_CONNECTED_ACCOUNT_CONTINUITY.md"


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_url(path: str) -> str:
    return f"https://github.com/jakekaloper-hub/schemin-26/blob/{BASELINE}/{path}"


def source_paths() -> list[Path]:
    paths = set((ROOT / "living-novel/manuscript").rglob("*.md"))
    chronicle = ROOT / "living-novel/historical-chronicle"
    paths.update(chronicle.glob("seasons/*/weeks/W[0-9][0-9].md"))
    for name in ("PROLOGUE.md", "POSTSEASON.md", "EPILOGUE.md"):
        paths.update(chronicle.glob(f"seasons/*/{name}"))
    paths.update((chronicle / "author-room").glob("*.md"))
    paths.update((ROOT / "living-novel/production/historical-saga/R53").glob("*NONCANON*.md"))
    rewrite = ROOT / "living-novel/production/full-rewrite-2026"
    paths.update((rewrite / "manuscript").glob("*.md"))
    paths.update((rewrite / "drafts").glob("*.md"))
    paths.update(rewrite.glob("*NONCANON.md"))
    paths.update(rewrite.glob("*READING_CANDIDATE.md"))
    return sorted(paths)


def classify(path: Path) -> tuple[str, str, str]:
    key = relative(path)
    if path.parent == ROOT / "living-novel/manuscript" and path.name in HARD_CANON:
        risk = " Retired institutional POV prevents active reader reuse; preserve source and use separately reviewed reconstruction." if path.name in LEGACY_READER_EXCLUDED else " Candidate reuse still requires current scene/temporal reconciliation."
        return "PRESERVED_HARD_CANON_SOURCE", "2026", "Whole-book matrix identifies hard manuscript canon; no new acceptance or overwrite." + risk
    if "/manuscript/v3/" in key:
        return "SUPERSEDED_SOURCE_ONLY", "2026", "Whole-book matrix rejects v3 as replacement authority; recover unique passages only after fact, POV and continuity reconciliation."
    if "/historical-chronicle/seasons/" in key:
        year = key.split("/seasons/")[1].split("/")[0]
        note = "Preserve original text and fixture anchors; owner-era and location bindings remain unresolved."
        if year == "2015" and "/weeks/" in key:
            note += " Existing 2015 audit recognizes structural coverage but FAILS final literary quality; revise conditional summary into eligible scenes when bindings are available."
        else:
            note += " Threshold/partial draft is not a completed or accepted season movement."
        return "EXISTING_HISTORICAL_DRAFT_REQUIRES_REVISION", year, note
    if "/R53/" in key or "/historical-chronicle/author-room/" in key:
        year = next((y for y in ("2022", "2024", "2025", "2026") if y in path.name), "UNRESOLVED")
        return "EXISTING_LITERARY_PILOT_NONCANON", year, "Recover dramatic questions and useful prose; pilot is not a book. Raw human-owner proof, venue and independent acceptance remain open. The mission historical binding audit separately identifies narrow fictional event associations for 2024/2025; it does not promote this pilot or establish a whole-season license."
    if "/full-rewrite-2026/" in key:
        year = "2022" if "2022" in path.name else "2026"
        assembly = " This is an assembled reading candidate; its contents must not be counted again as unique prose." if "READING_CANDIDATE" in path.name else ""
        return "EXISTING_REWRITE_CANDIDATE_NONCANON", year, "Preserve lineage and compare versions; later filename alone does not establish supersession or acceptance. Recheck current anatomy, POV, source cutoff and world state." + assembly
    return "EXISTING_MANUSCRIPT_ACCEPTANCE_UNVERIFIED", "2026", "Manuscript exists, but its presence does not prove canon or release authority; resolve owning acceptance before reuse."


def inventory_rows() -> list[dict]:
    tracked = subprocess.check_output(["git", "ls-tree", "-r", BASELINE], cwd=ROOT, text=True)
    blobs = {line.split("\t", 1)[1]: line.split()[2] for line in tracked.splitlines()}
    rows = []
    for path in source_paths():
        status, season, reuse = classify(path)
        content = path.read_text()
        title = next((line.lstrip("# ") for line in content.splitlines() if line.startswith("#")), path.stem)
        rows.append({"path": relative(path), "title": title, "season": season,
                     "sha256": digest(path), "baseline_git_blob": blobs.get(relative(path)),
                     "status": status, "reuse_note": reuse,
                     "diagnostic_word_count_including_metadata": len(content.split()),
                     "active_reader_inclusion": False,
                     "reader_exclusion": "Preserved source archive; not implicitly accepted as current mission manuscript."})
    return rows


def render_markdown(text: str) -> str:
    """Small safe reading renderer; retain unknown Markdown as literal text."""
    output, paragraph = [], []
    def flush():
        if paragraph:
            output.append("<p>" + "<br>".join(html.escape(s) for s in paragraph) + "</p>")
            paragraph.clear()
    for line in text.splitlines():
        if not line.strip():
            flush()
        elif re.match(r"^#{1,6} ", line):
            flush()
            level = min(len(line) - len(line.lstrip("#")) + 1, 6)
            output.append(f"<h{level}>" + html.escape(line.lstrip("# ")) + f"</h{level}>")
        elif line.strip() == "---":
            flush()
            output.append("<hr>")
        else:
            paragraph.append(line)
    flush()
    return "\n".join(output)


def manuscript_order(path: Path) -> tuple[int, str]:
    if path.parent.name not in SCENE_LANES:
        raise ValueError(f"No explicit scene chronology for mission lane {path.parent.name!r}; resolve its cutoff before reader assembly.")
    return SCENE_LANES[path.parent.name][0], path.name


def mission_manuscripts() -> list[Path]:
    # Deliberately exclude packets/review documents; add literary titles here as
    # the mission produces them, without selecting a canonical edition.
    paths = set((MISSION / "manuscript").glob("*/THE_*.md"))
    for name in EXPLICIT_LITERARY_FILES:
        path = MISSION / "manuscript" / name
        if not path.is_file():
            raise FileNotFoundError(f"Explicitly registered literary manuscript missing: {name}")
        paths.add(path)
    if any(path.parent.name in {"2024-title", "2025-reckoning"} for path in paths) and not HISTORICAL_BINDING_AUDIT.is_file():
        raise FileNotFoundError("Historical manuscript requires the event-scoped fictional binding audit; missing raw owner fields cannot be silently promoted.")
    if any(path.parent.name in {"2015-jake-week1", "2015-jake-arc", "2016-jake-arc", "2017-jake-turning", "2018-jake-breakwater"} for path in paths) and not CONNECTED_ACCOUNT_AUDIT.is_file():
        raise FileNotFoundError("2015 Jake candidate requires the Flaim connected-account audit.")
    return sorted(paths, key=manuscript_order)


def scope_disclosure(manuscripts: list[Path]) -> str:
    historical = [p for p in manuscripts if p.parent.name in HISTORICAL_LANES]
    current = [p for p in manuscripts if p.parent.name not in HISTORICAL_LANES]
    if historical:
        summary = f"<strong>This reader includes {len(historical)} proposed historical sequence(s) and {len(current)} current-2026 sequence(s). No historical season is complete.</strong> Historical material is limited to 2024/2025 event-scoped fictional associations and one 2015 Jake candidate supported by user-attested identity plus Flaim connected-account continuity. Raw human-owner identity remains UNKNOWN; neither route identifies other historical owners."
    else:
        summary = "<strong>All new prose currently included in this reader concerns 2026. No new historical manuscript is included yet.</strong> Narrow 2024/2025 fictional event lanes have been identified, but planned files do not count as written prose."
    return summary + ' Broader 2015–2025 coverage remains incomplete; no whole-season identity license follows from these exceptions. Read the <a href="../evidence/HISTORICAL_BINDING_AUDIT_2022_2025.md">event-scoped historical binding audit and correction to the earlier blanket hold</a>. Existing historical drafts remain preserved, and new geography, dialogue and consequences remain proposed.'


def coverage_summary() -> tuple[str, dict | None]:
    path = MISSION / "evidence/SEASON_DENOMINATORS.json"
    if not path.is_file():
        return "<p>Coverage audit is still being assembled.</p>", None
    evidence = json.loads(path.read_text())
    table = ["<section id=\"coverage\"><h2>Source coverage</h2>",
             "<p>Observed source contests are not certified complete schedules or accepted literary coverage. Unpaired rows remain separate; missing data is not an absent fixture. Existing prose remains preserved.</p>",
             "<table><caption>Historical source denominator audit</caption><thead><tr><th scope=\"col\">Season</th><th scope=\"col\">Regular paired</th><th scope=\"col\">Postseason paired</th><th scope=\"col\">Unpaired</th><th scope=\"col\">Repeated rows</th></tr></thead><tbody>"]
    for season in evidence["seasons"]:
        values = [season.get(k, "Unresolved") for k in ("season", "regular_season_contests", "postseason_contests", "unpaired_rows", "duplicate_display_rows")]
        table.append("<tr>" + "".join("<td>" + html.escape(str(v)) + "</td>" for v in values) + "</tr>")
    table.append('</tbody></table><p><a href="../evidence/SOURCE_COVERAGE_AUDIT.md">Read limitations and latest verified 2026 cutoff</a> · <a href="../evidence/SEASON_DENOMINATORS.json">Machine-readable denominators</a></p></section>')
    return "\n".join(table), {"path": relative(path), "sha256": digest(path)}


def build() -> dict:
    INVENTORY.mkdir(exist_ok=True)
    rows = inventory_rows()
    inventory = {"schema_version": 1, "baseline_revision": BASELINE,
                 "status": "READ_ONLY_SOURCE_INVENTORY_NOT_ACCEPTANCE",
                 "scope": "Historical chronicle prose, R53 pilots, manuscript tree including v3, full-rewrite manuscript/draft/reading candidates",
                 "counting_rule": "File counts and metadata-inclusive word counts are diagnostic, not unique manuscript length or literary acceptance.",
                 "sources": rows}
    (INVENTORY / "MANUSCRIPT_INVENTORY.json").write_text(json.dumps(inventory, indent=2) + "\n")
    report = ["# Existing manuscript inventory", "", f"Baseline: `{BASELINE}`. No original manuscript was edited.", "",
              "Existing prose is preserved, not relabeled unwritten. The 2015 regular-season audit explicitly reports 78 fixture anchors and literary FAIL; this inventory does not infer literary completion from files or length. Missing historical owner-era binding blocks unsupported principal scenes. The mission's HISTORICAL_BINDING_AUDIT_2022_2025 identifies narrow hard-fiction event associations for 2024/2025 without promoting raw human-owner UNKNOWN fields or granting whole-season permission. 2016 contains partial material. R53 contains pilots, not completed books. The original Prologue and Chapters I–III remain preserved hard-canon sources; legacy institutional POV material is excluded from this draft reading surface. Chapter IV's presence alone is not a release receipt.", "",
              "All entries remain archive links; only new mission manuscripts are embedded in the isolated reader. An assembled candidate can duplicate other entries, so counts must not be summed as unique prose.", "",
              "| Source | Season | Disposition | SHA-256 | Reuse action |", "|---|---|---|---|---|"]
    for row in rows:
        report.append(f"| [{row['path']}]({source_url(row['path'])}) | {row['season']} | {row['status']} | `{row['sha256']}` | {row['reuse_note']} |")
    (INVENTORY / "MANUSCRIPT_INVENTORY.md").write_text("\n".join(report) + "\n")
    manuscripts = mission_manuscripts()
    chapters, links, entries = [], [], []
    for i, path in enumerate(manuscripts, 1):
        anchor = f"manuscript-{i}"
        title = next((s.lstrip("# ") for s in path.read_text().splitlines() if s.startswith("#")), path.stem)
        links.append(f'<li><a href="#{anchor}">{html.escape(title)}</a></li>')
        historical_metadata = {}
        if path.parent.name in {"2024-title", "2025-reckoning"}:
            historical_metadata = {"raw_human_owner_status": "UNKNOWN", "fictional_binding_audit": relative(HISTORICAL_BINDING_AUDIT), "fictional_binding_audit_sha256": digest(HISTORICAL_BINDING_AUDIT)}
        elif path.parent.name in {"2015-jake-week1", "2015-jake-arc", "2016-jake-arc", "2017-jake-turning", "2018-jake-breakwater"}:
            historical_metadata = {"raw_human_owner_status": "UNKNOWN", "identity_basis": "USER_ATTESTED_IDENTITY_PLUS_PROVIDER_CONNECTED_ACCOUNT_CONTINUITY", "connected_account_audit": relative(CONNECTED_ACCOUNT_AUDIT), "connected_account_audit_sha256": digest(CONNECTED_ACCOUNT_AUDIT)}
        entries.append({"path": relative(path), "sha256": digest(path), "anchor": anchor,
                        "scene_lane_order": SCENE_LANES[path.parent.name][0],
                        "scene_cutoff_label": SCENE_LANES[path.parent.name][1],
                        "status": "DRAFT_NONCANON_NO_RELEASE_APPROVAL",
                        "scope": "EVENT_SCOPED_HISTORICAL_FICTION" if path.parent.name in HISTORICAL_LANES else "CURRENT_2026_DRAFT",
                        **historical_metadata})
        chapters.append(f'<article id="{anchor}"><p class="badge">Draft · noncanon · no release approval</p><p>{html.escape(SCENE_LANES[path.parent.name][1])}</p><p class="source">{html.escape(relative(path))}<br>SHA-256: {digest(path)}</p>{render_markdown(path.read_text())}<p><a href="#contents">Back to contents</a></p></article>')
    source_items = []
    for row in rows:
        source_items.append(f'<li><a href="{html.escape(source_url(row["path"]), quote=True)}">{html.escape(row["path"])}</a> — {html.escape(row["status"])}<p>{html.escape(row["reuse_note"])}</p></li>')
    body = "\n".join(chapters) or "<p>No new mission manuscript is present yet. This is an inventory preview, not a completed reader.</p>"
    coverage, coverage_source = coverage_summary()
    page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Commonwealth saga — draft reading room</title>
<style>body{margin:0;background:#f8f5ee;color:#241f1b;font:18px/1.65 Georgia,serif}main{max-width:76ch;margin:auto;padding:2rem 1.2rem}h1,h2,h3{line-height:1.25}a{color:#165777}a:focus{outline:3px solid #a64d16;outline-offset:3px}.notice{border-left:5px solid #a64d16;padding:1rem;background:#fff}.badge{font:bold .85rem system-ui;color:#733817}.source{font: .8rem/1.5 monospace;overflow-wrap:anywhere}article{border-top:2px solid #c5bbaa;margin-top:3rem;padding-top:2rem}p{margin:1em 0}details{margin-top:2rem}li{margin:.7rem 0}li p{font-size:.9rem}nav{background:#eee8dc;padding:1rem 1.5rem}table{width:100%;border-collapse:collapse;font: .85rem/1.4 system-ui}td,th{padding:.45rem;border-bottom:1px solid #c5bbaa;text-align:left}caption{text-align:left;margin-bottom:.6rem}@media print{body{background:white}nav,details{display:none}article{break-before:page}.source{font-size:9pt}}</style></head><body><main>
<h1>Commonwealth saga</h1><p>Isolated draft reading room · 2015–2026 mission</p>
<div class="notice"><strong>Partial production; not a finished saga or canonical release.</strong><p>''' + scope_disclosure(manuscripts) + '''</p><p>The 2026 lane stops at verified events; each included draft has its own earlier scene cutoff. No future result is invented. New scenes and durable consequences remain proposed. <a href="../CANDIDATE_EVENT_LINKS.json">Candidate scene-to-event links</a> establish draft traceability, not accepted coverage. Read the <a href="../evidence/HISTORICAL_UNBLOCK_CHECK_2026_10_24.md">initial historical unblock check</a> and <a href="../evidence/provider-readback/READBACK_INDEX.json">fresh provider-readback index</a>; the later binding audit above corrects the initial blanket fictional hold without changing raw owner fields.</p><p>This local preview embeds new mission prose. Preserved manuscripts remain source archive links, not silently approved reader paths. No publication manifest, canon or service was changed.</p></div>
<nav id="contents" aria-label="Draft contents"><h2>Draft contents</h2><ul>''' + "".join(links) + '''</ul><p><a href="../inventory/MANUSCRIPT_INVENTORY.md">Source inventory</a> · <a href="../ALL_SEASON_PROGRESS.json">All twelve seasons: observed denominators and proposed coverage</a> · <a href="../evidence/">Evidence and coverage files</a></p><p>A scene may link several events. Scene counts, scene-to-event links and distinct linked events are different measures; none establishes accepted coverage or a completed season.</p></nav>
''' + body + coverage + '''<details><summary>Preserved source archive — not active manuscript approval</summary><p>Links target the inspected baseline revision. Original text may contain superseded POV or anatomy; archive links do not license its use in new prose.</p><ul>''' + "".join(source_items) + '''</ul></details></main></body></html>'''
    (HERE / "index.html").write_text(page)
    manifest = {"schema_version": 1, "baseline_revision": BASELINE,
                "status": "PARTIAL_DRAFT_PREVIEW_NOT_PUBLICATION",
                "scope": "Local read-only presentation; no canon, release, interactive-owner-path or browser-acceptance claim.",
                "manuscripts": entries, "source_inventory_count": len(rows), "coverage_source": coverage_source,
                "output_sha256": digest(HERE / "index.html")}
    (HERE / "READER_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
