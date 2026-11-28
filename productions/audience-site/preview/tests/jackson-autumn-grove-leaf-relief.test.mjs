import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-COUNTRY-CLUB-JACKSON','LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(x=>x.id===id);
  assert.ok(p,'missing established Atlas site '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const estate=a=>a.locations.find(p=>p.id===ids[0]).group;
const crowns=a=>estate(a).children.filter(o=>o.userData.estateTreePart==='crown');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-6,'original folio candidate transform changed');
const grove=[[-9,-3,1.1],[-9,3,1.0],[-9,9,.9],[-5,11,1.08],[1,11,1.17],
  [10,1,1.05],[9,-4,1.25],[3,-8,.95],[-4,-8,1.12]];

test('all 49 existing Jackson autumn crowns gain physically recessed relief without moving one original tree',()=>{
  const beforeAtlas=JSON.stringify(atlas),beforeBindings=JSON.stringify(bindings);
  const a=build(),existing=crowns(a),original=new THREE.IcosahedronGeometry(1,2);
  assert.equal(atlas.locations.find(p=>p.id===ids[0]).canon_status,'PERMANENT_CANON');
  assert.equal(existing.length,49,'nine original trees: 4/5 crown lobes plus each top crown');
  assert.equal(estate(a).children.filter(o=>o.userData.estateTreePart==='trunk').length,9);
  assert.deepEqual(a.locations.map(p=>p.id),ids);
  let offset=0,maxInset=0,recessedVertices=0;
  const baseline=original.getAttribute('position');
  for(let i=0;i<grove.length;i++){
    const [x,z,scale]=grove[i],h=(2.5+.24*(i%3))*scale,lobes=4+(i%2);
    for(let k=0;k<=lobes;k++){
      const obj=existing[offset++],high=k===lobes,a0=(k/lobes)*Math.PI*2+i*.34;
      const dx=Math.cos(a0)*.66*scale,dz=Math.sin(a0)*.63*scale;
      const center=high?[x,h+1.05*scale,z]:
        [x+dx,h+(.46+(k%2)*.30)*scale,z+dz];
      const size=high?[1.10*scale,.85*scale,1.0*scale]:
        [(1.08+(k%3)*.12)*scale,(.85+(k%2)*.17)*scale,(.94+(k%2)*.14)*scale];
      center.forEach((v,d)=>near(obj.position.getComponent(d),v));
      size.forEach((v,d)=>near(obj.scale.getComponent(d),v));
      [.19+center[0]*.07,center[2]*.16,.1].forEach((v,d)=>near(obj.rotation.toArray()[d],v));
      assert.equal(obj.userData.estateTree,i);
      assert.equal(obj.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
      assert.equal(obj.userData.historicalReference,'W09-COUNTRY-CLUB-FOLIOS-05-08');
      assert.equal(obj.userData.originalCrownEnvelopePreserved,true);
      assert.equal(obj.userData.navigable,false);
      assert.deepEqual(obj.userData.routeIds,[]);
      assert.deepEqual(obj.userData.principalCharacters,[]);
      assert.equal(obj.geometry.name,'Candidate Jackson inward-scalloped autumn crown');
      assert.ok(obj.material.isMeshStandardMaterial);
      const pos=obj.geometry.getAttribute('position'),norm=obj.geometry.getAttribute('normal'),
        uv=obj.geometry.getAttribute('uv');
      assert.equal(pos.count,baseline.count,'no original triangle replaced or appended');
      assert.equal(norm.count,pos.count);assert.equal(uv.count,pos.count);
      for(let j=0;j<pos.count;j++){
        const ox=baseline.getX(j),oy=baseline.getY(j),oz=baseline.getZ(j);
        const px=pos.getX(j),py=pos.getY(j),pz=pos.getZ(j);
        const oldRadius=Math.hypot(ox,oy,oz),newRadius=Math.hypot(px,py,pz);
        assert.ok([px,py,pz,norm.getX(j),norm.getY(j),norm.getZ(j),
          uv.getX(j),uv.getY(j)].every(Number.isFinite));
        assert.ok(newRadius<=oldRadius+1e-6,'no new crown silhouette or reach');
        assert.ok(newRadius>=oldRadius*(1-.082)-1e-6,'no unbounded inset');
        if(oldRadius-newRadius>.02)recessedVertices++;
        maxInset=Math.max(maxInset,oldRadius-newRadius);
      }
    }
  }
  assert.equal(offset,existing.length);
  assert.ok(recessedVertices>700,'relief must change actual mesh vertices');
  assert.ok(maxInset>.04,'foliage relief must be visually meaningful');
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(estate(a).userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE',
    'Week 3 chili contamination has no verified cleanup event');
  assert.equal(JSON.stringify(atlas),beforeAtlas);
  assert.equal(JSON.stringify(bindings),beforeBindings);
  original.dispose();a.dispose();
});

test('Jackson folio relief is deterministic, restricted to estate trees and keeps existing opaque crown batches',()=>{
  const a=build(),b=build(),first=crowns(a),second=crowns(b),g=estate(a);
  assert.equal(first.length,second.length);
  const materialSet=new Set(first.map(o=>o.material));
  assert.equal(materialSet.size,5,'five existing autumn tones remain');
  for(let i=0;i<first.length;i++)
    assert.deepEqual(first[i].geometry.getAttribute('position').array,
      second[i].geometry.getAttribute('position').array);
  for(const location of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(location.group.getObjectByName('Candidate Jackson inward-scalloped autumn crown'),undefined);
  const batch=batchStaticGeometry(THREE,g);
  for(const material of materialSet)
    assert.equal(g.children.filter(o=>o.isMesh&&o.material===material).length,1,
      'unchanged amber material slots retain one opaque batch each');
  for(const geometry of batch.geometries)geometry.dispose();
  a.dispose();b.dispose();
});

test('historical calm and explicit pause keep independent ordinary pond/swamp/Temple water clock; disposals are once-only',()=>{
  const source=JSON.stringify(bindings),a=build(),first=crowns(a)[0],pond=a.water.find(w=>w.kind==='pond');
  let disposals=0;first.geometry.addEventListener('dispose',()=>disposals++);
  assert.ok(pond);
  const other=a.water.filter(w=>['swamp','channel','river','waterfall','pool'].includes(w.kind));
  assert.ok(other.length>=5);
  a.tick(2,{globalCalm:true,storm:0});
  assert.ok([pond,...other].every(w=>w.material.uniforms.uTime.value===2));
  a.tick(5,{globalCalm:true,storm:0});
  assert.ok([pond,...other].every(w=>w.material.uniforms.uTime.value===5));
  a.tick(9,{globalCalm:true,storm:4,paused:true});
  assert.ok([pond,...other].every(w=>w.material.uniforms.uTime.value===5));
  a.tick(13,{globalCalm:true,storm:0});
  assert.ok([pond,...other].every(w=>w.material.uniforms.uTime.value===13));
  a.dispose();a.dispose();a.tick(20);
  assert.equal(disposals,1);assert.equal(JSON.stringify(bindings),source);
});
