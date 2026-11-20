#!/usr/bin/env node
/**
 * Candidate Atlas siting, checked against current seven-region World control
 * plane; no active world/data mutation. Abstract 0..100 Atlas coordinates
 * are normalized fictional map sketches, NOT actual distances, GIS or known
 * shorelines. This model is only a bounded governance-ready siting proposal.
 */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=(root,n)=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const world=path.resolve(dir,'../../world/data');
const regions=read(world,'physical_zones.json'),locations=read(world,'locations.json'),routes=read(world,'routes.json'),candidates=read(world,'atlas_location_candidates.json');
const region=regions.regions.find(x=>x.id==='REG-INNER-SEA-LITTORAL');
const oldField=candidates.candidates.find(x=>x.id==='CAND-CHAMP-LAST-FIELD');
assert.ok(region && oldField);
const [minX,minY,maxX,maxY]=region.abstract_bounds;
const candidate={
schema:'schemin.postseason.architect_candidate_siting.v1',
status:'UNPROMOTED_FOUNDER_APPROVED_CREATIVE_DIRECTION__SITING_HYPOTHESIS',
proof:{
physical_region_id:region.id,
region_source:'world/data/physical_zones.json',
historic_last_field_candidate:oldField.id,
historic_last_field_zone:oldField.likely_physical_zone_ids[0],
present_day_active_location_count:locations.locations.length,
present_day_active_route_count:routes.routes.length,
coordinates_class:'FICTIONAL_NORMALIZED_ATLAS_ABSTRACT_SKETCH',
metric_geography:false
},
hypothesis:{
public_mainland_gate:{id:'CAND-POST-NEUTRAL-PUBLIC-LITTORAL-GATE',name:'Neutral Littoral Causeway Gate',abstract_position:[68.5,13.5],
physical_zone_id:region.id,owner_character_id:null,division_id:null,type:'seasonal_public_approach',status:'CANDIDATE_NOT_LOC',
important:'No ownership or security command delegated to nearby LLC Storm City'},
causeway_crossing:{id:'CAND-POST-MONUMENTAL-CAUSEWAY',name:'Championship Causeway',abstract_path:[[68.5,13.5],[69.5,12.7],[70.6,12.0],[71.8,11.5]],
water_crossing:'HYPOTHESIZED_SHALLOW_SHELTERED_BAY_NO_BATHYMETRIC_PROOF',structural_loads:null,actual_length_m:null,engineering:'STORM_SURGE_AND_FOUNDATION_SURVEY_REQUIRED'},
island_centre:{id:'CAND-POST-CHAMPIONSHIP-ISLAND',name:'Championship Island',abstract_position:[73.8,10.5],zone_id:region.id,
private_owner_id:null,government:'LEAGUE_NEUTRAL_EVENTS_AUTHORITY_CANDIDATE',
arena_orientations:'SIX_FIXED_ROUND_VENUES_IN_SITE_NETWORK__ROTATION_AND_TRUE_NORTH_UNVERIFIED'},
candidate_outer_envelope:{
western_edge:[71.9,9.9],northern_ridge:[74.3,12.8],eastern_seawall:[76.1,10.0],
southern_harbor:[73.4,8.3],
shape:'ILLUSTRATIVE_POLYGON_NOT_SURVEYED_CADASTRE',
water_or_coastline_surveyed:false
},
landmark_sites:{
CAND_POST_LAST_FIELD:[74.9,11.2],CAND_POST_CROWN_STAIR:[73.6,12.1],CAND_POST_GROVE_STANDARDS:[74.2,10.5],
CAND_POST_IRON_QUARRY:[72.5,10.2],CAND_POST_SALTWIND:[75.6,11.1],CAND_POST_BREAKWATER:[74.8,8.9],
LOSERS_BEACH:[72.2,9.3],CAUSEWAY_GATE:[71.9,11.5],
PUBLIC_COMMONS:[72.5,10.9],BROADCAST_HQ:[73.0,11.8],CONTENDERS_FORTRESS:[73.9,11.0]
},
existing_nearby_owner_domain:{id:'LOC-LLC-STORM-CITY',owner_character_id:'CHAR-DAVID-BABB',use:'PORT_ORIENTATION_REFERENCE_ONLY_NOT_LEAGUE_AUTHORITY'},
planned_links:[
{id:'CAND-ROUTE-LEAGUE-TO-NEUTRAL-PORT-APPROACH',from:'LOC-LEAGUE-CHAMBER',to:'CAND-POST-NEUTRAL-PUBLIC-LITTORAL-GATE',status:'PROPOSED_REGIONAL_PUBLIC_LINK_NEEDS_SOURCED_ROAD_CORRIDOR'},
{id:'CAND-ROUTE-CHAMPIONSHIP-CAUSEWAY',from:'CAND-POST-NEUTRAL-PUBLIC-LITTORAL-GATE',to:'CAND-POST-CHAMPIONSHIP-ISLAND',status:'PROPOSED_MONUMENTAL_FIXED_CROSSING'},
{id:'CAND-ROUTE-ISLAND-RELIEF-FERRY',from:'CAND-POST-CHAMPIONSHIP-ISLAND',to:'CAND-POST-NEUTRAL-PUBLIC-LITTORAL-GATE',status:'CONTINGENCY_ROUTE_SURVEY_REQUIRED'}
]
},
approval_checks:[
'Authoritative mapping: Are these abstract points really mainland coast, island rock and sheltered navigable water? Current atlas only confirms general region and terrain.',
'World neutral authority: confirm League ownership, public roads and independent admission without LLC property rights',
'Last Field candidate superset: formally version old Central Basin prospect to island location before promoting LOC- IDs',
'Flood/storm: coastline/tide, rubble, bridge footing, slipway, refuge, and spectator closure procedures',
'Founding chronology 2015: bridge and permanent Last Field must already exist in original fictional 2015 edition; modern cameras/screens added only in later eras',
'Technological exception: venue-specific modern electricity, screens and camera distribution requires controlled World/Tech rule decision',
'Keep the 2015–25 physical scenery fiction separate from recorded ESPN sports evidence',
'Human owner / memorial sources must not be inferred from nearby place names'
],
world_writes:[],live_site_updates:[],canon_promotion:false
};
function inRegion([x,y]){return x>=minX&&x<=maxX&&y>=minY&&y<=maxY;}
const points=[
candidate.hypothesis.public_mainland_gate.abstract_position,
...candidate.hypothesis.causeway_crossing.abstract_path,
candidate.hypothesis.island_centre.abstract_position,
...Object.values(candidate.hypothesis.landmark_sites)
];
assert.ok(points.every(inRegion),'Outside active physical zone bounding box');
assert.equal(candidate.hypothesis.public_mainland_gate.owner_character_id,null);
assert.ok(!candidate.hypothesis.planned_links.some(x=>x.to==='LOC-LLC-STORM-CITY'));
const locationsExisting=locations.locations.filter(x=>x.physical_zone_id===region.id);
const noOccupiedSite=([x,y])=>locationsExisting.every(l=>Math.hypot(x-l.abstract_position[0],y-l.abstract_position[1])>3);
assert.ok(noOccupiedSite(candidate.hypothesis.public_mainland_gate.abstract_position));
assert.ok(noOccupiedSite(candidate.hypothesis.island_centre.abstract_position));
assert.equal(oldField.likely_physical_zone_ids[0],'REG-CENTRAL-BASIN');
const hash=crypto.createHash('sha256').update(JSON.stringify({base:region.abstract_bounds,positions:points,old:oldField.id})).digest('hex');
candidate.proof.layout_source_sha256=hash;
const result=JSON.stringify(candidate,null,2)+'\n',dest=path.join(dir,'ATLAS_NEUTRAL_CAUSEWAY_SITING_HYPOTHESIS_V1.proposal.json');
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(dest,'utf8'),result);
else fs.writeFileSync(dest,result);
console.log(JSON.stringify({status:'PASS',region:region.id,proposed_sites:Object.keys(candidate.hypothesis.landmark_sites).length,
public_approach_owner:null,existing_location_collisions:0,active_world_writes:0,metric_safety_certified:false,canonical_stadium_moved:false}));
