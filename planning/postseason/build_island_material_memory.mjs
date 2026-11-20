#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const historic=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const sites=read('ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json');
const options=read('HISTORICAL_CHALLENGE_OPTION_BINDINGS_56_V1.json');
const byFixture=new Map(options.proposals.map(x=>[x.fixture_id,x]));
const phase=y=>y<=2016?'ORIGINAL_STONE_AND_SIMPLE_STANDS':y<=2020?'SIX_TEAM_EXPANSION_WITH_TWO_QF_SITES':'SEVEN_TEAM_CAMPUS_AND_PRODUCTION_HQ';
const annualMemory=[
[2015,'Founding terraces and the permanent Last Field ceremonial gates are first represented in the recovered championship archive.'],
[2016,'Two seasons of stone maintenance and repeat spectator movement create recognizable paths, not large new technology.'],
[2017,'The six-team bracket licenses distinct Iron Quarry and Saltwind quarterfinal grounds, with expanded protected entrances.'],
[2018,'A razor-thin quarterfinal becomes an archival inscription, not retroactive proof of a damaged building.'],
[2019,'League-name banners and program fixtures change; original stone paths and stadium orientation remain.'],
[2020,'The 0.75-point final intensifies scorekeeper/announcer protocol; no novel structural destruction is required.'],
[2021,'Breakwater opens as the dedicated third quarterfinal ground, with larger visitor and central production facilities proposed.'],
[2022,'Scars of recurrent staged equipment are visible, but the permanent stadium and playoff grounds remain serviceable.'],
[2023,'Modern camera and screen mountings can become visually dominant without changing the protected founding arches.'],
[2024,'Hospitality/suites and site-specific viewing platforms are upgraded; old arena surfaces retain identity.'],
[2025,'The nearly contemporary stadium complex has elaborate lighting, camera architecture and maintained historic stone beneath it.']
];
const perimeter=[
{id:'HERITAGE-OLD-RING',name:'The Old Ring',use:'DORMANT_OLDER_ARENA',terrain:'lower weathered stone circle',state:'STAFF_CLOSED',narrative:'An obsolete ring and benches, preserved as a visible memory of an earlier manner of trial; no verified League playoff is assigned here under Founder round law.'},
{id:'HERITAGE-VETERANS-YARD',name:"Veterans' Yard",use:'RETIRED_TRAINING_GROUND',terrain:'small enclosed practice courtyard',state:'STAFF_CLOSED',narrative:'Cracked old practice markers and an overgrown spectator bank are preserved instead of polished into a new final venue.'},
{id:'HERITAGE-CAUSEWAY-TRIAL',name:'Abandoned Tide Causeway Trial',use:'DORMANT_OBSTACLE_STRUCTURE',terrain:'isolated old tidal piers',state:'BARRIER_LOCKED',narrative:'An unsafe training route lies beside—not replacing—the monumental current causeway; it is a background ruin, not a public passage.'},
{id:'HERITAGE-POWDER-BERM',name:'The Powder Berm',use:'BLAST_EFFORT_HISTORY',terrain:'scraped rock berm behind a closed tactical yard',state:'PERMIT_REQUIRED',narrative:'Darkened gravel, blast panels and dismantled smoke-effect frames suggest staged explosive spectacles. No precise historic detonation is asserted without approved state event.'},
{id:'HERITAGE-FLOODED-MAZE',name:'The Sunken Course',use:'WATER_COURSE_REMNANT',terrain:'flooded masonry labyrinth on low island edge',state:'ACCESS_PROHIBITED',narrative:'A retired challenge maze with standing brackish water and plants reclaiming its former lanes; no contestant casually enters it.'},
{id:'HERITAGE-FALLEN-GALLERY',name:'The Fallen Gallery',use:'SPECTATOR_RUIN',terrain:'rock ledge with collapsed roof timbers',state:'MASONRY_SURVEY_HOLD',narrative:'An old viewing structure awaiting survey and preservation, with all ticket routes diverted around it.'},
{id:'HERITAGE-RUSTED-OVAL',name:'Rusted Oval',use:'RETIRED_RACE_TRACK',terrain:'gravel racing circuit beyond current arena fence',state:'CLOSED_TEST_RING',narrative:'Rust-stained barriers and stripped-out engines recall a changing taste for wheeled speed without pretending dirt bikes existed in 2015.'},
{id:'HERITAGE-ARCHERY-CRESCENT',name:'The Silent Crescent',use:'RETIRED_TARGET_RANGE',terrain:'shuttered stone arrow range',state:'RANGE_CLOSED',narrative:'Broken-but-locked target mounts sit behind a collapsed protective retaining wall, not freely accessible among spectators.'},
{id:'HERITAGE-PAINTBALL-FORT',name:'The Empty Fort',use:'RETIRED_TACTICAL_SET',terrain:'weathered mock-fort walls behind an inspection fence',state:'CLOSED_UNTIL_REFURBISHED',narrative:'A defunct nonlethal war-game set retains splattered panels and abandoned ramparts. Its date and original use remain fictional candidates.'}
];
const yearStates=[];
for(const [year,annotation] of annualMemory){
 const matches=historic.fixtures.filter(x=>x.year===year);
 const venues=sites.sites.filter(x=>['QUARTERFINAL_ONLY','SEMIFINAL_ONLY','FINAL_ONLY'].includes(x.round_assignment));
 const spaces=venues.map(v=>{
  const applicable=matches.filter(f=>f.staging.venue_id===v.id);
  const first=v.first_proposed_appearance;
  const inUse=applicable.length>0;
  const state=first===null||year<first?'NOT_YET_OPEN_FOR_PLAYOFF':inUse?'OPEN_FOR_DESIGNATED_ROUND':'MAINTENANCE_NO_BRACKET';
  const memoryCandidates=applicable.map(f=>{
   const scenario=byFixture.get(f.id);
   if(!scenario)throw Error('Missing obstacle suggestion '+f.id);
   return {fixture_id:f.id,obstacle_id:scenario.picked_obstacle_id,mechanical_effect_risk:scenario.physical_contract.required_controls,
    visual_afterimage:'Possible removable apparatus wear, scratched boundary paint, repaired rail or photographed temporary damage, never automatic structural collapse.',
    persistence:'NOT_CANON_WRITEBACK',source:'PROPOSED_SCENE_NOT_HISTORICAL_PHYSICAL_FACT'};
  });
  return {id:v.id,name:v.name,round:v.round_assignment,activation:state,matched_fixtures:applicable.map(f=>f.id),
   foundational_landmarks_preserved:year>=2015,maintenance:'Annual inspection of stone, seats, water diversion, public protection, stage rig and media mounts',
   permanent_explosion_damage_allowed:false,
   candidate_scene_scars:memoryCandidates};
 });
 yearStates.push({year,era:phase(year),theme:annotation,legacy_sites:spaces,postseason_visitors_only:true,
  maintenance_note:'Offseason public closure with limited caretakers; full tourist resort runs only during the postseason.',
  year_events_source:'FROZEN_SPORT_RESULTS_AND_PROPOSED_GEOGRAPHIC_MEMORY',
  museum_archive:{champion_slot:historic.annual.find(x=>x.year===year).champion_slot,status:'SPORTING_FACT; INSCRIPTION_FICTION'},
  media_technology_status:'YEAR_SPECIFIC_DRAFT_NOT_WORLD_TECH_RATIFICATION'});
}
assert.equal(yearStates.length,11);
assert.equal(perimeter.length,9);
assert.equal(yearStates.flatMap(y=>y.legacy_sites.flatMap(v=>v.matched_fixtures)).length,56);
const data={schema:'schemin.postseason.island_material_memory.v1',status:'HISTORICAL_ART_DIRECTION_NOT_ACTIVE_WORLD_EVENTS',
sources:['ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json','HISTORICAL_CHALLENGE_OPTION_BINDINGS_56_V1.json'],
principle:'Old scars exist if authored and approved; screens and suites evolve; the Last Field has the same maintained geometry and no catastrophic foundation damage.',
perimeter_ruins:perimeter,years:yearStates,release_holds:['NO_LOCATION_PROMOTION','NO_HISTORICAL_DAMAGE_CANON_WITHOUT_PROVENANCE','NO_2026_WINNER','YEAR_SCOPED_TECH_APPROVAL_REQUIRED']};
const output=path.join(dir,'ISLAND_MATERIAL_MEMORY_2015_2025_V1.json'),serial=JSON.stringify(data,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(output,'utf8'),serial);
else fs.writeFileSync(output,serial);
console.log(JSON.stringify({status:'PASS',years:yearStates.length,ruins:perimeter.length,fixture_links:56,first_2021_three_qf:yearStates.find(y=>y.year===2021).legacy_sites.filter(x=>x.round==='QUARTERFINAL_ONLY'&&x.matched_fixtures.length).length}));
