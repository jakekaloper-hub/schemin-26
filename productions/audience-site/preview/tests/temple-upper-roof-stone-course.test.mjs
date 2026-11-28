import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{const s=atlas.locations.find(p=>p.id===id);return {id,anchor:[s.abstract_position[0],0,s.abstract_position[1]],canonStatus:s.canon_status,landmarks:s.persistent_landmarks};});
const snapshot=JSON.stringify(bindings),name='Candidate Temple staggered upper roof stone course';
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const roof=a=>a.locations[0].group.getObjectByName(name);
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,`${a} != ${b}`);

test('Upper stone slab inherits the exact Temple identity, dimensions, material and adjacent tiers',()=>{
  const a=build();try{
    const g=a.locations[0].group,o=roof(a);
    assert.ok(o);assert.equal(g.children.filter(m=>m.name===name).length,1);
    assert.deepEqual(o.position.toArray(),[1,6.0600000000000005,-.1]);
    assert.deepEqual(o.userData.originalDimensions,[6.1,.32,4.5]);
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.sourceLandmark,'temple stone');
    assert.ok(bindings[0].landmarks.includes(o.userData.sourceLandmark));
    assert.equal(o.userData.navigable,false);assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);assert.equal(a.worldMutationAllowed,false);
    assert.equal(o.material.color.getHexString(),'b4ad89');
    assert.ok(g.getObjectByName('Candidate Temple recessed lower roof cornice'));
    assert.equal(g.children.filter(m=>m.geometry?.parameters?.width===5.2&&m.geometry.parameters.height===.3&&m.geometry.parameters.depth===3.9).length,1);
    assert.ok(a.locations.slice(1).every(l=>!l.group.getObjectByName(name)));
    assert.equal(JSON.stringify(bindings),snapshot);
  }finally{a.dispose();}
});

test('Deterministic inward joints preserve all original rims and bound physical tessellation',()=>{
  const a=build(),b=build(),base=new THREE.BoxGeometry(6.1,.32,4.5,40,10,30);
  try{
    const o=roof(a),p=o.geometry.attributes.position,q=base.attributes.position,n=o.geometry.attributes.normal;
    assert.equal(p.count,q.count);assert.ok(p.count<4200);
    assert.deepEqual(p.array,roof(b).geometry.attributes.position.array);
    let frontCuts=0,sideCuts=0,outer=0,max=0;
    for(let i=0;i<p.count;i++){
      const x=q.getX(i),y=q.getY(i),z=q.getZ(i),xx=p.getX(i),yy=p.getY(i),zz=p.getZ(i);
      assert.ok([xx,yy,zz,n.getX(i),n.getY(i),n.getZ(i)].every(Number.isFinite));near(y,yy);
      const front=Math.abs(Math.abs(z)-2.25)<1e-6&&Math.abs(x)<3.05-1e-6&&Math.abs(y)<.16-1e-6;
      const side=Math.abs(Math.abs(x)-3.05)<1e-6&&Math.abs(z)<2.25-1e-6&&Math.abs(y)<.16-1e-6;
      let inset=0;
      if(front){near(x,xx);inset=Math.abs(z)-Math.abs(zz);if(inset>.01)frontCuts++;}
      else if(side){near(z,zz);inset=Math.abs(x)-Math.abs(xx);if(inset>.01)sideCuts++;}
      else{near(x,xx);near(z,zz);outer++;}
      assert.ok(inset>=-1e-6&&inset<=.02301);max=Math.max(max,inset);
    }
    assert.ok(frontCuts>50&&sideCuts>35&&outer>2400&&max>.018);
    o.geometry.computeBoundingBox();const {min,max:hi}=o.geometry.boundingBox;
    for(const [v,w] of [[min.x,-3.05],[hi.x,3.05],[min.y,-.16],[hi.y,.16],[min.z,-2.25],[hi.z,2.25]])near(v,w);
  }finally{base.dispose();a.dispose();b.dispose();}
});

test('Upper stone slab uses existing opaque batching and does not freeze ordinary water in calm',()=>{
  const a=build();try{
    const g=a.locations[0].group,o=roof(a),count=g.children.length;
    let disposed=0;o.geometry.addEventListener('dispose',()=>disposed++);
    const batch=batchStaticGeometry(THREE,g);
    assert.ok(g.children.length<count&&batch.geometries.length>0);
    for(const geo of batch.geometries)geo.dispose();
    const water=a.water.filter(w=>['river','waterfall','pool','swamp','channel','pond'].includes(w.kind));assert.equal(water.length,6);
    a.tick(2,{globalCalm:true,storm:0});a.tick(6,{globalCalm:true,storm:0});
    assert.ok(water.every(w=>w.material.uniforms.uTime.value===6));
    a.tick(11,{globalCalm:true,storm:0,paused:true});
    assert.ok(water.every(w=>w.material.uniforms.uTime.value===6));
    a.dispose();a.dispose();assert.equal(disposed,1);
  }finally{a.dispose();}
});
