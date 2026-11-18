#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {compile,validate,DEFAULT_HISTORY,DEFAULT_SITES} from './build_postseason_inklings_packets.mjs';

const h=JSON.parse(fs.readFileSync(DEFAULT_HISTORY,'utf8'));
const s=JSON.parse(fs.readFileSync(DEFAULT_SITES,'utf8'));
const copy=x=>JSON.parse(JSON.stringify(x));
const tests=[];
function t(name,fn){fn();tests.push(name);}
function fail(name,edit){const a=copy(h),b=copy(s);edit(a,b);assert.throws(()=>validate(a,b),Error);tests.push(name);}

t('baseline 56 fixtures + 11 seasons',()=>{
assert.equal(validate(h,s),true);
const p=compile(h,s,'test-hash');
assert.equal(p.cards.length,56);
assert.equal(p.annual.length,11);
assert.equal(p.headline.challenge_stages,168);
assert.equal(p.headline.modern2026_winners_generated,0);
assert.equal(p.annual.reduce((n,y)=>n+y.contender_berths,0),67);
});
t('every fixture has three consecutive stages and official winner',()=>{
for(const card of compile(h,s).cards){
 assert.equal(card.beat_sequence.length,3);
 assert.deepEqual(card.beat_sequence.map(x=>x.n),[1,2,3]);
 const home=card.verified.home,away=card.verified.away;
 assert.equal(card.verified.winner_slot,home.points>away.points?home.team_slot:away.team_slot);
 assert.equal(card.production.location_release,'HOLD_NOT_ACTIVE_LOC');
}
});
t('fixed round arenas / founding rounds / era years',()=>{
const p=compile(h,s);
assert.deepEqual(p.annual.map(x=>x.season),Array.from({length:11},(_,i)=>i+2015));
assert.deepEqual(p.annual.filter(x=>x.season<=2016).map(x=>x.season_rounds.quarterfinals),[0,0]);
assert.equal(p.cards.filter(x=>x.round==='FINAL' && x.venue.name==='Last Field').length,11);
assert.equal(p.cards.filter(x=>x.round==='QF').length,23);
assert.equal(p.cards.filter(x=>x.round==='SF').length,22);
});
fail('reject score tampering',a=>{a.fixtures[0].winner_slot=999});
fail('reject premature canon promotion',a=>{a.fixtures[0].staging.status='CANON'});
fail('reject round arena crossover',a=>{a.fixtures.find(f=>f.round==='SF').staging.venue_id='CAND-POST-IRON-QUARRY'});
fail('reject duplicate fixture',a=>{a.fixtures[1].id=a.fixtures[0].id});
fail('reject wrong stage count',a=>{a.fixtures[0].staging.stages.pop()});
fail('reject extra unverified winner',a=>{a.annual[0].champion_slot=77});
fail('reject bye-manipulation',a=>{a.annual.find(x=>x.year===2025).bye_slots=[2]});
fail('reject simultaneous venue reuse',a=>{const k=a.fixtures.filter(x=>x.year===2025&&x.round==='QF');k[1].staging.venue_id=k[0].staging.venue_id;k[1].staging.venue_name=k[0].staging.venue_name;});
console.log(JSON.stringify({status:'PASS',count:tests.length,tests},null,2));
