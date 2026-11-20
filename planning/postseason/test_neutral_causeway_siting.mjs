#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),world=path.resolve(root,'../../world/data');
const read=(base,n)=>JSON.parse(fs.readFileSync(path.join(base,n),'utf8'));
const a=read(root,'ATLAS_NEUTRAL_CAUSEWAY_SITING_HYPOTHESIS_V1.proposal.json');
const c=read(world,'atlas_location_candidates.json');
const places=read(world,'locations.json'),routes=read(world,'routes.json'),regions=read(world,'physical_zones.json');
const checks=[];
function t(name,fn){fn();checks.push(name)}
const inner=regions.regions.find(x=>x.id==='REG-INNER-SEA-LITTORAL');
function inRegion(p){const [x,y]=p,[minX,minY,maxX,maxY]=inner.abstract_bounds;return x>=minX&&x<=maxX&&y>=minY&&y<=maxY}
t('Proposed neutral gate is not assigned to any active owner character or division',()=>{
 assert.equal(a.hypothesis.public_mainland_gate.owner_character_id,null);
 assert.equal(a.hypothesis.public_mainland_gate.division_id,null);
 assert.equal(a.hypothesis.island_centre.private_owner_id,null);
 assert.ok(!a.hypothesis.planned_links.some(x=>x.from==='LOC-LLC-STORM-CITY'||x.to==='LOC-LLC-STORM-CITY'));
});
t('Existing actual island region admits hypothetical points without claiming coastline',()=>{
 assert.equal(inner.id,'REG-INNER-SEA-LITTORAL');
 assert.ok(inner.environment.terrain.includes('islands'));
 const positions=[a.hypothesis.public_mainland_gate.abstract_position,...a.hypothesis.causeway_crossing.abstract_path,
 a.hypothesis.island_centre.abstract_position,...Object.values(a.hypothesis.landmark_sites)];
 assert.ok(positions.every(inRegion));
 assert.equal(a.hypothesis.candidate_outer_envelope.water_or_coastline_surveyed,false);
 assert.equal(a.hypothesis.causeway_crossing.actual_length_m,null);
 assert.equal(a.proof.metric_geography,false);
});
t('No existing active location is replaced by a staged candidate',()=>{
 assert.equal(places.locations.length,a.proof.present_day_active_location_count);
 assert.equal(routes.routes.length,a.proof.present_day_active_route_count);
 assert.ok(places.locations.every(x=>!x.id.startsWith('CAND-POST-')));
 assert.ok(routes.routes.every(x=>!x.id.startsWith('CAND-ROUTE-')));
 assert.deepEqual(a.world_writes,[]);
 assert.deepEqual(a.live_site_updates,[]);
});
t('The earlier central-basin Last Field source remains unchanged and explicitly cited',()=>{
 const old=c.candidates.find(x=>x.id==='CAND-CHAMP-LAST-FIELD');
 assert.ok(old);
 assert.deepEqual(old.likely_physical_zone_ids,['REG-CENTRAL-BASIN']);
 assert.equal(a.proof.historic_last_field_zone,'REG-CENTRAL-BASIN');
 assert.equal(a.canon_promotion,false);
});
t('All eleven planned arena and operations anchors are spatially separated',()=>{
 const x=Object.values(a.hypothesis.landmark_sites);
 assert.equal(x.length,11);
 assert.equal(new Set(x.map(p=>p.join(','))).size,11);
});
t('Siting remains a governance proposal with eight exact unresolved checks',()=>{
 assert.equal(a.approval_checks.length,8);
 assert.match(a.status,/UNPROMOTED/);
 assert.equal(a.hypothesis.causeway_crossing.engineering,'STORM_SURGE_AND_FOUNDATION_SURVEY_REQUIRED');
 assert.ok(a.approval_checks.some(x=>x.includes('World/Tech')));
});
console.log(JSON.stringify({status:'PASS',checks:checks.length,proposed_anchors:11,world_location_writes:0,world_route_writes:0,safety_survey:'PENDING',details:checks},null,2));
