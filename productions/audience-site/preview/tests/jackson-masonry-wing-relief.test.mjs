import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const source=atlas.locations.find(p=>p.id===id);
  assert.ok(source,'Atlas source location unavailable: '+id);
  return {id,anchor:[source.abstract_position[0],0,source.abstract_position[1]],
    canonStatus:source.canon_status,landmarks:source.persistent_landmarks};
});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const estate=a=>a.locations.find(p=>p.id===ids[2]).group;
const wings=a=>estate(a).children.filter(o=>o.userData?.estateWingPart==='mortar-relief');
const near=(x,y)=>assert.ok(Math.abs(x-y)<1e-5,'inherited envelope or transform changed');

test('both inherited brick-wing facades have real bounded inward-only masonry recesses and unchanged footprints',()=>{
  const source=JSON.stringify(atlas),before=JSON.stringify(bindings);
  const baseline=new THREE.BoxGeometry(2.2,2.2,3.6,32,24,16);
  const original=baseline.getAttribute('position'),a=build(),list=wings(a);
  assert.deepEqual(a.locations.map(p=>p.id),ids);
  assert.equal(list.length,2,'exactly two original side wings; no third building');
  assert.equal(estate(a).children.filter(o=>o.userData?.estateRoofPart==='hip-course').length,4);
  assert.equal(list[0].material,list[1].material,'existing single brick batch material');
  for(let i=0;i<2;i++){
    const wing=list[i],p=wing.geometry.getAttribute('position');
    assert.deepEqual(wing.position.toArray(),[i===0?-5:5,1.25,.1]);
    assert.deepEqual(wing.scale.toArray(),[1,1,1]);
    assert.deepEqual(wing.userData.originalWingDimensions,[2.2,2.2,3.6]);
    assert.equal(wing.userData.originalWingIndex,i);
    assert.equal(wing.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(wing.userData.sourceLandmark,'clubhouse');
    assert.equal(wing.userData.navigable,false);
    assert.deepEqual(wing.userData.routeIds,[]);
    assert.deepEqual(wing.userData.principalCharacters,[]);
    assert.equal(wing.geometry.name,'Candidate Jackson inward-recessed brick-wing mortar');
    assert.equal(p.count,original.count,'same two mesh objects; surface subdivision only');
    let etched=0,maxInset=0;
    const normal=wing.geometry.getAttribute('normal');
    for(let k=0;k<p.count;k++){
      const x=original.getX(k),y=original.getY(k),z=original.getZ(k);
      const nx=p.getX(k),ny=p.getY(k),nz=p.getZ(k);
      assert.ok([nx,ny,nz,normal.getX(k),normal.getY(k),normal.getZ(k)].every(Number.isFinite));
      near(ny,y);
      const front=Math.abs(Math.abs(z)-1.8)<1e-5&&Math.abs(x)<1.1-1e-5&&Math.abs(y)<1.1-1e-5;
      const side=Math.abs(Math.abs(x)-1.1)<1e-5&&Math.abs(z)<1.8-1e-5&&Math.abs(y)<1.1-1e-5;
      let inset=0;
      if(front){
        near(nx,x); assert.ok(Math.sign(nz)===Math.sign(z));
        assert.ok(Math.abs(nz)<=Math.abs(z)+1e-6);
        inset=Math.abs(z)-Math.abs(nz);
      }else if(side){
        near(nz,z); assert.ok(Math.sign(nx)===Math.sign(x));
        assert.ok(Math.abs(nx)<=Math.abs(x)+1e-6);
        inset=Math.abs(x)-Math.abs(nx);
      }else{
        near(nx,x);near(nz,z);
      }
      assert.ok(inset>=-1e-6&&inset<=.02501,'recess must fit inside previous masonry box');
      if(inset>.01)etched++;
      maxInset=Math.max(maxInset,inset);
    }
    assert.ok(etched>60,'mortared joints must be physically present on many vertices');
    assert.ok(maxInset>.015&&maxInset<=.02501,'visible but restrained groove depth');
    wing.geometry.computeBoundingBox();
    const box=wing.geometry.boundingBox;
    near(box.min.x,-1.1);near(box.max.x,1.1);
    near(box.min.y,-1.1);near(box.max.y,1.1);
    near(box.min.z,-1.8);near(box.max.z,1.8);
  }
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),source);
  assert.equal(JSON.stringify(bindings),before);
  baseline.dispose();a.dispose();
});

test('Jackson-only deterministic geometry preserves the original opaque batching and unresolved contamination',()=>{
  const a=build(),b=build(),aa=wings(a),bb=wings(b),g=estate(a);
  for(let i=0;i<aa.length;i++)assert.deepEqual(
    aa[i].geometry.getAttribute('position').array,
    bb[i].geometry.getAttribute('position').array);
  for(const location of a.locations.filter(l=>l.id!==ids[2]))
    assert.equal(location.group.getObjectByName('Candidate Jackson recessed masonry wing'),undefined);
  assert.equal(g.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  const club=atlas.locations.find(p=>p.id===ids[2]);
  assert.equal(club.canon_status,'PERMANENT_CANON');
  assert.ok(club.current_state.some(s=>s.includes('chili contamination')));
  assert.ok(club.current_state.some(s=>s.includes('cleanup state')));
  const material=aa[0].material,batch=batchStaticGeometry(THREE,g);
  assert.equal(g.children.filter(o=>o.isMesh&&o.material===material).length,1,
    'the two original walls still share exactly one opaque material batch');
  for(const geometry of batch.geometries)geometry.dispose();
  a.dispose();b.dispose();
});

test('global-calm El Nino weather does not freeze original running water; explicit pause and disposal do',()=>{
  const before=JSON.stringify(bindings),a=build(),wing=wings(a)[0];
  const waters=a.water.filter(w=>['waterfall','river','pool','swamp','channel','pond'].includes(w.kind));
  assert.equal(waters.length,6);
  let geometryDisposals=0,materialDisposals=0;
  wing.geometry.addEventListener('dispose',()=>geometryDisposals++);
  wing.material.addEventListener('dispose',()=>materialDisposals++);
  a.tick(2,{globalCalm:true,storm:0});
  a.tick(6,{globalCalm:true,storm:0});
  assert.ok(waters.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(10,{globalCalm:true,storm:5,paused:true});
  assert.ok(waters.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(14,{globalCalm:true,storm:0});
  assert.ok(waters.every(w=>w.material.uniforms.uTime.value===14));
  a.dispose();a.dispose();a.tick(25);
  assert.equal(geometryDisposals,1);
  assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(bindings),before);
});
