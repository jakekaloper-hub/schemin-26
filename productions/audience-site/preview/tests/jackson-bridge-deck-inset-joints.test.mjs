import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const source=atlas.locations.find(p=>p.id===id);
  assert.ok(source,'missing authoritative Atlas location '+id);
  return {id,anchor:[source.abstract_position[0],0,source.abstract_position[1]],
    canonStatus:source.canon_status,landmarks:source.persistent_landmarks};
});
const make=()=>buildRegionalAssets(THREE,bindings,()=>2);
function getBridge(a){
  const jackson=a.locations.find(l=>l.id===ids[2]).group;
  const arch=jackson.getObjectByName('Candidate Week 9 pond-side stone arch');
  const deck=arch.getObjectByName('Candidate Jackson bridge deck surface');
  return {jackson,arch,deck};
}
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,String(a)+' != '+String(b));

test('Jackson bridge keeps exactly one original static deck, unknown history and topology',()=>{
  const before=JSON.stringify(atlas),bindingBefore=JSON.stringify(bindings);
  const a=make(),{jackson,arch,deck}=getBridge(a);
  const location=atlas.locations.find(p=>p.id===ids[2]);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.ok(location.current_state.some(s=>s.includes('chili contamination')));
  assert.ok(location.current_state.some(s=>s.includes('cleanup state')));
  assert.equal(jackson.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.deepEqual(arch.position.toArray(),[7,.10,6]);
  assert.equal(arch.children.length,17,'original 2 faces, 14 parapet objects, one deck');
  assert.equal(arch.children.filter(o=>o.userData.bridgePart==='stone-arch').length,2);
  assert.equal(arch.children.filter(o=>o.userData.bridgePart==='deck').length,1);
  assert.equal(deck.isMesh,true);assert.equal(deck.geometry.type,'BoxGeometry');
  assert.deepEqual(deck.position.toArray(),[0,1.565,0]);
  assert.deepEqual(deck.scale.toArray(),[1,1,1]);
  assert.deepEqual(deck.userData.originalDimensions,[1.8,.19,5.48]);
  assert.equal(deck.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(deck.userData.sourceLandmark,'Week 9 pond-side stone arch');
  assert.equal(deck.userData.originalPerimeterPreserved,true);
  assert.equal(deck.userData.treadJointCount,12);
  assert.equal(deck.userData.navigable,false);
  assert.deepEqual(deck.userData.routeIds,[]);
  assert.deepEqual(deck.userData.principalCharacters,[]);
  assert.equal(deck.material.color.getHexString(),'997856');
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),before);
  assert.equal(JSON.stringify(bindings),bindingBefore);
  a.dispose();
});

test('all twelve insets are physical, inward only, deterministic, within unchanged deck hull',()=>{
  const a=make(),b=make(),{deck}=getBridge(a),{deck:other}=getBridge(b);
  const geo=deck.geometry,p=geo.getAttribute('position'),q=other.geometry.getAttribute('position');
  assert.deepEqual(Array.from(p.array),Array.from(q.array),'reproducible geometry');
  assert.equal(geo.parameters.width,1.8);
  assert.equal(geo.parameters.height,.19);
  assert.equal(geo.parameters.depth,5.48);
  assert.equal(geo.parameters.widthSegments,8);
  assert.equal(geo.parameters.depthSegments,52);
  assert.ok(p.count<1500,'no added meshes or excessive deck tessellation');
  const bounds=geo.boundingBox;
  for(const [axis,low,high] of [['x',-.9,.9],['y',-.095,.095],['z',-2.74,2.74]]){
    close(bounds.min[axis],low);close(bounds.max[axis],high);
  }
  for(let i=0;i<p.count;i++){
    const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
    assert.ok(x>=-.900001&&x<=.900001&&z>=-2.740001&&z<=2.740001);
    assert.ok(y>=-.095001&&y<=.095001,'only recessed; never extrudes above deck');
    if(Math.abs(x)>=.9-1e-6 || Math.abs(z)>=2.74-1e-6)
      assert.ok(Math.abs(Math.abs(y)-.095)<1e-5 || (y>-.095&&y<.095),
        'original side/top perimeter preserved');
  }
  const pitch=5.48/13;
  for(let j=1;j<=12;j++){
    const z=-2.74+j*pitch;
    const candidates=[];
    for(let i=0;i<p.count;i++)
      if(Math.abs(p.getX(i))<1e-6&&Math.abs(p.getZ(i)-z)<1e-5)
        candidates.push(p.getY(i));
    assert.ok(candidates.some(y=>y<.083),'physical recessed joint '+j);
  }
  for(let j=0;j<13;j++){
    const z=-2.74+(j+.5)*pitch;
    let found=false;
    for(let i=0;i<p.count;i++)if(Math.abs(p.getX(i))<1e-6&&
      Math.abs(p.getZ(i)-z)<1e-5&&Math.abs(p.getY(i)-.095)<1e-5)found=true;
    assert.ok(found,'original undepressed tread face '+j);
  }
  a.dispose();b.dispose();
});

test('static Jackson tread relief leaves water, El Niño calm, pause and disposal intact',()=>{
  const a=make(),{deck}=getBridge(a);
  const oldGeometry=deck.geometry;
  const bodies=a.water.filter(w=>['swamp','channel','river','waterfall','pool','pond'].includes(w.kind));
  assert.equal(bodies.length,6);
  assert.deepEqual(bodies.map(w=>w.kind).sort(),['channel','pond','pool','river','swamp','waterfall']);
  const pond=a.water.find(w=>w.kind==='pond');
  assert.deepEqual(pond.mesh.position.toArray(),[7,.06,6]);
  assert.deepEqual(pond.mesh.scale.toArray(),[3.8,2.3,1]);
  assert.equal(pond.mesh.geometry.getAttribute('position').count,321);
  assert.equal(pond.mesh.geometry.index.count,1800);
  a.tick(2,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2));
  a.tick(5,{globalCalm:true,storm:0,historicalReplay:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5));
  a.tick(13,{paused:true,globalCalm:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5));
  assert.equal(oldGeometry.getAttribute('position'),deck.geometry.getAttribute('position'));
  let disposals=0;
  oldGeometry.addEventListener('dispose',()=>disposals++);
  a.dispose();a.dispose();a.tick(18);
  assert.equal(disposals,1);
});
