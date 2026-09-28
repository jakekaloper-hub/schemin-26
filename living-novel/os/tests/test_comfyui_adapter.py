import json, importlib.util
from pathlib import Path

p=Path(__file__).parents[1]/"adapters"/"comfyui_adapter.py"
spec=importlib.util.spec_from_file_location("adapter",p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

job=json.loads((Path(__file__).parents[3]/"chronicles/proof-of-concept/prologue/S03_NOVEL_VISUAL_JOB_V1.json").read_text())
m.validate_job(job)
w=m.compile_job(job)
assert w["engine"]=="ComfyUI"
assert w["job_id"]=="PROLOGUE-S03-B004-V1"
assert w["state"]=="COMPILED_UNRENDERED"
assert "negative_constraints" in w["controls"]
print("PASS: S03 NovelVisualJob compiles to renderer-neutral ComfyUI workflow envelope")
