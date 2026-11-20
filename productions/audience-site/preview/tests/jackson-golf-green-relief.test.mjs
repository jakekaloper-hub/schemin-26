import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=source.locations.find(o=>o.id===id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const before=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const estate=a=>a.locations.find(l=>l.id==='LOC-COUNTRY-CLUB-JACKSON').group;
const greens=a=>estate(a).children.filter(o=>o.name==='Candidate Jackson sculpted course grass');

test('Jackson keeps exactly three source-bound course discs, all landmarks and unresolved Week 3 history',()=>{
  const canonical=source.locations.find(l=>l.id===ids[2]),a=build(),g=greens(a);
  assert.equal(canonical.canon_status,'PERMANENT_CANON');
  assert.ok(canonical.persistent_landmarks.includes('golf grounds'));
  assert.ok(canonical.current_state.some(s=>s.includes('chili contamination')));
  assert.ok(canonical.current_state.some(s=>s.includes('cleanup state')));
  assert.equal(g.length,3);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  g.forEach((o,i)=>{
    assert.deepEqual(o.position.toArray(),[-4+i*4,.02,7.5+(i%2)]);
    assert.deepEqual(o.scale.toArray(),[2.7,1.8,1]);
    assert.equal(o.rotation.x,-Math.PI/2);
    assert.equal(o.castShadow,false);
    assert.equal(o.material.color.getHexString(),'648c43');
    assert.equal(o.material,g[0].material);
    assert.equal(o.geometry.name,'Candidate Jackson bounded golf-ground relief');
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.sourceLandmark,'golf grounds');
    assert.equal(o.userData.originalGreenIndex,i);
    assert.equal(o.userData.originalDiscRadius,1);
    assert.equal(o.userData.originalSegments,30);
    assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);
  });
  assert.equal(a.water.filter(w=>w.kind==='pond').length,1);
  const pond=a.water.find(w=>w.kind==='pond').mesh;
  assert.deepEqual(pond.position.toArray(),[7,.06,6]);
  assert.deepEqual(pond.scale.toArray(),[3.8,2.3,1]);
  assert.equal(estate(a).children.filter(o=>o.geometry?.type==='CircleGeometry' &&
    o.material.color?.getHexString?.()==='c7ad76').length,2,'the two inherited sand discs remain');
  for(const other of a.locations.filter(l=>l.id!==ids[2]))
    assert.equal(other.group.children.filter(o=>o.name==='Candidate Jackson sculpted course grass').length,0);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),before);a.dispose();
});

test('Jackson green interiors carry deterministic physical relief, with exactly original fixed circular perimeter',()=>{
  const a=build(),b=build(),g=greens(a),same=greens(b);
  const old=new THREE.CircleGeometry(1,30),oldPos=old.getAttribute('position');
  for(let k=0;k<3;k++){
    const geo=g[k].geometry,p=geo.getAttribute('position'),n=geo.getAttribute('normal'),uv=geo.getAttribute('uv');
    assert.equal(p.count,211,'one center plus seven rings of 30 points');
    assert.equal(geo.index.count,1170,'no extra mesh or draw call');
    assert.deepEqual(p.array,same[k].geometry.getAttribute('position').array);
    assert.ok(geo.boundingSphere.radius<=1.001,'ellipse footprint remains original');
    let nonflat=0;
    for(let i=0;i<p.count;i++){
      const x=p.getX(i),y=p.getY(i),z=p.getZ(i),r=Math.hypot(x,y);
      assert.ok([x,y,z,n.getX(i),n.getY(i),n.getZ(i),uv.getX(i),uv.getY(i)].every(Number.isFinite));
      assert.ok(r<=1.000001,'no changed lateral footprint');
      assert.ok(Math.abs(z)<=.043001,'small interior vertical relief');
      if(Math.abs(z)>.003)nonflat++;
      if(i>=1+30*6){
        assert.ok(Math.abs(z)<.000001,'original outer boundary is stationary');
        const j=i-(1+30*6);
        assert.ok(Math.abs(x-oldPos.getX(j+1))<.000001);
        assert.ok(Math.abs(y-oldPos.getY(j+1))<.000001);
      }
    }
    assert.ok(nonflat>60,'actual sculpted surfaces rather than flat geometry');
  }
  old.dispose();a.dispose();b.dispose();
  assert.equal(JSON.stringify(bindings),before);
});

test('Jackson turf relief is static; existing water advances in calm, freezes only on pause, and disposes once',()=>{
  const a=build(),g=greens(a),geometry=g[0].geometry,material=g[0].material;
  const baseline=g.map(o=>o.geometry.getAttribute('position').array.slice());
  a.tick(1.7,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.7));
  a.tick(5.6,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.6));
  a.tick(8.4,{globalCalm:true,storm:6,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.6));
  a.tick(11.2,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===11.2));
  g.forEach((o,i)=>assert.deepEqual(o.geometry.getAttribute('position').array,baseline[i]));
  let geometryDisposals=0,materialDisposals=0;
  geometry.addEventListener('dispose',()=>geometryDisposals++);
  material.addEventListener('dispose',()=>materialDisposals++);
  a.dispose();a.dispose();a.tick(13);
  assert.equal(geometryDisposals,1);assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(bindings),before);
});
