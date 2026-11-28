import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(l=>l.id===id);
  assert.ok(p,'Source-bound Atlas location '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const sourceSnapshot=JSON.stringify(atlas),bindingSnapshot=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const temple=a=>a.locations.find(l=>l.id===ids[0]).group;
const tiers=a=>temple(a).children.filter(o=>o.name==='Candidate Temple seamed stepped tier');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,'tier exterior or position changed');

test('Four pre-existing Waterfall Temple stone tiers retain their exact source footprint, order and materials',()=>{
  const source=atlas.locations.find(l=>l.id===ids[0]),a=build(),t=tiers(a);
  assert.equal(source.canon_status,'PERMANENT_CANON');
  assert.ok(source.persistent_landmarks.includes('temple stone'));
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(temple(a).userData.locationId,ids[0]);
  assert.equal(t.length,4,'no added building or floor plane');
  for(let j=0;j<4;j++){
    const w=9-j*1.1,d=7-j*.75,o=t[j],g=o.geometry;
    assert.deepEqual(o.position.toArray(),[1,j*.58+.29,-.8]);
    assert.deepEqual(o.scale.toArray(),[1,1,1]);
    assert.equal(o.material.color.getHexString(),j%2?'ddd2a6':'b4ad89');
    assert.deepEqual(o.userData.originalDimensions,[w,.58,d]);
    assert.equal(o.userData.originalTierIndex,j);
    assert.equal(o.userData.originalPerimeterPreserved,true);
    assert.equal(o.userData.sourceLandmark,'temple stone');
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.navigable,false);
    assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);
    assert.equal(g.type,'BoxGeometry');
    assert.deepEqual([g.parameters.width,g.parameters.height,g.parameters.depth],[w,.58,d]);
    assert.deepEqual([g.parameters.widthSegments,g.parameters.heightSegments,g.parameters.depthSegments],[32,1,24]);
    assert.ok(g.getAttribute('position').count>=1800&&g.getAttribute('position').count<=2000,
      'surface-only bounded tessellation, same static mesh objects');
    assert.equal(o.material.isShaderMaterial,undefined,'existing opaque material batch');
  }
  for(const l of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(l.group.getObjectByName('Candidate Temple seamed stepped tier'),undefined);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),sourceSnapshot);
  assert.equal(JSON.stringify(bindings),bindingSnapshot);
  a.dispose();
});

test('Real inward staggered stone joints are repeatable while every side, bottom and outer top edge is unchanged',()=>{
  const a=build(),b=build(),t=tiers(a),u=tiers(b);
  for(let j=0;j<4;j++){
    const w=9-j*1.1,d=7-j*.75,baseline=new THREE.BoxGeometry(w,.58,d,32,1,24);
    const original=baseline.getAttribute('position'),p=t[j].geometry.getAttribute('position');
    const normals=t[j].geometry.getAttribute('normal');
    assert.deepEqual(p.array,u[j].geometry.getAttribute('position').array,'no nondeterministic sculpt');
    assert.equal(p.count,original.count);
    let recessed=0,strong=0,topInterior=0,topRim=0,maxInset=0;
    for(let i=0;i<p.count;i++){
      const x=original.getX(i),y=original.getY(i),z=original.getZ(i);
      const xx=p.getX(i),yy=p.getY(i),zz=p.getZ(i);
      assert.ok([xx,yy,zz,normals.getX(i),normals.getY(i),normals.getZ(i)].every(Number.isFinite));
      near(x,xx);near(z,zz);
      assert.ok(yy<=y+1e-6&&yy>=y-.05001,'only inward relief in inherited envelope');
      const top=Math.abs(y-.29)<1e-6;
      const interior=Math.abs(x)<w/2-1e-6&&Math.abs(z)<d/2-1e-6;
      const inset=y-yy;
      if(!top||!interior)near(yy,y);
      else{topInterior++;if(inset>.010)recessed++;if(inset>.030)strong++;}
      if(top&&!interior)topRim++;
      maxInset=Math.max(maxInset,inset);
    }
    assert.ok(topInterior>650&&recessed>150&&strong>70,'visibly incised top stone grid');
    assert.ok(topRim>90,'outer edges of all four platforms untouched');
    assert.ok(maxInset>.040&&maxInset<=.05001,'bounded dimensional depth');
    t[j].geometry.computeBoundingBox();
    const box=t[j].geometry.boundingBox;
    near(box.min.x,-w/2);near(box.max.x,w/2);
    near(box.min.y,-.29);near(box.max.y,.29);
    near(box.min.z,-d/2);near(box.max.z,d/2);
    baseline.dispose();
  }
  a.dispose();b.dispose();
  assert.equal(JSON.stringify(bindings),bindingSnapshot);
});

test('Existing stone materials remain in one opaque batch each; source historical state stays untouched',()=>{
  const a=build(),b=build(),t=tiers(a),u=tiers(b),group=temple(a);
  for(let j=0;j<4;j++)
    assert.deepEqual(t[j].geometry.getAttribute('position').array,u[j].geometry.getAttribute('position').array);
  assert.equal(t[0].material,t[2].material);
  assert.equal(t[1].material,t[3].material);
  assert.notEqual(t[0].material,t[1].material);
  assert.equal(group.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  const materials=new Set(t.map(o=>o.material.uuid));
  assert.equal(materials.size,2);
  const batch=batchStaticGeometry(THREE,group);
  for(const material of [t[0].material,t[1].material])
    assert.equal(group.children.filter(o=>o.isMesh&&o.material===material).length,1,
      'stone tier geometry must remain in pre-existing shared material draw');
  for(const geo of batch.geometries)geo.dispose();
  a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),sourceSnapshot);
});

test('Ordinary waterfall and river motion survives global calm, freezes on pause and disposes once',()=>{
  const a=build(),tier=tiers(a)[0],waters=a.water.filter(w=>
    ['river','waterfall','pool','swamp','channel','pond'].includes(w.kind));
  assert.equal(waters.length,6);
  let geoDisposals=0,materialDisposals=0;
  tier.geometry.addEventListener('dispose',()=>geoDisposals++);
  tier.material.addEventListener('dispose',()=>materialDisposals++);
  a.tick(2,{globalCalm:true,storm:0});
  a.tick(6,{globalCalm:true,storm:0});
  assert.ok(waters.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(10,{globalCalm:true,storm:5,paused:true});
  assert.ok(waters.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(14,{globalCalm:true,storm:0});
  assert.ok(waters.every(w=>w.material.uniforms.uTime.value===14));
  a.dispose();a.dispose();a.tick(25);
  assert.equal(geoDisposals,1);
  assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(bindings),bindingSnapshot);
});
