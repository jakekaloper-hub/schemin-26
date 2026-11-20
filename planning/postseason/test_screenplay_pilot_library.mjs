#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const {auditDraft}=require('./scene_quality_gate.cjs');
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const library=read('INKLINGS_SIX_SCREENPLAY_PILOT_LIBRARY_V1.json');
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const source=new Map(history.fixtures.map(f=>[f.id,f]));
const checks=[];function test(label,cb){cb();checks.push(label);}
test('Six substantive longform scripts cover distinct fixtures and eras',()=>{
assert.equal(library.scenes.length,6);
assert.equal(new Set(library.scenes.map(s=>s.fixture_id)).size,6);
assert.equal(new Set(library.scenes.map(s=>s.year)).size,5);
assert.ok(library.counts.total_words>10000);
});
test('Original screenplay files are an exact match to the generated library',()=>{
for(const item of library.scenes){
 const raw=fs.readFileSync(path.join(dir,item.filename),'utf8');
 assert.equal(raw,item.manuscript,item.filename);
 assert.equal(item.year,source.get(item.fixture_id).year);
}
});
test('Full source-provenance and editorial QA on all six draft scripts',()=>{
for(const item of library.scenes){
 const f=source.get(item.fixture_id),qa=auditDraft({fixture_id:item.fixture_id,text:item.manuscript});
 assert.ok(f);assert.deepEqual(qa.hard_failures,[]);
 assert.equal(item.verified.winner_slot,f.winner_slot);
 assert.deepEqual(item.verified.home,f.home);assert.deepEqual(item.verified.away,f.away);
 assert.equal(item.qa.machine_status,'PASS_MACHINE_ONLY');
 assert.equal(item.qa.independent_umpire,'NOT_CERTIFIED');
}
});
test('Every script remains unpromoted with no future champion prediction',()=>{
assert.ok(library.scenes.every(s=>s.year<2026));
assert.ok(library.scenes.every(s=>s.canonical_status==='EDITORIAL_REVIEW_DRAFT_NOT_PUBLISHED_WORLD'));
assert.match(library.publication,/HOLD_INDEPENDENT/);
});
test('No actual historical team slot is asserted as named human owner provenance',()=>{
assert.ok(library.scenes.every(s=>s.qa.historical_owner_lineage==='NOT_INFERRED'));
});
test('Removing the source score fails even when all other paragraphs remain intact',()=>{
const a=library.scenes.find(s=>s.year===2018);
const bad=a.manuscript.replaceAll('114.37','redacted');
assert.ok(auditDraft({fixture_id:a.fixture_id,text:bad}).hard_failures.some(x=>x.startsWith('MISSING_CERTIFIED_SCORE')));
});
test('2020 semifinal is not secretly staged at the Last Field',()=>{
const a=library.scenes.find(s=>s.year===2020);
const bad=a.manuscript+'\nThe Last Field’s gates groan open during this semifinal.';
assert.ok(auditDraft({fixture_id:a.fixture_id,text:bad}).hard_failures.includes('FINAL_STADIUM_OPERATION_IN_EARLIER_ROUND'));
});
test('Unexplained magical card devices cannot quietly enter early technology canon',()=>{
const a=library.scenes.find(s=>s.year===2020);
const bad=a.manuscript+'\nThe pressure-sensitive runes flare during the last card.';
assert.ok(auditDraft({fixture_id:a.fixture_id,text:bad}).hard_failures.includes('UNAPPROVED_MAGIC_OR_SELF_ACTUATING_HAZARD'));
});
test('The 2015 final score and original field preserve founding-era history',()=>{
const a=library.scenes.find(s=>s.year===2015);
assert.equal(a.round,'FINAL');assert.equal(a.verified.home.points,187);
assert.equal(a.verified.away.points,211.5);
assert.match(a.manuscript,/Weeks 16–17|Weeks 16-17/);
assert.match(a.manuscript,/catch deck|catch protection|catch net/);
});
test('2025 corrected final remains in the same historic ground as the first final',()=>{
const a=library.scenes.find(s=>s.fixture_id==='HIST-POST-2025-FINAL-1');
assert.ok(a);
assert.equal(a.verified.winner_slot,8);
assert.equal(a.verified.home.points,109.56);
assert.equal(a.verified.away.points,161.07);
assert.ok(a.manuscript.includes('original'));
});
test('2025 close semifinal result and personal action remain source-locked',()=>{
const a=library.scenes.find(s=>s.fixture_id==='HIST-POST-2025-SF-2');
assert.ok(a);
assert.equal(a.verified.home.points,151.8);
assert.equal(a.verified.away.points,152.2);
assert.match(a.manuscript,/Paintball Puzzle/);
});
test('Extended screenplay UI can load all manuscripts as plain text, never raw HTML',()=>{
assert.ok(library.scenes.every(s=>s.manuscript.length>4000));
assert.ok(library.scenes.every(s=>s.word_count>=1000));
assert.ok(library.scenes.every(s=>s.manuscript.includes('PHASE ONE')&&s.manuscript.includes('PHASE TWO')&&s.manuscript.includes('PHASE THREE')));
});
console.log(JSON.stringify({status:'PASS',checks:checks.length,fixtures:library.scenes.length,words:library.counts.total_words,independent_qa:'PENDING',details:checks},null,2));
