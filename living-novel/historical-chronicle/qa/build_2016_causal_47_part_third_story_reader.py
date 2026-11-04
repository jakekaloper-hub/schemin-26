"""Reassemble 47 source-exact noncanonical 2016 novel parts; no publication.

Chains the verified 46-part manuscript builder; errors on manifest, blob or
source-byte drift. Generated output is not a historical evidence claim.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
PRIOR_BUILDER = Path(__file__).with_name("build_2016_causal_46_part_turning_back_reader.py")
CHAPTER = "THE_NIGHT_BELOW_THE_ROOM_THE_THIRD_STORY_CH50_V2_NONCANON.md"
CHAPTER_SHA = "9cbfdd0db15734cfa25b8e9b7dcb55c4aedc04aa"
PRIOR_WORDS = 355259
CHAPTER_WORDS = 8335
WORDS = PRIOR_WORDS + CHAPTER_WORDS
TERMINAL = "<!-- END_CAUSAL_READING_COPY -->"
BEGIN = "<!-- BEGIN 2016_CAUSAL "
END = "<!-- END 2016_CAUSAL "
ROW = re.compile(r"(?m)^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$")


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def rows(text: str):
    return [(int(n), path, sha, int(words))
            for n, path, sha, words in ROW.findall(text)]


def prior_reader() -> str:
    spec = importlib.util.spec_from_file_location("reader_46", PRIOR_BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.build_from_repo()


def build(prior: str, chapter: str) -> str:
    previous = rows(prior)
    if [r[0] for r in previous] != list(range(1, 47)):
        raise ValueError("46-part predecessor manifest invalid")
    if sum(row[3] for row in previous) != PRIOR_WORDS:
        raise ValueError("46-part predecessor word-total drift")
    if prior.count(BEGIN) != 46 or prior.count(END) != 46 or prior.count(TERMINAL) != 1:
        raise ValueError("46-part predecessor marker drift")
    if len(chapter.split()) != CHAPTER_WORDS or blob(chapter.encode()) != CHAPTER_SHA:
        raise ValueError("Chapter L V2 source blob/word-count drift")

    first = prior.index(BEGIN)
    header = prior[:first]
    old_row = [line for line in header.splitlines() if line.startswith("| 46 | ")]
    if len(old_row) != 1 or "Source component words including metadata: 355259" not in header:
        raise ValueError("46-part predecessor header drift")
    if "# 46-part cumulative developmental edition" not in header:
        raise ValueError("46-part edition name drift")

    new_row = f"| 47 | `{CHAPTER}` | `{CHAPTER_SHA}` | {CHAPTER_WORDS} |"
    header = header.replace(old_row[0], old_row[0] + "\n" + new_row, 1)
    header = header.replace("Source component words including metadata: 355259",
                            f"Source component words including metadata: {WORDS}", 1)
    header = header.replace("# 46-part cumulative developmental edition",
                            "# 47-part cumulative developmental edition", 1)
    body, after = prior[first:].split(TERMINAL, 1)
    start = f"{BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
    end = f"{END}{CHAPTER} -->"
    output = (header + body.rstrip() + "\n\n" + start + "\n\n"
              + chapter.rstrip("\n") + "\n\n" + end + "\n\n"
              + TERMINAL + after)
    new_rows = rows(output)
    if [r[0] for r in new_rows] != list(range(1, 48)) or sum(r[3] for r in new_rows) != WORDS:
        raise ValueError("47-part reader manifest/count invalid")
    if output.count(BEGIN) != 47 or output.count(END) != 47 or output.count(TERMINAL) != 1:
        raise ValueError("47-part reader marker count invalid")
    preceding = prior[first:prior.index(TERMINAL)].rstrip()
    if preceding != output[output.index(BEGIN):output.index(start)].rstrip():
        raise ValueError("preceding 46 source components altered")
    embedded = output.split(start + "\n\n", 1)[1].split("\n\n" + end, 1)[0]
    if embedded != chapter.rstrip("\n"):
        raise ValueError("Chapter L V2 not embedded source-exact")
    return output


def build_from_repo() -> str:
    data = (BASE / CHAPTER).read_bytes()
    if blob(data) != CHAPTER_SHA:
        raise ValueError("Chapter L V2 Git blob drift")
    return build(prior_reader(), data.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    reader = build_from_repo()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(reader, encoding="utf-8")
    print(f"NONCANON: 47 source-exact components, {WORDS} source words => {args.output}")
