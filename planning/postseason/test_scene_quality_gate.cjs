#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {auditDraft}=require('./scene_quality_gate.cjs');
const dir=__dirname;
const cases=[
['HIST-POST-2018-QF-1','INKLINGS_2018_IRON_QUARRY_SCREENPLAY_PILOT_V2.md'],
['HIST-POST-2022-SF-1','INKLINGS_2022_CROWN_STAIR_SCREENPLAY_PILOT_V2.md']
];
const checks=[];
function test(label,callback){callback();checks.push(label);}
const inputs=cases.map(([fixture_id,file])=>({fixture_id,text:fs.readFileSync(path.join(dir,file),'utf8'),model:'ORIGINAL_EDITORIAL_DRAFT'}));
test('Two historical screenplay pilots meet source and three-stage mechanical preflight',()=>{
 for(const x of inputs){const q=auditDraft(x);assert.deepEqual(q.hard_failures,[],x.fixture_id+':'+JSON.stringify(q.hard_failures));assert.ok(q.word_count>1000);}
});
test('No early-round score can be silently omitted',()=>{
 const a={...inputs[0],text:inputs[0].text.replaceAll('114.37','score withheld')};
 assert.ok(auditDraft(a).hard_failures.some(x=>x.includes('MISSING_CERTIFIED_SCORE')));
});
test('Wrong permanent Last Field insertion fails early-round venue lock',()=>{
 const a={...inputs[0],text:inputs[0].text.replace('### EXT. THE IRON QUARRY — MORNING','EXT. IRON QUARRY — LAST FIELD')};
 assert.ok(auditDraft(a).hard_failures.includes('WRONG_PERMANENT_CHAMPIONSHIP_STADIUM_LOCATION'));
});
test('Unauthorized magical hovering stage marker fails',()=>{
 const a={...inputs[0],text:inputs[0].text+'\nA marker hovers above the quarry.\n'};
 assert.ok(auditDraft(a).hard_failures.includes('UNAPPROVED_MAGIC_OR_SELF_ACTUATING_HAZARD'));
});
test('In-world report cannot discuss source compiler authoring',()=>{
 const a={...inputs[0],text:inputs[0].text+'\nThe source system will now append the outcome.\n'};
 assert.ok(auditDraft(a).hard_failures.includes('IN_WORLD_META_SYSTEM_DIALOGUE'));
});
test('Unprotected arrows in active running corridors are vetoed',()=>{
 const a={...inputs[0],text:inputs[0].text.replace(/backstops/g,'open space').replace(/backstop/g,'open space')};
 assert.ok(auditDraft(a).hard_failures.includes('UNPROTECTED_PROJECTILE_AND_RUNNING_CORRIDOR'));
});
test('Stage performer substitution is prohibited',()=>{
 const a={...inputs[1],text:inputs[1].text+'\\nA younger engineer adjusts the rival mechanism and finishes the assembly.'};
 assert.ok(auditDraft(a).hard_failures.includes('SURROGATE_PERFORMS_PRINCIPAL_CONTEST_TASK'));
});
test('Historical matchup round must be named and accurate',()=>{
 const a={...inputs[0],text:inputs[0].text.replace(/quarterfinal/gi,'preliminary trial')};
 assert.ok(auditDraft(a).hard_failures.includes('ROUND_CONTEXT_NOT_EXPLICIT'));
});
test('No pre-playoff championship award in the semifinal',()=>{
 const a={...inputs[1],text:inputs[1].text+'\\nThe winner receives the championship trophy before the final.'};
 assert.ok(auditDraft(a).hard_failures.includes('PREMATURE_CHAMPIONSHIP_AWARD'));
});
test('Stage headers and both principal personas remain required',()=>{
 const a={...inputs[0],text:inputs[0].text.replace('PHASE TWO','MIDDLE')};
 assert.ok(auditDraft(a).hard_failures.includes('THREE_ORDERED_STAGES_AND_RESULT_REQUIRED'));
});
console.log(JSON.stringify({status:'PASS',checks:checks.length,editorial_pilots:inputs.length,scores_protected:true,independent_review:'PENDING',tests:checks},null,2));
