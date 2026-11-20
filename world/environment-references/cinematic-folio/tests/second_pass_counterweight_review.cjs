'use strict';
const fs=require('fs'),root=process.env.HOME+'/Developer/ai/bullpen-runtime';
const {createBullpen,adapters}=require(root);
const modelProvider=adapters.authenticatedChat.createAuthenticatedChatProvider({
 endpoint:'http://127.0.0.1:11434/v1/chat/completions',apiKey:'local-ollama',
 model:'gemma3:4b',timeoutMs:120000
});
const context={name:'Schemin 26',objective:'Counterweight review of Folio source-link fix and source-bound Island timeline, code only'};
const bp=createBullpen({modelProvider,eventBus:adapters.memory.createMemoryEventBus(),
 dataStore:adapters.memory.createMemoryDataStore(),
 workflowRegistry:adapters.memory.createMemoryWorkflowRegistry(),
 traceSink:adapters.memory.createMemoryTraceSink(),projectContext:context});
const cases=[
 ['the_gm','As Architect counterweight, assess whether fixing draft source links and adding an evidence-only Island timeline is a minimal useful change, rather than extra complexity.'],
 ['the_clubhouse_manager','As Librarian counterweight, examine duplicate-source risk and whether one Folio index must remain derived instead of becoming canon.'],
 ['the_scout','As Beat Writer counterweight, protect the Week 3 state cutoff and the distinction between verified historic bracket results and fictional Island venue staging.']
];
(async()=>{
const out=[];
for(const [directorSlug,focus] of cases){
 try {
 const r=await bp.consultation.consultDirector({directorSlug,
  userMessage:'PR337 records 23 active LOC, 12 homes, 18 routes, 7 regions, a 199-code draft concordance and an unmerged proposed 23-node/45-edge Island. Code-only second pass. '+focus+' Give specific grounded recommendation and one test. Do not invent facts or imply approval.',
  maxTokens:230});
 out.push({directorSlug,response:r.response,error:null});
 console.log('COUNTERWEIGHT',directorSlug,'COMPLETE');
 } catch(err) {out.push({directorSlug,response:null,error:err.message});console.log('COUNTERWEIGHT',directorSlug,'FAILED');}
}
const f='world/environment-references/cinematic-folio/SECOND_PASS_AI_CONSULT_RECEIPT_2026-11-20.json';
const d=JSON.parse(fs.readFileSync(f,'utf8'));
d.activated_counterweight_reviews={status:'LOCAL_AI_ROLE_INVOCATION_NOT_HUMAN_SIGNATURE',records:out};
d.actual_director_model_responses+=out.filter(x=>x.response).length;
d.errors+=out.filter(x=>x.error).length;
fs.writeFileSync(f,JSON.stringify(d,null,2)+'\n');
console.log('COUNTERWEIGHTS_COMPLETE',out.filter(x=>x.response).length);
})().catch(err=>{console.error(err.message);process.exitCode=1;});
