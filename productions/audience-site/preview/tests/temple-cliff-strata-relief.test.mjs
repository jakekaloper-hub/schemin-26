import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=source.locations.find(entry=>entry.id===id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const before=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const cliffs=a=>a.locations.find(l=>l.id===ids[0]).group.children
  .filter(o=>o.name==='Candidate Temple cliff strata relief');

test('Temple cliffs keep three original stone envelopes, material identities, and source location',()=>{
  const canonical=source.locations.find(l=>l.id===ids[0]),a=build(),c=cliffs(a);
  assert.equal(canonical.canon_status,'PERMANENT_CANON');
  assert.ok(canonical.persistent_landmarks.includes('waterfall'));
  assert.equal(c.length,3,'only the three existing cliff rocks');
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  const old=[
    {pos:[-6,3,-3],scale:[4,6,3],color:'677163'},
    {pos:[-8,2,-4],scale:[3.6,4.8,3.2],color:'777b6a'},
    {pos:[-5,1,-5],scale:[4,4,3.6],color:'596955'}
  ];
  c.forEach((o,i)=>{
    assert.deepEqual(o.position.toArray(),old[i].pos);
    assert.deepEqual(o.scale.toArray(),old[i].scale);
    assert.equal(o.rotation.x,.19+old[i].pos[0]*.07);
    assert.equal(o.rotation.y,old[i].pos[2]*.16);
    assert.equal(o.rotation.z,.1);
    assert.equal(o.material.color.getHexString(),old[i].color);
    assert.equal(o.userData.originalCliffIndex,i);
    assert.deepEqual(o.userData.originalDimensions,old[i].scale);
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.sourceLandmark,'waterfall');
    assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);
    assert.equal(o.geometry.type,'IcosahedronGeometry');
    assert.equal(o.geometry.parameters.detail,4);
  });
  for(const other of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(other.group.children.filter(o=>o.name==='Candidate Temple cliff strata relief').length,0);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();
});

test('Physical cliff strata are inward-only, visibly nonflat, deterministic and vertex-budgeted',()=>{
  const a=build(),b=build(),c=cliffs(a),d=cliffs(b);
  for(let k=0;k<3;k++){
    const geo=c[k].geometry,p=geo.getAttribute('position'),normal=geo.getAttribute('normal');
    assert.ok(p.count>900&&p.count<1900,'bounded static cliff tessellation');
    assert.deepEqual(p.array,d[k].geometry.getAttribute('position').array,'deterministic relief');
    assert.ok(geo.boundingSphere.radius<=1.000001,'original enclosing unit-sphere bound');
    let min=Infinity,max=0,seams=0;
    for(let i=0;i<p.count;i++){
      const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
      const r=Math.hypot(x,y,z);
      assert.ok([x,y,z,normal.getX(i),normal.getY(i),normal.getZ(i)].every(Number.isFinite));
      assert.ok(r>.92&&r<=1.000001,'only bounded inward sculpting');
      min=Math.min(min,r);max=Math.max(max,r);
      if(r<.947)seams++;
    }
    assert.ok(max-min>.03,'different physical rock strata depths');
    assert.ok(seams>20,'actual recessed bands, not just a material change');
  }
  a.dispose();b.dispose();
  assert.equal(JSON.stringify(bindings),before);
});

test('Cliff geometry remains static while ordinary water advances during global calm and disposes once',()=>{
  const a=build(),c=cliffs(a),vertices=c.map(o=>o.geometry.getAttribute('position').array.slice());
  assert.deepEqual(a.water.map(w=>w.kind),
    ['river','waterfall','landing-ripple','landing-ripple','landing-ripple','landing-ripple','pool','swamp','channel','pond']);
  a.tick(2.5,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2.5));
  a.tick(5.3,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.3));
  a.tick(9,{globalCalm:true,storm:6,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.3));
  a.tick(11,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===11));
  c.forEach((o,i)=>assert.deepEqual(o.geometry.getAttribute('position').array,vertices[i]));
  let geoDisposals=0,materialDisposals=0;
  c[0].geometry.addEventListener('dispose',()=>geoDisposals++);
  c[0].material.addEventListener('dispose',()=>materialDisposals++);
  a.dispose();a.dispose();a.tick(13);
  assert.equal(geoDisposals,1);assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(bindings),before);
});
