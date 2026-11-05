"""Assemble a source-exact 45-part 2016 NONCANON developmental reader in memory.

This extends the previously verified 44-part cumulative reading copy.
Does not touch historical league facts, protected hard canon or release surfaces.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
PRIOR_BUILDER=Path(__file__).with_name("build_2016_causal_44_part_oven_reader.py")
CHAPTER="THE_MORNING_OF_SMALL_LOAVES_THE_RETURN_ROAD_CH48_V2_NONCANON.md"
CHAPTER_SHA="c41f2faee9f3889ee0f7b88e9aa29ec56e31ad34"
PRIOR_WORDS=339262
CHAPTER_WORDS=8518
WORDS=PRIOR_WORDS+CHAPTER_WORDS
TERMINAL="<!-- END_CAUSAL_READING_COPY -->"
BEGIN="<!-- BEGIN 2016_CAUSAL "
END="<!-- END 2016_CAUSAL "
ROW=re.compile(r"(?m)^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$")

def blob(data:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def rows(text:str):
    return [(int(n),f,h,int(w)) for n,f,h,w in ROW.findall(text)]

def prior_reader()->str:
    spec=importlib.util.spec_from_file_location("reader_44",PRIOR_BUILDER)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.build_from_repo()

def build(prior:str,chapter:str)->str:
    previous=rows(prior)
    if [r[0] for r in previous]!=list(range(1,45)):
        raise ValueError("44-part predecessor manifest invalid")
    if sum(row[3] for row in previous)!=PRIOR_WORDS:
        raise ValueError("44-part predecessor word-total drift")
    if prior.count(BEGIN)!=44 or prior.count(END)!=44 or prior.count(TERMINAL)!=1:
        raise ValueError("44-part predecessor marker drift")
    if len(chapter.split())!=CHAPTER_WORDS or blob(chapter.encode())!=CHAPTER_SHA:
        raise ValueError("Chapter XLVIII V2 source blob/word-count drift")
    first=prior.index(BEGIN)
    header=prior[:first]
    old_row=[line for line in header.splitlines() if line.startswith("| 44 | ")]
    if len(old_row)!=1 or "Source component words including metadata: 339262" not in header:
        raise ValueError("44-part predecessor header drift")
    last=f"| 45 | \x60{CHAPTER}\x60 | \x60{CHAPTER_SHA}\x60 | {CHAPTER_WORDS} |"
    header=header.replace(old_row[0],old_row[0]+"\n"+last,1)
    header=header.replace("Source component words including metadata: 339262",f"Source component words including metadata: {WORDS}",1)
    header=header.replace("# 44-part cumulative developmental edition","# 45-part cumulative developmental edition",1)
    body,after=prior[first:].split(TERMINAL,1)
    start=f"{BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
    end=f"{END}{CHAPTER} -->"
    output=header+body.rstrip()+"\n\n"+start+"\n\n"+chapter.rstrip("\n")+"\n\n"+end+"\n\n"+TERMINAL+after
    new_rows=rows(output)
    if [r[0] for r in new_rows]!=list(range(1,46)) or sum(r[3] for r in new_rows)!=WORDS:
        raise ValueError("45-part reader manifest/count invalid")
    if output.count(BEGIN)!=45 or output.count(END)!=45 or output.count(TERMINAL)!=1:
        raise ValueError("45-part reader marker count invalid")
    if prior[first:prior.index(TERMINAL)].rstrip()!=output[output.index(BEGIN):output.index(start)].rstrip():
        raise ValueError("preceding 44 source components altered")
    if output.split(start+"\n\n",1)[1].split("\n\n"+end,1)[0]!=chapter.rstrip("\n"):
        raise ValueError("Chapter XLVIII V2 not embedded source-exact")
    return output

def build_from_repo()->str:
    data=(BASE/CHAPTER).read_bytes()
    if blob(data)!=CHAPTER_SHA: raise ValueError("new source blob drift")
    return build(prior_reader(),data.decode("utf-8"))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    output=build_from_repo()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(output,encoding="utf-8")
    print(f"NONCANON: 45 source-exact components, {WORDS} source words => {args.output}")
