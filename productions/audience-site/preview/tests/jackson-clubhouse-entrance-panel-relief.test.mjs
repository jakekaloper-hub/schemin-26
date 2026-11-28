import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const place=atlas.locations.find(p=>p.id===id);
  assert.ok(place,'Missing canonical location '+id);
  return {id,anchor:[place.abstract_position[0],0,place.abstract_position[1]],
    canonStatus:place.canon_status,landmarks:place.persistent_landmarks};
});
const before=JSON.stringify(atlas),bindingsBefore=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const estate=a=>a.locations.find(l=>l.id===ids[2]).group;
const doors=a=>estate(a).children.filter(o=>o.userData.estateDoorPart==='panel-relief');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,`Expected ${b}, got ${a}`);

test('Inherited Jackson entrance remains one source-bound, non-navigable original-material box',()=>{
  const a=build(),source=atlas.locations.find(l=>l.id===ids[2]),g=estate(a),d=doors(a);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(source.canon_status,'PERMANENT_CANON');
  assert.ok(source.persistent_landmarks.includes('clubhouse'));
  assert.ok(source.current_state.some(s=>s.includes('chili contamination')));
  assert.ok(source.current_state.some(s=>s.includes('cleanup state')));
  assert.equal(g.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(d.length,1);
  const o=d[0];
  assert.deepEqual(o.position.toArray(),[0,1.35,2.14]);
  assert.deepEqual(o.scale.toArray(),[1,1,1]);
  assert.deepEqual(o.userData.originalDimensions,[.9,1.9,.05]);
  assert.equal(o.userData.originalPerimeterPreserved,true);
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(o.userData.sourceLandmark,'clubhouse');
  assert.equal(o.userData.navigable,false);
  assert.deepEqual(o.userData.routeIds,[]);
  assert.deepEqual(o.userData.principalCharacters,[]);
  assert.equal(o.material.color.getHexString(),'45605b');
  assert.equal(o.geometry.type,'BoxGeometry');
  assert.deepEqual([o.geometry.parameters.width,o.geometry.parameters.height,o.geometry.parameters.depth],
    [.9,1.9,.05]);
  assert.deepEqual([o.geometry.parameters.widthSegments,o.geometry.parameters.heightSegments,
    o.geometry.parameters.depthSegments],[48,48,1]);
  assert.equal(o.children.length,0);
  for(const other of a.locations.filter(l=>l.id!==ids[2]))
    assert.equal(other.group.getObjectByName(o.name),undefined);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  a.dispose();
  assert.equal(JSON.stringify(atlas),before);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});

test('Four finite physical inset panels preserve the exact inherited front rim, sides, back, and bounds',()=>{
  const a=build(),b=build(),o=doors(a)[0],other=doors(b)[0];
  const baseline=new THREE.BoxGeometry(.9,1.9,.05,48,48,1);
  const raw=baseline.getAttribute('position'),p=o.geometry.getAttribute('position');
  const normal=o.geometry.getAttribute('normal');
  assert.equal(p.count,raw.count);
  assert.deepEqual(p.array,other.geometry.getAttribute('position').array);
  assert.ok(p.count<5500,'Finite single box mesh budget');
  let recessed=0,deep=0,peak=0,untouched=0;
  const quadrants=new Set();
  for(let i=0;i<p.count;i++){
    const x=raw.getX(i),y=raw.getY(i),z=raw.getZ(i);
    const xx=p.getX(i),yy=p.getY(i),zz=p.getZ(i);
    assert.ok([xx,yy,zz,normal.getX(i),normal.getY(i),normal.getZ(i)].every(Number.isFinite));
    near(xx,x);near(yy,y);
    const frontInterior=Math.abs(z-.025)<1e-6&&Math.abs(x)<.45-1e-6&&Math.abs(y)<.95-1e-6;
    const inset=z-zz;
    if(!frontInterior){near(inset,0);untouched++;continue;}
    assert.ok(inset>=-1e-6&&inset<=.01801,'No outward material or cut through door');
    if(inset>1e-5)recessed++;
    if(inset>.014){deep++;quadrants.add((x<0?'L':'R')+(y<0?'B':'T'));}
    peak=Math.max(peak,inset);
  }
  assert.ok(untouched>400,'Original perimeter/back/side faces unchanged');
  assert.ok(recessed>500,'Genuine 3D front face rather than material label');
  assert.ok(deep>200,'Sufficient physical panel area');
  assert.deepEqual([...quadrants].sort(),['LB','LT','RB','RT']);
  assert.ok(peak>.0179&&peak<=.01801);
  o.geometry.computeBoundingBox();
  const bb=o.geometry.boundingBox;
  for(const [actual,expected] of [[bb.min.x,-.45],[bb.max.x,.45],
    [bb.min.y,-.95],[bb.max.y,.95],[bb.min.z,-.025],[bb.max.z,.025]])
    near(actual,expected);
  baseline.dispose();a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),before);
});

test('Door remains static-batchable and all six ordinary water clocks advance during synthetic calm',()=>{
  const a=build(),g=estate(a),o=doors(a)[0],count=g.children.length;
  let geoDisposals=0,materialDisposals=0;
  o.geometry.addEventListener('dispose',()=>geoDisposals++);
  o.material.addEventListener('dispose',()=>materialDisposals++);
  const batch=batchStaticGeometry(THREE,g);
  assert.ok(g.children.length<count,'Existing static batcher still compacts site');
  for(const item of batch.geometries)item.dispose();
  assert.equal(a.water.filter(w=>['pond','swamp','channel','river','pool','waterfall'].includes(w.kind)).length,6);
  a.tick(3,{globalCalm:true,storm:0});
  a.tick(11,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===11));
  a.tick(16,{globalCalm:true,storm:8,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===11));
  a.tick(22,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===22));
  a.dispose();a.dispose();a.tick(25);
  assert.equal(geoDisposals,1);
  assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(atlas),before);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});
