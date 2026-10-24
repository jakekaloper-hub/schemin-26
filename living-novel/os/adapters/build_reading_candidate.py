"""Reproducible *noncanonical* reading excerpt. Never promote unresolved POV source."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
SRC=[
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md",
 "living-novel/production/full-rewrite-2026/G07_CANDIDATE_SCENE_THE_RECEIPT_AND_THE_HILL_NONCANON.md",
]
LEGACY=[
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md",
]
def words(text):return len(re.findall(r"\b[\w’'-]+\b",text))
def audit(path):
 data=(ROOT/path).read_bytes();s=data.decode("utf-8")
 return {"path":path,"sha256":hashlib.sha256(data).hexdigest(),"word_count":words(s),
   "legacy_institutional_pov_risk":bool(re.search(r"\b(?:edrin|master oren)\b",s,re.I))}
def build():
 selected=[audit(x) for x in SRC]
 if any(x["legacy_institutional_pov_risk"] for x in selected):raise ValueError("legacy Edrin/Oren contamination")
 rejected=[audit(x) for x in LEGACY]
 combined="# SCHEMIN’ ’26 — NONCANON READING CANDIDATE\n\n> Developmental excerpt, not a complete novel or approved canon. The Chapter III text is a source reading and the following sequence is a noncanonical candidate.\n\n"
 for row in selected:
  combined+="\n\n---\n\n"+(ROOT/row["path"]).read_text()+"\n"
 return combined,{"release_status":"HOLD_NOT_FINAL_NOVEL","source_files":selected,
   "legacy_files_excluded":rejected,"assembled_word_count":words(combined),
   "independent_umpire_approved":False,"founder_approved":False,
   "art_byte_verified":False,"published":False}
if __name__=="__main__":
 import sys
 content,manifest=build()
 dest=ROOT/"living-novel/production/full-rewrite-2026"
 (dest/"G09_NONCANON_READING_CANDIDATE.md").write_text(content)
 (dest/"G09_NONCANON_READING_CANDIDATE_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
 print(json.dumps({"words":manifest["assembled_word_count"],"excluded":len(manifest["legacy_files_excluded"]),"release_status":manifest["release_status"]}))
