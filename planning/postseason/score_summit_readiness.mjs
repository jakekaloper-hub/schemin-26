#!/usr/bin/env node
/**
 * Evidence-scored self-audit for the Founder V2 postseason island prototype.
 * This is NOT a simulated independent Umpire signoff or licensed GIS survey.
 * Scoring deliberately penalizes those unresolved gates.
 */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const root=path.dirname(fileURLToPath(import.meta.url));
const get=name=>JSON.parse(fs.readFileSync(path.join(root,name),'utf8'));
const lex=get('OBSTACLE_LEXICON_120_V1.json');
const options=get('HISTORICAL_CHALLENGE_OPTION_BINDINGS_56_V1.json');
const material=get('ISLAND_MATERIAL_MEMORY_2015_2025_V1.json');
const history=get('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const consult=get('SIMULATED_CONSULTENGINE_18_DIRECTORS_3_ADVISORS_RECEIPT.json');
const site=fs.readFileSync(path.join(root,'site','CHAMPIONSHIP_ISLAND_PREVIEW.html'),'utf8');
const tests=['test_obstacle_physical_engine.mjs','test_postseason_founder_v2_integrity.mjs','test_inklings_interventions.mjs','test_summit_integrity.mjs','test_island_circulation.mjs','test_tournament_runtime.mjs','test_postseason_cross_os_preflight.mjs','test_broadcast_history.mjs','site/test_site.mjs'];
const runStatus=[];
for(const test of tests){
 const output=execFileSync(process.execPath,[path.join(root,test)],{encoding:'utf8',timeout:20000});
 const result=JSON.parse(output);
 assert.equal(result.status||result.result,'PASS','Failed '+test);
 runStatus.push({test,result:'PASS',test_count:result.tests||result.checks||result.cases||null});
}
const independentUmpire=false,activeAtlas=false,realPhysicalSimulation=false;
const score=[
{name:'Creative diversity',weight:20,earned:18,evidence:'12 categories, 120 distinct scenarios, 56 unique fixture options; stage grammar still partly templated'},
{name:'Physical/geographic realism',weight:20,earned:14,evidence:'Six site-affordance and weather/era validators, 45 planning links; no measured coastline, engineering survey, or Newtonian solver'},
{name:'Historical persistence',weight:15,earned:13,evidence:'11 dated annual venue states, 9 dormant or ruined sublocations, repairs and media lineage; staged historical scars unapproved'},
{name:'Competitive source truth',weight:15,earned:15,evidence:'All 56 verified matches, champions, scores and byes retained; 2026 winner remains unset'},
{name:'Spectator experience',weight:10,earned:9,evidence:'Interactive exhibit, 56 matchup views, stage/arena weather simulator, 11 finales; no rendered film/video'},
{name:'Inklings/Bullpen execution',weight:10,earned:8,evidence:'Source-locked compilers, 18-director+3-advisor scripted engine rehearsal; no independently running AI production team'},
{name:'Canon, memorial and QA',weight:10,earned:6,evidence:'Historic score separation and release holds; missing independent Umpire, active Atlas approval, Farrell naming chronology and tech exception'}
];
const total=score.reduce((a,x)=>a+x.earned,0);
assert.equal(score.reduce((a,x)=>a+x.weight,0),100);
assert.equal(total,83);
assert.equal(lex.obstacles.length,120);assert.equal(options.proposals.length,56);assert.equal(history.fixtures.length,56);assert.equal(material.years.length,11);
assert.equal(consult.board.director_count,18);assert.equal(consult.consultants.length,3);
assert.ok(site.includes('id="challenges"'));
const out={
schema:'schemin.postseason.summit_readiness_rubric.v1',status:'CREATOR_SELF_ASSESSMENT_NOT_INDEPENDENT_QA',date:'2026-11-19',
score:total,threshold:85,meets_threshold:total>=85,release_ready:false,
hard_gates:{independent_umpire:independentUmpire,active_atlas_location:activeAtlas,measured_physical_engine:realPhysicalSimulation,official_2026_winners_available:false,farrell_memorial_naming_chronology_verified:false},
dimensions:score,
tests:runStatus,
summit_sources:['SUMMIT_2026_11_19_18_DIRECTORS_12_ANGLES_V1.md','SIMULATED_CONSULTENGINE_18_DIRECTORS_3_ADVISORS_RECEIPT.json'],
revision_decisions:[
 {owner:'Beat Writer + Inklings',phase:'NEXT_SCENE_WRITING',work:'Replace remaining generic phase vocabulary with distinct full dramatic scripts, especially 56 different physical climax sequences',status:'OPEN'},
 {owner:'Architect + Groundskeeper',phase:'ATLAS_HARDENING',work:'Ground causeway in active coastline/port route and verify hydrology, load-bearing and spectator emergency capacity',status:'BLOCKED_BY_CANON_WORLD_SURVEY'},
 {owner:'Scout + Librarian',phase:'HISTORIC_OWNER_PROVENANCE',work:'Recover human owner continuity and historical Michael Farrell naming evidence before personally attributed camp memory',status:'BLOCKED_SOURCE'},
 {owner:'World/Tech + Setup Man',phase:'BROADCAST_CANON',work:'Reconcile island-modern camera and screens with broader premodern Commonwealth and global relay technology',status:'CANON_APPROVAL_REQUIRED'},
 {owner:'Independent Umpire',phase:'RELEASE',work:'Review exact diff, scene packs and source/provenance test receipts, then authorize appropriate stage of promotion',status:'PENDING_INDEPENDENT_REVIEW'}
 ],
notes:['No fabricated independent score from three public figures','Passing algorithmic tests does not certify real physics or artistic excellence','Rubric <85 means preproduction improvements still necessary; do not merge or publish the canonical island.']
};
const target=path.join(root,'POSTSEASON_SUMMIT_MEASURED_RUBRIC_V1.json'),serial=JSON.stringify(out,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(target,'utf8'),serial,'Rubric evidence drift');
else fs.writeFileSync(target,serial);
console.log(JSON.stringify({status:'PASS',scored:total,threshold:85,release:'HOLD',test_suites:tests.length,output:path.basename(target)}));
