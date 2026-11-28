import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const place=atlas.locations.find(p=>p.id===id);
  assert.ok(place,'Missing canonical location '+id);
  return {id,anchor:[place.abstract_position[0],0,place.abstract_position[1]],
    canonStatus:place.canon_status,landmarks:place.persistent_landmarks};
});
const atlasBefore=JSON.stringify(atlas),bindingsBefore=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const club=a=>a.locations.find(l=>l.id==='LOC-COUNTRY-CLUB-JACKSON').group;
const windows=a=>club(a).children.filter(o=>o.userData.estateWindowPart==='glazing-relief');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,'Inherited geometry envelope changed');

test('Five inherited Jackson glass-window boxes remain source-bound with original positions and materials',()=>{
  const a=build(),w=windows(a),c=club(a),source=atlas.locations.find(p=>p.id===ids[2]);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(source.canon_status,'PERMANENT_CANON');
  assert.ok(source.persistent_landmarks.includes('clubhouse'));
  assert.ok(source.current_state.some(x=>x.includes('chili contamination')));
  assert.ok(source.current_state.some(x=>x.includes('cleanup state')));
  assert.equal(c.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(w.length,5);
  assert.deepEqual(w.map(v=>v.position.x),[-3,-1.5,0,1.5,3]);
  for(const v of w){
    near(v.position.y,.85+1.05/2);near(v.position.z,2.12);
    assert.deepEqual(v.scale.toArray(),[1,1,1]);
    assert.deepEqual(v.userData.originalDimensions,[.55,1.05,.04]);
    assert.equal(v.material.color.getHexString(),'385953');
    assert.equal(v.material.roughness,.30);
    assert.equal(v.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(v.userData.sourceLandmark,'clubhouse');
    assert.equal(v.userData.originalPerimeterPreserved,true);
    assert.equal(v.userData.navigable,false);
    assert.deepEqual(v.userData.routeIds,[]);
    assert.deepEqual(v.userData.principalCharacters,[]);
    assert.equal(v.geometry.type,'BoxGeometry');
    assert.deepEqual([v.geometry.parameters.width,v.geometry.parameters.height,
      v.geometry.parameters.depth],[.55,1.05,.04]);
    assert.deepEqual([v.geometry.parameters.widthSegments,v.geometry.parameters.heightSegments,
      v.geometry.parameters.depthSegments],[24,32,1]);
    assert.equal(v.children.length,0,'No extra pane draw calls');
  }
  for(const other of a.locations.filter(l=>l.id!==ids[2]))
    assert.equal(other.group.getObjectByName('Candidate Jackson recessed clubhouse glazing'),undefined);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),atlasBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
  a.dispose();
});

test('Each front has two deterministic physical recesses; original glazing envelopes and reverse faces are untouched',()=>{
  const a=build(),b=build(),w=windows(a),v=windows(b);
  const reference=new THREE.BoxGeometry(.55,1.05,.04,24,32,1);
  const base=reference.getAttribute('position');
  for(let k=0;k<w.length;k++){
    const geom=w[k].geometry,p=geom.getAttribute('position'),norm=geom.getAttribute('normal');
    assert.equal(p.count,base.count);
    assert.ok(p.count<2500,'Finite inherited one-mesh tessellation');
    assert.deepEqual(p.array,v[k].geometry.getAttribute('position').array);
    let deep=0,peak=0,untouched=0;
    const halves=new Set();
    for(let i=0;i<p.count;i++){
      const x=base.getX(i),y=base.getY(i),z=base.getZ(i);
      const xx=p.getX(i),yy=p.getY(i),zz=p.getZ(i);
      assert.ok([xx,yy,zz,norm.getX(i),norm.getY(i),norm.getZ(i)].every(Number.isFinite));
      near(x,xx);near(y,yy);
      const interior=Math.abs(z-.02)<1e-6&&Math.abs(x)<.275-1e-6&&Math.abs(y)<.525-1e-6;
      const inset=z-zz;
      if(!interior){near(inset,0);untouched++;continue;}
      assert.ok(inset>=-1e-6&&inset<=.01401,'Inward-only bounded panel');
      if(inset>.010){deep++;halves.add(x<0?'left':'right');}
      peak=Math.max(peak,inset);
    }
    assert.deepEqual([...halves].sort(),['left','right'],'Two actual front glazing panels');
    assert.ok(deep>150,'Physical glazing recess, not just a shader label');
    assert.ok(peak>.0139&&peak<=.01401);
    assert.ok(untouched>500,'Inherited edge, back and reverse surfaces');
    geom.computeBoundingBox();
    const bb=geom.boundingBox;
    for(const [got,expected] of [[bb.min.x,-.275],[bb.max.x,.275],
      [bb.min.y,-.525],[bb.max.y,.525],[bb.min.z,-.02],[bb.max.z,.02]])
      near(got,expected);
  }
  reference.dispose();a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),atlasBefore);
});

test('Opaque batching and six ordinary water clocks survive global calm, pause and once-only disposal',()=>{
  const a=build(),c=club(a),w=windows(a),first=w[0],preCount=c.children.length;
  let geoDisposed=0,glassDisposed=0;
  first.geometry.addEventListener('dispose',()=>geoDisposed++);
  first.material.addEventListener('dispose',()=>glassDisposed++);
  const batch=batchStaticGeometry(THREE,c);
  assert.ok(c.children.length<preCount,'Opaque window material still batchable');
  assert.equal(a.water.filter(w=>['pond','swamp','channel','river','pool','waterfall'].includes(w.kind)).length,6);
  for(const g of batch.geometries)g.dispose();
  const animated=a.water;
  a.tick(3,{globalCalm:true,storm:0});
  a.tick(9,{globalCalm:true,storm:0});
  assert.ok(animated.every(w=>w.material.uniforms.uTime.value===9));
  a.tick(15,{globalCalm:true,storm:6,paused:true});
  assert.ok(animated.every(w=>w.material.uniforms.uTime.value===9));
  a.tick(20,{globalCalm:true,storm:0});
  assert.ok(animated.every(w=>w.material.uniforms.uTime.value===20));
  a.dispose();a.dispose();a.tick(25);
  assert.equal(geoDisposed,1);assert.equal(glassDisposed,1);
  assert.equal(JSON.stringify(atlas),atlasBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});
