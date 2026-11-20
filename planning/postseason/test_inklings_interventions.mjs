#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {compile,validateInterventions} from './build_postseason_inklings_packets.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=name=>JSON.parse(fs.readFileSync(path.join(root,name),'utf8'));
const cp=x=>JSON.parse(JSON.stringify(x));
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const sites=read('ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json');
const registry=read('INKLINGS_56_SIGNATURE_ENCOUNTER_INTERVENTIONS_V1.json');
const compiled=read('INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json');
const lastField=read('INKLINGS_ELEVEN_CHAMPIONSHIP_FINALE_SCRIPTS_V1.proposal.json');
const tests=[];
function test(name,fn){fn();tests.push(name);}
function reject(name,fn){const x=cp(registry);fn(x);assert.throws(()=>validateInterventions(x,history),Error);tests.push(name);}
test('Every historic fixture has a distinct and nonempty original Inklings intervention',()=>{
 assert.equal(validateInterventions(registry,history),true);
 assert.equal(registry.items.length,56);
 assert.equal(new Set(registry.items.map(x=>x.fixture_id)).size,56);
 assert.equal(new Set(registry.items.map(x=>x.signature_action)).size,56);
});
test('Compiled fixture scenes carry unique physical stage plus audience response',()=>{
 const byId=new Map(registry.items.map(x=>[x.fixture_id,x]));
 assert.equal(compiled.cards.length,56);
 for(const c of compiled.cards) {
   const src=byId.get(c.verified_fixture_id);assert.ok(src);
   assert.equal(c.beat_sequence[1].action,src.signature_action);
   assert.equal(c.storyroom.spectator_cutaway,src.spectator_cutaway);
   assert.equal(c.storyroom.heritage_consequence,src.legacy_note);
   assert.equal(c.beat_sequence[1].source_class,'FICTION_ORIGINAL_INKLINGS_INTERVENTION');
   assert.equal(c.creative_status,'NONCANON_WORKSHOP_OUTPUT');
 }
});
test('Eleven separate authored championship finales preserve exact winners',()=>{
 assert.equal(lastField.scenes.length,11);
 const finalMap=new Map(history.fixtures.filter(f=>f.round==='FINAL').map(f=>[f.year,f]));
 for(const s of lastField.scenes) {
   const f=finalMap.get(s.year);assert.ok(f);
   assert.equal(s.verified.fixture_id,f.id);
   assert.equal(s.verified.winner_slot,f.winner_slot);
   assert.equal(s.verified.home.points,f.home.points);
   assert.equal(s.verified.away.points,f.away.points);
   assert.equal(s.venue_id,'CAND-POST-LAST-FIELD');
   assert.equal(s.prose.length,3);
 }
});
reject('Reject missing scene treatment',x=>x.items.pop());
reject('Reject duplicate fixture treatment',x=>x.items[1].fixture_id=x.items[0].fixture_id);
reject('Reject unanchored historical fixture ID',x=>x.items[0].fixture_id='FUTURE-WINNER');
reject('Reject duplicated physical signature actions',x=>x.items[1].signature_action=x.items[0].signature_action);
reject('Reject blank audience cutaway',x=>x.items[0].spectator_cutaway='');
reject('Reject missing heritage consequence',x=>{delete x.items[0].legacy_note;});
reject('Reject source registry masquerading as canon',x=>x.schema='approved-canon');
console.log(JSON.stringify({status:'PASS',tests:tests.length,interventions:56,scripted_championships:11,stage_count:168,results:tests},null,2));
