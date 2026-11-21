'use strict';
// Real, recorded local AI consultations through the installed Bullpen runtime.
// Named authors and specialists are methodology lenses, never claimed participants.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const runtime='/Users/jakekaloper/Developer/ai/bullpen-runtime';
const root='/Users/jakekaloper/Developer/ai/week10-six-sheet-recovery-20261116';
const pre=path.join(root,'memo-os/week-10/preproduction'),out=__dirname;
const {createConsultEngine}=require(runtime+'/runtime/consultEngine');
const {createAuthenticatedChatProvider}=require(runtime+'/adapters/models/authenticatedChat');
const {BULLPEN_ORG}=require(runtime+'/core/org/directorOrg');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const manifest=read(pre+'/render-inputs/manifest.json');
const pages=manifest.pages.map(p=>read(pre+'/'+p.request));
const chars=read(pre+'/character-world-packet.json').characters;
const registry=read(root+'/living-novel/consultants/ADVISOR_REGISTRY_V1.json');
const specialists=read(root+'/memo-os/cinematography/PRODUCTION_SPECIALIST_REFERENCE_BENCH_V1.json').profiles;
const evidence={scope:'Pre-render audit only. No new image is generated. Assess actual written render inputs, not nonexistent final pixels.',
 constraints:'User requires real 1080x1920 full-page grayscale memo folios with full editorial copy, not approximate miniatures. Six contacts are downstream scaled copies. All 12 canonical crop bytes recovered and hash checked; later Chili appearance is recovered from visually matching local copy with separately recorded hash. No finality invented: all six ESPN winners remain UNDECIDED. Earlier generic images rejected.',
 visualObservations:'Official Week2 p2 and Weeks7,8,9 p2 opened as actual pixels. Weeks7-9 Opening Drive is briefing table/map/banners/sealed folio with dominant OPENING DRIVE and substantial integrated prose, not bridge-travel picture. Week7 p8-10 Forgotten Court has RIGHT-WALL mounted backboard, red ivy, worn hard court, ruin/waterfall skyline. Week9 p12-14 soccer terrace has grass goal, high stepped walls, approach arch, narrow exit, trapped truck and wrecked net. Separate regions.',
 identities:chars.map(c=>({id:c.character_id,name:c.current_display_name,morphology:c.assertions.subject_morphology,negative:c.assertions.negative_rules,override:c.character_id==='CHAR-BRANDON-PRYOR'?c.latest_override.visual_lock:null})),
 pages:pages.map(p=>({id:p.page_id,sheet:p.sheet,position:p.reading_position,characters:p.reference_images.filter(r=>r.character_id).map(r=>r.character_id),location:p.scene.encounter,camera:p.scene.camera_and_composition,body:p.publication_copy.body,headline:p.publication_copy.headline,department:p.publication_copy.department_heading,refs:p.reference_images.map(r=>({role:r.role,application:r.application}))}))};
