import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{const p=atlas.locations.find(v=>v.id===id);return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],canonStatus:p.canon_status,landmarks:p.persistent_landmarks};});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const name='Candidate Mud Dogs recessed fallen timber';
const timber=a=>a.locations[0].group.getObjectByName(name);
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,`${a} != ${b}`);
const start=new THREE.Vector3(-5,.5,1),end=new THREE.Vector3(0,.8,4),length=start.distanceTo(end);

test('Inherited timber retains exact endpoint transforms, original bark material and source scope',()=>{
  const before=JSON.stringify(bindings),a=build();try{
    const g=a.locations[0].group,o=timber(a);
    assert.ok(o);assert.equal(g.children.filter(m=>m.name===name).length,1);
    assert.ok(new THREE.Vector3(0,-length/2,0).applyQuaternion(o.quaternion).add(o.position).distanceTo(start)<1e-6);
    assert.ok(new THREE.Vector3(0,length/2,0).applyQuaternion(o.quaternion).add(o.position).distanceTo(end)<1e-6);
    assert.equal(o.material,g.children.find(m=>m.userData.wetlandPart==='upper-branch').material);
    assert.ok(o.material.map&&o.material.bumpMap);assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.navigable,false);assert.deepEqual(o.userData.routeIds,[]);assert.deepEqual(o.userData.principalCharacters,[]);
    assert.ok(a.locations.slice(1).every(l=>!l.group.getObjectByName(name)));
    assert.equal(a.worldMutationAllowed,false);assert.equal(JSON.stringify(bindings),before);
  }finally{a.dispose();}
});

test('Subdivided timber is deterministic, physically incised and entirely within original seven-sided taper',()=>{
  const a=build(),b=build(),old=new THREE.CylinderGeometry(.32*.62,.32,length,7);try{
    const geo=timber(a).geometry,p=geo.attributes.position,n=geo.attributes.normal;
    assert.deepEqual(p.array,timber(b).geometry.attributes.position.array);
    assert.equal(geo.index.count/3,2800);assert.equal(old.index.count/3,28);
    let max=0,ends=0;
    for(let i=0;i<p.count;i++){
      const x=p.getX(i),y=p.getY(i),z=p.getZ(i),r=Math.hypot(x,z);
      assert.ok([x,y,z,n.getX(i),n.getY(i),n.getZ(i)].every(Number.isFinite));
      assert.ok(Math.abs(y)<=length/2+1e-5);
      if(r<1e-8)continue;
      // Seven supporting planes independently bound the original polygon.
      const taper=.32*(1-(1-.62)*(y/length+.5)),apothem=taper*Math.cos(Math.PI/7);
      let maxDot=-Infinity;
      for(let j=0;j<7;j++){const angle=(j+.5)*2*Math.PI/7;maxDot=Math.max(maxDot,x*Math.sin(angle)+z*Math.cos(angle));}
      assert.ok(maxDot<=apothem+1e-6);
      const inset=apothem-maxDot;max=Math.max(max,inset);
      if(Math.abs(Math.abs(y)-length/2)<1e-5){near(maxDot,apothem);ends++;}
    }
    assert.ok(ends>100&&max>.025&&max<.065);
    for(let row=0;row<=24;row++){
      const i=row*57,j=i+56;
      assert.ok(new THREE.Vector3().fromBufferAttribute(p,i).distanceTo(new THREE.Vector3().fromBufferAttribute(p,j))<1e-6);
      assert.ok(new THREE.Vector3().fromBufferAttribute(n,i).distanceTo(new THREE.Vector3().fromBufferAttribute(n,j))<1e-6);
    }
  }finally{old.dispose();a.dispose();b.dispose();}
});

test('Timber keeps one opaque bark batch; ordinary water continues in calm and freezes only on pause',()=>{
  const a=build();try{
    const g=a.locations[0].group,o=timber(a),material=o.material;
    let disposed=0;o.geometry.addEventListener('dispose',()=>disposed++);
    const batch=batchStaticGeometry(THREE,g);
    assert.equal(g.children.filter(m=>m.isMesh&&m.material===material).length,1);
    for(const geo of batch.geometries)geo.dispose();
    const water=a.water.filter(w=>['river','waterfall','pool','swamp','channel','pond'].includes(w.kind));assert.equal(water.length,6);
    a.tick(3,{globalCalm:true,storm:0});a.tick(8,{globalCalm:true,storm:0});assert.ok(water.every(w=>w.material.uniforms.uTime.value===8));
    a.tick(12,{globalCalm:true,storm:0,paused:true});assert.ok(water.every(w=>w.material.uniforms.uTime.value===8));
    a.dispose();a.dispose();assert.equal(disposed,1);
  }finally{a.dispose();}
});
