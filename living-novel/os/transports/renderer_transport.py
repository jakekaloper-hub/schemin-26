"""Renderer transports for Novel OS.
No credentials are stored in source. Runtime configuration is injected via env/config.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from hashlib import sha256
from datetime import datetime, timezone
import json, os, urllib.request

@dataclass
class RenderReceipt:
    job_id: str
    engine: str
    provider: str
    model_checkpoint: str
    workflow_version: str
    workflow_hash: str
    reference_assets: list
    control_modules: list
    seed: int | None
    dimensions: dict
    generation_parameters: dict
    execution_timestamp: str
    output_artifact: str | None
    output_hash: str | None
    status: str

    def to_dict(self): return asdict(self)

class RendererTransport:
    def submit(self, workflow: dict) -> RenderReceipt:
        raise NotImplementedError

class HttpComfyTransport(RendererTransport):
    """Fallback for a reachable ComfyUI-compatible /prompt endpoint."""
    def __init__(self, base_url: str):
        self.base_url=base_url.rstrip("/")
    def submit(self, workflow: dict) -> RenderReceipt:
        payload=json.dumps({"prompt": workflow["native_graph"]}).encode()
        req=urllib.request.Request(self.base_url+"/prompt",data=payload,headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req,timeout=60) as r:
            result=json.loads(r.read())
        return _receipt(workflow,"http-comfy",result.get("prompt_id"),"SUBMITTED")

class RunpodComfyTransport(RendererTransport):
    """Preferred hosted transport. Endpoint and API key are runtime-only."""
    def __init__(self, endpoint_id: str|None=None, api_key: str|None=None):
        self.endpoint_id=endpoint_id or os.getenv("RUNPOD_ENDPOINT_ID")
        self.api_key=api_key or os.getenv("RUNPOD_API_KEY")
        if not self.endpoint_id or not self.api_key:
            raise RuntimeError("RUNPOD_ENDPOINT_ID and RUNPOD_API_KEY are required at runtime")
    def submit(self, workflow: dict) -> RenderReceipt:
        url=f"https://api.runpod.ai/v2/{self.endpoint_id}/run"
        body=json.dumps({"input":{"workflow":workflow["native_graph"],"novel_os":workflow["provenance"]}}).encode()
        req=urllib.request.Request(url,data=body,headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"})
        with urllib.request.urlopen(req,timeout=60) as r:
            result=json.loads(r.read())
        return _receipt(workflow,"runpod",result.get("id"),"SUBMITTED")

def _receipt(workflow, provider, artifact, status):
    raw=json.dumps(workflow,sort_keys=True).encode()
    return RenderReceipt(
        job_id=workflow["job_id"], engine="ComfyUI", provider=provider,
        model_checkpoint=workflow.get("model_checkpoint","UNBOUND"),
        workflow_version=workflow.get("adapter","unknown"),
        workflow_hash=sha256(raw).hexdigest(),
        reference_assets=workflow.get("provenance",{}).get("references",[]),
        control_modules=workflow.get("control_modules",[]),
        seed=workflow.get("seed"), dimensions=workflow.get("output",{}),
        generation_parameters=workflow.get("generation_parameters",{}),
        execution_timestamp=datetime.now(timezone.utc).isoformat(),
        output_artifact=artifact, output_hash=None, status=status)
