import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const site=atlas.locations.find(x=>x.id===id);
  assert.ok(site, 'Existing source Atlas site '+id);
  return {id,anchor:[site.abstract_position[0],0,site.abstract_position[1]],
    canonStatus:site.canon_status,landmarks:site.persistent_landmarks};
});
const beforeAtlas=JSON.stringify(atlas),beforeBindings=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const fall=a=>a.water.find(w=>w.kind==='waterfall');
function lateral(u,v,t){
  const hold=Math.sin(Math.PI*u)**2*Math.sin(Math.PI*v);
  return .019*hold*(Math.sin(v*12.6-t*2.35+u*5.4)
    +.34*Math.sin(v*24.1-t*3.9-u*8.1));
}

test('One original Southern Wetlands Temple sheet gains physical interior x shear without changing perimeter, source, or budget',()=>{
  const a=build(),w=fall(a),site=a.locations.find(x=>x.id===ids[0]);
  const sourceSite=atlas.locations.find(x=>x.id===ids[0]);
  assert.equal(sourceSite.physical_zone_id,'REG-SOUTHERN-WETLANDS');
  assert.equal(sourceSite.canon_status,'PERMANENT_CANON');
  assert.ok(sourceSite.persistent_landmarks.includes('waterfall'));
  assert.deepEqual(a.locations.map(x=>x.id),ids);
  assert.equal(a.water.filter(x=>x.kind==='waterfall').length,1);
  assert.equal(w.mesh.parent,site.group);
  assert.deepEqual(w.mesh.position.toArray(),[-5.8,3.75,1.8]);
  assert.deepEqual(w.mesh.userData.originalDimensions,[2.15,6.9]);
  assert.equal(w.mesh.userData.originalPerimeterPreserved,true);
  assert.equal(w.mesh.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.deepEqual(w.mesh.userData.routeIds,[]);
  assert.deepEqual(w.mesh.userData.principalCharacters,[]);
  const g=w.mesh.geometry,p=g.getAttribute('position'),uv=g.getAttribute('uv');
  assert.equal(g.type,'PlaneGeometry');
  assert.deepEqual([g.parameters.width,g.parameters.height,g.parameters.widthSegments,g.parameters.heightSegments],[2.15,6.9,24,32]);
  let edges=0;
  for(let i=0;i<p.count;i++){
    const u=uv.getX(i),v=uv.getY(i);
    if(u===0||u===1||v===0||v===1){
      edges++;
      assert.ok(Math.abs(p.getX(i)-(u-.5)*2.15)<1e-5);
      assert.ok(Math.abs(Math.abs(p.getY(i))-(Math.abs(v-.5)*6.9))<1e-5);
      assert.ok(Math.abs(p.getZ(i))<1e-7);
      for(const time of [0,1.25,8.5])assert.ok(Math.abs(lateral(u,v,time))<1e-8);
    }
  }
  assert.ok(edges>=108);
  const shader=w.material.vertexShader;
  assert.match(shader,/if\(uFall>\.5\)\{/);
  assert.match(shader,/p\.z\+=\.10\*sideHold\*endHold\*folds/);
  assert.match(shader,/lateralCurrent=sin\(uv\.y\*12\.6-uTime\*2\.35\+uv\.x\*5\.4\)/);
  assert.match(shader,/\.34\*sin\(uv\.y\*24\.1-uTime\*3\.9-uv\.x\*8\.1\)/);
  assert.match(shader,/p\.x\+=\.019\*sideHold\*sideHold\*endHold\*lateralCurrent/);
  assert.ok(shader.indexOf('p.x+=.019')>shader.indexOf('if(uFall>.5){'));
  assert.ok(shader.indexOf('p.x+=.019')<shader.indexOf('if(uWetland>.5){'));
  assert.doesNotMatch(shader.slice(shader.indexOf('if(uFall>.5){'),shader.indexOf('if(uWetland>.5){')),
    /\buStorm\b|\buRain\b|\buGlobalCalm\b/);
  assert.ok(a.water.filter(x=>x.kind!=='waterfall').every(x=>(x.material.uniforms.uFall?.value??0)===0));
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),beforeAtlas);
  assert.equal(JSON.stringify(bindings),beforeBindings);
  a.dispose();
});

test('Two downstream harmonics create bounded time-driven interior sideways flow, including zero at every water-sheet edge',()=>{
  let maximum=0,minimum=0,changed=0;
  for(let ui=0;ui<=48;ui++)for(let vi=0;vi<=64;vi++){
    const u=ui/48,v=vi/64;
    for(const time of [0,.23,2.5,5.75,9]){
      const dx=lateral(u,v,time);
      maximum=Math.max(maximum,dx);minimum=Math.min(minimum,dx);
      assert.ok(Number.isFinite(dx)&&Math.abs(dx)<=.019*1.34+1e-8);
      if(ui===0||ui===48||vi===0||vi===64)assert.ok(Math.abs(dx)<1e-8);
    }
    if(Math.abs(lateral(u,v,.23)-lateral(u,v,2.5))>.006)changed++;
  }
  assert.ok(maximum>.017&&minimum<-.017,'Both inward and outward wave phases remain visible');
  assert.ok(changed>300,'Motion affects a broad interior, not a single point');
  assert.ok(Math.abs(lateral(.5,.5,0)-lateral(.5,.5,2.5))>.005);
  const a=build(),b=build();
  assert.equal(fall(a).material.vertexShader,fall(b).material.vertexShader,'Deterministic same-source shader');
  a.dispose();b.dispose();
});

test('Original water and scene clocks survive synthetic global calm, explicit pause, batching and once-only disposal',()=>{
  const a=build(),w=fall(a),temple=a.locations[0].group,originalCount=temple.children.length;
  const batches=batchStaticGeometry(THREE,temple);
  assert.ok(temple.children.length<originalCount);
  assert.ok(temple.children.includes(w.mesh),'Animated water never becomes a static batch');
  for(const geometry of batches.geometries)geometry.dispose();
  assert.deepEqual(a.water.map(x=>x.kind),[
    'river','waterfall','landing-ripple','landing-ripple','landing-ripple','landing-ripple','pool','swamp','channel','pond'
  ]);
  for(const t of [1.2,3.8,9.75]){
    a.tick(t,{storm:0,weatherMode:'GLOBAL_CALM'});
    assert.ok(a.water.every(x=>x.material.uniforms.uTime.value===t));
  }
  a.tick(20,{paused:true,storm:0,weatherMode:'GLOBAL_CALM'});
  assert.ok(a.water.every(x=>x.material.uniforms.uTime.value===9.75));
  let geoDisposed=0,materialDisposed=0;
  w.mesh.geometry.addEventListener('dispose',()=>geoDisposed++);
  w.material.addEventListener('dispose',()=>materialDisposed++);
  a.dispose();a.dispose();a.tick(40);
  assert.equal(geoDisposed,1);
  assert.equal(materialDisposed,1);
  assert.equal(JSON.stringify(atlas),beforeAtlas);
  assert.equal(JSON.stringify(bindings),beforeBindings);
});
