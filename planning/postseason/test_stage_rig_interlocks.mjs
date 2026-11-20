#!/usr/bin/env node
import assert from 'node:assert/strict';
import {RIGS,createRig,applyRigEvent,executeThreePhases} from './stage_rig_interlocks.mjs';
const tests=[];
function test(label,cb){cb();tests.push(label);}
const arrow='HIST-POST-2018-QF-1',clock='HIST-POST-2022-SF-1';
test('Two original-fiction rigs match their sourced 2018 and 2022 stadiums',()=>{
 assert.equal(Object.keys(RIGS).length,2);
 assert.equal(RIGS[arrow].venue,'CAND-POST-IRON-QUARRY');
 assert.equal(RIGS[clock].venue,'CAND-POST-CROWN-STAIR');
 assert.equal(RIGS[clock].geometry.inspector_role,'STOP_OR_VERIFY_ONLY_NEVER_CONSTRUCT_OR_ADJUST');
});
test('2018 shared archery/running trial closes exactly three safe phases',()=>{
 const x=executeThreePhases(arrow);
 assert.equal(x.status,'COMPLETE');
 assert.deepEqual(x.completed.map(y=>y.phase),[1,2,3]);
 assert.equal(x.official_points,null);
 assert.equal(x.history.filter(y=>y.event==='SHOT_A').length,3);
 assert.equal(x.history.filter(y=>y.event==='RUN_B').length,3);
});
test('2022 Clockwork Siege equal-kit trial closes three protected phases',()=>{
 const x=executeThreePhases(clock);
 assert.equal(x.status,'COMPLETE');
 assert.equal(x.completed.length,3);
 assert.equal(x.official_points,null);
 assert.equal(x.history.filter(y=>y.event==='ADJUST_A').length,3);
 assert.equal(x.history.filter(y=>y.event==='READ_SAFE_STOP').length,3);
});
test('Archery course cannot open sprint lanes while firing is active',()=>{
 let x=createRig(arrow);x=applyRigEvent(x,'INSPECT');x=applyRigEvent(x,'OPEN_RANGE');
 assert.throws(()=>applyRigEvent(x,'OPEN_RUN'),/UNSAFE_SEQUENCE/);
});
test('No contestant may fire during an uninspected stage',()=>{
 assert.throws(()=>applyRigEvent(createRig(arrow),'SHOT_A','A'),/UNSAFE_SEQUENCE/);
});
test('Owner B or assistant may not shoot for contestant A',()=>{
 let x=createRig(arrow);x=applyRigEvent(x,'INSPECT');x=applyRigEvent(x,'OPEN_RANGE');
 assert.throws(()=>applyRigEvent(x,'SHOT_A','B'),/OWNER_CHARACTER_MUST_ACT_PERSONALLY/);
 assert.throws(()=>applyRigEvent(x,'SHOT_A','ENGINEER'),/OWNER_CHARACTER_MUST_ACT_PERSONALLY/);
});
test('Stage referee cannot construct personally on behalf of entrant',()=>{
 let x=createRig(clock);x=applyRigEvent(x,'INSPECT');x=applyRigEvent(x,'OPEN_BUILD');
 assert.throws(()=>applyRigEvent(x,'ADJUST_A','REFEREE'),/OWNER_CHARACTER_MUST_ACT_PERSONALLY/);
});
test('Contestant cannot self certify official gate inspection',()=>{
 assert.throws(()=>applyRigEvent(createRig(clock),'INSPECT','A'),/OFFICIAL_INTERLOCK_REQUIRES_REFEREE/);
});
test('Equal kits are mandatory for Clockwork test',()=>{
 let x=createRig(clock);for(const [e,a] of [['INSPECT','REFEREE'],['OPEN_BUILD','REFEREE'],['ADJUST_A','A'],['ADJUST_B','B'],['CLOSE_BUILD','REFEREE']])x=applyRigEvent(x,e,a);
 x={...x,kit:{identical:false}};
 assert.throws(()=>applyRigEvent(x,'START_TEST'),/EQUAL_KITS_REQUIRED/);
});
test('No premature stage certification without range clearance',()=>{
 let x=createRig(arrow);x=applyRigEvent(x,'INSPECT');
 assert.throws(()=>applyRigEvent(x,'CERTIFY_STAGE'),/UNSAFE_SEQUENCE/);
});
test('No winner, actual score, real dimensions or public safety certification is fabricated',()=>{
 const x=executeThreePhases(clock);
 assert.equal(x.official_points,null);assert.equal(x.observer,'OUTCOME_NEUTRAL_NO_WINNER');
 assert.equal(RIGS[clock].actual_mass_kg,null);
 assert.equal(RIGS[clock].real_cantilever_length_m,null);
 assert.equal(RIGS[clock].real_approved_friction_coefficient,null);
 assert.match(RIGS[clock].scale,/NOT_ENGINEERING_CERTIFICATION/);
});
console.log(JSON.stringify({status:'PASS',tests:tests.length,rigs:2,stages:6,official_winner_simulated:0,checks:tests},null,2));
