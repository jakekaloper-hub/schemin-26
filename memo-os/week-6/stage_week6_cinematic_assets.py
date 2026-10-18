#!/usr/bin/env python3
"""Safely stage exact Week 6 PNG source bytes from the already-approved candidate ZIP.
Does not approve cinematic references or change the active reference registry.
Usage: python3 memo-os/week-6/stage_week6_cinematic_assets.py /path/to/ZIP [--write]
Without --write: read-only manifest and integrity validation.
"""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EXPECTED={
 "LOC-RED-RUINS":("golden_hour_jungle_ruin_stadium.png","1b589d2eb888f428a19171d0850faba84289fa5b694dc813f799150c36ec24ec"),
 "LOC-COUNTRY-CLUB-JACKSON":("golden_hour_cypress_golf_retreat.png","56ddc7b1ca50747ccb3097a0936ba0f832715cdd1cd911569ac803e4ae51cb71"),
 "LOC-SLOB-FOOTHILL-CAMP":("rustic_mountain_dodgeball_camp_at_sunset.png","94d8b7cbf6bd001b0a41c56e7f58bea8e40ecc75571300a3965330a24f7a91da"),
 "LOC-CHILI-STABLE":("golden_hour_ranch_rodeo_landscape.png","ef1c2a1063eed6ce2b8b4af38da4e2a5ebcabb051f0b4dbb0b22f181a2246365"),
 "LOC-MUD-DOGS-SWAMP":("misty_bayou_landing_at_dawn.png","9dc76844e7c64725004cec79d6387b18943b3559471503e1fb7f05562c684114"),
 "LOC-TDS-WATERFALL-TEMPLE":("misty_jungle_waterfall_temple.png","e44ae1c8f036c5e93634ef7fb0c50671fed02de2e9cbb32e5e1ca22222857e42")
}
def stage(path:Path,write=False):
 assert path.is_file(),"SOURCE_ZIP_UNAVAILABLE"
 candidates=ROOT/"world/environment-references/candidates/week-6"
 with zipfile.ZipFile(path) as z:
  files={Path(i.filename).name:i for i in z.infolist() if not i.is_dir() and i.filename.lower().endswith(".png")}
  assert set(files)=={v[0] for v in EXPECTED.values()},"PNG_MEMBERSHIP_DRIFT"
  for loc,(name,digest) in EXPECTED.items():
   data=z.read(files[name])
   assert data[:8]==b"\\x89PNG\\r\\n\\x1a\\n".decode("unicode_escape").encode("latin1"),(loc,"INVALID_PNG")
   actual=hashlib.sha256(data).hexdigest()
   assert actual==digest,(loc,"SOURCE_BYTE_HASH_MISMATCH",actual)
   # PNG IHDR width/height are big endian at byte offsets 16..23
   w=int.from_bytes(data[16:20],"big");h=int.from_bytes(data[20:24],"big")
   assert (w,h)==(1672,941),(loc,"DIMENSION_DRIFT",w,h)
   target=candidates/loc/"CINEMATIC_CANDIDATE_V1.png"
   if write:
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists(): assert hashlib.sha256(target.read_bytes()).hexdigest()==digest,"REFUSE_OVERWRITE_DIFFERENT_ASSET"
    else:target.write_bytes(data)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==digest,"WRITTEN_BYTES_MISMATCH"
   print(loc,name,actual,f"{w}x{h}", "STAGED" if write else "VERIFIED_ONLY")
 print("6/6 VERIFIED. Active approved cinematic registry UNCHANGED; independent approval still REQUIRED.")
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("source_zip",type=Path);a.add_argument("--write",action="store_true");x=a.parse_args();stage(x.source_zip,x.write)
