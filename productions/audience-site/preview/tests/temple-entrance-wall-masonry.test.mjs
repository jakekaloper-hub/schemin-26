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
  assert.ok(site,'Missing source location '+id);
  return {id,anchor:[site.abstract_position[0],0,site.abstract_position[1]],
    canonStatus:site.canon_status,landmarks:site.persistent_landmarks};
});
const originalSource=JSON.stringify(atlas),originalBindings=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const temple=a=>a.locations.find(p=>p.id===ids[0]).group;
const walls=a=>temple(a).children.filter(o=>o.name==='Candidate Temple recessed entrance masonry');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,'Original surface boundary or placement changed');

test('Temple preserves its one existing entrance hall, door, tiers, pillar caps and source-bound identity',()=>{
  const site=atlas.locations.find(p=>p.id===ids[0]),a=build(),group=temple(a),list=walls(a);
  assert.equal(site.canon_status,'PERMANENT_CANON');
  assert.ok(site.persistent_landmarks.includes('temple stone'));
  assert.deepEqual(a.locations.map(p=>p.id),ids);
  assert.equal(list.length,1,'No new hall or second facades');
  const wall=list[0];
  assert.deepEqual(wall.position.toArray(),[1,3.7,-1]);
  assert.deepEqual(wall.scale.toArray(),[1,1,1]);
  assert.deepEqual(wall.userData.originalDimensions,[5.2,2.8,3.6]);
  assert.equal(wall.userData.originalPerimeterPreserved,true);
  assert.equal(wall.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(wall.userData.sourceLandmark,'temple stone');
  assert.equal(wall.userData.navigable,false);
  assert.deepEqual(wall.userData.routeIds,[]);
  assert.deepEqual(wall.userData.principalCharacters,[]);
  assert.equal(wall.material.color.getHexString(),'54604a','Original dark-stone material');
  assert.equal(wall.geometry.type,'BoxGeometry');
  assert.deepEqual([wall.geometry.parameters.width,wall.geometry.parameters.height,
    wall.geometry.parameters.depth],[5.2,2.8,3.6]);
  assert.deepEqual([wall.geometry.parameters.widthSegments,wall.geometry.parameters.heightSegments,
    wall.geometry.parameters.depthSegments],[32,24,20]);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple seamed stepped tier').length,4);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple fluted stone pillar').length,5);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple stone tread relief').length,9);
  assert.equal(group.children.filter(o=>o.geometry?.type==='BoxGeometry'&&
    o.geometry.parameters.width===1.25&&o.geometry.parameters.height===2.3&&
    o.geometry.parameters.depth===.15).length,1,'Original entrance remains');
  assert.equal(group.children.filter(o=>o.geometry?.type==='BoxGeometry'&&
    o.geometry.parameters.width===.7&&o.geometry.parameters.height===.22&&
    o.geometry.parameters.depth===.65).length,5,'Original five capitals remain');
  for(const l of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(l.group.getObjectByName('Candidate Temple recessed entrance masonry'),undefined);
  assert.equal(group.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),originalSource);
  assert.equal(JSON.stringify(bindings),originalBindings);
  a.dispose();
});

test('Deterministic physical mortar relief is inward-only; top, bottom, corner edges and inherited bounds stay fixed',()=>{
  const a=build(),b=build(),w=walls(a)[0],v=walls(b)[0];
  const baseline=new THREE.BoxGeometry(5.2,2.8,3.6,32,24,20);
  const old=baseline.getAttribute('position'),p=w.geometry.getAttribute('position');
  const normals=w.geometry.getAttribute('normal');
  assert.equal(p.count,old.count);
  assert.ok(p.count<5000,'Bounded surface tessellation rather than a second asset');
  assert.deepEqual(p.array,v.geometry.getAttribute('position').array);
  let incised=0,strong=0,maxInset=0,outer=0;
  for(let i=0;i<p.count;i++){
    const x=old.getX(i),y=old.getY(i),z=old.getZ(i);
    const xx=p.getX(i),yy=p.getY(i),zz=p.getZ(i);
    assert.ok([xx,yy,zz,normals.getX(i),normals.getY(i),normals.getZ(i)].every(Number.isFinite));
    near(yy,y);
    const front=Math.abs(Math.abs(z)-1.8)<1e-6&&Math.abs(x)<2.6-1e-6&&Math.abs(y)<1.4-1e-6;
    const side=Math.abs(Math.abs(x)-2.6)<1e-6&&Math.abs(z)<1.8-1e-6&&Math.abs(y)<1.4-1e-6;
    let inset=0;
    if(front){near(xx,x);assert.equal(Math.sign(zz),Math.sign(z));inset=Math.abs(z)-Math.abs(zz);}
    else if(side){near(zz,z);assert.equal(Math.sign(xx),Math.sign(x));inset=Math.abs(x)-Math.abs(xx);}
    else{near(xx,x);near(zz,z);outer++;}
    assert.ok(inset>=-1e-6&&inset<=.03401,'Masonry never protrudes beyond original wall');
    if(inset>.002)incised++;
    if(inset>.009)strong++;
    maxInset=Math.max(maxInset,inset);
  }
  assert.ok(incised>300&&strong>250,'Physical joints cover existing faces');
  assert.ok(maxInset>.025&&maxInset<=.03401,'Shallow masonry incisions');
  assert.ok(outer>500,'Untouched inherited exterior edges, top, bottom');
  w.geometry.computeBoundingBox();
  const bounds=w.geometry.boundingBox;
  for(const [actual,expected] of [[bounds.min.x,-2.6],[bounds.max.x,2.6],
    [bounds.min.y,-1.4],[bounds.max.y,1.4],[bounds.min.z,-1.8],[bounds.max.z,1.8]])
    near(actual,expected);
  baseline.dispose();a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),originalSource);
});

test('Original opaque material batching, water-in-calm, explicit pause and once-only disposal survive',()=>{
  const a=build(),wall=walls(a)[0],group=temple(a);
  const batch=batchStaticGeometry(THREE,group);
  assert.equal(group.children.filter(o=>o.isMesh&&o.material===wall.material).length,1,
    'Existing dark stone material remains one opaque batch');
  for(const geometry of batch.geometries)geometry.dispose();
  const water=a.water.filter(w=>['river','waterfall','pool','swamp','channel','pond'].includes(w.kind));
  assert.equal(water.length,6);
  let geometryDisposals=0,materialDisposals=0;
  wall.geometry.addEventListener('dispose',()=>geometryDisposals++);
  wall.material.addEventListener('dispose',()=>materialDisposals++);
  a.tick(2,{globalCalm:true,storm:0});
  a.tick(6,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(11,{globalCalm:true,storm:6,paused:true});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(14,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===14));
  a.dispose();a.dispose();a.tick(20);
  assert.equal(geometryDisposals,1);
  assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(bindings),originalBindings);
  assert.equal(JSON.stringify(atlas),originalSource);
});
