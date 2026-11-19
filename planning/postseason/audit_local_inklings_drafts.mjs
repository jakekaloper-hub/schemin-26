#!/usr/bin/env node
/** Source-first adversarial filter for untrusted AI-written screenplays.
 * Never publishes generated text or changes Canon.
 */
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const hist=JSON.parse(fs.readFileSync(path.join(root,'HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json'),'utf8'));
const byId=new Map(hist.fixtures.map(f=>[f.id,f]));
const opt=n=>process.argv.find(x=>x.startsWith('--'+n+'='))?.split('=').slice(1).join('=');
const inp=opt('input');if(!inp)throw Error('--input= is required');
const dir=path.resolve(process.cwd(),inp);
const files=fs.readdirSync(dir).filter(x=>x.startsWith('HIST-POST-')&&x.endsWith('.proposal.json'));
const escape=s=>s.replace(/[^A-Za-z0-9]/g,x=>'\\'+x);
function inspect(x){
 const f=byId.get(x.fixture_id);if(!f)throw Error('Unknown fixture '+x.fixture_id);
 const winner=f.winner_slot===f.home.team_slot?f.home:f.away;
 const loser=f.winner_slot===f.home.team_slot?f.away:f.home;
 const body=String(x.text||''),issues=[];
 const wrong=new RegExp(escape(loser.name)+'(?:(?!\\n\\n).){0,95}(?:victorious|verified winner|emerges? victorious|stands? victorious|is the winner|defeats?|has won|prevails?)','ig');
 if(wrong.test(body))issues.push('LOSER_DESCRIBED_AS_VICTOR');
 const wrongShort=new RegExp(escape(loser.name.split(' ')[0])+'(?:(?!\\n\\n).){0,45}(?:is victorious|stands victorious|emerges victorious)','ig');
 if(wrongShort.test(body))issues.push('LOSER_SHORT_NAME_VICTORY_CONTRADICTION');
 if(/phase\s*(?:one|two|1|2)\s*result/i.test(body))issues.push('UNTRUSTED_INTERMEDIATE_SCORE_OR_DECLARATION');
 const sourceScores=new Set([f.home.points.toFixed(2),f.away.points.toFixed(2),String(f.home.points),String(f.away.points)]);
 const numbers=[...body.matchAll(/\b\d{1,4}\.\d{1,3}\b/g)].map(m=>m[0]);
 const invented=numbers.filter(n=>!sourceScores.has(n));
 if(invented.length)issues.push('INVENTED_STAGE_SCORE:'+invented.slice(0,6).join(','));
 if(/energy blast|glowing crystal|magical blast|teleport|saber flashing|supernatural beam|enchanted weapon/i.test(body))issues.push('UNAPPROVED_SUPERNATURAL_EFFECT');
 if(/2026.{0,75}(?:winner|champion|finalist)/i.test(body))issues.push('PREWRITTEN_2026_OUTCOME');
 if(!body.includes(f.home.name)||!body.includes(f.away.name))issues.push('MISSING_TWO_OPPONENTS');
 for(const key of ['PHASE ONE','PHASE TWO','PHASE THREE'])if(!body.toUpperCase().includes(key))issues.push('MISSING_'+key.replaceAll(' ','_'));
 if(body.trim().split(/\s+/).length<650)issues.push('SHORT_UNDERDEVELOPED_SCREENPLAY_TARGET_650_WORDS');
 if(/deep crevice|ground gave way beneath|fell into a chasm|fell off the cliff/i.test(body))issues.push('UNPROTECTED_HISTORIC_ARENA_COLLAPSE');
 if(/weapons in hand|unsheathed weapon|sharp blade/i.test(body) && !/padded|controlled|blunted/i.test(body))issues.push('UNSPECIFIED_CONTROLLED_WEAPON_SAFETY');
 if(/HIST-POST-[0-9]{4}/.test(body))issues.push('INTERNAL_FIXTURE_ID_LEAKED_IN_WORLD_DIALOGUE');
 if(/[\u3400-\u9fff]/.test(body))issues.push('UNREVIEWED_LANGUAGE_SCRIPT_LEAK');
 if(!/(RESULT CERTIFIED|FINAL RESULT|OFFICIAL RESULT)/i.test(body))issues.push('MISSING_RESULT_CERTIFICATION');
 if(!body.includes(winner.name))issues.push('MISSING_SOURCE_WINNER');
 return {fixture_id:x.fixture_id,model:x.model,source_winner_slot:f.winner_slot,
  sha256:crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex'),
  initial_format_qa:x.qa,
  audit_status:issues.length?'REJECT_SOURCE_OR_CANON_DRIFT':'SCREEN_PASSED_EDITORIAL_NOT_YET_APPROVED',
  pass:issues.length===0,issues,
  publication_allowed:false,formal_independent_umpire:'PENDING'};
}
const results=files.map(f=>inspect(JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'))));
const receipt={schema:'schemin.inklings.model_draft_adversarial_audit.v1',status:'PREPRODUCTION_ONLY',
 files:results.length,passed:results.filter(x=>x.pass).length,rejected:results.filter(x=>!x.pass).length,
 results,release:'HOLD_SOURCE_EDITS_AND_FORMAL_UMPIRE'};
const dst=path.resolve(process.cwd(),opt('output')||path.join(inp,'AUDIT.json'));
fs.writeFileSync(dst,JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify({status:'AUDIT_COMPLETE_NOT_PUBLICATION',passed:receipt.passed,rejected:receipt.rejected,
 findings:results.map(x=>({fixture_id:x.fixture_id,diagnostics:x.issues})),receipt:dst}));
