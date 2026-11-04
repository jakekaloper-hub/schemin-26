"""Build source-exact 43-part 2016 NONCANON developmental manuscript in memory.

Reuse the established 42-part builder, verify its 42 source-blob anchors,
append new Chapter XLVI V2 as component 43, and fail closed on drift.
This is an author-side assembly tool, not publication or approval.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
PRIOR_BUILDER = Path(__file__).with_name("build_2016_causal_42_part_bowl_reader.py")
CHAPTER = "THE_DISTANCE_BETWEEN_TWO_GATES_CART_WITHOUT_A_STRAIGHT_WHEEL_CH46_V2_NONCANON.md"
CHAPTER_SHA = "7d13718436fd4a84d37ba5093a920052bb870787"
PRIOR_WORDS = 323490
NEW_WORDS = 7833
WORDS = PRIOR_WORDS + NEW_WORDS
TERMINAL = "<!-- END_CAUSAL_READING_COPY -->"
BEGIN = "<!-- BEGIN 2016_CAUSAL "
END = "<!-- END 2016_CAUSAL "
ROW = re.compile(r"(?m)^\\| (\\d+) \\| `([^`]+)` \\| `([a-f0-9]{40})` \\| (\\d+) \\|$")

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(text: str):
    return [(int(n), f, h, int(w)) for n, f, h, w in ROW.findall(text)]

def prior_reader() -> str:
    spec = importlib.util.spec_from_file_location("prior_42_source_reader", PRIOR_BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.build_from_repo()

def build(prior: str, chapter: str) -> str:
    original_rows = rows(prior)
    if [r[0] for r in original_rows] != list(range(1, 43)):
        raise ValueError("predecessor 42-source manifest invalid")
    if sum(r[3] for r in original_rows) != PRIOR_WORDS:
        raise ValueError("prior word total drift")
    if prior.count(BEGIN) != 42 or prior.count(END) != 42:
        raise ValueError("predecessor component marker count invalid")
    if prior.count(TERMINAL) != 1:
        raise ValueError("predecessor terminal missing or duplicate")
    if len(chapter.split()) != NEW_WORDS or blob(chapter.encode()) != CHAPTER_SHA:
        raise ValueError("chapter content or word count drift")

    first = prior.index(BEGIN)
    header = prior[:first]
    last_row = [line for line in header.splitlines() if line.startswith("| 42 | ")]
    if len(last_row) != 1 or "Source component words including metadata: 323490" not in header:
        raise ValueError("predecessor 42-part header drift")
    newline = f"| 43 | `{CHAPTER}` | `{CHAPTER_SHA}` | {NEW_WORDS} |"
    header = header.replace(last_row[0], last_row[0] + "\n" + newline, 1)
    header = header.replace("Source component words including metadata: 323490",
                            f"Source component words including metadata: {WORDS}", 1)
    header = header.replace("# 42-part cumulative developmental edition",
                            "# 43-part cumulative developmental edition", 1)

    body_and_terminal = prior[first:]
    body, after = body_and_terminal.split(TERMINAL, 1)
    start = f"{BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
    end = f"{END}{CHAPTER} -->"
    output = (header + body.rstrip() + "\n\n" + start + "\n\n" +
              chapter.rstrip("\n") + "\n\n" + end + "\n\n" +
              TERMINAL + after)
    output_rows = rows(output)
    if [r[0] for r in output_rows] != list(range(1, 44)):
        raise ValueError("new 43-part manifest invalid")
    if sum(r[3] for r in output_rows) != WORDS:
        raise ValueError("new 43-part total invalid")
    if output.count(BEGIN) != 43 or output.count(END) != 43:
        raise ValueError("new 43-part markers invalid")
    if prior[first:prior.index(TERMINAL)].rstrip() != output[output.index(BEGIN):output.index(start)].rstrip():
        raise ValueError("predecessor component bodies changed")
    if output.split(start + "\n\n", 1)[1].split("\n\n" + end, 1)[0] != chapter.rstrip("\n"):
        raise ValueError("new chapter embed is not source-exact")
    return output

def build_from_repo() -> str:
    data = (BASE / CHAPTER).read_bytes()
    if blob(data) != CHAPTER_SHA:
        raise ValueError("stale Chapter XLVI V2 source blob")
    return build(prior_reader(), data.decode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    text = build_from_repo()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"NONCANON 43-component, {WORDS}-word developmental reader: {args.output}")
