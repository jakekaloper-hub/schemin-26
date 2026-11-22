/**
 * Candidate-only image worker for the existing Bullpen art_job stage.
 * Consumes a separately validated character-custody adapter and a renderer
 * adapter, then reuses raster-preflight. Neither adapter is supplied here.
 * Receipt echoes are NOT proof that a provider actually mounted a reference.
 * No returned artifact can approve likeness, editorial copy or publication.
 */
import { inspectPngFile } from "./raster-preflight.js";

const SHA=/^[a-f0-9]{64}$/;
const mandatory=[
  "character_id","owner_id","expected_sha256","mounted_sha256",
  "generation_reference_id","subject_slot","subject_binding_id",
  "mount_receipt_id","capability_receipt_id","canonical_asset_path"
];
const echoes=[
  "character_id","owner_id","expected_sha256","mounted_sha256",
  "generation_reference_id","subject_slot","subject_binding_id",
  "mount_receipt_id","capability_receipt_id"
];
const nonempty=value=>typeof value==="string"&&value.trim().length>0;
const blocked=(code,reason)=>({blocked:true,code,reason});
const isValidReference=r=>r&&typeof r==="object"&&mandatory.every(k=>nonempty(r[k]))
  && SHA.test(r.expected_sha256)&&SHA.test(r.mounted_sha256)
  && r.expected_sha256===r.mounted_sha256;
const allUnique=(arr,key)=>new Set(arr.map(x=>x[key])).size===arr.length;

function validRequest(req){
  if(!req || !/^W\d{2}-P\d{2}$/.test(req.page_id||"")
      || !SHA.test(req.request_sha256||"") || !Array.isArray(req.canvas)
      || req.canvas.length!==2 || req.canvas[0]!==1080 || req.canvas[1]!==1920
      || !Array.isArray(req.characters) || !req.characters.length
      || !req.characters.every(isValidReference)
      || !allUnique(req.characters,"character_id")
      || !allUnique(req.characters,"subject_slot")
      || !allUnique(req.characters,"subject_binding_id")) return false;
  return true;
}

function matches(a,b,keys=echoes){
  return keys.every(k=>a?.[k]===b?.[k]);
}

function matchesSubjects(source,observed){
  if(!Array.isArray(observed)||observed.length!==source.length
      || !observed.every(isValidReference)) return false;
  const index=new Map(observed.map(x=>[x.character_id,x]));
  return source.every(c=>matches(c,index.get(c.character_id)));
}

export function createImageCandidateWorker({root,referenceCustodian,renderer}={}){
  if(!nonempty(root)) throw new TypeError("explicit artwork root required");
  return async({input={}}={})=>{
    const req=input.render_request;
    if(!validRequest(req)) return blocked("UNVERIFIED_RENDER_PACKET",
      "An exact portrait page and nonduplicated character-binding packet are required");
    if(typeof referenceCustodian?.verify!=="function")
      return blocked("SOURCE_CUSTODY_NOT_CONNECTED","No independently operating source-custody adapter");
    if(typeof renderer?.render!=="function")
      return blocked("RENDERER_NOT_CONNECTED","No configured image-generation provider");
    if(referenceCustodian===renderer)
      return blocked("NONINDEPENDENT_ADAPTERS","Source custodian and image renderer cannot be the same adapter");
    let custody;
    try { custody=await referenceCustodian.verify(req); }
    catch {return blocked("CHARACTER_CUSTODY_UNVERIFIED","Custody verification failed");}
    if(custody?.status!=="PASS" || !nonempty(custody.receipt_id)
        || !nonempty(custody.reviewer_id)
        || !matchesSubjects(req.characters,custody.characters))
      return blocked("CHARACTER_CUSTODY_UNVERIFIED",
        "Custodian receipt absent, incomplete or inconsistent with the locked request");
    let result;
    try {result=await renderer.render({request:req,custody_receipt_id:custody.receipt_id});}
    catch {return blocked("RENDERER_UNAVAILABLE","Provider failed; no candidate receipt");}
    if(result?.page_id!==req.page_id
       || result.request_sha256!==req.request_sha256
       || result.custody_receipt_id!==custody.receipt_id
       || !nonempty(result.output_instance_id)
       || !nonempty(result.operator_id)
       || result.operator_id===custody.reviewer_id
       || !nonempty(result.renderer_route) || !nonempty(result.workflow_id)
       || !nonempty(result.model_id)
       || !nonempty(result.relativePath)
       || !SHA.test(result.sha256||"")
       || !matchesSubjects(req.characters,result.subjects))
      return blocked("RENDER_RECEIPT_MISMATCH",
        "Output or per-subject receipt was not echoed exactly by the renderer");
    const raster=inspectPngFile({
      root,relativePath:result.relativePath,expectedSha256:result.sha256,
      width:req.canvas[0],height:req.canvas[1]
    });
    if(raster.state!=="RASTER_PREFLIGHT_PASSED")
      return blocked("RASTER_PREFLIGHT_BLOCKED",
        raster.code+": "+raster.reason);
    return {artifact:{
      kind:"IMAGE_RENDER_CANDIDATE",state:"RENDERED_UNAPPROVED",
      page_id:req.page_id,request_sha256:req.request_sha256,
      output_sha256:raster.sha256,output_byte_size:raster.byte_size,
      output_instance_id:result.output_instance_id,output_relative_path:result.relativePath,
      width:raster.width,height:raster.height,renderer_route:result.renderer_route,
      workflow_id:result.workflow_id,model_id:result.model_id,
      operator_id:result.operator_id,
      source_custody_receipt_id:custody.receipt_id,
      source_custody_reviewer_id:custody.reviewer_id,
      subjects:req.characters.map(r=>({
        character_id:r.character_id,source_sha256:r.expected_sha256,
        mount_receipt_id:r.mount_receipt_id,subject_binding_id:r.subject_binding_id,
        subject_slot:r.subject_slot
      })),
      technical_integrity_verified:true,
      character_binding_evidence:"RECEIPT_FIELDS_MATCHED_NOT_PROVIDER_AUTHENTICATED",
      character_qa_approved:false,editorial_qa_approved:false,
      independent_visual_qa_completed:false,publication_eligible:false
    }};
  };
}
