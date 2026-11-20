import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const source=atlas.locations.find(p=>p.id===id);
  assert.ok(source,'Missing Atlas location '+id);
  return {id,anchor:[source.abstract_position[0],0,source.abstract_position[1]],
    canonStatus:source.canon_status,landmarks:source.persistent_landmarks};
});
const before=JSON.stringify(atlas),originalBindings=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const estate=a=>a.locations.find(l=>l.id===ids[2]).group;
const treads=a=>estate(a).children.filter(o=>o.userData.estateStepPart==='joint-relief');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-5,'expected '+b+', got '+a);

test('Jackson keeps the original three entrance-step meshes, positions, material and unresolved state',()=>{
  const a=build(),s=atlas.locations.find(p=>p.id===ids[2]),t=treads(a);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(s.canon_status,'PERMANENT_CANON');
  assert.ok(s.persistent_landmarks.includes('clubhouse'));
  assert.ok(s.current_state.some(x=>x.includes('chili contamination')));
  assert.ok(s.current_state.some(x=>x.includes('cleanup state')));
  assert.equal(estate(a).userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(t.length,3);
  assert.equal(t[0].material,t[1].material);
  assert.equal(t[1].material,t[2].material);
  assert.equal(t[0].material.color.getHexString(),'ddd2a6');
  for(let i=0;i<t.length;i++){
    const o=t[i];
    assert.deepEqual(o.position.toArray(),[0,i*.1,4.8-i*.34]);
    assert.deepEqual(o.scale.toArray(),[1,1,1]);
    assert.deepEqual(o.userData.originalDimensions,[3,.1,.4]);
    assert.equal(o.userData.originalStepIndex,i);
    assert.equal(o.userData.originalPerimeterPreserved,true);
    assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(o.userData.sourceLandmark,'clubhouse');
    assert.equal(o.userData.navigable,false);
    assert.deepEqual(o.userData.routeIds,[]);
    assert.deepEqual(o.userData.principalCharacters,[]);
    assert.equal(o.children.length,0);
  }
  for(const other of a.locations.filter(l=>l.id!==ids[2]))
    assert.equal(other.group.children.filter(o=>o.userData.estateStepPart).length,0);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  a.dispose();
  assert.equal(JSON.stringify(atlas),before);
  assert.equal(JSON.stringify(bindings),originalBindings);
});

test('Three original envelopes gain deterministic finite inward-only top seams and riser scores',()=>{
  const a=build(),b=build(),t=treads(a),u=treads(b);
  for(let j=0;j<3;j++){
    const g=t[j].geometry,p=g.getAttribute('position'),n=g.getAttribute('normal');
    const base=new THREE.BoxGeometry(3,.1,.4,48,8,24);
    const raw=base.getAttribute('position');
    assert.equal(g.type,'BoxGeometry');
    assert.deepEqual([g.parameters.width,g.parameters.height,g.parameters.depth],[3,.1,.4]);
    assert.deepEqual([g.parameters.widthSegments,g.parameters.heightSegments,g.parameters.depthSegments],[48,8,24]);
    assert.equal(p.count,raw.count);
    assert.ok(p.count<6000,'One original step, finite single-mesh budget');
    assert.deepEqual(p.array,u[j].geometry.getAttribute('position').array);
    let topRecess=0,frontRecess=0,unchanged=0,deepSeams=0;
    for(let i=0;i<p.count;i++){
      const x=raw.getX(i),y=raw.getY(i),z=raw.getZ(i);
      const nx=p.getX(i),ny=p.getY(i),nz=p.getZ(i);
      assert.ok([nx,ny,nz,n.getX(i),n.getY(i),n.getZ(i)].every(Number.isFinite));
      near(nx,x);
      const interiorTop=Math.abs(y-.05)<1e-6&&Math.abs(x)<1.5-1e-6&&Math.abs(z)<.2-1e-6;
      const interiorFront=Math.abs(z-.2)<1e-6&&Math.abs(x)<1.5-1e-6&&Math.abs(y)<.05-1e-6;
      if(interiorTop){
        near(nz,z);
        assert.ok(ny<=y+1e-6&&y-ny<=.01201,'Top recess only inward');
        if(y-ny>1e-5)topRecess++;
        if(y-ny>.008&&Math.abs(Math.abs(x)-.5)<.025)deepSeams++;
      }else if(interiorFront){
        near(ny,y);
        assert.ok(nz<=z+1e-6&&z-nz<=.00901,'Front riser only inward');
        if(z-nz>1e-5)frontRecess++;
      }else{
        near(ny,y);near(nz,z);unchanged++;
      }
    }
    assert.ok(topRecess>100,'Genuine top-surface vertices depressed');
    assert.ok(frontRecess>20,'Genuine front-riser groove depth');
    assert.ok(deepSeams>8,'Both top joint bands are physical, not paint');
    assert.ok(unchanged>300,'Entire side/back/bottom, outer riser and tread rims stay fixed');
    g.computeBoundingBox();
    for(const [actual,expected] of [
      [g.boundingBox.min.x,-1.5],[g.boundingBox.max.x,1.5],
      [g.boundingBox.min.y,-.05],[g.boundingBox.max.y,.05],
      [g.boundingBox.min.z,-.2],[g.boundingBox.max.z,.2]])near(actual,expected);
    base.dispose();
  }
  a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),before);
});

test('Inherited batching and six ordinary water clocks survive global calm, pause and disposal',()=>{
  const a=build(),g=estate(a),t=treads(a);
  const count=g.children.length;
  let geoDisposals=0,matDisposals=0;
  t[0].geometry.addEventListener('dispose',()=>geoDisposals++);
  t[0].material.addEventListener('dispose',()=>matDisposals++);
  const b=batchStaticGeometry(THREE,g);
  assert.ok(g.children.length<count,'Original static batching compacted geometry');
  for(const geometry of b.geometries)geometry.dispose();
  assert.deepEqual(a.water.map(w=>w.kind),[
    'river','waterfall','landing-ripple','landing-ripple',
    'landing-ripple','landing-ripple','pool','swamp','channel','pond']);
  a.tick(3,{globalCalm:true,storm:0});
  a.tick(12,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===12));
  a.tick(19,{globalCalm:true,storm:9,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===12));
  a.tick(23,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===23));
  a.dispose();a.dispose();a.tick(25);
  assert.equal(geoDisposals,1);
  assert.equal(matDisposals,1);
  assert.equal(JSON.stringify(atlas),before);
  assert.equal(JSON.stringify(bindings),originalBindings);
});
