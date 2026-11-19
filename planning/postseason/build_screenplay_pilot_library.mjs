#!/usr/bin/env node
/**
 * Source-bound registry of six substantive historical screenplays.
 * PASS_MACHINE_ONLY is not canon approval; the scripts remain editorial drafts.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const dir=path.dirname(fileURLToPath(import.meta.url));
const {auditDraft}=require('./scene_quality_gate.cjs');
const source=JSON.parse(fs.readFileSync(path.join(dir,'HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json'),'utf8'));
const historical=new Map(source.fixtures.map(x=>[x.id,x]));
const files=[
['HIST-POST-2015-FINAL-1','INKLINGS_2015_FIRST_STONE_LAST_FIELD_SCREENPLAY_V1.md'],
['HIST-POST-2018-QF-1','INKLINGS_2018_IRON_QUARRY_SCREENPLAY_PILOT_V2.md'],
['HIST-POST-2020-SF-1','INKLINGS_2020_LAST_HAND_CROWN_STAIR_SCREENPLAY_V1.md'],
['HIST-POST-2022-SF-1','INKLINGS_2022_CROWN_STAIR_SCREENPLAY_PILOT_V2.md'],
['HIST-POST-2025-SF-2','INKLINGS_2025_FOUR_TENTHS_GROVE_SCREENPLAY_V1.md'],
['HIST-POST-2025-FINAL-1','INKLINGS_2025_LAST_FIELD_SCREENPLAY_PILOT_V2.md']
];
const seen=new Set();
const articles=files.map(([fixture_id,filename])=>{
 assert.ok(!seen.has(fixture_id));seen.add(fixture_id);
 const f=historical.get(fixture_id);assert.ok(f,fixture_id);
 const text=fs.readFileSync(path.join(dir,filename),'utf8');
 const audit=auditDraft({fixture_id,text,model:'EDITORIAL_LONGFORM_DRAFT'});
 if(audit.hard_failures.length)throw Error('Historical screenplay quality failure: '+fixture_id+' '+audit.hard_failures.join(','));
 if(audit.word_count<1000)throw Error('Screenplay too short for independent review '+fixture_id);
 return {
  fixture_id,year:f.year,round:f.round,filename,
  public_title:text.split(/\n/).find(x=>x.startsWith('# '))?.replace(/^#\s*/,'')||'Historical island screenplay',
  verified:{home:f.home,away:f.away,winner_slot:f.winner_slot,provider:'ESPN_FLAIM_HISTORICAL'},
  manuscript:text,word_count:audit.word_count,
  qa:{machine_status:audit.machine_gate,hard_failures:audit.hard_failures,warnings:audit.warnings,
    independent_umpire:'NOT_CERTIFIED',historical_owner_lineage:'NOT_INFERRED'},
  canonical_status:'EDITORIAL_REVIEW_DRAFT_NOT_PUBLISHED_WORLD'
 };
});
assert.equal(articles.length,6);
const output={
schema:'schemin.postseason.inklings_screenplay_pilot_library.v1',
status:'SIX_SOURCE_LOCKED_EDITORIAL_SCREENPLAYS_NO_CANON_PROMOTION',
scenes:articles,
counts:{longform_pilots:6,archive_matchups:source.fixtures.length,total_words:articles.reduce((x,a)=>x+a.word_count,0)},
source_integrity:'Original ESPN fantasy records only determine verified competitors and scores; fictional challenge action not a true historical event.',
publication:'HOLD_INDEPENDENT_UMPIRE_ATLAS_CHARACTER_CANON_WORLD_TECH'
};
const target=path.join(dir,'INKLINGS_SIX_SCREENPLAY_PILOT_LIBRARY_V1.json');
const serial=JSON.stringify(output,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(target,'utf8'),serial,'Published draft library out of sync');
else fs.writeFileSync(target,serial);
console.log(JSON.stringify({status:'PASS',...output.counts,mode:process.argv.includes('--check')?'CHECK':'BUILD',qa:'PASS_MACHINE_ONLY',independent_review:'PENDING'}));