fs.writeFileSync(out+'/review-input-evidence.json',JSON.stringify(evidence,null,2));
const evhash=crypto.createHash('sha256').update('bounded-context-v2'+JSON.stringify(evidence)).digest('hex');
const provider=createAuthenticatedChatProvider({endpoint:'http://127.0.0.1:11434/v1/chat/completions',apiKey:'local-ollama',model:'qwen2.5-coder:7b',timeoutMs:120000,
 fetchImpl:async (url,opts)=>{const body=JSON.parse(opts.body); const res=await fetch('http://127.0.0.1:11434/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},signal:opts.signal,body:JSON.stringify({model:body.model,messages:body.messages,stream:false,format:'json',keep_alive:'10m',options:{num_ctx:8192,num_thread:4,temperature:0.1,num_predict:340}})});if(!res.ok)return res;const d=await res.json();return new Response(JSON.stringify({model:d.model,choices:[{message:{content:d.message.content}}],usage:{prompt_tokens:d.prompt_eval_count,completion_tokens:d.eval_count}}),{status:200,headers:{'Content-Type':'application/json'}});}});
const events=[],traces=[];
const engine=createConsultEngine({modelProvider:provider,eventBus:{emit:(...x)=>events.push(x)},traceSink:{record:x=>traces.push(x)},boardConcurrency:1,projectContext:{name:'Schemin 26 Week 10',owner:'Jake Kaloper',objective:'Finish pre-render source and full-folio correctness audit on PR315',current_phase:'Source-backed grayscale folio preflight',sources_of_truth:{repositories:['jakekaloper-hub/schemin-26'],documents:['memo-os/week-10/preproduction/render-inputs/manifest.json']},constraints:{quality:['Actual canonical images and full body copy required','No fabricated sport finality or actual-person participation','No art generation in this audit']}}});
const tasks=[...BULLPEN_ORG.map(d=>({kind:'director',id:d.slug,name:d.title,domain:d.domain})),...registry.author_council.core_eight.map(id=>{const a=registry.advisors.find(a=>a.id===id);return {kind:'inklings_lens',id,name:a.display_name,domain:a.lens,dossier:a.dossier_path};}),...specialists.map(p=>({kind:'production_lens',id:p.domain,name:p.name,domain:p.domain}))];
const instruction='Audit the supplied actual page contracts with your assigned discipline. Return JSON only: {"scope":"pre-render written/source audit", "findings":[{"page_ids":["W10-Pxx"],"severity":"critical|major|minor","observation":"specific evidence-backed defect or residual risk", "required_fix":"actionable exact correction"}],"preflight_disposition":"repair|ready_for_grayscale_proof", "limit":"no rendered output exists"}. Maximum 1 strongest finding. Metaphorical story headlines are intentional and approved; they are separate from department headings. Do not rename headlines merely to describe the picture. Do not demand final scores or raster QA before grayscale proof generation. All scene references have an application scope; do not transfer identity or geography from unrelated style exemplars. Do not invent source facts or falsely assert a known completed step is absent. Distinguish a real contradiction from a future per-output inspection. Never claim the real named professional participated. Do not repeat generic safety boilerplate. Check all sheets, including medical/standings wording. Critique concrete mismatches. An empty findings array is permitted only when no actual written defect is found.';
(async()=>{
 const results=[];
 for(const task of tasks){
  const filename=out+'/reviews/'+task.kind+'-'+task.id+'.json';fs.mkdirSync(path.dirname(filename),{recursive:true});
  if(fs.existsSync(filename)){const old=read(filename);if(old.evidence_sha256===evhash&&old.status==='returned'){results.push(old);continue;}}
  let dossier='';if(task.dossier){try{dossier=fs.readFileSync(path.join(root,task.dossier),'utf8').slice(0,2200);}catch{}}
  const ti=tasks.indexOf(task);const deep=pages.filter(p=>p.sheet===(ti%6)+1).map(p=>({id:p.page_id,copy:p.publication_copy,camera:p.scene.camera_and_composition,continuity:p.scene.continuity_out}));
  const bounded={scope:evidence.scope,constraints:evidence.constraints,visualObservations:evidence.visualObservations,identities:evidence.identities.map(c=>({name:c.name,morphology:c.morphology})),all34:pages.map(p=>({id:p.page_id,sheet:p.sheet,title:p.publication_copy.headline,venue:p.scene.encounter.venue_id})),deep_page_sample:deep};
  const userMessage='Discipline: '+task.name+' / '+task.domain+'\nMethodology (not personal participation): '+dossier.slice(0,450)+'\nACTUAL SOURCE EVIDENCE:\n'+JSON.stringify(bounded)+'\n\n'+instruction;
  fs.writeFileSync(out+'/reviews/'+task.kind+'-'+task.id+'-input.txt',userMessage);
  const started=new Date().toISOString();let result;
  try{
   let answer;if(task.kind==='director'){answer=await engine.consultDirector({directorSlug:task.id,userMessage,maxTokens:520});answer=answer.response;}
   else answer=(await provider.generate({system:'You are an independent AI production auditor applying a registered methodology lens. You are not the named human. Source-grounded critique only.',messages:[{role:'user',content:userMessage}],maxTokens:520})).text;
   result={...task,status:'returned',model:'qwen2.5-coder:7b',provider:'Ollama on authorized local Mac via Bullpen runtime',evidence_sha256:evhash,started_at:started,finished_at:new Date().toISOString(),response:answer,primary_review_sheet:(tasks.indexOf(task)%6)+1,actual_input_sha256:crypto.createHash('sha256').update(userMessage).digest('hex'),real_person_participation:false};
  }catch(e){result={...task,status:'failed',evidence_sha256:evhash,error:String(e.message),started_at:started,finished_at:new Date().toISOString()};}
  if(result.status==='returned'){try{const parsed=JSON.parse(result.response);if(!Array.isArray(parsed.findings)||!parsed.preflight_disposition)throw new Error('Missing required findings/disposition');result.structured=parsed;result.response_validated=true;}catch(e){result.status='invalid_response';result.validation_error=e.message;}}fs.writeFileSync(filename,JSON.stringify(result,null,2));results.push(result);console.log(JSON.stringify({completed:results.length,total:tasks.length,...task,status:result.status}));
 }
 fs.writeFileSync(out+'/bullpen-review-results.json',JSON.stringify({evidence_sha256:evhash,expected:tasks.length,returned:results.filter(x=>x.status==='returned').length,results},null,2));
 fs.writeFileSync(out+'/bullpen-runtime-events.json',JSON.stringify({events,traces},null,2));
 console.log('REVIEWS_FINISHED');
})().catch(e=>{console.error(e.stack);process.exitCode=1});
