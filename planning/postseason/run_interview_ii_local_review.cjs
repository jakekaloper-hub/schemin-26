#!/usr/bin/env node
'use strict';
/* Local model-backed Bullpen review. Not live human advisers or certified Umpire. */
const fs=require('fs'),path=require('path');
const core=process.env.BULLPEN_CORE_PATH,root=__dirname;
if(!core||!fs.existsSync(path.join(core,'runtime','consultEngine.js')))throw Error('BULLPEN_CORE_PATH required');
const bullpen=require(core);
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const traces=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const scenes=read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json');
const chosen=scenes.cards.find(x=>x.fixture_id==='HIST-POST-2025-FINAL-1');
const drawName=draw.ceremonies.find(x=>x.fixture_id===chosen.fixture_id).obstacle_name;
const scar=traces.traces.find(x=>x.fixture_id===chosen.fixture_id);
const constraints=[
'ESPN source determines real winners/seeds. Physical events are proposed fictional reconstructions.',
'All three phases must be performed personally by both historical franchise personae; real human owner lineage must NOT be inferred from franchise slot.',
'Every encounter leaves a permanent history/terrain imprint, even though hazards are safely repaired.',
'The Last Field original gates/footprint are maintained despite effects and modern stadium machinery.',
'No permanent principal death, spectator harm, unsupported Michael Farrell biography or trophy-naming date.',
'2026 contest results/participants unknown and cannot be invented.',
'Your output is a LOCAL MODEL CRITIQUE, not authorized independent Umpire certification.'
].join('\n');
const common=[
'Championship Island 2015–2025: 56 verified league H2H matches, 120 original contest seeds, 56 source-independent retrospective ceremonial draws, 56 persistent terrain/material traces, 168 draft personal performance phases, 672 camera-shot contracts.',
'2025 verified final: The Immortal 161.07 defeats ObiWan Jacoby 109.56. Fictional draw: '+drawName+'. Proposed impact: '+scar.trace_kind+' at '+scar.original_material_anchor+'.',
'Stage rough drafts: '+JSON.stringify(chosen.acts.map(x=>x.scene_text.slice(0,300))),
'Please report FOUR specific weaknesses or risks with concrete corrective suggestions and observable failure tests. Do not merely praise. Do not claim live human participation.',
constraints
].join('\n');
const model=process.env.OLLAMA_MODEL||'qwen2.5-coder:7b';
const provider=bullpen.adapters.authenticatedChat.createAuthenticatedChatProvider({
 endpoint:'http://127.0.0.1:11434/v1/chat/completions',apiKey:'local-loopback-only',model,timeoutMs:120000});
const bus=bullpen.adapters.memory.createMemoryEventBus();
const trace=bullpen.adapters.memory.createMemoryTraceSink();
const engine=bullpen.createConsultEngine({modelProvider:provider,eventBus:bus,traceSink:trace,projectContext:{projectName:'Schemin 26 Championship Island',projectId:'schemin-26'}});
(async()=>{
const roles=[
 ['the_beat_writer','Test authentic scene choreography, individual character agency, progressive dramatic stakes and varied competitor strategies.'],
 ['the_architect','Test physics, fixed-stadium continuity, stage safety, cumulative impact and year-correct spatial/technical conditions.'],
 ['the_umpire','Adversarial Umpire-perspective critique, NOT formal signoff. Test source/fiction boundaries, unapproved releases, quality misrepresentation and future leaks.']
];
const reviews=[];
for(const [slug,scope] of roles){
 const x=await engine.consultDirector({directorSlug:slug,userMessage:scope+'\n'+common,maxTokens:480});
 reviews.push({director:slug,model,text:x.response,human:false,approval:'ADVISORY_NOT_INDEPENDENT_CERTIFICATION'});
 console.log(JSON.stringify({director:slug,words:x.response.trim().split(/\s+/).length,mode:'ACTUAL_LOCAL_MODEL'}));
}
const receipt={schema:'schemin.postseason.interview_ii_local_critique.v1',status:'REAL_MODEL_DIRECTOR_METHOD_CONSULTATIONS_ADVISORY_ONLY',
 note:'Three distinct Director prompts, one local LLM model, authentic Bullpen consultation interface. Not three different models, not human consultants, not official independent Umpire signoff.',
 model,context:'PR #322 candidate files',historical_fixture_count:history.fixtures.length,
 event_count:bus.events.length,trace_count:trace.traces.length,reviews,
 release:'PENDING_INDEPENDENT_UMPIRE'};
fs.writeFileSync(path.join(root,'INTERVIEW_II_LOCAL_MODEL_CRITIQUE_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',review_count:reviews.length,model,release:receipt.release}));
})().catch(e=>{console.error(e.message);process.exitCode=1});
