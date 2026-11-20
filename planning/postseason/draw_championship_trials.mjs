#!/usr/bin/env node
/**
 * Founder Interview II: ceremonial candidate-only challenge draw.
 * Deterministic SHA256, source-independent of scores and outcomes.
 * This recreates a FICTIONAL historical ritual, not actual prior draw records.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {evaluatePhysicalFit} from './arena_physical_affordances.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
export const CEREMONY={
  schema:'schemin.championship_draw_rules.v1',
  status:'FOUNDER_AUTHORIZED_FICTIONAL_RITUAL__NOT_VERIFIED_HISTORICAL_CEREMONY',
  founder_key:'F12',
  draw_type:'PUBLIC_PRECOMMITTED_SHA256_MODULO_ELIGIBLE_LIST',
  domain:'SCHEMIN-26|POSTSEASON-CHAMPIONSHIP-ISLAND|DRAW|V1',
  disclosed_salt:'FOUNDER-II-ISLAND-2015-2025-HISTORICAL-FICTIONAL-RECONSTRUCTION',
  important:'No seed, eligible pool or winner may be chosen after observing a preferred result. Published narrative must distinguish constructed historical draw from sourced ESPN bracket.',
  source_exclusion:['home_points','away_points','winner_slot','winning team','historical point differential','human owner'],
  published_fields:['year','fixture_id','round','venue_candidate_id','pool_ids_sorted','pool_hash_sha256','draw_ticket_sha256','selected_index','selected_obstacle_id','verification_status'],
  eligibility_law:'Stable lexicon ID order, physical venue and round, minimum technology year, no severe-event conditions. One per fixture, all three stages directly executed by principal.',
  avoid_repeating_seed:'Consecutive allocated historical matches within the same season and round should prefer unique selections via a predeclared no-repeat ordering; if no options remain the draw may reuse.',
  winner_policy:'The draw chooses WHAT is attempted, never WHO wins. Official ESPN source remains independently immutable.',
  future_2026_policy:'DO NOT DRAW A NAMED 2026 MATCHUP UNTIL OFFICIAL PAIRING IS LOCKED; a source-specific future-season seed can be published before outcome, but not in advance of opponents.'
};
const hex=x=>crypto.createHash('sha256').update(x,'utf8').digest('hex');
export function drawOne({fixture,obstacles,historySalt=CEREMONY.disclosed_salt,excludedIds=[]}){
  if(!fixture||typeof fixture.id!=='string'||!fixture.id)throw Error('Fixture ID missing');
  if(!Number.isInteger(fixture.year)||!['QF','SF','FINAL'].includes(fixture.round))throw Error('Invalid dated round');
  if(!fixture.staging?.venue_id)throw Error('No permanent arena');
  if(!Array.isArray(obstacles))throw Error('Missing obstacle library');
  // Deliberately ignore source score, source winner and owner details.
  const eligible=obstacles.filter(o=>evaluatePhysicalFit({obstacle:o,venue_id:fixture.staging.venue_id,round:fixture.round,year:fixture.year}).eligible)
    .map(o=>o.id).sort();
  const available=eligible.filter(id=>!excludedIds.includes(id));
  const pool=available.length?available:eligible;
  if(pool.length===0)throw Error('No compatible challenge for '+fixture.id);
  const poolHash=hex(pool.join('\n'));
  const ticket=hex([CEREMONY.domain,historySalt,fixture.year,fixture.id,fixture.round,fixture.staging.venue_id,poolHash].join('|'));
  const index=Number(BigInt('0x'+ticket)%BigInt(pool.length));
  return {
    fixture_id:fixture.id,year:fixture.year,round:fixture.round,venue_candidate_id:fixture.staging.venue_id,
    eligible_count:eligible.length,selection_pool_count:pool.length,
    pool_ids_sorted:pool,pool_hash_sha256:poolHash,
    draw_ticket_sha256:ticket,selected_index:index,
    selected_obstacle_id:pool[index],source_class:'INVENTED_CEREMONIAL_DRAW',
    source_exclusion_verified:true,ceremonial_status:'PROPOSED_HISTORICAL_FICTION_NOT_ARCHIVE_FACT',
    round_owner_performance:'SINGLE_PRINCIPAL_THREE_PHASES',
    original_sporting_result_unmodified:true
  };
}
/**
 * 2026 draw is permitted only after official ESPN seed/pairing lock, and
 * without a pre-known result. This does not fill future slots autonomously.
 */
