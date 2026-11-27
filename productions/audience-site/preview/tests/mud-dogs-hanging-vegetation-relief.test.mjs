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
  assert.ok(p,'missing canonical Atlas location '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const swamp=a=>a.locations.find(l=>l.id===ids[0]).group;
const strands=a=>swamp(a).children.filter(o=>o.userData.wetlandPart==='hanging-vegetation');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-6,'original inherited strand transform changed');

test('28 inherited hanging-vegetation cones gain finite deterministic inward folds, never expanded bounds or new canopy',()=>{
  const snapshot=JSON.stringify(atlas),initialBindings=JSON.stringify(bindings);
  const a=build(),v=strands(a);
  assert.equal(v.length,28,'14 original stands × 2 original hanging elements');
  assert.equal(atlas.locations.find(l=>l.id===ids[0]).canon_status,'PERMANENT_CANON');
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  let changed=0,maxInset=0;
  for(let i=0;i<14;i++)for(let k=0;k<2;k++){
    const t=v[i*2+k],angle=i*2.4,r=3.8+(i%4)*1.5,x=Math.cos(angle)*r,z=Math.sin(angle)*r;
    const y=.12,h=3.3+(i%3)*.9,b=k*Math.PI+i*.29;
    const span=.65+(i%3)*.12;
    [x+Math.cos(b)*.74,y+h-.18,z+Math.sin(b)*.74].forEach((n,j)=>near(t.position.getComponent(j),n));
    near(t.rotation.z,k?-.12:.12);
    assert.equal(t.userData.wetlandStand,i);
    assert.equal(t.userData.wetlandPart,'hanging-vegetation');
    assert.equal(t.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(t.userData.originalRadiusEnvelopePreserved,true);
    near(t.userData.originalVerticalSpan,span);
    assert.equal(t.userData.navigable,false);
    assert.deepEqual(t.userData.routeIds,[]);
    assert.deepEqual(t.userData.principalCharacters,[]);
    assert.equal(t.material.isMeshStandardMaterial,true);
    assert.equal(t.geometry.name,'Candidate Mud Dogs folded hanging vegetation');
    const p=t.geometry.getAttribute('position'),n=t.geometry.getAttribute('normal'),uv=t.geometry.getAttribute('uv');
    assert.ok(p.count>40,'genuine physical segments rather than flat paint');
    assert.equal(p.count,n.count);assert.equal(p.count,uv.count);
    for(let j=0;j<p.count;j++){
      const px=p.getX(j),py=p.getY(j),pz=p.getZ(j),radius=Math.hypot(px,pz);
      const outer=.085*Math.max(0,.5-py/span);
      assert.ok([px,py,pz,n.getX(j),n.getY(j),n.getZ(j),uv.getX(j),uv.getY(j)].every(Number.isFinite));
      assert.ok(Math.abs(py)<=span/2+1e-6,'height/endpoints exceeded');
      assert.ok(radius<=outer+1e-5,'original cone silhouette expanded');
      if(radius>1e-8)assert.ok(radius>=outer*(1-.24)-1e-5,'inset exceeded bounded 24 percent');
      if(radius>1e-8&&Math.abs(py+span/2)<1e-6)near(radius,.085);
      const inset=outer-radius;maxInset=Math.max(maxInset,inset);
      if(inset>.004)changed++;
    }
  }
  assert.ok(changed>60,'folds must reach sampled vertices');
  assert.ok(maxInset>.010,'geometry must exhibit real fold depth');
  for(const other of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(other.group.getObjectByName('Candidate Mud Dogs folded hanging vegetation'),undefined);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),snapshot);assert.equal(JSON.stringify(bindings),initialBindings);
  a.dispose();
});

