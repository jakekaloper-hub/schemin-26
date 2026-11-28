import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const site=atlas.locations.find(p=>p.id===id);
  assert.ok(site,'Missing canonical Atlas location '+id);
  return {id,anchor:[site.abstract_position[0],0,site.abstract_position[1]],
    canonStatus:site.canon_status,landmarks:site.persistent_landmarks};
});
const sourceBefore=JSON.stringify(atlas),bindingsBefore=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const temple=a=>a.locations.find(p=>p.id===ids[0]).group;
const doors=a=>temple(a).children.filter(o=>o.name==='Candidate Temple recessed entrance door panels');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,'Original geometric envelope changed');

test('Inherited Temple door is one unchanged source-bound entrance, with no new site, route or canon write',()=>{
  const a=build(),site=atlas.locations.find(p=>p.id===ids[0]),group=temple(a),list=doors(a);
  assert.equal(site.canon_status,'PERMANENT_CANON');
  assert.ok(site.persistent_landmarks.includes('temple stone'));
  assert.deepEqual(a.locations.map(p=>p.id),ids);
  assert.equal(list.length,1,'Do not add a second entrance');
  const door=list[0];
  near(door.position.x,1);near(door.position.y,2.32+2.3/2);near(door.position.z,1.02);
  assert.deepEqual(door.scale.toArray(),[1,1,1]);
  assert.deepEqual(door.userData.originalDimensions,[1.25,2.3,.15]);
  assert.equal(door.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(door.userData.sourceLandmark,'temple stone');
  assert.equal(door.userData.originalPerimeterPreserved,true);
  assert.equal(door.userData.navigable,false);
  assert.deepEqual(door.userData.routeIds,[]);
  assert.deepEqual(door.userData.principalCharacters,[]);
  assert.equal(door.material.color.getHexString(),'263c35','Original door color/material');
  assert.equal(door.geometry.type,'BoxGeometry');
  assert.deepEqual([door.geometry.parameters.width,door.geometry.parameters.height,
    door.geometry.parameters.depth],[1.25,2.3,.15]);
  assert.deepEqual([door.geometry.parameters.widthSegments,door.geometry.parameters.heightSegments,
    door.geometry.parameters.depthSegments],[40,48,1]);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple recessed entrance masonry').length,1);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple seamed stepped tier').length,4);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple fluted stone pillar').length,5);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple stone tread relief').length,9);
  assert.equal(group.children.filter(o=>o.isMesh&&o.geometry?.parameters?.width===1.25&&
    o.geometry?.parameters?.height===2.3&&o.geometry?.parameters?.depth===.15).length,1);
  for(const l of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(l.group.getObjectByName(door.name),undefined);
  assert.equal(group.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
  a.dispose();
});

test('Four physical door-panel recesses are deterministic, front-only, inward and strictly within original bounds',()=>{
  const a=build(),b=build(),door=doors(a)[0],second=doors(b)[0];
  const base=new THREE.BoxGeometry(1.25,2.3,.15,40,48,1);
  const original=base.getAttribute('position'),p=door.geometry.getAttribute('position');
  const normal=door.geometry.getAttribute('normal');
  assert.equal(p.count,original.count);
  assert.ok(p.count<6000,'Finite tessellation and unchanged single mesh');
  assert.deepEqual(p.array,second.geometry.getAttribute('position').array);
  let deep=0,maxInset=0,untouched=0;
  const quadrants=new Set();
  for(let i=0;i<p.count;i++){
    const x=original.getX(i),y=original.getY(i),z=original.getZ(i);
    const xx=p.getX(i),yy=p.getY(i),zz=p.getZ(i);
    assert.ok([xx,yy,zz,normal.getX(i),normal.getY(i),normal.getZ(i)].every(Number.isFinite));
    near(xx,x);near(yy,y);
    const interior=Math.abs(z-.075)<1e-6&&Math.abs(x)<.625-1e-6&&Math.abs(y)<1.15-1e-6;
    const inset=z-zz;
    if(!interior){near(zz,z);untouched++;continue;}
    assert.ok(inset>=-1e-6&&inset<=.02701,'Only inward, bounded carving');
    if(inset>.015){
      deep++;
      quadrants.add((x<0?'L':'R')+(y<0?'B':'T'));
    }
    maxInset=Math.max(maxInset,inset);
  }
  assert.deepEqual([...quadrants].sort(),['LB','LT','RB','RT'],'Four actual panel sections');
  assert.ok(deep>350,'Substantial physical panel face relief');
  assert.ok(maxInset>.026&&maxInset<=.02701,'Carving has physical depth');
  assert.ok(untouched>2200,'Inherited back, sides, upper/lower and perimeter untouched');
  door.geometry.computeBoundingBox();
  const bb=door.geometry.boundingBox;
  for(const [actual,expected] of [[bb.min.x,-.625],[bb.max.x,.625],
    [bb.min.y,-1.15],[bb.max.y,1.15],[bb.min.z,-.075],[bb.max.z,.075]])
    near(actual,expected);
  base.dispose();a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),sourceBefore);
});

test('Original static batch, water motion in global calm, explicit pause and once-only disposal remain',()=>{
  const a=build(),door=doors(a)[0],group=temple(a);
  const batched=batchStaticGeometry(THREE,group);
  assert.equal(group.children.filter(o=>o.isMesh&&o.material===door.material).length,1,
    'Existing opaque door material has one mesh');
  for(const geo of batched.geometries)geo.dispose();
  const water=a.water.filter(w=>['river','waterfall','pool','swamp','channel','pond'].includes(w.kind));
  assert.equal(water.length,6);
  let geometryDisposals=0,materialDisposals=0;
  door.geometry.addEventListener('dispose',()=>geometryDisposals++);
  door.material.addEventListener('dispose',()=>materialDisposals++);
  a.tick(2,{globalCalm:true,storm:0});
  a.tick(7,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===7));
  a.tick(11,{globalCalm:true,storm:6,paused:true});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===7));
  a.tick(15,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===15));
  a.dispose();a.dispose();a.tick(20);
  assert.equal(geometryDisposals,1);
  assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});
