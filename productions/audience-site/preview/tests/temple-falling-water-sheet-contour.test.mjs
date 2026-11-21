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
  assert.ok(site,'Missing authority-backed Atlas site '+id);
  return {id,anchor:[site.abstract_position[0],0,site.abstract_position[1]],
    canonStatus:site.canon_status,landmarks:site.persistent_landmarks};
});
const sourceAtlas=JSON.stringify(atlas),sourceBindings=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,`Expected ${a} near ${b}`);
const temple=a=>a.locations.find(l=>l.id===ids[0]).group;
const sheet=a=>a.water.filter(w=>w.kind==='waterfall');

test('Source-backed Temple retains exactly its one original animated waterfall and all inherited boundaries',()=>{
  const source=atlas.locations.find(p=>p.id===ids[0]);
  assert.equal(source.canon_status,'PERMANENT_CANON');
  assert.equal(source.physical_zone_id,'REG-SOUTHERN-WETLANDS');
  assert.ok(source.persistent_landmarks.includes('waterfall'));
  const a=build(),region=temple(a),matches=sheet(a);
  assert.deepEqual(a.locations.map(p=>p.id),ids);
  assert.equal(matches.length,1);
  const flow=matches[0],o=flow.mesh;
  assert.equal(region.children.filter(m=>m===o).length,1,'Same inherited regional water mesh');
  assert.equal(region.children.filter(m=>m.name===o.name).length,1);
  assert.equal(o.name,'Candidate Temple contoured animated waterfall sheet');
  assert.equal(o.geometry.type,'PlaneGeometry');
  assert.deepEqual([o.geometry.parameters.width,o.geometry.parameters.height,
    o.geometry.parameters.widthSegments,o.geometry.parameters.heightSegments],
    [2.15,6.9,24,32]);
  near(o.position.x,-5.8);near(o.position.y,7.2-6.9/2);near(o.position.z,1.8);
  assert.deepEqual(o.scale.toArray(),[1,1,1]);
  assert.deepEqual(o.userData.originalDimensions,[2.15,6.9]);
  assert.equal(o.userData.originalPerimeterPreserved,true);
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(o.userData.sourceLandmark,'waterfall');
  assert.equal(o.userData.navigable,false);
  assert.deepEqual(o.userData.routeIds,[]);
  assert.deepEqual(o.userData.principalCharacters,[]);
  assert.equal(o.material.isShaderMaterial,true);
  assert.equal(o.material.uniforms.uFall.value,1);
  assert.equal(o.material.uniforms.uRiver.value,0);
  assert.equal(o.castShadow,false);assert.equal(o.renderOrder,2);
  for(const other of a.locations.filter(p=>p.id!==ids[0]))
    assert.equal(other.group.getObjectByName(o.name),undefined);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),sourceAtlas);
  assert.equal(JSON.stringify(bindings),sourceBindings);
  a.dispose();
});

test('Original crest, receiving edge, both sides and positions stay fixed; bounded real depth relief and normals repeat',()=>{
  const a=build(),b=build(),o=sheet(a)[0].mesh,again=sheet(b)[0].mesh;
  const base=new THREE.PlaneGeometry(2.15,6.9,24,32);
  const p=o.geometry.getAttribute('position'),p0=base.getAttribute('position'),
    uv=base.getAttribute('uv'),n=o.geometry.getAttribute('normal');
  assert.equal(p.count,p0.count);
  assert.ok(p.count<900,'Existing tessellation budget retained');
  assert.deepEqual(p.array,again.geometry.getAttribute('position').array,'Deterministic candidate geometry');
  let held=0,folded=0,strong=0,maxRelief=0;
  for(let i=0;i<p.count;i++){
    const u=uv.getX(i),v=uv.getY(i),dz=p.getZ(i)-p0.getZ(i);
    near(p.getX(i),p0.getX(i));near(p.getY(i),p0.getY(i));
    assert.ok([dz,n.getX(i),n.getY(i),n.getZ(i)].every(Number.isFinite));
    assert.ok(dz>=-1e-6&&dz<=.17001,'Only bounded inward-scene contour, no new sheet extent');
    if(u<1e-6||u>1-1e-6||v<1e-6||v>1-1e-6){
      near(dz,0);held++;
    }else{
      if(dz>.04)folded++;
      if(dz>.10)strong++;
    }
    maxRelief=Math.max(maxRelief,dz);
    near(Math.hypot(n.getX(i),n.getY(i),n.getZ(i)),1);
  }
  assert.equal(held,2*(25+33)-4,'Entire original perimeter immovable');
  assert.ok(folded>200&&strong>40,'Appreciable interior 3D water contour');
  assert.ok(maxRelief>.14&&maxRelief<.17,'Shallow but substantial hero waterfall depth');
  o.geometry.computeBoundingBox();
  const bounds=o.geometry.boundingBox;
  for(const [actual,expected] of [[bounds.min.x,-1.075],[bounds.max.x,1.075],
    [bounds.min.y,-3.45],[bounds.max.y,3.45],[bounds.min.z,0]])
    near(actual,expected);
  assert.ok(bounds.max.z>.14&&bounds.max.z<.17);
  base.dispose();a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),sourceAtlas);
});

test('Moving sheet survives batching, global El Niño calm, explicit pause and once-only disposal',()=>{
  const a=build(),g=temple(a),o=sheet(a)[0].mesh,originalCount=g.children.length;
  const batch=batchStaticGeometry(THREE,g);
  assert.ok(g.children.length<originalCount,'Opaque static meshes compact');
  assert.ok(g.children.includes(o),'Dynamic waterfall must not enter static batching');
  for(const geometry of batch.geometries)geometry.dispose();
  const moving=a.water.filter(w=>['river','waterfall','pool','swamp','channel','pond'].includes(w.kind));
  assert.equal(moving.length,6);
  let disposed=0,materialDisposals=0;
  o.geometry.addEventListener('dispose',()=>disposed++);
  o.material.addEventListener('dispose',()=>materialDisposals++);
  a.tick(2,{globalCalm:true,storm:0});
  a.tick(8,{globalCalm:true,storm:0});
  assert.ok(moving.every(w=>w.material.uniforms.uTime.value===8));
  a.tick(11,{globalCalm:true,storm:0,paused:true});
  assert.ok(moving.every(w=>w.material.uniforms.uTime.value===8));
  a.tick(16,{globalCalm:true,storm:0});
  assert.ok(moving.every(w=>w.material.uniforms.uTime.value===16));
  a.dispose();a.dispose();a.tick(30);
  assert.equal(disposed,1);assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(atlas),sourceAtlas);
  assert.equal(JSON.stringify(bindings),sourceBindings);
});
