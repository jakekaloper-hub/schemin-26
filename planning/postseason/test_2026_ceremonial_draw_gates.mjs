#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {draw2026VerifiedPairing} from './draw_championship_trials.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const obstacles=JSON.parse(fs.readFileSync(path.join(root,'OBSTACLE_LEXICON_120_V1.json'),'utf8')).obstacles;
const baseLock={season:2026,league_id:'1417621',source:'ESPN',snapshot_id:'SYNTHETIC_TEST_LOCK_DO_NOT_PUBLISH',qualification_locked:true};
const baseFixture={id:'SYNTHETIC_QF_EXAMPLE',fixture_id:'SYNTHETIC_QF_EXAMPLE',year:2026,
 source:'ESPN',provenance_snapshot:baseLock.snapshot_id,
 home_id:'SYNTHETIC_T2',away_id:'SYNTHETIC_T7',round:'QF',staging:{venue_id:'CAND-POST-IRON-QUARRY'}};
const cp=v=>JSON.parse(JSON.stringify(v));
const tests=[];
function t(n,cb){cb();tests.push(n)}
function bad(n,change){const l=cp(baseLock),f=cp(baseFixture);change(f,l);assert.throws(()=>draw2026VerifiedPairing({fixture:f,sourceLock:l,obstacles}),Error);tests.push(n);}
t('Official bracket lock enables source-labeled result-free ceremonial draw',()=>{
 const result=draw2026VerifiedPairing({fixture:baseFixture,sourceLock:baseLock,obstacles});
 assert.ok(result.eligible_count>0);
 assert.ok(result.result_still_pending);
 assert.equal(result.release,'PRECONTEST_DRAW_ONLY_NO_CANON_PROMOTION');
 assert.equal(result.participants_verified_from_source,true);
});
t('Precommitted fixture/lock reproduces exactly and never carries result',()=>{
 const a=draw2026VerifiedPairing({fixture:baseFixture,sourceLock:baseLock,obstacles});
 const b=draw2026VerifiedPairing({fixture:baseFixture,sourceLock:baseLock,obstacles});
 assert.deepEqual(a,b);assert.ok(!('winner_id' in a));
});
bad('No 2026 draw before qualification lock',(f,l)=>{l.qualification_locked=false;});
bad('No 2026 draw without official source',(f,l)=>{l.source='TEST';});
bad('No 2026 draw against incorrect league',(f,l)=>{l.league_id='1417622';});
bad('No unrecognized pairing provenance',(f,l)=>{f.provenance_snapshot='WRONG_HASH';});
bad('No future team name placeholder identity',(f,l)=>{f.away_id='';});
bad('No self matchup',(f,l)=>{f.away_id=f.home_id;});
bad('No fictitious opponent score before draw',(f,l)=>{f.away_points=144;});
bad('No premature winner supplied',(f,l)=>{f.winner_id='SYNTHETIC_T2';});
bad('No incompatible nonexistent challenge venue',(f,l)=>{f.staging.venue_id='CAND-POST-UNKNOWN';});
console.log(JSON.stringify({status:'PASS',cases:tests.length,source:'SYNTHETIC_ONLY_NEVER_PUBLIC',2026_real_draws_created:0,tests},null,2));
