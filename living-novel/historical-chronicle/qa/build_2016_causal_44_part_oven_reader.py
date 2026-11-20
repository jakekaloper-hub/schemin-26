"""Build verified source-exact 44-part 2016 NONCANON developmental reading in memory.

Reuse the tested 43-part cart builder; no historical evidence or canon changes.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
PRIOR_BUILDER = Path(__file__).with_name("build_2016_causal_43_part_cart_reader.py")
CHAPTER = "THE_BELL_THAT_HAD_NO_OWNER_THE_OVEN_WITHOUT_A_BELL_CH47_V2_NONCANON.md"
CHAPTER_SHA = "47d7f0839ad61f28d5d2191640ba2ad622f4a8a7"
PRIOR_WORDS = 331323
NEW_WORDS = 7939
WORDS = PRIOR_WORDS + NEW_WORDS
TERMINAL = "<!-- END_CAUSAL_READING_COPY -->"
BEGIN = "<!-- BEGIN 2016_CAUSAL "
END = "<!-- END 2016_CAUSAL "
ROW = re.compile(r"(?m)^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$")

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(text: str):
    return [(int(n), f, h, int(w)) for n, f, h, w in ROW.findall(text)]

def prior_reader() -> str:
    spec = importlib.util.spec_from_file_location("prior_43_source_reader", PRIOR_BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.build_from_repo()

def build(prior: str, chapter: str) -> str:
    previous = rows(prior)
    if [r[0] for r in previous] != list(range(1, 44)):
        raise ValueError("predecessor 43-source manifest invalid")
    if sum(r[3] for r in previous) != PRIOR_WORDS:
        raise ValueError("predecessor word total drift")
    if prior.count(BEGIN) != 43 or prior.count(END) != 43:
        raise ValueError("predecessor component marker count invalid")
    if prior.count(TERMINAL) != 1:
        raise ValueError("predecessor terminal missing or duplicate")
    if len(chapter.split()) != NEW_WORDS or blob(chapter.encode()) != CHAPTER_SHA:
        raise ValueError("new chapter content or count drift")
    first = prior.index(BEGIN)
    header = prior[:first]
    last = [line for line in header.splitlines() if line.startswith("| 43 | ")]
    if len(last) != 1 or "Source component words including metadata: 331323" not in header:
        raise ValueError("43-part header drift")
    new_row = f"| 44 | `{CHAPTER}` | `{CHAPTER_SHA}` | {NEW_WORDS} |"
    header = header.replace(last[0], last[0] + "\n" + new_row, 1)
    header = header.replace("Source component words including metadata: 331323",
                            f"Source component words including metadata: {WORDS}", 1)
    header = header.replace("# 43-part cumulative developmental edition",
                            "# 44-part cumulative developmental edition", 1)
    body, after = prior[first:].split(TERMINAL, 1)
    start = f"{BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
    end = f"{END}{CHAPTER} -->"
    output = (header + body.rstrip() + "\n\n" + start + "\n\n" +
              chapter.rstrip("\n") + "\n\n" + end + "\n\n" + TERMINAL + after)
    new_rows = rows(output)
    if [r[0] for r in new_rows] != list(range(1, 45)):
        raise ValueError("new 44-part manifest invalid")
    if sum(r[3] for r in new_rows) != WORDS:
        raise ValueError("44-part word total invalid")
    if output.count(BEGIN) != 44 or output.count(END) != 44:
        raise ValueError("new component count invalid")
    if prior[first:prior.index(TERMINAL)].rstrip() != output[output.index(BEGIN):output.index(start)].rstrip():
        raise ValueError("earlier 43 embedded source sections changed")
    if output.split(start + "\n\n", 1)[1].split("\n\n" + end, 1)[0] != chapter.rstrip("\n"):
        raise ValueError("Chapter XLVII not embedded source-exact")
    return output

def build_from_repo() -> str:
    data = (BASE / CHAPTER).read_bytes()
    if blob(data) != CHAPTER_SHA:
        raise ValueError("Chapter XLVII source blob drift")
    return build(prior_reader(), data.decode("utf-8"))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    contents = build_from_repo()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(contents, encoding="utf-8")
    print(f"NONCANON 44-component, {WORDS}-word reader: {args.output}")
