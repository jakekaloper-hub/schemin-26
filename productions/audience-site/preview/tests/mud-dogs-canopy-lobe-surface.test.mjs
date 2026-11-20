import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(x=>x.id===id);
  assert.ok(p,'Missing existing source '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const swamp=a=>a.locations.find(p=>p.id===ids[0]).group;
const lobes=a=>swamp(a).children.filter(o=>o.userData.wetlandPart==='canopy-lobe');
const near=(x,y)=>assert.ok(Math.abs(x-y)<1e-6,'changed original lobe transform');

test('all 56 inherited Mud Dogs crown lobes have bounded inward physical texture, no changed identity or transform',()=>{
  const before=JSON.stringify(atlas),oldBindings=JSON.stringify(bindings),a=build();
  const crowns=lobes(a),original=new THREE.IcosahedronGeometry(1,2);
  const oldP=original.getAttribute('position');
  assert.equal(crowns.length,56,'14 existing cypress-like stands × 4 existing crown lobes');
  assert.equal(atlas.locations.find(p=>p.id===ids[0]).canon_status,'PERMANENT_CANON');
  assert.deepEqual(a.locations.map(p=>p.id),ids);
  let maxRelief=0,countRelief=0;
  for(let i=0;i<14;i++)for(let j=0;j<4;j++){
    const obj=crowns[i*4+j],angle=i*2.4,r=3.8+(i%4)*1.5,h=3.3+(i%3)*.9;
    const x=Math.cos(angle)*r,z=Math.sin(angle)*r;
    const center=[x+Math.sin(i*1.7+j*1.3)*.24,.12+h+.24+j*.44,z+Math.cos(i+j*2.1)*.23];
    const width=(1.42-j*.24)*(i%3===1?.87:i%3===2?1.09:1);
    const rise=(.92-j*.09)*(i%3===1?1.17:.95);
    center.forEach((v,k)=>near(obj.position.getComponent(k),v));
    [width,rise,width*.82].forEach((v,k)=>near(obj.scale.getComponent(k),v));
    [.19+center[0]*.07,center[2]*.16,.1].forEach((v,k)=>near(obj.rotation.toArray()[k],v));
    assert.equal(obj.userData.wetlandStand,i);
    assert.equal(obj.userData.wetlandPart,'canopy-lobe');
    assert.equal(obj.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(obj.userData.originalLobeEnvelopePreserved,true);
    assert.deepEqual(obj.userData.routeIds,[]);
    assert.deepEqual(obj.userData.principalCharacters,[]);
    assert.equal(obj.userData.navigable,false);
    assert.ok(obj.material.isMeshStandardMaterial);
    assert.equal(obj.geometry.name,'Candidate Mud Dogs inward-scalloped canopy lobe');
    const p=obj.geometry.getAttribute('position'),uv=obj.geometry.getAttribute('uv'),n=obj.geometry.getAttribute('normal');
    assert.equal(p.count,oldP.count,'no added geometry triangles');
    assert.equal(p.count,uv.count);assert.equal(p.count,n.count);
    for(let k=0;k<p.count;k++){
      const x=p.getX(k),y=p.getY(k),z=p.getZ(k),ox=oldP.getX(k),oy=oldP.getY(k),oz=oldP.getZ(k);
      const initial=Math.hypot(ox,oy,oz),current=Math.hypot(x,y,z);
      assert.ok([x,y,z,uv.getX(k),uv.getY(k),n.getX(k),n.getY(k),n.getZ(k)].every(Number.isFinite));
      assert.ok(current<=initial+1e-6,'original lobe radial footprint expanded');
      assert.ok(current>=initial*(1-.086)-1e-6,'recess exceeded conservative radial envelope');
      near(x*oy-y*ox,0);near(y*oz-z*oy,0);near(z*ox-x*oz,0);
      const delta=initial-current;
      if(delta>.015)countRelief++;
      maxRelief=Math.max(maxRelief,delta);
    }
  }
  assert.ok(countRelief>200,'canopies exhibit physical shape rather than only material color');
  assert.ok(maxRelief>.045,'recess is not lost to vertex sampling');
  for(const other of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(other.group.getObjectByName('Candidate Mud Dogs inward-scalloped canopy lobe'),undefined);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),before);assert.equal(JSON.stringify(bindings),oldBindings);
  original.dispose();a.dispose();
});

test('crown relief builds deterministically and preserves existing opaque material batching',()=>{
  const a=build(),b=build(),ca=lobes(a),cb=lobes(b),group=swamp(a);
  const colors=new Set(ca.map(o=>o.material.color.getHexString()));
  assert.equal(colors.size,3,'same existing three foliage tones');
  for(let k=0;k<ca.length;k++){
    assert.deepEqual(ca[k].geometry.getAttribute('position').array,
      cb[k].geometry.getAttribute('position').array);
    assert.equal(ca[k].material.color.getHexString(),cb[k].material.color.getHexString());
  }
  const materials=new Set(ca.map(o=>o.material));
  const batches=batchStaticGeometry(THREE,group);
  for(const material of materials)
    assert.equal(group.children.filter(o=>o.isMesh&&o.material===material).length,1,
      'same opaque static draw per original leaf material');
  for(const geo of batches.geometries)geo.dispose();
  a.dispose();b.dispose();
});

test('existing calm/pause water clock remains unchanged; the crown geometry disposes exactly once',()=>{
  const before=JSON.stringify(bindings),a=build(),geo=lobes(a)[0].geometry;
  let disposed=0;geo.addEventListener('dispose',()=>disposed++);
  const water=a.water.filter(w=>['swamp','channel','river','waterfall','pool','pond'].includes(w.kind));
  assert.ok(water.length>=6);
  a.tick(2,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===2));
  a.tick(5,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===5));
  a.tick(8,{globalCalm:true,storm:6,paused:true});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===5));
  a.tick(12,{globalCalm:true,storm:0});
  assert.ok(water.every(w=>w.material.uniforms.uTime.value===12));
  a.dispose();a.dispose();a.tick(15);
  assert.equal(disposed,1);
  assert.equal(JSON.stringify(bindings),before);
});
