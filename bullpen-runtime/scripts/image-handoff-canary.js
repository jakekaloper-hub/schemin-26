#!/usr/bin/env node
/**
 * Read-only preflight of existing Memo render-input requests. No provider,
 * source custody, character binding or release acceptance is simulated.
 * Usage: node scripts/image-handoff-canary.js /path/to/W10-P05/request.json ...
 */
import { readFileSync } from "node:fs";
import { basename } from "node:path";
import { createHash } from "node:crypto";
import { createImageCandidateWorker } from "../src/image-candidate-worker.js";

const hash=buffer=>createHash("sha256").update(buffer).digest("hex");
if (!process.argv.slice(2).length) {
  console.error("At least one existing render-input request path is required");
  process.exit(64);
}
const worker=createImageCandidateWorker({root:process.cwd()});
const results=[];
for(const file of process.argv.slice(2)){
  const bytes=readFileSync(file), r=JSON.parse(bytes.toString("utf8"));
  const references=(r.reference_images||[]).filter(x=>x.character_id);
  const subjects=[...new Set(references.map(x=>x.character_id))];
  // The preflight does not fabricate unavailable mount and binding receipts.
  const render_request={
    page_id:r.page_id,request_sha256:hash(bytes),canvas:r.canvas,
    characters:subjects.map(cid=>{
      const s=references.find(x=>x.character_id===cid);
      return {character_id:cid,expected_sha256:s?.sha256,canonical_asset_path:s?.repo_path};
    })
  };
  const outcome=await worker({input:{render_request}});
  results.push({
    page_id:r.page_id,request_filename:basename(file),
    request_sha256:render_request.request_sha256,
    current_source_references:references.length,
    character_ids:subjects,
    complete_generation_binding_receipts:references.filter(x=>
      x.mount_receipt_id&&x.subject_binding_id&&x.generation_reference_id).length,
    state:outcome.blocked?"BLOCKED":"UNEXPECTED_READY",
    reason_code:outcome.code||"NONE",image_artifacts_created:0
  });
}
console.log(JSON.stringify({kind:"MEMO_ART_JOB_HANDOFF_CANARY",production_approved:false,
  image_generation_executed:false,results},null,2));
if(results.some(x=>x.state!=="BLOCKED"))process.exitCode=1;
