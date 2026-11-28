import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(entry=>entry.id===id);
  assert.ok(p,'missing source Atlas place: '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const swamp=a=>a.locations.find(l=>l.id===ids[0]).group;
const roots=a=>swamp(a).children.filter(o=>o.userData.wetlandPart==='buttress-root')
  .sort((a,b)=>a.userData.wetlandStand-b.userData.wetlandStand);
const close=(a,b)=>assert.ok(a.distanceTo(b)<1e-6,'original root anchor moved');

test('56 existing Mud Dogs buttress-root arms retain exact endpoint anchors and radius envelope',()=>{
  const before=JSON.stringify(atlas),bindingBefore=JSON.stringify(bindings),a=build();
  const r=roots(a),old=new THREE.CylinderGeometry(.11*.62,.11,1,7);
  assert.equal(r.length,56,'14 established tree stands × 4 existing root arms');
  assert.equal(atlas.locations.find(x=>x.id===ids[0]).canon_status,'PERMANENT_CANON');
  assert.equal(r[0].material,swamp(a).children.find(x=>x.userData.wetlandPart==='trunk').material);
  const seen=new Set();
  for(let stand=0;stand<14;stand++)for(let k=0;k<4;k++){
    const o=r[stand*4+k],angle=stand*2.4,rad=3.8+(stand%4)*1.5;
    const x=Math.cos(angle)*rad,z=Math.sin(angle)*rad,y=.12;
    const b=k*Math.PI/2+stand*.31,reach=.85+(stand%3)*.15;
    const start=new THREE.Vector3(x,y+.67,z);
    const end=new THREE.Vector3(x+Math.cos(b)*reach,y+.045,z+Math.sin(b)*reach);
    const length=start.distanceTo(end);
    assert.equal(o.userData.wetlandStand,stand);
    assert.equal(o.userData.wetlandPart,'buttress-root');
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.originalEndpointsPreserved,true);
    assert.equal(o.userData.originalRadiusEnvelopePreserved,true);
    assert.deepEqual(o.userData.routeIds,[]);
    assert.equal(o.userData.navigable,false);
    assert.equal(o.geometry.name,'Candidate Mud Dogs contoured buttress root');
    assert.ok(o.geometry.getAttribute('position').count>old.getAttribute('position').count*3);
    close(new THREE.Vector3(0,-length/2,0).applyQuaternion(o.quaternion).add(o.position),start);
    close(new THREE.Vector3(0,length/2,0).applyQuaternion(o.quaternion).add(o.position),end);
    const pos=o.geometry.getAttribute('position'),normal=o.geometry.getAttribute('normal');
    const uv=o.geometry.getAttribute('uv'),recessed=[];
    assert.equal(pos.count,normal.count);assert.equal(pos.count,uv.count);
    for(let j=0;j<pos.count;j++){
      const px=pos.getX(j),py=pos.getY(j),pz=pos.getZ(j),radius=Math.hypot(px,pz);
      const original=.11-(.11-.11*.62)*(py/length+.5);
      assert.ok(Number.isFinite(px)&&Number.isFinite(py)&&Number.isFinite(pz));
      assert.ok(Math.abs(py)<=length/2+1e-6);
      assert.ok(radius<=original+1e-6,'recess never adds footprint or exceeds old arm cylinder');
      for(const v of [normal.getX(j),normal.getY(j),normal.getZ(j),uv.getX(j),uv.getY(j)])
        assert.ok(Number.isFinite(v),'finite textured normal and UV');
      if(radius>.00001 && Math.abs(py)<length/4)recessed.push(original-radius);
      if(radius>.00001 && Math.abs(Math.abs(py)-length/2)<1e-5)
        assert.ok(Math.abs(radius-original)<1e-5,'old end rings/caps remain exact');
    }
    assert.ok(Math.max(...recessed)>.003,'visible physical contour, not flat material illusion');
    seen.add(o.geometry);
  }
  assert.equal(seen.size,56,'one existing arm mesh and geometry per root');
  assert.deepEqual(a.locations.map(x=>x.id),ids);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),before);assert.equal(JSON.stringify(bindings),bindingBefore);
  old.dispose();a.dispose();
});

test('candidate root geometry is deterministic, localized and keeps one opaque shared bark batch',()=>{
  const a=build(),b=build(),r=roots(a),comparison=roots(b),s=swamp(a);
  assert.equal(r.length,comparison.length);
  for(let i=0;i<r.length;i++){
    assert.deepEqual(Array.from(r[i].geometry.getAttribute('position').array),
      Array.from(comparison[i].geometry.getAttribute('position').array));
    assert.equal(r[i].material,r[0].material);
  }
  for(const l of a.locations.filter(x=>x.id!==ids[0]))
    assert.equal(l.group.getObjectByName('Candidate Mud Dogs contoured buttress root'),undefined);
  const geometryCount=s.children.filter(o=>o.userData.wetlandPart==='buttress-root').length;
  assert.equal(geometryCount,56);
  const result=batchStaticGeometry(THREE,s);
  assert.equal(s.children.filter(o=>o.isMesh&&o.material===r[0].material).length,1,
    'sculpted roots still share established trunk/root opaque draw');
  for(const geo of result.geometries)geo.dispose();
  a.dispose();b.dispose();
});

test('El Niño global calm leaves regular swamp/Temple water clock alive, explicit pause freezes, disposal once',()=>{
  const before=JSON.stringify(bindings),a=build(),root=roots(a)[0];
  let disposals=0;root.geometry.addEventListener('dispose',()=>disposals++);
  const wet=a.water.filter(w=>['swamp','channel','river','waterfall','pool','pond'].includes(w.kind));
  assert.ok(wet.length>=6);
  a.tick(3,{globalCalm:true,storm:0});
  for(const w of wet)assert.equal(w.material.uniforms.uTime.value,3);
  a.tick(7,{globalCalm:true,storm:0});
  for(const w of wet)assert.equal(w.material.uniforms.uTime.value,7);
  a.tick(10,{globalCalm:true,storm:0,paused:true});
  for(const w of wet)assert.equal(w.material.uniforms.uTime.value,7);
  a.tick(14,{globalCalm:true,storm:0});
  for(const w of wet)assert.equal(w.material.uniforms.uTime.value,14);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();a.dispose();
  assert.equal(disposals,1);
});
