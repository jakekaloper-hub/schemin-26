#!/usr/bin/env node
/** Offline negative controls for bounded autonomous Inklings manuscript audit. */
import assert from 'node:assert/strict';import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {execFileSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),script=path.join(root,'audit_local_inklings_drafts.mjs');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'inklings-qa-'));
const fname=path.join(tmp,'HIST-POST-2018-QF-1.proposal.json');
const receipt=path.join(tmp,'AUDIT.json');
const core='EXT. IRON QUARRY — DAY\nPHASE ONE\nKardiac Kids and Schreck Chappell personally inspect equal protected lanes and neutral markers. Both perform the task themselves before the gathered officials. The quarry surface is stable, the target apparatus is inspected, and the crowd remains behind a safe barrier.\nPHASE TWO\nBoth contenders change approach when the neutral course narrows. Kardiac Kids takes the inside protected route, while Schreck Chappell attempts a wider crossing. Each rival counters directly and retains agency without assistance.\nPHASE THREE\nTheir final attempts are witnessed under the same legal rules and the arena retains only a dated surface mark after safe repair. Officials delay all winner announcements until the verified league result is available.\n';
const filler='Two opposing historical franchise personae act under a clear objective, grounded terrain, safe spectator access, and a controlled technical course. ';
const body=core+filler.repeat(42)+'\nRESULT CERTIFIED\nKardiac Kids 114.37 to Schreck Chappell 114.27. The official historical winner is Kardiac Kids. EPILOGUE. A safe repaired quarry mark remains.';
function run(text){
 fs.writeFileSync(fname,JSON.stringify({fixture_id:'HIST-POST-2018-QF-1',text,model:'SYNTHETIC_FIXTURE_TEST',qa:'PRELIMINARY_FORMAT_SCREEN_ONLY'}));
 execFileSync(process.execPath,[script,'--input='+tmp,'--output='+receipt],{encoding:'utf8',timeout:20000});
 return JSON.parse(fs.readFileSync(receipt,'utf8')).results[0];
}
const tests=[];
function check(name,alter,expected){
 const result=run(alter(body));
 if(expected==='PASS')assert.equal(result.pass,true,JSON.stringify(result.issues));
 else {assert.equal(result.pass,false);assert.ok(result.issues.some(x=>x.includes(expected)),JSON.stringify(result.issues));}
 tests.push(name);
}
try{
check('Source-accurate protected full-length fixture passes syntax and result screen',s=>s,'PASS');
check('False champion language is rejected',s=>s+'\nSchreck Chappell emerges victorious as champion.','LOSER_DESCRIBED_AS_VICTOR');
check('Unverified intermediate score is rejected',s=>s+'\nPHASE ONE RESULT Schreck Chappell 10.9 points.','INVENTED_STAGE_SCORE');
check('Magical blast is rejected',s=>s+'\nThe Immortal uses an energy blast.','UNAPPROVED_SUPERNATURAL_EFFECT');
check('Unprotected collapsing Last Field-like floor is rejected',s=>s+'\nThe ground gave way beneath him into a deep crevice.','UNPROTECTED_HISTORIC_ARENA_COLLAPSE');
check('In-world internal fixture ID is rejected',s=>s+'\nANNOUNCER: HIST-POST-2018-QF-1 starts now!','INTERNAL_FIXTURE_ID_LEAKED_IN_WORLD_DIALOGUE');
check('Unexpected language leakage is rejected',s=>s+'\nA decisive 反击 follows.','UNREVIEWED_LANGUAGE_SCRIPT_LEAK');
check('Truncated prose is rejected',s=>s.slice(0,530),'SHORT_UNDERDEVELOPED_SCREENPLAY');
console.log(JSON.stringify({status:'PASS',test_count:tests.length,tests}));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
