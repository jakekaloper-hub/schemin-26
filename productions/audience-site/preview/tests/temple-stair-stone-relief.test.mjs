import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const world=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=world.locations.find(location=>location.id===id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const snapshot=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const temple=a=>a.locations.find(l=>l.id===ids[0]);
const treads=a=>temple(a)?.group.children.filter(o=>o.name==='Candidate Temple stone tread relief')||[];

test('Temple stone source retains nine original stair placements and landmark identity',()=>{
  const source=world.locations.find(l=>l.id===ids[0]),a=build(),t=treads(a);
  assert.equal(source.canon_status,'PERMANENT_CANON');
  assert.ok(source.persistent_landmarks.includes('temple stone'));
  assert.equal(a.locations.length,3);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(temple(a).group.userData.locationId,ids[0]);
  assert.equal(t.length,9,'no new steps or separate decorative meshes');
  assert.equal(t[0].material,t[2].material);
  assert.equal(t[1].material,t[3].material);
  assert.notEqual(t[0].material,t[1].material);
  for(let j=0;j<9;j++){
    const o=t[j];
    assert.deepEqual(o.position.toArray(),[1,j*.24+.12,5.3-j*.43]);
    assert.deepEqual(o.scale.toArray(),[1,1,1]);
    assert.deepEqual(o.userData.originalDimensions,[2.8,.24,.55]);
    assert.equal(o.userData.sourceLandmark,'temple stone');
    assert.equal(o.userData.originalStepIndex,j);
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);
  }
  for(const l of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(l.group.children.filter(o=>o.name==='Candidate Temple stone tread relief').length,0);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),snapshot);a.dispose();
});

test('Each existing tread has bounded deterministic physical joints, wear and unchanged edges',()=>{
  const a=build(),b=build(),t=treads(a),u=treads(b);
  for(let j=0;j<9;j++){
    const g=t[j].geometry,p=g.getAttribute('position'),n=g.getAttribute('normal');
    assert.equal(g.type,'BoxGeometry');
    assert.deepEqual([g.parameters.width,g.parameters.height,g.parameters.depth],[2.8,.24,.55]);
    assert.deepEqual([g.parameters.widthSegments,g.parameters.heightSegments,g.parameters.depthSegments],[28,1,8]);
    assert.ok(p.count>500&&p.count<800,'bounded vertex budget for one static tread');
    assert.deepEqual(p.array,u[j].geometry.getAttribute('position').array,'repeatable physical relief');
    let groove=0,interior=0,rim=0;
    for(let i=0;i<p.count;i++){
      const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
      assert.ok([x,y,z,n.getX(i),n.getY(i),n.getZ(i)].every(Number.isFinite));
      assert.ok(Math.abs(x)<=1.400001&&Math.abs(z)<=.275001,'same original step footprint');
      assert.ok(y>=-.120001&&y<=.120001,'same original height envelope');
      if(Math.abs(y-.12)<.000001&&(Math.abs(x)>1.39999||Math.abs(z)>.27499))rim++;
      if(y>0&&y<.12&&Math.abs(x)<1.4&&Math.abs(z)<.275)interior++;
      if(Math.abs(x)<.000001&&Math.abs(z)<.2&&y>0&&y<.105)groove++;
    }
    assert.ok(rim>=70,'all four original top edges stay put');
    assert.ok(interior>100,'physical surface differs from flat original top');
    assert.ok(groove>=5,'incised center joint, not just a material effect');
  }
  assert.equal(JSON.stringify(bindings),snapshot);a.dispose();b.dispose();
});

test('Temple relief is static; global calm keeps natural water moving until explicit pause',()=>{
  const a=build(),t=treads(a),p=t.map(o=>o.geometry.getAttribute('position').array.slice());
  assert.deepEqual(a.water.map(w=>w.kind),['river','waterfall','landing-ripple','landing-ripple','landing-ripple','landing-ripple','pool','swamp','channel','pond']);
  a.tick(1.8,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.8));
  a.tick(4.2,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.2));
  a.tick(8.1,{globalCalm:true,paused:true,storm:8});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.2));
  a.tick(10.1,{globalCalm:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===10.1));
  for(let j=0;j<9;j++)assert.deepEqual(t[j].geometry.getAttribute('position').array,p[j]);
  let geometryDisposals=0,materialDisposals=0;
  t[0].geometry.addEventListener('dispose',()=>geometryDisposals++);
  t[0].material.addEventListener('dispose',()=>materialDisposals++);
  a.dispose();a.dispose();a.tick(12);
  assert.equal(geometryDisposals,1);assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(bindings),snapshot);
});
