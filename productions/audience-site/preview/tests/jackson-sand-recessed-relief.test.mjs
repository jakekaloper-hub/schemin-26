import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(s=>s.id===id);
  assert.ok(p,'Missing source-defined location: '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const sourceBefore=JSON.stringify(atlas),bindingsBefore=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const estate=a=>a.locations.find(l=>l.id===ids[2]).group;
const sands=a=>estate(a).children.filter(o=>o.userData.estateSandPart==='recessed-original-disc');
const near=(actual,expected,tol=1e-5)=>
  assert.ok(Math.abs(actual-expected)<=tol,'Expected '+expected+' got '+actual);

test('Both existing Jackson sand discs preserve source identity, transforms, material and unresolved Week 3 cleanup',()=>{
  const a=build(),s=sands(a),record=atlas.locations.find(l=>l.id===ids[2]);
  assert.equal(atlas.locations.length,23);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(record.canon_status,'PERMANENT_CANON');
  assert.ok(record.persistent_landmarks.includes('clubhouse'));
  assert.ok(record.current_state.some(x=>x.includes('chili contamination')));
  assert.ok(record.current_state.some(x=>x.includes('cleanup state')));
  assert.equal(estate(a).userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(s.length,2);
  for(let i=0;i<2;i++){
    const o=s[i],coords=[[-6,6],[3,9]][i];
    assert.deepEqual(o.position.toArray(),[coords[0],.03,coords[1]]);
    assert.deepEqual(o.scale.toArray(),[1.3,.6,1]);
    near(o.rotation.x,-Math.PI/2);
    assert.equal(o.material,s[0].material);
    assert.equal(o.geometry.name,'Candidate Jackson recessed sand surface');
    assert.deepEqual(o.userData.originalCoordinates,coords);
    assert.equal(o.userData.originalRadius,1);
    assert.equal(o.userData.originalSegments,20);
    assert.equal(o.userData.sourceLandmark,'golf grounds');
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.navigable,false);
    assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);
    assert.equal(o.children.length,0);
  }
  for(const l of a.locations.filter(l=>l.id!==ids[2]))
    assert.equal(l.group.children.filter(o=>o.userData.estateSandPart).length,0);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  a.dispose();
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});

test('Deterministic physical sand relief is inward only, keeps 20 exact perimeter points and finite normals',()=>{
  const a=build(),b=build(),s=sands(a),other=sands(b);
  for(let j=0;j<2;j++){
    const g=s[j].geometry,p=g.getAttribute('position'),uv=g.getAttribute('uv'),
      normal=g.getAttribute('normal');
    assert.equal(g.type,'CircleGeometry');
    assert.equal(g.parameters.radius,1);
    assert.equal(g.parameters.segments,20);
    assert.deepEqual(p.array,other[j].geometry.getAttribute('position').array);
    assert.equal(p.count,161);
    assert.equal(uv.count,p.count);
    assert.equal(normal.count,p.count);
    assert.equal(g.getIndex().count,900);
    near(p.getX(0),0);near(p.getY(0),0);near(p.getZ(0),-.024);
    let indented=0,flatBorder=0;
    for(let i=0;i<p.count;i++){
      const x=p.getX(i),y=p.getY(i),z=p.getZ(i),r=Math.hypot(x,y);
      assert.ok([x,y,z,normal.getX(i),normal.getY(i),normal.getZ(i)].every(Number.isFinite));
      assert.ok(r<=1+1e-6,'Original unit-disc perimeter not exceeded');
      assert.ok(z<=1e-6&&z>=-.0241,'No upward growth / deeper-than-candidate recess');
      assert.ok(normal.getZ(i)>.6,'Water-facing surface normals stay oriented');
      if(i>=141){
        const k=i-141;
        near(x,Math.cos(k*2*Math.PI/20));
        near(y,Math.sin(k*2*Math.PI/20));
        near(z,0);
        flatBorder++;
      }else if(z<-.001)indented++;
    }
    assert.equal(flatBorder,20);
    assert.ok(indented>100,'Physical interior recess, not a flat shader effect');
    g.computeBoundingBox();
    near(g.boundingBox.min.x,-1);
    near(g.boundingBox.max.x,1);
    assert.ok(g.boundingBox.min.z>=-.0241);
    near(g.boundingBox.max.z,0);
  }
  a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),sourceBefore);
});

test('No extra drawables; inherited batching, calm-water animation, pause and once-only disposal remain',()=>{
  const a=build(),g=estate(a),s=sands(a),count=g.children.length;
  let geoDisposals=0,materialDisposals=0;
  s[0].geometry.addEventListener('dispose',()=>geoDisposals++);
  s[0].material.addEventListener('dispose',()=>materialDisposals++);
  const batch=batchStaticGeometry(THREE,g);
  assert.ok(g.children.length<count,'Inherited static batcher still compacts drawables');
  for(const geo of batch.geometries)geo.dispose();
  assert.deepEqual(a.water.map(w=>w.kind),[
    'river','waterfall','landing-ripple','landing-ripple',
    'landing-ripple','landing-ripple','pool','swamp','channel','pond']);
  a.tick(3,{globalCalm:true,storm:0});
  a.tick(12,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===12));
  a.tick(19,{globalCalm:true,storm:9,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===12));
  a.tick(23,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===23));
  a.dispose();a.dispose();a.tick(25);
  assert.equal(geoDisposals,1);
  assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});
