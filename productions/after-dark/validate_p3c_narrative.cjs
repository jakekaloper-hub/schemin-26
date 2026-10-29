#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const load=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const validate=p=>{
 assert.equal(p.schema_version,'1.0');
 assert.ok(p.episode_id && p.story_cutoff && p.source_refs?.length);
 assert.equal(p.canon_status,'NONCANON_DRAFT');
 assert.equal(p.venue.status,'CANDIDATE_NOT_ACTIVE');
 assert.equal(p.story_levels.micro.scene_objective.length>12,true);
 assert.equal(p.story_levels.macro.thread_id.length>3,true);
 assert.equal(new Set(p.coverage.map(t=>t.team_id)).size,12);
 assert.equal(p.coverage.length,12);
 for(const x of p.appearances){
  assert.ok(x.character_id && x.last_verified_location && x.travel_status && x.knowledge_cutoff && x.reason);
  if(x.mode==='IN_PERSON')assert.equal(x.travel_status,'ROUTE_VERIFIED');
  if(x.last_verified_location==='UNKNOWN')assert.notEqual(x.mode,'IN_PERSON');
 }
 for(const c of p.claims)assert.ok(c.source_ref && c.as_of && ['VERIFIED','EDITORIAL','FICTIONAL_PROPOSAL','FORECAST'].includes(c.classification));
 assert.ok(p.future_threads.every(t=>t.status==='PROPOSED' || t.status==='UNKNOWN'));
 return p;
};
if(require.main===module){const p=load('productions/after-dark/fixtures/p3c_llc_episode.json');validate(p);const invalid=structuredClone(p);invalid.appearances.push({character_id:'CHAR-DAVID-BABB',last_verified_location:'UNKNOWN',mode:'IN_PERSON',travel_status:'UNVERIFIED',knowledge_cutoff:p.story_cutoff,reason:'interview'});assert.throws(()=>validate(invalid));console.log('P3C narrative contract: 2/2 fixtures PASS (positive and blocked teleport).');}
module.exports={validate};