export function draw2026VerifiedPairing({fixture,sourceLock,obstacles}){
 if(!sourceLock || sourceLock.qualification_locked!==true
    || sourceLock.source!=='ESPN'
    || !sourceLock.snapshot_id || String(sourceLock.league_id)!=='1417621'
    || sourceLock.season!==2026)throw Error('SOURCE_LOCK_REQUIRED_BEFORE_2026_CEREMONY');
 if(!fixture || fixture.year!==2026 || fixture.source!=='ESPN'
    || !fixture.fixture_id || fixture.id!==fixture.fixture_id
    || fixture.provenance_snapshot!==sourceLock.snapshot_id
    || !fixture.home_id || !fixture.away_id || fixture.home_id===fixture.away_id)
    throw Error('VERIFIED_2026_PAIRING_REQUIRED');
 if(fixture.winner_id||fixture.home_points!==undefined||fixture.away_points!==undefined)
    throw Error('DO_NOT_FEED_RESULT_TO_PRECONTEST_DRAW');
 const result=drawOne({fixture,obstacles,
   historySalt:'PUBLIC_2026_OFFICIAL_BRACKET_LOCK_'+sourceLock.snapshot_id});
 return {...result,release:'PRECONTEST_DRAW_ONLY_NO_CANON_PROMOTION',
    participants_verified_from_source:true,result_still_pending:true};
}
export function drawHistorical(history,lexicon){
  assert.equal(history?.fixtures?.length,56);
  assert.equal(lexicon?.obstacles?.length,120);
  const used=new Map();
  const results=[];
  for(const f of history.fixtures){
    const key=f.year+'-'+f.round;
    const ticket=drawOne({fixture:f,obstacles:lexicon.obstacles,excludedIds:used.get(key)||[]});
    used.set(key,[...(used.get(key)||[]),ticket.selected_obstacle_id]);
    const obstacle=lexicon.obstacles.find(x=>x.id===ticket.selected_obstacle_id);
    results.push({...ticket,obstacle_name:obstacle.name,obstacle_family:obstacle.family,
      required_capabilities:obstacle.needs,stage_contract:obstacle.three_phase,
      memo_visual_status:'PREPRODUCTION_NOT_RENDERED',owner_identity:'HISTORICAL_SLOT_NOT_VERIFIED_HUMAN'});
  }
  if(results.length!==56)throw Error('Historical count');
  return {
    schema:'schemin.island_historical_draw_manifest.v1',
    status:'AUTHORIAL_RETROSPECTIVE_CEREMONY_NOT_FACTUAL_HISTORIC_DRAW',
    source:'HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json',
    obstacle_source:'OBSTACLE_LEXICON_120_V1.json',
    draw_constitution:CEREMONY,
    count:results.length,
    winner_ids_in_draw_data:0,
    ceremonies:results
  };
}
if(process.argv[1] && fs.realpathSync(process.argv[1])===fs.realpathSync(fileURLToPath(import.meta.url))){
  const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
  const lex=read('OBSTACLE_LEXICON_120_V1.json');
  const out=drawHistorical(history,lex);
  const text=JSON.stringify(out,null,2)+'\n';
  const target=path.join(dir,'HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
  if(process.argv.includes('--check'))assert.equal(fs.readFileSync(target,'utf8'),text,'Stored draw is not reproducible');
  else fs.writeFileSync(target,text,'utf8');
  console.log(JSON.stringify({status:'PASS',mode:process.argv.includes('--check')?'CHECK':'BUILD',ceremonies:out.count,unique_selections:new Set(out.ceremonies.map(x=>x.selected_obstacle_id)).size,
    scores_used:false,world_mutation:false}));
}
