import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { deflateSync } from "node:zlib";
import { createImageCandidateWorker } from "../src/image-candidate-worker.js";
import { BullpenRuntime } from "../src/runtime.js";

const hash = b => createHash("sha256").update(b).digest("hex");
const crc = b => {
  let c = 0xffffffff;
  for (const byte of b) {
    c ^= byte;
    for (let bit=0; bit<8; bit++) c = (c >>> 1) ^ ((c & 1) ? 0xedb88320 : 0);
  }
  return (c ^ 0xffffffff) >>> 0;
};
const chunk = (label, data) => {
  const body=Buffer.concat([Buffer.from(label), data]), buf=Buffer.alloc(body.length+8);
  buf.writeUInt32BE(data.length,0); body.copy(buf,4); buf.writeUInt32BE(crc(body),body.length+4);
  return buf;
};
const makePng = (width=1080,height=1920) => {
  const ihdr=Buffer.alloc(13);ihdr.writeUInt32BE(width,0);ihdr.writeUInt32BE(height,4);ihdr[8]=8;ihdr[9]=2;
  return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk("IHDR",ihdr),chunk("IDAT",deflateSync(Buffer.alloc(height*(1+width*3)))),chunk("IEND",Buffer.alloc(0))]);
};
const dir=mkdtempSync(join(tmpdir(),"schemin-art-handoff-test-"));
const png=makePng(), pngSha=hash(png);
writeFileSync(join(dir,"folio.png"),png);
const ref = {
  character_id:"CHAR-ONE", owner_id:"owner-1",
  expected_sha256:"a".repeat(64), mounted_sha256:"a".repeat(64),
  generation_reference_id:"gen-ref-1", subject_slot:"character-main",
  subject_binding_id:"bind-1", mount_receipt_id:"mount-1",
  capability_receipt_id:"cap-1", canonical_asset_path:"private/character-1.jpeg"
};
const request={page_id:"W11-P01", request_sha256:"f".repeat(64), canvas:[1080,1920], characters:[ref]};
const custody={status:"PASS", receipt_id:"custody-1", reviewer_id:"custodian-1", characters:[{...ref}]};
const output={
  page_id:"W11-P01", relativePath:"folio.png", sha256:pngSha,
  output_instance_id:"render-1", operator_id:"generator-1",
  custody_receipt_id:"custody-1", request_sha256:"f".repeat(64),
  renderer_route:"local-renderer-test", workflow_id:"workflow-1", model_id:"model-1",
  subjects:[{...ref}]
};
function harness({custodyResponse=custody,rendererResponse=output}={}){
  const calls={custodian:0,renderer:0};
  const referenceCustodian={async verify(){calls.custodian++;return custodyResponse;}};
  const renderer={async render(){calls.renderer++;return rendererResponse;}};
  const worker=createImageCandidateWorker({root:dir,referenceCustodian,renderer});
  return {worker,calls};
}
const ctx={input:{render_request:request},stage:{id:"art_job"}};

test("unavailable external image or custody adapter blocks without pretending to render",async()=>{
 const noRenderer=await createImageCandidateWorker({root:dir,referenceCustodian:{verify:async()=>custody}})(ctx);
 assert.equal(noRenderer.blocked,true); assert.equal(noRenderer.code,"RENDERER_NOT_CONNECTED");
 const noCustodian=await createImageCandidateWorker({root:dir,renderer:{render:async()=>output}})(ctx);
 assert.equal(noCustodian.blocked,true); assert.equal(noCustodian.code,"SOURCE_CUSTODY_NOT_CONNECTED");
});

test("rejects malformed page packet and any absent or duplicate subject before invocation",async()=>{
 const {worker,calls}=harness();
 for(const bad of [
  {...request,request_sha256:"invalid"},
  {...request,characters:[]},
  {...request,characters:[ref,ref]},
  {...request,characters:[{...ref,subject_binding_id:""}]},
  {...request,canvas:[1920,1080]},
 ]) {
  const r=await worker({input:{render_request:bad}});
  assert.equal(r.blocked,true);
  assert.equal(r.code,"UNVERIFIED_RENDER_PACKET");
 }
 assert.equal(calls.custodian,0);assert.equal(calls.renderer,0);
});

test("rejects missing or mismatched independent custodian receipts before invoking renderer",async()=>{
 for(const bad of [
  {status:"HOLD",receipt_id:"custody-1",characters:[ref]},
  {...custody,characters:[{...ref,mounted_sha256:"b".repeat(64)}]},
  {...custody,characters:[{...ref,subject_slot:"wrong"}]},
  {...custody,characters:[]},
  {...custody,reviewer_id:""},
 ]) {
  const {worker,calls}=harness({custodyResponse:bad});
  const r=await worker(ctx);
  assert.equal(r.blocked,true);
  assert.equal(r.code,"CHARACTER_CUSTODY_UNVERIFIED");
  assert.equal(calls.renderer,0);
 }
});

test("rejects a renderer that does not echo the exact declared subject binding",async()=>{
 const {worker}=harness({rendererResponse:{...output,subjects:[{...ref,subject_binding_id:"other"}]}});
 const r=await worker(ctx);
 assert.equal(r.blocked,true);assert.equal(r.code,"RENDER_RECEIPT_MISMATCH");
});

test("rejects a renderer output for a different source packet or custody receipt",async()=>{
 for(const bad of [
  {...output,request_sha256:"b".repeat(64)},
  {...output,custody_receipt_id:"custody-other"}
 ]) {
  const {worker}=harness({rendererResponse:bad});
  const result=await worker(ctx);
  assert.equal(result.blocked,true);
  assert.equal(result.code,"RENDER_RECEIPT_MISMATCH");
 }
});

test("rejects missing image bytes or altered hashes instead of producing a candidate",async()=>{
 for(const o of [{...output,relativePath:"missing.png"},{...output,sha256:"b".repeat(64)}]) {
  const {worker}=harness({rendererResponse:o});
  const r=await worker(ctx);
  assert.equal(r.blocked,true);
  assert.equal(r.code,"RASTER_PREFLIGHT_BLOCKED");
 }
});

test("emits only an unreviewed image artifact when custody echoes and PNG integrity match",async()=>{
 const {worker,calls}=harness();
 const r=await worker(ctx);
 assert.equal(calls.custodian,1);assert.equal(calls.renderer,1);
 assert.equal(r.artifact.kind,"IMAGE_RENDER_CANDIDATE");
 assert.equal(r.artifact.state,"RENDERED_UNAPPROVED");
 assert.equal(r.artifact.output_sha256,pngSha);
 assert.equal(r.artifact.character_binding_evidence,"RECEIPT_FIELDS_MATCHED_NOT_PROVIDER_AUTHENTICATED");
 assert.equal(r.artifact.character_qa_approved,false);
 assert.equal(r.artifact.publication_eligible,false);
 assert.equal(r.artifact.independent_visual_qa_completed,false);
});

test("runtime still blocks an artwork job without its separate independent visual gate",async()=>{
 const {worker}=harness();
 const pipeline={id:"source-bound-image-canary",stages:[{id:"art_job",worker:"visualDevelopment",gate:"characterVisionGate"}]};
 const r=await new BullpenRuntime({workers:{visualDevelopment:worker}}).run({pipeline,input:ctx.input,jobId:"candidate-only"});
 assert.equal(r.status,"blocked");
 assert.match(r.failure.reason,/missing gate/);
 assert.equal(r.artifacts.length,0);
});
