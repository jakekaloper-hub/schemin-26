#!/usr/bin/env node
/**
 * Autonomous-but-bounded Inklings local screenplay writer.
 * Must be explicitly invoked on a historical known fixture; never writes
 * canonical World data, 2026 projections, live website or final publication.
 * Uses a locally running Ollama model via authenticated Bullpen provider adapter.
 * Writes ONLY noncanon markdown and source-bound manifest to --out directory.
 *
 * Usage: BULLPEN_CORE_PATH=/path/to/bullpen node run_inklings_local_scene_writer.cjs
 *        --fixtures HIST-POST-2025-FINAL-1,HIST-POST-2018-QF-1
 */
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=__dirname,core=process.env.BULLPEN_CORE_PATH;
if(!core||!fs.existsSync(path.join(core,'index.js')))throw Error('Authentic Bullpen core required');
const bullpen=require(core);
const read=x=>JSON.parse(fs.readFileSync(path.join(root,x),'utf8'));
const fsinput=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const stages=read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json');
const impacts=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const all=fsinput.fixtures;
const getArg=(k,def)=>{const x=process.argv.find(a=>a.startsWith('--'+k+'='));return x?x.slice(k.length+3):def;};
const ids=getArg('fixtures','HIST-POST-2025-FINAL-1').split(',').map(x=>x.trim());
if(ids.length<1||ids.length>3)throw Error('Bounded limit: one to three specified source-verified historic fixtures per invocation');
if(new Set(ids).size!==ids.length||ids.some(id=>!all.some(f=>f.id===id)))throw Error('Only known 2015–2025 fixtures may be scripted');
const outdir=path.resolve(root,getArg('out','drafts-local-llm'));
const model=process.env.OLLAMA_MODEL||'qwen2.5-coder:7b';
const provider=bullpen.adapters.authenticatedChat.createAuthenticatedChatProvider({
 endpoint:'http://127.0.0.1:11434/v1/chat/completions',apiKey:'local-loopback-only',model,timeoutMs:120000});
