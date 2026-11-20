#!/usr/bin/env node
/**
 * Two executable, schematic stage-apparatus safety protocol state machines:
 *   2018 Arrow and Sprint (Iron Quarry QF)
 *   2022 Clockwork Siege (Crown Stair SF)
 *
 * This tests equipment interlocks / solo actions at proposal scale, not
 * real projectile ballistics, structural certification, medical safety or
 * actual competition outcome. The official winner remains external ESPN truth.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const draws=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const byId=new Map(history.fixtures.map(x=>[x.id,x])),byDraw=new Map(draws.ceremonies.map(x=>[x.fixture_id,x]));
export const RIGS=Object.freeze({
'HIST-POST-2018-QF-1':{
  challenge:'Arrow and Sprint',venue:'CAND-POST-IRON-QUARRY',round:'QF',era:2018,
  type:'PROTECTED_ARCHERY_THEN_SPRINT',
  geometry:{
    equal_separate_target_bays:2,independently_lockable_target_backstops:true,run_lanes:2,
    live_range_and_run_path_may_overlap:false,safety_gate:'CLOSED_UNTIL_RANGE_CLEAR',
    sloping_quarry_surface:'GRADED_NON_SLIP_REMOVABLE_INLAY',
    closing_marker:'LOWER_QUARRY_SHELF_REPLACEABLE_PLATE'
  },
  scale:'NORMALIZED_DESIGN_UNITS_NO_METRIC_DISTANCES',
  stage_count:3,
  no_score_from_trial:true,
  legacy_trace:'TRACE-HIST-POST-2018-QF-1'
},
'HIST-POST-2022-SF-1':{
  challenge:'Clockwork Siege',venue:'CAND-POST-CROWN-STAIR',round:'SF',era:2022,
  type:'EQUAL_KIT_ENGINEERING_LOAD_TEST',
  geometry:{
    matched_neutral_kits:true,build_zones:2,independent_lift_devices:2,
    bracing_kit:'SAME_APPROVED_PARTS_PER_ACTOR',counterweight_track:'TEST_CELL_ONLY',
    sacrificial_test_floor:'SEALED_PLATE_OVER_ORIGINAL_STONE',
    mechanical_stop:'ENGAGES_BEFORE_LOAD_LIMIT',
    inspector_role:'STOP_OR_VERIFY_ONLY_NEVER_CONSTRUCT_OR_ADJUST'
  },
  permitted_load_steps_normalized:[0.25,0.5,0.75],
  load_upper_envelope_normalized:1,
  max_lateral_deflection_fraction_normalized:0.18,
  actual_mass_kg:null,real_cantilever_length_m:null,real_approved_friction_coefficient:null,
  scale:'NORMALIZED_MECHANICAL_PREVIS_ONLY_NOT_ENGINEERING_CERTIFICATION',
  stage_count:3,
  no_score_from_trial:true,
  legacy_trace:'TRACE-HIST-POST-2022-SF-1'
}});
const keyEvents={
PROTECTED_ARCHERY_THEN_SPRINT:{
 INITIAL:'INSPECT',
 INSPECTED:'OPEN_RANGE',
 RANGE_OPEN:'SHOT_A',
 AFTER_A:'SHOT_B',
 AFTER_B:'CLOSE_RANGE',
 RANGE_CLOSED:'CONFIRM_CLEAR',
 RANGE_CLEAR:'OPEN_RUN',
 RUN_OPEN:'RUN_A',
 AFTER_RUN_A:'RUN_B',
 AFTER_RUN_B:'CLOSE_RUN',
 RUN_CLOSED:'CERTIFY_STAGE'
},
EQUAL_KIT_ENGINEERING_LOAD_TEST:{
 INITIAL:'INSPECT',
 INSPECTED:'OPEN_BUILD',
 BUILD_OPEN:'ADJUST_A',
 AFTER_A:'ADJUST_B',
 AFTER_B:'CLOSE_BUILD',
 BUILD_CLOSED:'START_TEST',
 TEST_ACTIVE:'READ_SAFE_STOP',
 TEST_STOPPED:'LOCK_DEVICE',
 DEVICE_LOCKED:'CERTIFY_STAGE'
}};
const nextStates={
PROTECTED_ARCHERY_THEN_SPRINT:{
 INITIAL:'INSPECTED',INSPECTED:'RANGE_OPEN',RANGE_OPEN:'AFTER_A',AFTER_A:'AFTER_B',
 AFTER_B:'RANGE_CLOSED',RANGE_CLOSED:'RANGE_CLEAR',RANGE_CLEAR:'RUN_OPEN',
 RUN_OPEN:'AFTER_RUN_A',AFTER_RUN_A:'AFTER_RUN_B',AFTER_RUN_B:'RUN_CLOSED',RUN_CLOSED:'STAGE_CLOSED'},
EQUAL_KIT_ENGINEERING_LOAD_TEST:{
 INITIAL:'INSPECTED',INSPECTED:'BUILD_OPEN',BUILD_OPEN:'AFTER_A',AFTER_A:'AFTER_B',
 AFTER_B:'BUILD_CLOSED',BUILD_CLOSED:'TEST_ACTIVE',TEST_ACTIVE:'TEST_STOPPED',
 TEST_STOPPED:'DEVICE_LOCKED',DEVICE_LOCKED:'STAGE_CLOSED'}
};
export function createRig(fixtureId){
 const rig=RIGS[fixtureId],fixture=byId.get(fixtureId),draw=byDraw.get(fixtureId);
 if(!rig||!fixture||!draw)throw Error('NO_AUTHORIZED_PROPOSAL_FIXTURE');
 if(draw.obstacle_name!==rig.challenge||fixture.staging.venue_id!==rig.venue||fixture.round!==rig.round||fixture.year!==rig.era)
  throw Error('SOURCE_DRAW_OR_VENUE_MISMATCH');
 return {fixture_id:fixtureId,type:rig.type,phase:1,status:'INITIAL',history:[],
  completed:[],observer:'OUTCOME_NEUTRAL_NO_WINNER',official_points:null,
  kit:{identical:rig.type==='EQUAL_KIT_ENGINEERING_LOAD_TEST'?rig.geometry.matched_neutral_kits:true},
  condition:'UNMEASURED_SCHEMATIC_DESIGN',release:'PREVIS_ONLY'};
}
export function applyRigEvent(state,event,actor='REFEREE'){
 const rig=RIGS[state.fixture_id];if(!rig||state.phase>3)throw Error('OUT_OF_SCOPE_RIG');
 const expected=keyEvents[rig.type][state.status];
 if(!expected||event!==expected)throw Error('UNSAFE_SEQUENCE:'+state.status+' EXPECT:'+expected+' GOT:'+event);
 const performerEvents=new Set(['SHOT_A','SHOT_B','RUN_A','RUN_B','ADJUST_A','ADJUST_B']);
 const role={SHOT_A:'A',SHOT_B:'B',RUN_A:'A',RUN_B:'B',ADJUST_A:'A',ADJUST_B:'B'}[event]||null;
 if(performerEvents.has(event)&&actor!==role)throw Error('OWNER_CHARACTER_MUST_ACT_PERSONALLY');
 if(!performerEvents.has(event)&&actor!=='REFEREE')throw Error('OFFICIAL_INTERLOCK_REQUIRES_REFEREE');
 if(event==='START_TEST'&&!state.kit.identical)throw Error('EQUAL_KITS_REQUIRED');
 const after=nextStates[rig.type][state.status];
 const next={...state,status:after,history:[...state.history,{phase:state.phase,event,actor}]};
 if(after==='STAGE_CLOSED'){
   next.completed=[...state.completed,{phase:state.phase,closed:true,provenance:'SCHEMATIC_STAGING_ONLY'}];
   next.phase=state.phase+1;
   next.status=next.phase<=3?'INITIAL':'COMPLETE';
 }
 return next;
}
export function executeThreePhases(fixtureId){
 let state=createRig(fixtureId);
 const protocol=RIGS[fixtureId];
 while(state.status!=='COMPLETE'){
   const event=keyEvents[protocol.type][state.status];
   if(!event)throw Error('RIG_STUCK:'+state.status);
   const actor=event.endsWith('_A')?'A':event.endsWith('_B')?'B':'REFEREE';
   state=applyRigEvent(state,event,actor);
 }
 if(state.completed.length!==3||state.official_points!==null)throw Error('RESULT_CLAIM_OR_STAGE_COUNT_BAD');
 return state;
}
function build(){
 const simulations=Object.keys(RIGS).map(fixture_id=>{
  const s=executeThreePhases(fixture_id),rig=RIGS[fixture_id];
  return {fixture_id,source_draw:byDraw.get(fixture_id).obstacle_name,
   venue_candidate_id:rig.venue,era:rig.era,
   rig_protocol:rig,
   three_stages_closed:s.completed,
   inspected_event_log:s.history,
   winner:null,official_points:null,
   physical_consequence:rig.legacy_trace,
   safety_claim:'ABSTRACT_INTERLOCK_RULES_ONLY_REAL_LOADS_AND_CROWD_CLEARANCES_NOT_VERIFIED'};
 });
 return {schema:'schemin.postseason.illustrative_rig_protocols.v1',
  status:'TWO_VALIDATED_HISTORICAL_SCENE_PROTOCOLS_FICTION_ONLY',
  stage_protocols:simulations,
  no_live_results:true,no_real_engineering_certification:true,no_2026_result:true};
}
const compiled=build();
const out=path.join(dir,'HISTORICAL_RIG_INTERLOCK_PROTOCOLS_V1.proposal.json'),serial=JSON.stringify(compiled,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(out,'utf8'),serial);
else fs.writeFileSync(out,serial);
console.log(JSON.stringify({status:'PASS',rigs:compiled.stage_protocols.length,closed_phases:compiled.stage_protocols.reduce((n,x)=>n+x.three_stages_closed.length,0),realtime_winner_simulated:false}));