test('folds regenerate bit-for-bit, reuse original opaque moss batch and exactly 28 mesh objects',()=>{
  const a=build(),b=build(),one=strands(a),two=strands(b);
  assert.equal(one.length,28);assert.equal(two.length,28);
  assert.ok(one.every(o=>o.material===one[0].material));
  for(let i=0;i<28;i++){
    assert.deepEqual(one[i].geometry.getAttribute('position').array,
      two[i].geometry.getAttribute('position').array);
    assert.equal(one[i].material.color.getHexString(),two[i].material.color.getHexString());
  }
  const group=swamp(a),moss=one[0].material,originalDrawMaterials=new Set(group.children.filter(o=>o.isMesh).map(o=>o.material));
  const compiled=batchStaticGeometry(THREE,group);
  assert.equal(group.children.filter(o=>o.isMesh&&o.material===moss).length,1,
    'all 28 existing hanging strands remain in one shared static opaque moss batch');
  assert.ok(group.children.every(o=>!o.isMesh||originalDrawMaterials.has(o.material)),
    'no new opaque render material after static batching');
  for(const geo of compiled.geometries)geo.dispose();
  a.dispose();b.dispose();
});

test('El Niño calm does not suppress ordinary river/wetland/pond flow, pause still holds; disposal once',()=>{
  const before=JSON.stringify(bindings),a=build(),first=strands(a)[0].geometry;
  let disposals=0;first.addEventListener('dispose',()=>disposals++);
  const waters=a.water.filter(w=>['swamp','channel','river','waterfall','pool','pond'].includes(w.kind));
  assert.equal(waters.length,6);
  a.tick(3,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===3));
  a.tick(7,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===7));
  a.tick(11,{globalCalm:true,storm:7,paused:true});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===7));
  a.tick(15,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===15));
  assert.equal(swamp(a).userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  a.dispose();a.dispose();a.tick(18);
  assert.equal(disposals,1);
  assert.equal(JSON.stringify(bindings),before);
});

test('hanging foliage UV wrap uses area-weighted side normals without changing the pointed tip or cap',()=>{
  const a=build();
  try {
    const v=strands(a);assert.equal(v.length,28);
    for(const o of v){
      const g=o.geometry,p=g.getAttribute('position'),n=g.getAttribute('normal'),idx=g.getIndex();
      const {radialSegments:r,heightSegments:h}=g.parameters,stride=r+1,sideCount=stride*(h+1);
      const raw=g.clone();raw.computeVertexNormals();const original=raw.getAttribute('normal');
      const pos=i=>new THREE.Vector3().fromBufferAttribute(p,i);
      const normal=i=>new THREE.Vector3().fromBufferAttribute(n,i);
      for(let row=0;row<=h;row++){
        const first=row*stride,last=first+r,sum=new THREE.Vector3(),used=new Set();
        assert.ok(pos(first).distanceTo(pos(last))<1e-6);
        for(let k=0;k<idx.count;k+=3){
          const tri=[idx.getX(k),idx.getX(k+1),idx.getX(k+2)];
          if(tri.some(i=>i>=sideCount)||!tri.some(i=>i===first||i===last))continue;
          for(const i of tri)used.add(i);
          const [x,y,z]=tri.map(pos);sum.add(y.sub(x).cross(z.sub(x)));
        }
        sum.normalize();
        assert.ok(normal(first).distanceTo(normal(last))<1e-6,'UV wrap lighting discontinuity');
        assert.ok(normal(first).distanceTo(sum)<1e-6,'area-weighted side seam');
        assert.ok(Math.abs(normal(first).length()-1)<1e-6);
        if(row===0){
          const tip=[first,last].filter(i=>used.has(i));
          assert.equal(tip.length,1,'only one wrap duplicate is referenced at the cone tip');
          assert.ok(normal(tip[0]).distanceTo(new THREE.Vector3().fromBufferAttribute(original,tip[0]))<1e-6,'referenced apex normal unchanged');
        }
      }
      for(let i=0;i<p.count;i++){
        if(i<sideCount&&(i%stride===0||i%stride===r))continue;
        assert.deepEqual(normal(i).toArray(),new THREE.Vector3().fromBufferAttribute(original,i).toArray(),'non-seam tip, side and cap normals unchanged');
      }
      raw.dispose();
    }
  } finally {a.dispose();}
});
