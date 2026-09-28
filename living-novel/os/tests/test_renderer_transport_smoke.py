"""Offline execution-readiness smoke test: validates adapter→transport receipt boundary without spending a render."""
from hashlib import sha256
import json, importlib.util
from pathlib import Path
root=Path(__file__).parents[3]
tp=root/"living-novel/os/transports/renderer_transport.py"
spec=importlib.util.spec_from_file_location("transport",tp); t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
workflow={
 "job_id":"SMOKE-NONCANON-001","adapter":"novel-os-comfyui/v1","native_graph":{"1":{"class_type":"SaveImage","inputs":{}}},
 "provenance":{"references":[]},"control_modules":[],"output":{"width":64,"height":64,"format":"png"},
 "model_checkpoint":"SMOKE_ONLY","seed":1,"generation_parameters":{}
}
receipt=t._receipt(workflow,"offline-smoke","noncanon://smoke","SUBMITTED")
assert receipt.job_id=="SMOKE-NONCANON-001"
assert receipt.workflow_hash==sha256(json.dumps(workflow,sort_keys=True).encode()).hexdigest()
assert receipt.provider=="offline-smoke"
print("PASS: adapter/transport/RenderReceipt ingestion boundary")
