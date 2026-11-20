#!/usr/bin/env node
/** Historical-source integrity and Founder-V2 production acceptance test. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const load=name=>JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
const v1=load('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.proposal.json');
const v2=load('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const sites=load('ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json');
const cards=load('INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json');
const contract=load('POSTSEASON_2026_ISLAND_EVENT_CONTRACT.proposal.json');
const tests=[];
function check(n,f){f();tests.push(n);}
check('all 56 verified historical fixture facts exactly preserved',()=>{
  assert.equal(v1.fixtures.length,56);
  assert.equal(v2.fixtures.length,56);
  const byId=new Map(v2.fixtures.map(f=>[f.id,f]));
  for(const old of v1.fixtures){
    const cur=byId.get(old.id);assert.ok(cur,old.id);
    for(const k of ['year','round','scoring_period','winner_slot'])assert.deepEqual(cur[k],old[k],old.id+':'+k);
    assert.deepEqual(cur.home,old.home,old.id+':home');
    assert.deepEqual(cur.away,old.away,old.id+':away');
  }
});
check('annual entrants, bye and champion identities preserved',()=>{
  for(const old of v1.annual){
    const cur=v2.annual.find(y=>y.year===old.year);assert.ok(cur);
    for(const k of ['entrants','bye_slots','round_counts','champion_slot'])assert.deepEqual(cur[k],old[k],old.year+':'+k);
  }
});
check('fixed playoff round classification throughout eleven years',()=>{
  const type={QF:'QUARTERFINAL_ONLY',SF:'SEMIFINAL_ONLY',FINAL:'FINAL_ONLY'};
  const loc=new Map(sites.sites.map(x=>[x.id,x]));
  for(const f of v2.fixtures){
    const site=loc.get(f.staging.venue_id);assert.ok(site);
    assert.equal(site.round_assignment,type[f.round],f.id);
    assert.equal(site.name,f.staging.venue_name);
  }
});
check('all 168 production stage beats are present and noncanon',()=>{
  assert.equal(cards.cards.length,56);
  assert.equal(cards.annual.length,11);
  assert.equal(cards.headline.challenge_stages,168);
  for(const c of cards.cards){
    assert.equal(c.beat_sequence.length,3);
    assert.equal(c.creative_status,'NONCANON_WORKSHOP_OUTPUT');
    assert.equal(c.production.location_release,'HOLD_NOT_ACTIVE_LOC');
    assert.equal(c.production.independent_umpire,'PENDING');
    const actual=v2.fixtures.find(f=>f.id===c.verified_fixture_id);assert.ok(actual);
    assert.equal(c.verified.winner_slot,actual.winner_slot);
  }
});
check('2026 event contract has only six future fixtures and locked unknown winners',()=>{
  assert.equal(contract.schedule.qualification_count,7);
  assert.equal(contract.schedule.reseed,false);
  assert.deepEqual(contract.venue_assignment.rounds.QUARTERFINAL,['CAND-POST-IRON-QUARRY','CAND-POST-SALTWIND','CAND-POST-BREAKWATER']);
  assert.deepEqual(contract.venue_assignment.rounds.SEMIFINAL,['CAND-POST-CROWN-STAIR','CAND-POST-GROVE']);
  assert.deepEqual(contract.venue_assignment.rounds.CHAMPIONSHIP,['CAND-POST-LAST-FIELD']);
  assert.equal(contract.schedule.verified_individual_round_outcomes,false);
  assert.equal(contract.schedule.rounds.reduce((n,x)=>n+x.fixture_count,0),6);
});
check('island remains unpromoted and memorial chronology guarded',()=>{
  assert.equal(sites.status,'FOUNDER_APPROVED_CREATIVE_DIRECTION_ATLAS_PROMOTION_PENDING');
  assert.equal(sites.geography.precise_location,null);
  assert.equal(sites.geography.route_id,null);
  assert.equal(sites.media_law.needs_canon_amendment,true);
  assert.ok(contract.holds.some(x=>x.toLowerCase().includes('memorial')));
  assert.ok(contract.holds.some(x=>x.toLowerCase().includes('causeway')));
});
console.log(JSON.stringify({result:'PASS',tests:tests.length,fixtures:v2.fixtures.length,stages:cards.headline.challenge_stages,yearCount:v2.annual.length,checks:tests},null,2));
