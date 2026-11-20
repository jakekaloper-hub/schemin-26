import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const world=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=world.locations.find(entry=>entry.id===id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const snapshot=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const shafts=a=>a.locations.find(l=>l.id===ids[0]).group.children
  .filter(o=>o.name==='Candidate Temple fluted stone pillar');

test('Source-bound Temple retains exactly five original shafts, placements and stone capitals',()=>{
  const a=build(),t=shafts(a),canonical=world.locations.find(l=>l.id===ids[0]);
  assert.equal(canonical.canon_status,'PERMANENT_CANON');
  assert.ok(canonical.persistent_landmarks.includes('temple stone'));
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(a.locations[0].group.userData.locationId,ids[0]);
  assert.equal(t.length,5);
  const shared=t[0].material;
  assert.equal(shared.color.getHexString(),'b4ad89');
  t.forEach((o,n)=>{
    const i=n-2;
    assert.deepEqual(o.position.toArray(),[1+i*1.05,2.3+3.1/2,1.1]);
    assert.deepEqual(o.scale.toArray(),[1,1,1]);
    assert.equal(o.material,shared);
    assert.deepEqual(o.userData.originalDimensions,[.23,.29,3.1]);
    assert.equal(o.userData.originalPillarIndex,i);
    assert.equal(o.userData.sourceLandmark,'temple stone');
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);
    assert.equal(o.geometry.type,'CylinderGeometry');
    assert.deepEqual([o.geometry.parameters.radiusTop,o.geometry.parameters.radiusBottom,
      o.geometry.parameters.height,o.geometry.parameters.radialSegments,o.geometry.parameters.heightSegments],
      [.23,.29,3.1,32,8]);
  });
  const capitals=a.locations[0].group.children.filter(o=>o.geometry.type==='BoxGeometry'&&
    o.geometry.parameters.width===.7&&o.geometry.parameters.height===.22&&
    o.geometry.parameters.depth===.65);
  assert.equal(capitals.length,5);
  for(const l of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(l.group.children.filter(o=>o.name==='Candidate Temple fluted stone pillar').length,0);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),snapshot);a.dispose();
});

test('Deterministic inward-only stone fluting preserves both original circular end rings',()=>{
  const a=build(),b=build(),t=shafts(a),u=shafts(b);
  const baseline=new THREE.CylinderGeometry(.23,.29,3.1,32,8);
  const flat=baseline.getAttribute('position');let shaped=0;
  t.forEach((o,n)=>{
    const g=o.geometry,p=g.getAttribute('position'),normal=g.getAttribute('normal');
    assert.equal(p.count,flat.count);
    assert.ok(p.count>=300&&p.count<=500,'bounded static shaft geometry');
    assert.deepEqual(p.array,u[n].geometry.getAttribute('position').array);
    assert.ok(g.boundingSphere.radius<=1.61);
    let incisions=0;
    for(let j=0;j<p.count;j++){
      const x=p.getX(j),y=p.getY(j),z=p.getZ(j);
      const oldR=Math.hypot(flat.getX(j),flat.getZ(j)),newR=Math.hypot(x,z),inset=oldR-newR;
      assert.ok([x,y,z,normal.getX(j),normal.getY(j),normal.getZ(j)].every(Number.isFinite));
      assert.ok(inset>=-.000001&&inset<.015,'inside original taper');
      assert.equal(y,flat.getY(j));
      if(Math.abs(y)>=1.55-.000001)
        assert.ok(Math.abs(x-flat.getX(j))<.000001&&Math.abs(z-flat.getZ(j))<.000001);
      if(inset>.004)incisions++;
    }
    assert.ok(incisions>20,'physical carved grooves, not a shader-only effect');
    shaped+=incisions;
  });
  assert.ok(shaped>100);
  baseline.dispose();a.dispose();b.dispose();assert.equal(JSON.stringify(bindings),snapshot);
});

test('Static shafts keep natural water moving during calm, freeze on pause and dispose once',()=>{
  const a=build(),t=shafts(a),positions=t.map(o=>o.geometry.getAttribute('position').array.slice());
  assert.deepEqual(a.water.map(w=>w.kind),
    ['river','waterfall','landing-ripple','landing-ripple','landing-ripple','landing-ripple','pool','swamp','channel','pond']);
  a.tick(1.8,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.8));
  a.tick(4.2,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.2));
  a.tick(8.1,{globalCalm:true,storm:6,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.2));
  a.tick(10.1,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===10.1));
  t.forEach((o,n)=>assert.deepEqual(o.geometry.getAttribute('position').array,positions[n]));
  let geometryDisposals=0,materialDisposals=0;
  t[0].geometry.addEventListener('dispose',()=>geometryDisposals++);
  t[0].material.addEventListener('dispose',()=>materialDisposals++);
  a.dispose();a.dispose();a.tick(12);
  assert.equal(geometryDisposals,1);assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(bindings),snapshot);
});
