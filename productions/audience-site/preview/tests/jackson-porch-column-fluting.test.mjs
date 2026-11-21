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
  assert.ok(p,'Source location missing: '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const sourceBefore=JSON.stringify(atlas),bindingsBefore=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const estate=a=>a.locations.find(l=>l.id===ids[2]).group;
const columns=a=>estate(a).children.filter(o=>o.userData.estatePorchPart==='shaft-fluting');
const near=(actual,expected,tolerance=1e-5)=>
  assert.ok(Math.abs(actual-expected)<=tolerance,`expected ${expected}, got ${actual}`);

test('Six inherited source-bound Jackson porch supports preserve positions, octagons, material and site state',()=>{
  const a=build(),c=columns(a),record=atlas.locations.find(l=>l.id===ids[2]);
  assert.equal(atlas.locations.length,23);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(record.canon_status,'PERMANENT_CANON');
  assert.ok(record.persistent_landmarks.includes('clubhouse'));
  assert.ok(record.current_state.some(x=>x.includes('chili contamination')));
  assert.ok(record.current_state.some(x=>x.includes('cleanup state')));
  assert.equal(estate(a).userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(c.length,6);
  for(let i=0;i<c.length;i++){
    const o=c[i];
    near(o.position.x,-4+i*1.34);
    assert.deepEqual(o.position.toArray().slice(1),[.37+2.3/2,3.6]);
    assert.equal(o.material,c[0].material);
    assert.equal(o.material.color.getHexString(),'e4d8b3');
    assert.deepEqual(o.scale.toArray(),[1,1,1]);
    assert.equal(o.geometry.type,'CylinderGeometry');
    assert.deepEqual([o.geometry.parameters.radiusTop,o.geometry.parameters.radiusBottom,
      o.geometry.parameters.height,o.geometry.parameters.radialSegments,
      o.geometry.parameters.heightSegments],[.13,.16,2.3,64,12]);
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.sourceLandmark,'clubhouse');
    assert.deepEqual(o.userData.originalDimensions,[.13,.16,2.3]);
    assert.equal(o.userData.originalSides,8);
    assert.equal(o.userData.originalPerimeterPreserved,true);
    assert.equal(o.userData.navigable,false);
    assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);
    assert.equal(o.children.length,0);
  }
  for(const l of a.locations.filter(l=>l.id!==ids[2]))
    assert.equal(l.group.children.filter(o=>o.userData.estatePorchPart).length,0);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  a.dispose();
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});

test('Real deterministic shaft relief carves inward between all original octagonal corners without changing caps or silhouette',()=>{
  const a=build(),b=build(),c=columns(a),d=columns(b);
  let totalRecess=0,totalCap=0,totalCorner=0;
  for(let j=0;j<c.length;j++){
    const o=c[j],p=o.geometry.getAttribute('position'),
      n=o.geometry.getAttribute('normal');
    assert.deepEqual(p.array,d[j].geometry.getAttribute('position').array);
    assert.ok(p.count>=800&&p.count<1200,'One mesh, finite detail budget');
    assert.equal(n.count,p.count);
    let midFaceGrooves=0,capVertices=0,cornerVertices=0;
    for(let i=0;i<p.count;i++){
      const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
      assert.ok([x,y,z,n.getX(i),n.getY(i),n.getZ(i)].every(Number.isFinite));
      const radius=Math.hypot(x,z);
      if(radius<1e-7)continue; // original cap centers
      const sector=Math.PI/4,angle=Math.atan2(x,z);
      let delta=angle%sector;
      if(delta>sector/2)delta-=sector;
      if(delta<-sector/2)delta+=sector;
      const taper=.13+(.16-.13)*(1.15-y)/2.3;
      const octagon=Math.cos(sector/2)/Math.cos(sector/2-Math.abs(delta));
      const originalR=taper*octagon;
      const inset=originalR-radius;
      assert.ok(inset>=-1e-5&&inset<=.011001,'No outward growth or excessive recess');
      if(Math.abs(Math.abs(y)-1.15)<1e-5){
        near(inset,0);
        capVertices++;
      }
      if(Math.abs(delta)<1e-5){
        near(inset,0);
        cornerVertices++;
      }
      if(Math.abs(y)<.5&&Math.abs(Math.abs(delta)-sector/2)<.0001&&inset>.006)
        midFaceGrooves++;
    }
    assert.ok(midFaceGrooves>10,'Physically depressed flute faces, not shader-only');
    assert.ok(capVertices>100,'Unmodified original octagonal end caps');
    assert.ok(cornerVertices>60,'Original polygon corner rays retained at all heights');
    o.geometry.computeBoundingBox();
    near(o.geometry.boundingBox.min.y,-1.15);
    near(o.geometry.boundingBox.max.y,1.15);
    near(o.geometry.boundingBox.min.x,-.16);
    near(o.geometry.boundingBox.max.x,.16);
    near(o.geometry.boundingBox.min.z,-.16);
    near(o.geometry.boundingBox.max.z,.16);
    totalRecess+=midFaceGrooves;totalCap+=capVertices;totalCorner+=cornerVertices;
  }
  assert.ok(totalRecess>60&&totalCap>600&&totalCorner>360);
  a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),sourceBefore);
});

test('Static batching, ordinary water clocks during global calm, pause and once-only disposal survive porch relief',()=>{
  const a=build(),g=estate(a),c=columns(a),count=g.children.length;
  let geometryDisposals=0,materialDisposals=0;
  c[0].geometry.addEventListener('dispose',()=>geometryDisposals++);
  c[0].material.addEventListener('dispose',()=>materialDisposals++);
  const batch=batchStaticGeometry(THREE,g);
  assert.ok(g.children.length<count,'Existing static geometry batcher still compacts');
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
  assert.equal(geometryDisposals,1);
  assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});
