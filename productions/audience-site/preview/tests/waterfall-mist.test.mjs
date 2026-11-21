import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const locations=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,locations,()=>2);
const effect=a=>a.locations.find(l=>l.id==='LOC-TDS-WATERFALL-TEMPLE').group.getObjectByName('Candidate waterfall plunge mist');

test('Temple receives one source-local, soft-edge mist draw bound to the existing waterfall plunge',()=>{
 const assets=build(),mist=effect(assets);
 assert.ok(mist?.isPoints,'the real waterfall needs a single-draw localized mist layer');
 assert.equal(mist.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(mist.userData.sourceLandmark,'waterfall');
 assert.equal(mist.userData.navigable,false);
 assert.deepEqual(mist.userData.routeIds,[]);
 const p=mist.geometry.getAttribute('position'),phase=mist.geometry.getAttribute('aPhase'),drift=mist.geometry.getAttribute('aDrift');
 assert.ok(p.count>=100&&p.count<=220,'limit mist count / draw cost');
 assert.equal(phase.count,p.count);assert.equal(drift.count,p.count);
 for(let i=0;i<p.count;i++){
  assert.ok(p.getX(i)>-7.65&&p.getX(i)<-3.95,'must stay close to the existing waterfall x=-5.8');
  assert.ok(p.getY(i)>=.18&&p.getY(i)<1.3,'initial spray originates at the existing plunge, not a new watercourse');
  assert.ok(p.getZ(i)>1.5&&p.getZ(i)<4.4,'local spray only, no scene-wide fog');
  assert.ok(phase.getX(i)>=0&&phase.getX(i)<=1);
 }
 assert.ok(mist.material.isShaderMaterial);
 assert.equal(mist.material.transparent,true);
 assert.equal(mist.material.depthWrite,false);
 assert.ok(mist.material.vertexShader.includes('uTime'));
 assert.ok(mist.material.fragmentShader.includes('gl_PointCoord'));
 assert.ok(mist.material.fragmentShader.includes('smoothstep'),'each particle needs a soft radial fade');
 assert.equal(assets.root.getObjectsByProperty('name','Candidate waterfall plunge mist').length,1);
 assets.dispose();
});

test('Temple mist is absent from other owners and never promotes location, history or principal characters',()=>{
 const before=JSON.stringify(locations),assets=build();
 assert.deepEqual(assets.locations.map(l=>l.id),locations.map(l=>l.id));
 assert.equal(assets.worldMutationAllowed,false);assert.deepEqual(assets.principalCharacters,[]);
 for(const l of assets.locations.filter(l=>l.id!=='LOC-TDS-WATERFALL-TEMPLE'))
  assert.equal(l.group.getObjectByName('Candidate waterfall plunge mist'),undefined);
 assert.equal(JSON.stringify(locations),before);
 assets.dispose();
});

test('Plunge mist advances alongside waterfall under El Niño calm and holds on explicit pause',()=>{
 const assets=build(),mist=effect(assets),fall=assets.water.find(w=>w.kind==='waterfall');
 assert.ok(mist?.material.uniforms.uTime);
 assets.tick(2,{storm:0});
 assert.equal(mist.material.uniforms.uTime.value,2);assert.equal(fall.material.uniforms.uTime.value,2);
 assets.tick(4,{storm:0});
 assert.equal(mist.material.uniforms.uTime.value,4);assert.equal(fall.material.uniforms.uTime.value,4);
 assets.tick(9,{storm:0,paused:true});
 assert.equal(mist.material.uniforms.uTime.value,4);assert.equal(fall.material.uniforms.uTime.value,4);
 assets.dispose();assets.dispose();
});
