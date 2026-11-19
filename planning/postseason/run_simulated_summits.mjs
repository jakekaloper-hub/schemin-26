#!/usr/bin/env node
/**
 * ACTUAL Bullpen ConsultEngine API invocation using a DISCLOSED DETERMINISTIC
 * SCENARIO PROVIDER, for the Founder's requested SIMULATED summit.
 *
 * IMPORTANT: This is NOT eighteen independently thinking AI model agents and
 * NOT a human consultation with the three named public-method advisors.
 * Source-grounded authored debate input is supplied via fixed role prompts.
 * Event/trace receipts demonstrate orchestration API exercised, not advice validity.
 *
 * BULLPEN_CORE_PATH=/path/to/bullpen node planning/postseason/run_simulated_summits.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const home=path.dirname(fileURLToPath(import.meta.url));
const core=process.env.BULLPEN_CORE_PATH;
if(!core || !fs.existsSync(path.join(core,'runtime','consultEngine.js')))throw new Error('BULLPEN_CORE_PATH must identify an existing, local, authentic Bullpen runtime checkout');
const {createConsultEngine}=require(path.join(core,'runtime','consultEngine.js'));
const {BULLPEN_ORG}=require(path.join(core,'core','org','directorOrg.js'));
const {listAdvisors}=require(path.join(core,'runtime','externalAdvisors.js'));

const perspectives={
the_closer:'One competition constitution, no sidecar canon; two summits must produce a source-linked executable change set.',
the_setup_man:'A modular 3-stage arena needs power, rigging, stage reset, broadcast failover, spectator routing and defined hazard states.',
the_scout:'Protect ESPN bracket, seeds and winners independently from all fictional competition forms and scene proposals.',
the_umpire:'Hard veto on invented historical fact, unapproved Atlas location writes, lethal principal-character mechanics, and unsourced claims.',
the_beat_writer:'Require opposing character strategies, active counters, escalation, one outcome, and emotional consequence; never a random gag montage.',
the_groundskeeper:'The old grounds need visible weathering, scar/repair/dormancy history and a maintenance schedule before every annual reuse.',
the_gm:'Create a useful navigable obstacle lexicon and fixture-to-scene pipeline; measure adoption and distinctness, not list length alone.',
the_pitching_coach:'Constrained combinatorial challenge grammar and negative tests beat an open-ended thousands-of-prompts agent loop.',
the_warden:'Use restrained, survivable weaponry, projectile backstops, safe crowd barriers, water rescue and controlled pyrotechnics.',
the_commissioner:'Former champions and newcomers deserve neutral competition conditions; the bye is protected rest, not a fabricated victory.',
the_analyst:'A fictional points display cannot invent conversions from physical trial time to ESPN fantasy points; the real sports score remains locked.',
the_librarian:'Preserve 2015–25 team slots and venue dates; a 2025 screen may not appear in the 2015 original event.',
the_agent:'Make the audience understand each rule and tactical reversal in the first thirty seconds of a competition scene.',
the_bookkeeper:'Build reusable event rigs and maintenance budgets; no 120 unique stadiums, no magical no-cost modern broadcast expansion.',
the_commissioner_general:'Honor the Michael Farrell memorial; use genre influences without copyrighted scene copying or invented biographies.',
the_clubhouse_manager:'Assign actual support roles—stewards, referees, operators, registrars, stage builders—across changing era capacities.',
the_scout_master:'Spectator logistics, premium suites, resort accessibility and a dignified championship procession must reinforce, not overwhelm, competition.',
the_architect:'Implement round-fixed venue capabilities and an Atlas-derived spatial compatibility contract; do not fork World OS.'
};
const advisorText={
'jeff_lunsford':'The opportunity is a reusable production product: one lexicon feeding interactive Atlas preview, weekly Memo and historical Novel. Overbuilding 120 bespoke rigs is poor leverage. Measure stories rendered per certified venue capability and do not promote a raw catalog without readers comprehending it.',
'john_ezzell':'Treat challenge registry as candidate content, not geography truth. Stable IDs, source-of-truth boundaries, schema versioning, interoperability contracts and negative tests prevent two competing Atlas maps. Reusing the exact venue IDs in the current PR is essential.',
'tim_veil':'The system must be reproducible and fail closed: frozen historical result spine, seeded or deterministic challenge selection, valid site affordances, explicit era state, no unverified 2026 fixtures, and independent quality gates. Model or simulator output never authorizes canon.'
};
const counters={};
const trace=[],events=[];
const provider={async generate(req){
 counters[req.purpose]=(counters[req.purpose]||0)+1;
 if(req.purpose==='director_consult'){
   const slug=req.director?.slug;
   if(!perspectives[slug])throw new Error('Missing authored Director scenario '+slug);
   return {text:perspectives[slug],model:'SCRIPTED_SCENARIO_PROVIDER_NOT_LLM'};
 }
 if(req.purpose==='board_synthesis')return {text:'The 18 seeded perspectives agree on one physical obstacle lexicon, Founder fixed arenas, historical scars, a lean beach village, evidence-locked outcomes, and split world-technology/release gates. Dissent: the bigger the catalog, the more demanding the compatibility QA.',model:'SCRIPTED_SCENARIO_PROVIDER_NOT_LLM'};
 if(req.purpose==='external_advisor_lens'){
   const name=(req.system.match(/documented work of ([^\.]+)\./)||[])[1]||'';
   const slug=name.includes('Lunsford')?'jeff_lunsford':name.includes('Ezzell')?'john_ezzell':name.includes('Veil')?'tim_veil':null;
   if(!slug)throw new Error('Unknown advisor marker '+name);
   return {text:advisorText[slug],model:'SCRIPTED_SCENARIO_PROVIDER_NOT_LLM'};
 }
 throw new Error('Unsupported simulation purpose '+req.purpose);
}};
const engine=createConsultEngine({
 modelProvider:provider,eventBus:{emit:(type,obj)=>events.push({type,actor:obj?.director||obj?.advisor||null})},
 traceSink:{record:x=>trace.push({type:x.type,actor:x.director||x.advisor||null})},
 projectContext:{projectName:'Schemin 26 Championship Island',projectId:'schemin-26'},
 boardConcurrency:4,retryDelayMs:0
});
const directors=BULLPEN_ORG.map(x=>x.slug);
if(directors.length!==18||Object.keys(perspectives).length!==18)throw new Error('18-person governance roster mismatch');
const advisors=['jeff_lunsford','john_ezzell','tim_veil'];
if(!advisors.every(s=>listAdvisors().some(x=>x.slug===s)))throw new Error('Three official consultant registry slugs missing');
const board=await engine.conveneBoardMeeting({
 topic:'Full board: Championship Island 12-angle competition grammar, sports/challenges, 2015–25 heritage, modern 2026, spatial-physical operating model and release',
 directorSlugs:directors
});
const consult=[];
for(const slug of advisors)consult.push(await engine.consultExternalAdvisor({advisorSlug:slug,userMessage:'Review the same Founder V2 Championship Island, 18-Director 12-angle summit plan. Prioritize concrete implementation critiques and measurable acceptance gates.',maxTokens:300}));
if(board.responses.some(x=>x.error||!x.response)||!board.synthesis)throw new Error('Some scripted board submissions missing');
const report={
schema:'schemin.postseason.simulated_consultengine_receipt.v1',
status:'SIMULATED_MODEL_RESPONSES_EXECUTED_VIA_REAL_BULLPEN_CONSULT_ENGINE',
disclaimer:'Real Bullpen runtime consultation APIs invoked using scripted deterministic response provider, not independently reasoning model workers, not human advisors, not advisory endorsement.',
board:{director_count:board.responses.length,synthesis:board.synthesis,participants:board.responses.map(x=>({slug:x.director.slug,title:x.director.name||x.director.slug,assessment:x.response}))},
consultants:consult.map((x,i)=>({slug:advisors[i],name:x.advisor.name,mode:x.mode,humanVerified:x.humanVerified,disclaimer:x.disclaimer,review:x.response})),
telemetry:{calls:counters,events:events.length,traces:trace.length},
source:'SUMMIT_2026_11_19_18_DIRECTORS_12_ANGLES_V1.md',
approval:'NOT_INDEPENDENT_QA_NOT_CANON'
};
if(report.board.director_count!==18||report.consultants.length!==3||report.telemetry.calls.director_consult!==18||report.telemetry.calls.external_advisor_lens!==3)throw new Error('Live orchestration rehearsal incomplete');
const out=path.join(home,'SIMULATED_CONSULTENGINE_18_DIRECTORS_3_ADVISORS_RECEIPT.json');
fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',output:path.basename(out),directors:18,consultants:3,telemetry:report.telemetry,provider:'DISCLOSED_SCRIPTED_SCENARIO'}));
