"""Assemble reconstructed continuous Prologue–III as a noncanonical review edition."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
FILES=[
 "living-novel/production/full-rewrite-2026/G07_RECONSTRUCTED_OPENING_PROLOGUE_CH01_CH02_NONCANON.md",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md",
]
def build():
 out="# SCHEMIN’ ’26 — TWELVE-POV DEVELOPMENTAL READING EDITION\n\n> **NONCANON EDITORIAL CANDIDATE.** Reconstructed opening followed by existing Chapter III source. No Founder approval, independent Umpire approval, art QA or publication.\n\n"
 refs=[]
 for path in FILES:
  b=(ROOT/path).read_bytes()
  refs.append({"path":path,"sha256":hashlib.sha256(b).hexdigest(),"word_count":len(b.decode().split())})
  out+="\n---\n\n"+b.decode().split("## Reconstruction transaction status")[0].strip()+"\n"
 return out,{"status":"HOLD_NONCANON_REVIEW","sources":refs,"assembled_word_count":len(out.split()),"legacy_prologue_chapter_1_2_excluded":True,
  "interactive_12_path_equivalence":"NOT_VERIFIED","approved_art_placement":"NOT_VERIFIED",
  "independent_editorial_approval":False,"founder_canon_approval":False,"published":False}
if __name__=="__main__":
 body,manifest=build()
 dest=ROOT/"living-novel/production/full-rewrite-2026"
 (dest/"G09_RECONSTRUCTED_PROLOGUE_THROUGH_CH03_READING_CANDIDATE.md").write_text(body)
 (dest/"G09_RECONSTRUCTED_PROLOGUE_THROUGH_CH03_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
 print("words",manifest["assembled_word_count"],"sources",len(manifest["sources"]))
