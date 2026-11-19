'use strict';
/**
 * Adversarial deterministic screenplay preflight.
 * An APPROVED result means only machine-detectable constraints passed; never
 * independently certified art, story quality, Atlas geography or historical owners.
 * This module is designed to prevent false READY_FOR_EDITORIAL_REVIEW tags.
 */
const fs=require('fs');
const path=require('path');
const ROOT=__dirname;
const read=x=>JSON.parse(fs.readFileSync(path.join(ROOT,x),'utf8'));
const fixtures=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const draws=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const sourceMap=new Map(fixtures.fixtures.map(x=>[x.id,x]));
const drawnMap=new Map(draws.ceremonies.map(x=>[x.fixture_id,x]));
const stages=['PHASE ONE','PHASE TWO','PHASE THREE'];
const scoreString=x=>Number(x).toFixed(2);
function sections(raw){
 const upper=raw.toUpperCase();
 const starts=stages.map(s=>upper.indexOf(s));
 const marker=upper.indexOf('RESULT CERTIFIED');
 if(starts.some(x=>x<0)||marker<0||starts.some((x,i)=>i>0 && x<=starts[i-1])||marker<=starts[2])return null;
 return starts.map((x,i)=>raw.slice(x,(i===2?marker:starts[i+1])));
}
function matchName(raw,name){
 // For exact league aliases, simple string inclusion avoids regex punctuation mistakes.
 return String(raw).toLowerCase().includes(String(name).toLowerCase());
}
function auditDraft({fixture_id,text,model=null}){
 const fixture=sourceMap.get(fixture_id),draw=drawnMap.get(fixture_id);
 if(!fixture||!draw)throw Error('Unknown source fixture: '+fixture_id);
 const t=String(text||''),warnings=[],hard=[];
 const add=(target,msg)=>{if(!target.includes(msg))target.push(msg);};
 if(!t.trim())add(hard,'EMPTY_SCRIPT');
 const wordCount=t.trim().split(/\s+/).filter(Boolean).length;
 if(wordCount<550)add(hard,'INSUFFICIENT_SCENE_DEPTH_UNDER_550_WORDS');
 if(wordCount>2500)add(warnings,'EXCESSIVE_LENGTH_REVIEW_PACING');
 if(!/EXT\./i.test(t))add(hard,'NO_PHYSICAL_ESTABLISHING_SLUG');
 if(!matchName(t,fixture.home.name)||!matchName(t,fixture.away.name))add(hard,'BOTH_CONTESTANTS_NOT_IDENTIFIED');
 if(!matchName(t,draw.obstacle_name))add(hard,'CEREMONIAL_DRAW_NOT_IDENTIFIED');
 if(!matchName(t,fixture.staging.venue_name))add(hard,'CORRECT_FIXED_ARENA_NOT_IDENTIFIED');
 const blocks=sections(t);
 if(!blocks)add(hard,'THREE_ORDERED_STAGES_AND_RESULT_REQUIRED');
 else for(let i=0;i<blocks.length;i++){
   const b=blocks[i];
   if(!matchName(b,fixture.home.name))add(hard,'SOLO_HOME_ABSENT_IN_STAGE_'+(i+1));
   if(!matchName(b,fixture.away.name))add(hard,'SOLO_AWAY_ABSENT_IN_STAGE_'+(i+1));
   if(b.trim().split(/\s+/).length<65)add(warnings,'THIN_CHOREOGRAPHY_STAGE_'+(i+1));
 }
 for(const n of [scoreString(fixture.home.points),scoreString(fixture.away.points)]){
  if(!t.includes(n))add(hard,'MISSING_CERTIFIED_SCORE_'+n);
 }
 const winner=fixture.home.team_slot===fixture.winner_slot?fixture.home:fixture.away;
 if(!matchName(t.slice(Math.max(0,t.toUpperCase().indexOf('RESULT CERTIFIED'))),winner.name))
   add(hard,'WINNER_NOT_DECLARED_AT_CERTIFICATION');
 if(!/certif|official|arbiter|judge/i.test(t))add(hard,'NO_FORMAL_SOURCE_RESULT_CERTIFICATION');
 if(!/repair|retain|archiv|preserv|seal/i.test(t))add(hard,'NO_PERMANENT_SCAR_AND_SAFE_REMEDIATION');
 const round={QF:/\bquarterfinal\b/i,SF:/\bsemifinal\b/i,FINAL:/\bchampionship\b|\bfinal\b/i}[fixture.round];
 if(!round.test(t))add(hard,'ROUND_CONTEXT_NOT_EXPLICIT');
 if(fixture.round==='QF' && /\bthe final four are here\b/i.test(t))add(hard,'QUARTERFINAL_MISTAKEN_FOR_FINAL_FOUR');
 if(fixture.round!=='FINAL' && /receives the (?:championship )?(?:belt|trophy)/i.test(t))
   add(hard,'PREMATURE_CHAMPIONSHIP_AWARD');
 // Founder F18: contest performed personally. Supporting workers can PREPARE/inspect,
 // but cannot build, fire, compete, or complete the stages on behalf of a principal.
 const surrogatePatterns=[
  /\b(?:one|an?|another|younger|senior|other)\s+engineer\b.{0,110}\b(?:adjust|assemble|brace|repair|redirect|reinforc|leap|finish)/is,
  /\b(?:their|his|her|the)\s+team\s+(?:scrambl|assembl|construct|build|rush|attack|fight|perform|compete|complete|reinforc)/i,
  /\b(?:teammate|team mate|companion|assistant|aide|retinue)\b.{0,90}\b(?:complet|perform|fire|steer|build|finish|win)/is
 ];
 if(surrogatePatterns.some(p=>p.test(t)))add(hard,'SURROGATE_PERFORMS_PRINCIPAL_CONTEST_TASK');
 const magicPatterns=[
  /\b(?:marker|symbol|stone)\s+(?:hovers|levitates|floats in midair|shudders with magic)\b/i,
  /\b(?:ignites|glows|glowing|magically)\b.{0,50}\b(?:stone|sigil|marker|energy)\b/i,
  /\b(?:stone|sigil|marker)\b.{0,50}\b(?:glows|radiates|ignites)\b/i
 ];
 if(magicPatterns.some(p=>p.test(t)))add(hard,'UNAPPROVED_MAGIC_OR_SELF_ACTUATING_HAZARD');
 if(/\b(?:sheer drop into|plunge into|leap into)\b.{0,55}\b(?:pit|abyss|void)\b/i.test(t)
    && !/\b(?:catch net|safety net|harness|padded landing|rescue)\b/i.test(t))
   add(hard,'UNMITIGATED_FATAL_ARENA_HAZARD');
 if(/\b(?:a wiry woman|a broad-shouldered man|a younger engineer)\b/i.test(t))
   add(warnings,'UNVERIFIED_HISTORIC_PERSON_DESCRIPTION');
 if(/\b(?:2026)\b.{0,80}\b(?:champion|finalist|title winner|won)\b/i.test(t))
   add(hard,'FUTURE_2026_OUTCOME_CONTAMINATION');
 if(/\b(?:I personally interviewed|actual historical physical footage|real-world injury confirmed)\b/i.test(t))
   add(hard,'FALSE_HISTORY_OR_ACCESS_CLAIM');
 if(!/BROADCAST|COMMENTAT|ANNOUNC/i.test(t))add(warnings,'NO_PROFESSIONAL_BROADCAST_PERSPECTIVE');
 return {
   fixture_id,word_count:wordCount,expected_draw:draw.obstacle_name,
   verified:{winner_slot:fixture.winner_slot,scores:[fixture.home.points,fixture.away.points]},
   hard_failures:hard,warnings,
   machine_gate:hard.length?'HOLD_MACHINE_FAILURE':'PASS_MACHINE_ONLY',
   editorial_gate:'PENDING_BEAT_WRITER_AND_INDEPENDENT_UMPIRE',
   model:model||null,
   caveat:'Deterministic checks cannot independently certify narrative, history or actual physical safety.'
 };
}
module.exports={auditDraft};
if(require.main===module){
 const file=process.argv[2];
 if(!file)throw Error('Usage node scene_quality_gate.cjs /path/to/draft.proposal.json');
 const result=JSON.parse(fs.readFileSync(file,'utf8'));
 const output=auditDraft(result);
 console.log(JSON.stringify(output,null,2));
 if(output.hard_failures.length)process.exitCode=2;
}