const bus=bullpen.adapters.memory.createMemoryEventBus();
const traces=bullpen.adapters.memory.createMemoryTraceSink();
const words=t=>String(t).trim().split(/\s+/).filter(Boolean).length;
const sha=t=>crypto.createHash('sha256').update(t).digest('hex');
const unsafeOutput=t=>/(2026.{0,80}(?:champion|title.?winner|finalist))|(?:real world injury confirmed)|(?:I personally interviewed)/i.test(t);
(async()=>{
fs.mkdirSync(outdir,{recursive:true});
const results=[];
for(const id of ids){
 const fixture=all.find(f=>f.id===id);
 const contract=stages.cards.find(x=>x.fixture_id===id);
 const impact=impacts.traces.find(x=>x.fixture_id===id);
 const ceremony=draw.ceremonies.find(x=>x.fixture_id===id);
 if(!contract||!impact||!ceremony)throw Error('Missing source packet for '+id);
 const winner=fixture.home.team_slot===fixture.winner_slot?fixture.home:fixture.away;
 const loser=fixture.home.team_slot===fixture.winner_slot?fixture.away:fixture.home;
 const prompt=[
'You are an INKLINGS creative production writer under Bullpen Beat Writer authority. Produce a fully original, cinematic 700–950 word English DRAFT screenplay with separate three-phase action sequences and comprehensible physical objective. Do not write like a named existing novelist. Do not mention instructions.',
'The historical fantasy league scoreboard is VERIFIED FACT. This competition arena and physical challenge are FICTIONAL secondary-world dramatizations.',
'This fiction is set in season '+fixture.year+'; playoff round '+fixture.round+'; permanently fixed-round location '+fixture.staging.venue_name+'. Never use internal IDs as announcer dialogue.',
'Both named contender personae must personally perform ALL THREE STAGES. Competitor A: '+fixture.home.name+'; Competitor B: '+fixture.away.name+'. Keep the winner and real-world fantasy scores UNKNOWN in your prose; the source system will append the official result after you finish writing.',
'The draw selects the challenge '+ceremony.obstacle_name+'. State three explicit neutral safety-checked objectives and contested checkpoints. If this is Quarry Ambush, the course is constructed from removable foam/stone-faced panels at the Last Field; the permanent stadium has NO real quarry, collapse, deep chasm or unstable floor. All stage apparatus is load inspected.',
'Stage briefs: '+JSON.stringify(contract.acts.map(a=>({number:a.number,objective:a.objective,action:a.scene_text.slice(0,460)}))),
'The arena must acquire a lasting physical mark: '+impact.trace_kind+' at '+impact.original_material_anchor+'. It is safely restored without erasing material history.',
'Write dynamic scene action, one broadcaster line per stage, two distinct physical strategies, changing terrain use, and material realism. STOP at the end of PHASE THREE BEFORE ANY VICTORY OR SCORE IS KNOWN. Do not invent interim scores, declared phase winners, energy blasts or magical mechanics.',
'No real historical human-owner names or biographies based merely on team slot. No principal death or spectator harm. No invented Farrell biography or trophy naming. Last Field original gates, foundation and field orientation always maintained. No sharp unauthorized weapons, supernatural powers, magical energy, glowing crystals, physical collapse or unprotected crevices. All controlled strikes and projectiles must have visible safety measures.',
'Use headings EXT., PHASE ONE, PHASE TWO, PHASE THREE and stop immediately. Each phase must show BOTH characters acting personally and the opponent countering. Do not write RESULT CERTIFIED or EPILOGUE; the compiler writes those using verified records. NEVER declare either winner, any phase victor, or any numerical phase points. No internal fixture IDs in prose. English only. Do not assume 2026 happened.'
].join('\n');
 const response=await provider.generate({purpose:'inklings_scene_writer',system:'Write only a source-neutral three-stage fictional contest up to the moment officials call time. Do not assign a winner, title or scores; the immutable source system writes the final result. No historical owner biography, supernatural powers or invented stage numbers.',messages:[{role:'user',content:prompt}],maxTokens:2400,projectContext:{projectName:'Schemin 26',projectId:'schemin-26'}});
 const generated=String(response?.text||'').trim();
 const body=generated+'\n\nRESULT CERTIFIED\nThe official, externally verified  '+fixture.year+' title-path result is '+winner.name+' '+winner.points.toFixed(2)+' to '+loser.name+' '+loser.points.toFixed(2)+'. The in-world demonstration did not generate these fantasy-football scores. The surviving competitor advances; the defeated competitor leaves for the seasonal resort.\n\nEPILOGUE\n The stage equipment is safely inspected, and '+impact.trace_kind+' remains an identifiable permanent historic trace at '+impact.original_material_anchor+'. No irreversible harm to any principal or spectator is depicted.\n';
 const issues=[];
 for(const label of [fixture.home.name,fixture.away.name])if(!body.includes(label))issues.push('MISSING_PERSONA:'+label);
 for(const header of ['PHASE ONE','PHASE TWO','PHASE THREE'])if(!body.includes(header))issues.push('MISSING_PHASE:'+header);
 if(words(body)<320)issues.push('SHORT_DRAFT');
 if(unsafeOutput(body))issues.push('POTENTIAL_CANON_FUTURE_OR_FALSE_HISTORY');
 const record={fixture_id:id,model,source_year:fixture.year,truth:{winner_slot:fixture.winner_slot,scores:[fixture.home.points,fixture.away.points]},
 selected_obstacle:ceremony.selected_obstacle_id,permanent_impact:impact.trace_id,word_count:words(body),qa:issues.length?'REJECT_PRELIMINARY':'PRELIMINARY_FORMAT_SCREEN_ONLY',issues,
 disclaimer:'Locally model-generated fictional script draft. No human author, independent Umpire, renderer or live canon signoff.',text:body};
 fs.writeFileSync(path.join(outdir,id+'.proposal.json'),JSON.stringify(record,null,2)+'\n');
 results.push({fixture_id:id,words:record.word_count,qa:record.qa,issues});
 console.log(JSON.stringify(results.at(-1)));
}
const manifest={schema:'schemin.inklings.local_writer_receipt.v1',status:'MODEL_GENERATED_UNRELEASED_DRAFTS',model,fixtures:results,events:bus.events.length,traces:traces.traces.length};
fs.writeFileSync(path.join(outdir,'MANIFEST.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify({status:'COMPLETE_DRAFTS_UNRELEASED',model,count:results.length,output:outdir}));
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
