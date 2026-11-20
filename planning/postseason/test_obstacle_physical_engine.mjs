#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {VENUES,RISK_CONTROLS,evaluatePhysicalFit,candidateCompatibility} from './arena_physical_affordances.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=name=>JSON.parse(fs.readFileSync(path.join(root,name),'utf8'));
const lex=read('OBSTACLE_LEXICON_120_V1.json');
const hist=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const options=read('HISTORICAL_CHALLENGE_OPTION_BINDINGS_56_V1.json');
const material=read('ISLAND_MATERIAL_MEMORY_2015_2025_V1.json');
const checks=[];
function t(name,fn){fn();checks.push(name);}
const ids=new Map(lex.obstacles.map(x=>[x.id,x]));
t('Twelve curated families and 120 unique physical challenge designs',()=>{
assert.equal(lex.families.length,12);assert.equal(lex.obstacles.length,120);
assert.equal(new Set(lex.obstacles.map(x=>x.name)).size,120);
assert.equal(new Set(lex.obstacles.map(x=>x.id)).size,120);
assert.ok(lex.obstacles.every(x=>x.three_phase.length===3 && x.three_phase.every((p,i)=>p.n===i+1)));
});
t('All physical hazards have specifically named safety and spectator controls',()=>{
assert.ok(lex.obstacles.every(x=>Array.isArray(RISK_CONTROLS[x.risk_class]) && RISK_CONTROLS[x.risk_class].length>=3));
assert.ok(lex.obstacles.every(x=>x.canon_status==='CREATIVE_CANDIDATE_NOT_HISTORICAL_ESPN'));
});
t('All six fixed event-round arena envelopes are unique and complete',()=>{
assert.equal(Object.keys(VENUES).length,6);
assert.equal(Object.values(VENUES).filter(x=>x.round==='QF').length,3);
assert.equal(Object.values(VENUES).filter(x=>x.round==='SF').length,2);
assert.equal(Object.values(VENUES).filter(x=>x.round==='FINAL').length,1);
});
t('2026 compositional space is large but not fake individually authored scenarios',()=>{
const tally=candidateCompatibility(lex,2026);
assert.equal(tally.total_valid_site_scenario_pairs,642);
assert.ok(Object.values(tally.eligible_scenarios_by_site).every(x=>x>50));
const historyComb=Array.from({length:11},(_,i)=>candidateCompatibility(lex,2015+i).total_valid_site_scenario_pairs).reduce((a,b)=>a+b,0);
assert.ok(historyComb>3000);
});
t('All 56 frozen sports pairings have distinct physically possible story options',()=>{
assert.equal(options.proposals.length,56);
assert.equal(new Set(options.proposals.map(x=>x.picked_obstacle_id)).size,56);
assert.deepEqual(new Set(options.proposals.map(x=>x.fixture_id)),new Set(hist.fixtures.map(x=>x.id)));
for(const f of options.proposals){
const o=ids.get(f.picked_obstacle_id);
assert.ok(o);
const fit=evaluatePhysicalFit({obstacle:o,venue_id:f.venue_candidate_id,year:f.year,round:f.round});
assert.ok(fit.eligible,JSON.stringify(fit.reasons));
assert.equal(f.three_stages.length,3);
const original=hist.fixtures.find(x=>x.id===f.fixture_id);
assert.equal(f.historical_source.winner_slot,original.winner_slot);
}
});
t('Historical high tech cannot be present in founding 2015 scene',()=>{
const bike=lex.obstacles.find(x=>x.name==='Dirt Bike Clifftop');
assert.ok(evaluatePhysicalFit({obstacle:bike,venue_id:'CAND-POST-SALTWIND',round:'QF',year:2026}).eligible);
assert.ok(evaluatePhysicalFit({obstacle:bike,venue_id:'CAND-POST-SALTWIND',round:'QF',year:2015}).reasons.includes('TECH_NOT_AVAILABLE_IN_HISTORICAL_ERA'));
});
t('Stadium class is not overridden by challenge spectacle',()=>{
const sumo=lex.obstacles.find(x=>x.name==='Stone Circle Sumo');
assert.ok(evaluatePhysicalFit({obstacle:sumo,venue_id:'CAND-POST-CROWN-STAIR',round:'QF',year:2026}).reasons.includes('WRONG_ROUND_FOR_PERMANENT_ARENA'));
});
t('Incompatible waterborne hardware cannot be invented at Crown Stair',()=>{
const canoe=lex.obstacles.find(x=>x.name==='Canoe Slalom');
assert.ok(evaluatePhysicalFit({obstacle:canoe,venue_id:'CAND-POST-CROWN-STAIR',round:'SF',year:2026}).reasons.includes('MISSING_CAPABILITY:water_basin'));
});
t('Wind, storm-surge, and old-growth fire closures fail closed',()=>{
const a=lex.obstacles.find(x=>x.name==='Stone Circle Sumo');
assert.ok(evaluatePhysicalFit({obstacle:a,venue_id:'CAND-POST-SALTWIND',round:'QF',year:2026,conditions:{weather:'STORM'}}).reasons.includes('CLOSED_SEVERE_CLIFF_WEATHER'));
assert.ok(evaluatePhysicalFit({obstacle:a,venue_id:'CAND-POST-BREAKWATER',round:'QF',year:2026,conditions:{tide:'STORM_SURGE'}}).reasons.includes('CLOSED_UNSAFE_HARBOR_WATER'));
const paint=lex.obstacles.find(x=>x.name==='Paintball Citadel');
assert.ok(evaluatePhysicalFit({obstacle:paint,venue_id:'CAND-POST-GROVE',round:'SF',year:2026,conditions:{fire_hazard:'HIGH'}}).reasons.includes('CLOSED_GROVE_FIRE_RISK'));
});
t('Historical arena maintenance does not auto-promote blast scars or structural damage',()=>{
assert.equal(material.years.length,11);
assert.equal(material.perimeter_ruins.length,9);
assert.ok(material.perimeter_ruins.every(x=>x.state&&x.narrative));
assert.ok(material.years.every(y=>y.legacy_sites.find(s=>s.id==='CAND-POST-LAST-FIELD')?.permanent_explosion_damage_allowed===false));
assert.ok(material.years.every(y=>y.legacy_sites.every(site=>site.candidate_scene_scars.every(c=>c.persistence==='NOT_CANON_WRITEBACK'))));
});
t('Year-state archive covers every fixture once with correct era-specific QF grounds',()=>{
const fixtures=material.years.flatMap(y=>y.legacy_sites.flatMap(site=>site.matched_fixtures));
assert.equal(fixtures.length,56);
assert.equal(new Set(fixtures).size,56);
assert.equal(material.years.find(x=>x.year===2015).legacy_sites.filter(s=>s.round==='QUARTERFINAL_ONLY'&&s.matched_fixtures.length).length,0);
assert.equal(material.years.find(x=>x.year===2017).legacy_sites.filter(s=>s.round==='QUARTERFINAL_ONLY'&&s.matched_fixtures.length).length,2);
assert.equal(material.years.find(x=>x.year===2021).legacy_sites.filter(s=>s.round==='QUARTERFINAL_ONLY'&&s.matched_fixtures.length).length,3);
});
console.log(JSON.stringify({status:'PASS',checks:checks.length,scenario_seeds:120,round_site_options_2026:642,proposed_hist:56,ruins:9,assertions:checks},null,2));
