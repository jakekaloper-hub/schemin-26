"""Reproducible, nonpublishing 42-part 2016 causal reader builder.

Appends source-exact Chapter XLV V2 to the *existing 41-part reader* without
modifying its 41 component bodies. The predecessor is a frozen input. Any
hash, manifest, or component discrepancy fails closed. The generated file is
an editorial development artifact, NEVER hard canon or public release.
"""
from __future__ import annotations
import argparse
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
PREVIOUS = "READING_COPY_2016_CAUSAL_CH01_44_FORTY_ONE_PARTS_BOOT_THRESHOLD_NONCANON.md"
PREVIOUS_SHA = "b8ea32a932cfeeebc0f5f359ed90eed0a776918d"
CHAPTER = "THE_ROAD_THAT_WOULD_NOT_WAIT_MEASURE_OF_EMPTY_BOWL_CH45_V2_NONCANON.md"
CHAPTER_SHA = "5b7fa2e705d633a3599668dc13cb6dc15e74201c"
OLD_TOTAL = 316215
NEW_WORDS = 7275
TOTAL = OLD_TOTAL + NEW_WORDS
TERMINAL = "<!-- END_CAUSAL_READING_COPY -->"
ROW_RE = re.compile(r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", re.M)
START_RE = re.compile(r"<!-- BEGIN 2016_CAUSAL ")

def gitblob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def build(previous: str, chapter: str) -> str:
    """Construct entire reader, preserving all previous 41 marked sections."""
    if previous.count(TERMINAL) > 1:
        raise ValueError("ambiguous previous terminal markers")
    if len(START_RE.findall(previous)) != 41 or previous.count("<!-- END 2016_CAUSAL ") != 41:
        raise ValueError("prior component marker count mismatch")
    previous_rows = ROW_RE.findall(previous)
    if [int(row[0]) for row in previous_rows] != list(range(1, 42)):
        raise ValueError("prior 41-part source manifest incomplete/out of order")
    if sum(int(row[3]) for row in previous_rows) != OLD_TOTAL:
        raise ValueError("previous reader word total mismatch")
    if len(chapter.split()) != NEW_WORDS:
        raise ValueError("V2 chapter word count drift")
    first = previous.index("<!-- BEGIN 2016_CAUSAL ")
    header, rest = previous[:first], previous[first:]
    old_row = re.compile(r"(?m)^\| 41 \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$")
    if len(old_row.findall(header)) != 1:
        raise ValueError("cannot locate manifest row 41")
    new_row = f"| 42 | `{CHAPTER}` | `{CHAPTER_SHA}` | {NEW_WORDS} |"
    header = old_row.sub(lambda m: m.group(0) + "\n" + new_row, header)
    if f"Source component words including metadata: {OLD_TOTAL}" not in header:
        raise ValueError("previous total header is absent")
    header = header.replace(
        f"Source component words including metadata: {OLD_TOTAL}",
        f"Source component words including metadata: {TOTAL}"
    ).replace("41-part", "42-part").replace("41 parts", "42 parts")
    if rest.count(TERMINAL) == 1:
        before_end, after_end = rest.split(TERMINAL, 1)
    else:
        end_matches = list(re.finditer(r"<!-- END 2016_CAUSAL [^>]* -->", rest))
        if len(end_matches) != 41:
            raise ValueError("prior component end markers missing")
        before_end = rest[:end_matches[-1].end()]
        after_end = rest[end_matches[-1].end():]
    start = f"<!-- BEGIN 2016_CAUSAL {CHAPTER} | git_blob {CHAPTER_SHA} -->"
    end = f"<!-- END 2016_CAUSAL {CHAPTER} -->"
    appended = "\n\n" + start + "\n\n" + chapter.rstrip("\n") + "\n\n" + end + "\n\n"
    result = (
        "# 42-part cumulative developmental edition — Chapter XLV V2 / NONCANON\n"
        "Source-exact print proof only. Independent review HOLD; no canon/publication.\n\n"
        + header + before_end.rstrip() + appended + TERMINAL + after_end
    )
    rows = ROW_RE.findall(result)
    if [int(row[0]) for row in rows] != list(range(1, 43)):
        raise ValueError("generated manifest is incomplete")
    if sum(int(x[3]) for x in rows) != TOTAL:
        raise ValueError("generated total mismatch")
    if len(START_RE.findall(result)) != 42 or result.count("<!-- END 2016_CAUSAL ") != 42:
        raise ValueError("generated marker count mismatch")
    prior_start = previous.index("<!-- BEGIN 2016_CAUSAL ")
    prior_end = prior_start + len(before_end)
    new_start = result.index("<!-- BEGIN 2016_CAUSAL ")
    new_end = result.index(start)
    if previous[prior_start:prior_end].rstrip() != result[new_start:new_end].rstrip():
        raise ValueError("41 predecessor bodies mutated during assembly")
    if result.split(start + "\n\n", 1)[1].split("\n\n" + end, 1)[0] != chapter.rstrip("\n"):
        raise ValueError("new chapter body mismatch")
    return result

def build_from_repo() -> str:
    previous_bytes = (BASE / PREVIOUS).read_bytes()
    chapter_bytes = (BASE / CHAPTER).read_bytes()
    if gitblob(previous_bytes) != PREVIOUS_SHA:
        raise ValueError("stale previous 41-part blob")
    if gitblob(chapter_bytes) != CHAPTER_SHA:
        raise ValueError("stale Chapter XLV V2 blob")
    return build(previous_bytes.decode("utf-8"), chapter_bytes.decode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    edition = build_from_repo()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(edition, encoding="utf-8")
    print(f"NONCANON assembled 42 source-exact components, {TOTAL} source words at {args.output}")
