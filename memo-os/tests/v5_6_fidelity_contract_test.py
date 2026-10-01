#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
MEMO=ROOT/"memo-os"
TESTS=MEMO/"tests"

errors=[]

def need(path,*tokens):
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return
    text=path.read_text()
    for token in tokens:
        if token not in text:
            errors.append(f"{path.relative_to(ROOT)} missing {token}")

need(MEMO/"PAGE_FIDELITY_MODEL_V1.md",
     "F1 — Scene specificity",
     "F10 — 390px hierarchy",
     "generic hero",
     "Week 2",
     "Week 3")
need(TESTS/"WEEK2_WEEK3_PUBLICATION_ANATOMY_AUDIT_V1.md",
     "Week 2 — 14-page anatomy",
     "Week 3 — 21-page anatomy",
     "The design unit is the **finished PNG page**")
need(TESTS/"V5_6_PUBLICATION_FIDELITY_NEGATIVE_CONTROL_01.md",
     "Technical acceptance:** PASS",
     "Publication fidelity:** FAIL",
     "Real page acceptance:** FAIL")
need(MEMO/"week-4"/"WEEK_4_ACCEPTANCE_REBUILD_BRIEF_V2.md",
     "Full-page cinematic editorial tableau",
     "Not:",
     "390px")

reg_path=TESTS/"V5_6_PROMOTION_EVIDENCE_REGISTER.json"
if reg_path.exists():
    reg=json.loads(reg_path.read_text())
    if (reg.get("week4_real_page_acceptance") or {}).get("status")!="FAIL":
        errors.append("negative-control Week 4 page must remain FAIL until replacement passes fidelity")
else:
    errors.append("promotion evidence register missing")

if errors:
    print("FIDELITY CONTRACT: FAIL")
    for e in errors: print("-",e)
    raise SystemExit(1)

print("FIDELITY CONTRACT: PASS")
print("Week2/Week3 anatomy, Page Fidelity Model, negative control, and rebuild brief are wired.")
