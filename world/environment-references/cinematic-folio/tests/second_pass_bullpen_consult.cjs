'use strict';
const fs=require('fs'),path=require('path');
const repo=process.cwd(),root=process.env.HOME+'/Developer/ai/bullpen-runtime';
const {createBullpen,compileIntent,adapters}=require(root);
const {routeTask}=require(root+'/runtime/router');
const {createAuthenticatedChatProvider}=adapters.authenticatedChat;
const task='/bullpen strengthen Commonwealth Folio Studio implementation: source provenance audit, timeline, draft island, viewer usability, security, tests and production review without image generation';
const intent=compileIntent(task);
const routes={
architecture:routeTask('Audit code architecture frontend implementation and test security review',{material:true,forceCounterweights:true,maxSecondary:4}),
provenance:routeTask('Audit canonical source truth provenance unmerged cross PR draft geography',{material:true,forceCounterweights:true,maxSecondary:4}),
creative:routeTask('Audit narrative historical continuity reader access visual production orientation',{material:true,forceCounterweights:true,maxSecondary:4})
};
const ctx={name:'Schemin 26',objective:'Second-pass code review: established 3 divisions/12 homes, 23 LOC, 7 regions, 18 roads, 199 draft codes, Island 23 nodes/45 edges; no image generation.'};
const provider=createAuthenticatedChatProvider({endpoint:'http://127.0.0.1:11434/v1/chat/completions',apiKey:'local-ollama',model:'gemma3:4b',timeoutMs:120000});
const bp=createBullpen({modelProvider:provider,eventBus:adapters.memory.createMemoryEventBus(),dataStore:adapters.memory.createMemoryDataStore(),workflowRegistry:adapters.memory.createMemoryWorkflowRegistry(),traceSink:adapters.memory.createMemoryTraceSink(),projectContext:ctx});
const evidence='Repo PR337 head daa20ae. Folio Studio site/app.js has six tabs: map with 23 active locations and 18 mainland routes; 3 divisions/12 homes; 23 approved structural SVG (NO cinematic art); Island 23 nodes/45 edges and 9 venues draft PR322; 199 exact IDs across PR324+PR325, concordance PR339; character library PR253 internal only. World-state source dated end_of_week_3_2026. Source sha in derived world.json. Source URL builder linkToSource(path,ref="main") runs over source_sha256, including folio and PR bridge files that only live on PR337. Possible broken links. No PNG generation, no data promotion. Two physical Last Field proposals remain unresolved. Prior Python 13 unit tests+browser smoke passed.';
const reviews=[
['the_architect','Find concrete frontend/backend issues and minimal patch plus regression test.'],
['the_librarian','Audit source-link correctness, main-vs-draft provenance and historical status.'],
['the_setup_man','Audit repeatable build and CI, breakage when source changes, browser testing.'],
['the_beat_writer','Audit 12 POVs and reader understanding of lived places, era and identity.'],
['the_umpire','Review independent evidence gates, false approval, privacy, technical risks.'],
['the_closer','Integrate minimum justified changes, prioritize implementation instead of more planning.']
];
(async()=>{
 console.log('ROUTE',JSON.stringify({command:intent.command,three: Object.fromEntries(Object.entries(routes).map(([k,v])=>[k,{primary:v.primary,secondaries:v.secondary,counterweight_plan:v.counterweight_plan}]))}));
 const roleResults=[];
 for(let i=0;i<reviews.length;i+=2){
 const batch=await Promise.all(reviews.slice(i,i+2).map(async([directorSlug,question])=>{
 try{let x=await bp.consultation.consultDirector({directorSlug,userMessage:evidence+'\nReview focus: '+question+'\nReturn strongest 2 source-bounded defects, one test, one recommendation. Under 220 words, no unsupported facts.',maxTokens:290});console.log('ROLE_DONE',directorSlug,x.response.slice(0,100).replace(/\n/g,' '));return{directorSlug,response:x.response,error:null};}
 catch(err){console.log('ROLE_ERR',directorSlug,err.message);return{directorSlug,response:null,error:err.message};}
 }));
 roleResults.push(...batch);
 }
 let prod=await provider.generate({purpose:'visual_production_method_review',system:'You are a project-local AI assistant doing Visual Direction Lead production analysis using environment-design methods publicly associated with Dylan Cole; you are NOT that person, have not consulted him, and are not an independent reviewer. Source-first, no images.',messages:[{role:'user',content:evidence+'\nFocus on reuse of 23 environment references and visual orientation: precise code/UI adjustments for future scene location continuity, nothing generated. Max 180 words.'}],maxTokens:260,projectContext:ctx});
 let ink=await provider.generate({purpose:'inklings_editorial_function_review',system:'You are an AI analytic function under the Inklings storyroom, not a famous human author. Use published-method critique lenses: Ursula K. Le Guin (lived culture/POV), Brandon Sanderson (rules clarity), Tolkien (historic geography). No imitation, no invented engagement or extra canon.',messages:[{role:'user',content:evidence+'\nAssess reader navigation between 12 owner homelands, main/current versus draft Island, and past-vs-current era; give 2 specific UI/data fixes; no images. Max 180 words.'}],maxTokens:260,projectContext:ctx});
 const receipt={schema:'schemin.folio_second_pass_ai_consult_v1',status:'LOCAL_MODEL_CONSULTATIONS_NOT_HUMAN_DIRECTOR_APPROVAL',source_commit:'daa20ae954903d269d96d5f014f746b08f04f4b6',utc:new Date().toISOString(),model:'gemma3:4b',intent_command:intent.command,route_summaries:Object.fromEntries(Object.entries(routes).map(([k,v])=>[k,{primary:v.primary,secondary:v.secondary,counterweight_plan:v.counterweight_plan}])),directors:roleResults,production:{role:'Visual Direction Lead',lens:'Dylan Cole environment-design published-method reference ONLY',response:prod.text},inklings:{role:'Inklings editorial function',lenses:['Ursula K. Le Guin method','Brandon Sanderson method','J.R.R. Tolkien method'],response:ink.text},actual_director_model_responses:roleResults.filter(x=>x.response).length,errors:roleResults.filter(x=>x.error).length};
 const dest=path.join(repo,'world/environment-references/cinematic-folio/SECOND_PASS_AI_CONSULT_RECEIPT_2026-11-20.json');
 fs.writeFileSync(dest,JSON.stringify(receipt,null,2)+'\n');
 console.log('RECEIPT_WRITTEN',dest,receipt.actual_director_model_responses,receipt.errors);
})().catch(err=>{console.error('ERROR',err.stack);process.exitCode=1;});
