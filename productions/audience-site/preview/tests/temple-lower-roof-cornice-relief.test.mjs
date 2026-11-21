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
  assert.ok(site,'Source Atlas location absent: '+id);
  return {id,anchor:[site.abstract_position[0],0,site.abstract_position[1]],
    canonStatus:site.canon_status,landmarks:site.persistent_landmarks};
});
const originalAtlas=JSON.stringify(atlas),originalBindings=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const temple=a=>a.locations.find(l=>l.id===ids[0]).group;
const cornice=a=>temple(a).children.filter(o=>o.name==='Candidate Temple recessed lower roof cornice');
const near=(v,w)=>assert.ok(Math.abs(v-w)<=1e-5,'Changed original location/roof envelope');

test('Inherited Temple lower roof is one candidate mesh at its original position with original source identity',()=>{
  const source=atlas.locations.find(p=>p.id===ids[0]),a=build(),group=temple(a);
  assert.equal(source.canon_status,'PERMANENT_CANON');
  assert.ok(source.persistent_landmarks.includes('temple stone'));
  assert.deepEqual(a.locations.map(p=>p.id),ids);
  assert.equal(group.userData.locationId,ids[0]);
  const list=cornice(a);assert.equal(list.length,1);
  const roof=list[0];
  near(roof.position.x,1);near(roof.position.y,5.7);near(roof.position.z,-.1);
  assert.deepEqual(roof.scale.toArray(),[1,1,1]);
  assert.deepEqual(roof.userData.originalDimensions,[6.7,.4,5]);
  assert.equal(roof.userData.originalPerimeterPreserved,true);
  assert.equal(roof.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(roof.userData.sourceLandmark,'temple stone');
  assert.equal(roof.userData.navigable,false);
  assert.deepEqual(roof.userData.routeIds,[]);
  assert.deepEqual(roof.userData.principalCharacters,[]);
  assert.equal(roof.material.color.getHexString(),'ddd2a6','Inherit edge-stone material');
  assert.equal(group.children.filter(o=>o.geometry?.type==='BoxGeometry'&&
    o.geometry.parameters.width===6.1&&o.geometry.parameters.height===.32&&
    o.geometry.parameters.depth===4.5).length,1,'Upper roof tier retained');
  assert.equal(group.children.filter(o=>o.geometry?.type==='BoxGeometry'&&
    o.geometry.parameters.width===5.2&&o.geometry.parameters.height===.3&&
    o.geometry.parameters.depth===3.9).length,1,'Top roof tier retained');
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple recessed entrance door panels').length,1);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple recessed entrance masonry').length,1);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple seamed stepped tier').length,4);
  assert.equal(group.children.filter(o=>o.name==='Candidate Temple fluted stone pillar').length,5);
  for(const other of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(other.group.getObjectByName(roof.name),undefined);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),originalAtlas);
  assert.equal(JSON.stringify(bindings),originalBindings);
  a.dispose();
});

test('Physical recesses are deterministic, bounded and restricted to original vertical faces, preserving every rim',()=>{
  const a=build(),b=build(),o=cornice(a)[0],again=cornice(b)[0];
  const baseline=new THREE.BoxGeometry(6.7,.4,5,40,8,32);
  const old=baseline.getAttribute('position'),p=o.geometry.getAttribute('position');
  const normals=o.geometry.getAttribute('normal');
  assert.equal(o.geometry.type,'BoxGeometry');
  assert.deepEqual([o.geometry.parameters.width,o.geometry.parameters.height,o.geometry.parameters.depth],[6.7,.4,5]);
  assert.deepEqual([o.geometry.parameters.widthSegments,o.geometry.parameters.heightSegments,
    o.geometry.parameters.depthSegments],[40,8,32]);
  assert.equal(p.count,old.count);
  assert.ok(p.count<4500,'Bounded static tessellation');
  assert.deepEqual(p.array,again.geometry.getAttribute('position').array,'Repeatable geometry');
  let frontCuts=0,sideCuts=0,outer=0,maxInset=0;
  for(let i=0;i<p.count;i++){
    const x=old.getX(i),y=old.getY(i),z=old.getZ(i);
    const xx=p.getX(i),yy=p.getY(i),zz=p.getZ(i);
    assert.ok([xx,yy,zz,normals.getX(i),normals.getY(i),normals.getZ(i)].every(Number.isFinite));
    near(yy,y);
    const front=Math.abs(Math.abs(z)-2.5)<1e-6&&Math.abs(x)<3.35-1e-6&&Math.abs(y)<.2-1e-6;
    const side=Math.abs(Math.abs(x)-3.35)<1e-6&&Math.abs(z)<2.5-1e-6&&Math.abs(y)<.2-1e-6;
    let inset=0;
    if(front){
      near(xx,x);assert.equal(Math.sign(zz),Math.sign(z));
      inset=Math.abs(z)-Math.abs(zz);
      if(inset>.012)frontCuts++;
    }else if(side){
      near(zz,z);assert.equal(Math.sign(xx),Math.sign(x));
      inset=Math.abs(x)-Math.abs(xx);
      if(inset>.012)sideCuts++;
    }else{
      near(xx,x);near(zz,z);outer++;
    }
    assert.ok(inset>=-1e-6&&inset<=.03601,'Inward-only incision');
    maxInset=Math.max(maxInset,inset);
  }
  assert.ok(frontCuts>30,'Visible physical front/back recesses');
  assert.ok(sideCuts>20,'Visible physical side recesses');
  assert.ok(outer>2500,'All upper/bottom planes, corners and exterior edges unchanged');
  assert.ok(maxInset>.027&&maxInset<=.03601,'Restrained physical relief, no expansion');
  o.geometry.computeBoundingBox();const bounds=o.geometry.boundingBox;
  for(const [actual,expected] of [[bounds.min.x,-3.35],[bounds.max.x,3.35],
    [bounds.min.y,-.2],[bounds.max.y,.2],[bounds.min.z,-2.5],[bounds.max.z,2.5]])
    near(actual,expected);
  baseline.dispose();a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),originalAtlas);
});

test('Existing opaque batching, independent water under global calm, pause and once-only disposal survive',()=>{
  const a=build(),roof=cornice(a)[0],group=temple(a);
  const beforeCount=group.children.length;
  const batch=batchStaticGeometry(THREE,group);
  assert.ok(group.children.length>0&&group.children.length<beforeCount,
    'Existing static batching intentionally folds original meshes into fewer GPU objects');
  assert.ok(batch.geometries.length>0,'Existing opaque geometry can be batched');
  for(const geo of batch.geometries)geo.dispose();
  const water=a.water.filter(w=>['river','waterfall','pool','swamp','channel','pond'].includes(w.kind));
  assert.equal(water.length,6);
  let geometryDisposals=0,materialDisposals=0;
  roof.geometry.addEventListener('dispose',()=>geometryDisposals++);
  roof.material.addEventListener('dispose',()=>materialDisposals++);
  a.tick(2,{globalCalm:true,storm:0});
  a.tick(6,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(11,{globalCalm:true,storm:5,paused:true});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(14,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===14));
  a.dispose();a.dispose();a.tick(22);
  assert.equal(geometryDisposals,1);
  assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(atlas),originalAtlas);
  assert.equal(JSON.stringify(bindings),originalBindings);
});
