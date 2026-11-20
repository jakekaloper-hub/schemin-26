#!/usr/bin/env node
/**
 * Schematic venue/arena spatial staging compiler for Founder Interviews I & II.
 * Not a surveyed Atlas, 3D physics solver, engineering safety certification,
 * or claim of geographic measurements.
 *
 * A two-level coordinate model:
 *  - island diagram: existing 980 x 650 interactive map "display pixels"
 *  - competition arena: local [-1,1] normalized "stage units"
 *
 * All stadiums stay anchored. A/B must move independently through three stages.
 * Every grounded route requires the already-versioned 45-link topology.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {VENUES,evaluatePhysicalFit} from './arena_physical_affordances.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const topo=read('ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json');
const scenes=read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json');
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const lib=read('OBSTACLE_LEXICON_120_V1.json');
const impacts=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const mapCoords={
MAINLAND_PUBLIC_LITTORAL:[72,302],CAUSEWAY_OUTER_GATE:[161,302],CAUSEWAY_RIDGE:[273,302],
ISLAND_ENTRY_CHECK:[398,305],HARBOR_RELIEF:[383,212],BROADCAST_HQ:[451,200],
TAILGATE_COMMONS:[490,342],LOSERS_BEACH:[381,437],BEACH_PAVILIONS:[340,512],
IRON_QUARRY:[516,474],SALTWIND_STEPS:[753,240],BREAKWATER_GROUNDS:[686,508],
CONTENDER_FORTRESS:[610,306],BYE_HOUSE:[635,245],CROWN_STAIR:[563,169],
GROVE_STANDARDS:[683,375],CHAMPIONS_WALK:[744,315],FARRELL_SANCTUARY:[797,392],
MUSEUM_TROPHY_HALL:[807,332],LAST_FIELD:[843,248],LAST_FIELD_SUITES:[886,188],
UTILITY_PLANT:[774,529],EMERGENCY_PIER:[851,555]
};
const venueToNode={
'CAND-POST-IRON-QUARRY':'IRON_QUARRY','CAND-POST-SALTWIND':'SALTWIND_STEPS',
'CAND-POST-BREAKWATER':'BREAKWATER_GROUNDS','CAND-POST-CROWN-STAIR':'CROWN_STAIR',
'CAND-POST-GROVE':'GROVE_STANDARDS','CAND-POST-LAST-FIELD':'LAST_FIELD'
};
const environment={
IRON_QUARRY:{slope:'stepped_bowl',ground:'stone_gravel',wind:'sheltered',water:'runoff_drains',surface_level:'tiered',lighting:'open',control:'ROCKFALL_INSPECTION_REQUIRED'},
SALTWIND_STEPS:{slope:'steep_safe_terraces',ground:'limestone_rigging',wind:'crosswind_exposed',water:'sea_spray',surface_level:'tiered',lighting:'open',control:'STORM_WIND_CLOSE'},
BREAKWATER_GROUNDS:{slope:'seawall_platforms',ground:'tideproof_stone',wind:'maritime',water:'tide_gated_basin',surface_level:'tiered',lighting:'open',control:'TIDE_SURGE_CLOSE'},
CROWN_STAIR:{slope:'ceremonial_stair',ground:'historic_stone',wind:'protected',water:'managed_drainage',surface_level:'tiered',lighting:'stadium',control:'STAIR_FALL_PROTECTION'},
GROVE_STANDARDS:{slope:'gentle_natural_bowl',ground:'reinforced_turf',wind:'filtered_by_trees',water:'root_zone_runoff',surface_level:'mixed',lighting:'canopy',control:'TREE_AND_FIRE_RISK'},
LAST_FIELD:{slope:'maintained_level_oval',ground:'sacrificial_stage_infill_above_stone',wind:'open_air_controlled',water:'controlled_stadium_drainage',surface_level:'level',lighting:'broadcast',control:'FOUNDING_FOUNDATION_PROTECTED'}
};
const stageGeometry=[
{name:'opening',A:[-0.68,-0.52],B:[0.68,-0.52],barrier_radius:0.08,contest_ring:0.87},
{name:'counterpressure',A:[-0.43,0.06],B:[0.43,0.06],barrier_radius:0.08,contest_ring:0.87},
{name:'decisive',A:[-0.13,0.59],B:[0.13,0.59],barrier_radius:0.08,contest_ring:0.87}
];
function dist(a,b){return Math.hypot(a[0]-b[0],a[1]-b[1]);}
export function route(from,to,mode){
 const known=new Set(topo.nodes.map(n=>n.id));assert.ok(known.has(from)&&known.has(to));
 const q=[from],seen=new Set(q),prev=new Map();
 for(const x of q){
  if(x===to)break;
  for(const e of topo.edges){
   if(!e.modes.includes(mode))continue;
   const y=e.from===x?e.to:e.to===x?e.from:null;
   if(y&&!seen.has(y)){seen.add(y);q.push(y);prev.set(y,x);}
  }
 }
 if(!seen.has(to))return null;
 const p=[to];while(p[0]!==from)p.unshift(prev.get(p[0]));
 return p;
}
export function validateStageContest({venue_id,obstacle,year,round,conditions={}}){
 const fit=evaluatePhysicalFit({obstacle,venue_id,year,round,conditions});
 const reasons=[...fit.reasons];
 const node=venueToNode[venue_id];
 if(!node || !mapCoords[node])reasons.push('NO_GROUNDED_DIAGRAM_NODE');
 if(!route('CONTENDER_FORTRESS',node,'contender'))reasons.push('NO_SEPARATE_PERSONAL_ENTRANCE');
 if(!route('TAILGATE_COMMONS',node,'public'))reasons.push('NO_PUBLIC_SPECTATOR_ROUTE');
 if(!route('BROADCAST_HQ',node,'media'))reasons.push('NO_INDEPENDENT_MEDIA_ROUTE');
 if(!route('UTILITY_PLANT',node,'service'))reasons.push('NO_STAGING_SERVICE_ROUTE');
 for(const s of stageGeometry){
  if(dist(s.A,s.B)<=s.barrier_radius*2)reasons.push('CONTESTANTS_COLLIDE_UNINTENTIONALLY');
  if(Math.hypot(...s.A)>=s.contest_ring||Math.hypot(...s.B)>=s.contest_ring)reasons.push('PLAYER_OUTSIDE_PROTECTED_COURT');
 }
 if(venue_id==='CAND-POST-LAST-FIELD'&&year<2015)reasons.push('HISTORIC_GROUND_NOT_DEFINED');
 return {eligible:reasons.length===0,reasons,site_node:node,terrain:environment[node],
   field_geometry_status:'NORMALIZED_STAGE_LAYOUT_NOT_METRIC_PHYSICS',
   route_paths:{
    contender:route('CONTENDER_FORTRESS',node,'contender'),
    spectator:route('TAILGATE_COMMONS',node,'public'),
    broadcast:route('BROADCAST_HQ',node,'media'),
    service:route('UTILITY_PLANT',node,'service')
   },
   crowd_boundary:{radius_min:0.95,neutral_spectator_distance:'UNMEASURED_REQUIRES_PHYSICAL_SURVEY'},
   official_source:'ESPN_ONLY',
   structural_certification:false,world_location_promotion:false};
}
function build(){
 assert.equal(topo.nodes.length,23);assert.equal(topo.edges.length,45);
 assert.equal(Object.keys(mapCoords).length,23);
 const idMap=new Map(lib.obstacles.map(o=>[o.id,o]));
 const draws=new Map(draw.ceremonies.map(x=>[x.fixture_id,x]));
 const traces=new Map(impacts.traces.map(x=>[x.fixture_id,x]));
 const packets=scenes.cards.map(c=>{
  const drawn=draws.get(c.fixture_id),o=idMap.get(drawn.selected_obstacle_id),trace=traces.get(c.fixture_id);
  const fit=validateStageContest({venue_id:c.venue_id,obstacle:o,year:c.year,round:c.round});
  assert.equal(fit.eligible,true,c.fixture_id+':'+fit.reasons.join(','));
  assert.equal(c.acts.length,3);
  const stageViews=c.acts.map((a,i)=>({...stageGeometry[i],
   A_action:a.solo_contender_A.action,B_action:a.solo_contender_B.action,
   personally_performed:true,public_geometry:'TWO_SIDE_BY_SIDE_LANES_REJOIN_ONLY_AT_CERTIFIED_FINAL',
   official_point_conversion:'NOT_ALLOWED'}));
  return {fixture_id:c.fixture_id,season:c.year,round:c.round,venue_candidate_id:c.venue_id,
    diagram_center:mapCoords[venueToNode[c.venue_id]],
    stage_axes:stageViews,
    access:fit.route_paths,
    physical_fit:fit,
    deferred_real_geometry:['arena_bounding_dimensions','slope_degrees','spectator_clearances','load_limits','escape_travel_times'],
    memorial_conflict:'NO_STAGE_OR_SERVICE_ROUTE_THROUGH_FARRELL_SANCTUARY',
    persistent_fixture_impact:trace.trace_id,
    source_verified_winner_slot:c.verified_sports.winner_slot,
    state:'FICTIONAL_CANDIDATE_NOT_ACTIVE_ATLAS'};
 });
 const sites=Object.entries(venueToNode).map(([id,node])=>({
  id,node,diagram_center:mapCoords[node],terrain:environment[node],
  permanent_stage_axis:{longitudinal:'south_to_north_schematic',opposing_gates:['west_side','east_side']},
  normalized_stage_footprint:{x:[-1,1],y:[-1,1]},stage_template:stageGeometry,
  preservation_rule:id==='CAND-POST-LAST-FIELD'?'ORIGINAL_LAST_FIELD_GATES_AND_FOUNDATION_FIXED_2015_2025':'ROUND_SPECIFIC_PERMANENT_TERRAIN_AND_SITE_AFFORDANCES',
  real_map_coordinates:null}));
 return {schema:'schemin.postseason.schematic_spatial_stage_engine.v1',
  status:'CANDIDATE_SCHEMATIC_NOT_GEOGRAPHIC_ENGINEERING_OR_PHYSICS_CERTIFICATION',
  grid:{width:980,height:650,units:'CURRENT_ATLAS_PREVIEW_DISPLAY_PIXELS',orientation:'SKETCH_ONLY_NOT_TRUE_NORTH',island_extent:'UNMEASURED',actual_coordinates:null},
  diagrams:topo.nodes.map(n=>({...n,screen_position:mapCoords[n.id]})),
  permanent_round_sites:sites,
  scene_packets:packets,
  annual_safety_limit:'SITE_REUSE_REQUIRES_EVIDENCED_REPAIRS_IN_WORLD_STATE',
  no_sport_result_simulation:true,no_live_world_data_mutation:true,no_2026_outcome:true};
}
const result=build(),serial=JSON.stringify(result,null,2)+'\n';
const out=path.join(dir,'ISLAND_SPATIAL_STAGE_ENGINE_V1.proposal.json');
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(out,'utf8'),serial);
else fs.writeFileSync(out,serial);
console.log(JSON.stringify({status:'PASS',nodes:result.diagrams.length,permanent_sites:result.permanent_round_sites.length,fixtures:result.scene_packets.length,stages:result.scene_packets.reduce((n,x)=>n+x.stage_axes.length,0),simulated_winners:0}));
