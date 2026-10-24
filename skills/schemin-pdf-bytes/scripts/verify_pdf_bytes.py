#!/usr/bin/env python3
"""Verify original PDF bytes against an authoritative Schemin archive manifest."""
import argparse, datetime as dt, hashlib, json
from pathlib import Path
POINTER=b"version https://git-lfs.github.com/spec/v1\n"
def verify(manifest, repo_root, week):
    found=[x for x in manifest.get("files",[]) if x.get("week")==week]
    if len(found)!=1: raise ValueError("week must resolve to exactly one record")
    x=found[0]; h=x.get("sha256"); n=x.get("size_bytes"); rel=x.get("archive_path")
    if not(isinstance(h,str) and len(h)==64 and all(y in "0123456789abcdef" for y in h)
      and type(n)==int and n>0 and isinstance(rel,str)
      and not rel.startswith("/") and ".." not in Path(rel).parts
      and rel.startswith(f"archive/publications/2026/week-{week:02d}/")):
        raise ValueError("unsafe or invalid archive record")
    root=Path(repo_root).resolve(); path=(root/rel).resolve()
    if not path.is_relative_to(root): raise ValueError("archive path traversal")
    receipt={"week":week,"manifest_path":rel,"expected_sha256":h,
             "expected_size_bytes":n,"verified_at_utc":dt.datetime.now(dt.timezone.utc).isoformat()}
    if not path.is_file():return {**receipt,"status":"FAIL","reason":"FILE_MISSING"}
    with path.open("rb") as f: head=f.read(64)
    if head.startswith(POINTER):return {**receipt,"status":"POINTER_ONLY","reason":"GIT_LFS_BYTES_NOT_MATERIALIZED"}
    if not head.startswith(b"%PDF-"):return {**receipt,"status":"FAIL","reason":"NOT_PDF_BYTES"}
    size=0; digest=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            size+=len(block);digest.update(block)
    actual=digest.hexdigest();ok=(size==n and actual==h)
    return {**receipt,"status":"VERIFIED_REAL_BYTES" if ok else "FAIL",
            "actual_size_bytes":size,"actual_sha256":actual,
            "reason":"MATCH" if ok else "HASH_OR_SIZE_MISMATCH"}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--repo-root",type=Path,required=True)
    p.add_argument("--week",type=int,required=True)
    p.add_argument("--receipt",type=Path)
    a=p.parse_args();out=verify(json.loads(a.manifest.read_text()),a.repo_root,a.week)
    text=json.dumps(out,indent=2)+"\n"
    if a.receipt:
        a.receipt.parent.mkdir(parents=True,exist_ok=True);a.receipt.write_text(text)
    print(text,end="");raise SystemExit(0 if out["status"]=="VERIFIED_REAL_BYTES" else 2)
