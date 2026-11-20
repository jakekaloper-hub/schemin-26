#!/usr/bin/env node
/**
 * Do not mutate active Atlas! Create a tracked candidate supersession packet
 * by comparing Founder island direction with current authoritative world data.
 */
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const world=path.resolve(root,'../..','world','data');
const w=n=>JSON.parse(fs.readFileSync(path.join(world,n),'utf8'));
const p=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const zones=w('physical_zones.json'), locations=w('locations.json'),route=w('routes.json'),candidates=w('atlas_location_candidates.json');
const topology=p('ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json');
const last=candidates.candidates.find(x=>x.id==='CAND-CHAMP-LAST-FIELD');
const inner=zones.regions.find(x=>x.id==='REG-INNER-SEA-LITTORAL');
assert.ok(last&&inner);
assert.deepEqual(last.likely_physical_zone_ids,['REG-CENTRAL-BASIN']);
assert.ok(inner.environment.terrain.includes('islands'));
assert.ok(inner.environment.terrain.includes('sheltered bays'));
assert.ok(inner.adjacent_region_ids.includes('REG-CENTRAL-BASIN'));
assert.ok(!locations.locations.some(x=>x.id==='LOC-CHAMPIONSHIP-ISLAND'||x.id==='LOC-POST-LAST-FIELD'));
const anchor=locations.locations.find(x=>x.id==='LOC-LLC-STORM-CITY');
assert.ok(anchor&&anchor.physical_zone_id==='REG-INNER-SEA-LITTORAL');
const out={
schema:'schemin.postseason.last_field_atlas_supersession_packet.v1',status:'FOUNDER_CREATIVE_DIRECTION_APPROVED__GEOGRAPHY_PROMOTION_HELD',
current:{candidate_id:last.id,zone_ids:last.likely_physical_zone_ids,status:last.lifecycle_status,technology:last.technology_translation,activation:last.activation_trigger},
proposed:{candidate_id:last.id,zone_ids:['REG-INNER-SEA-LITTORAL'],function:'Same physically fixed Last Field, but within a causeway-connected championship-only offshore precinct since the earliest reconstructed 2015 fiction',new_active_location_id:null,coordinates:null,route_id:null,modern_media:'ISLAND_EXCEPTION_PENDING_WORLD_TECH',event_eligibility:['CHAMPIONSHIP'],public_launch:'BLOCKED_UNTIL_SOURCE_LOCK'},
plausibility:{actual_region:inner.name,terrain:inner.environment.terrain,adjacencies:inner.adjacent_region_ids,related_canon_active_littoral_location:anchor.id,anchor_warning:'LLC Storm City is owner-linked. DO NOT turn that owner domain into private control of the neutral championship causeway.',island_route_links:topology.edges.length,island_nodes:topology.nodes.length,exact_mainland_anchor:'UNRESOLVED_NEUTRAL_PUBLIC_CORRIDOR'},
no_mutation:{live_locations:locations.locations.length,live_routes:route.routes.length,location_writeback:false,route_writeback:false},
required_gates:[
'Choose specific existing neutral mainland route or propose governed publicly neutral new location',
'Resolve island location coordinates/topology in abstract map bounds without treating abstract coordinates as real meters',
'Confirm storm surge, causeway structural loads, utility corridors and emergency access',
'Version and supersede old Central Basin candidate explicitly; do not delete audit provenance',
'Confirm island camera/screen modern-tech exception independently of global world technology',
'Preserve 2026 championship-only reveal restriction and protected Michael Farrell memorial'
],
fact_boundary:'Physical island and 2015–2025 venue use are original secondary-world fiction, not externally verified venue records.'
};
const filename=path.join(root,'ATLAS_LAST_FIELD_SUPERSESSION_PACKET_V1.json'),json=JSON.stringify(out,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(filename,'utf8'),json);
else fs.writeFileSync(filename,json);
console.log(JSON.stringify({status:'PASS',candidate:last.id,from:last.likely_physical_zone_ids[0],to:inner.id,liveWorldMutations:0,remainingGates:out.required_gates.length}));
