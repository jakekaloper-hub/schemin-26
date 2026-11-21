import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const s=atlas.locations.find(p=>p.id===id);
  assert.ok(s,'source place exists: '+id);
  return {id,anchor:[s.abstract_position[0],0,s.abstract_position[1]],
    canonStatus:s.canon_status,landmarks:s.persistent_landmarks};
});
const frozenSources=[JSON.stringify(atlas),JSON.stringify(bindings)];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function impact(u,v,t){
  const radius=Math.hypot((u-.5)*2,(v-.5)*2);
  const hold=1-smooth(.64,.96,radius);
  const distance=Math.hypot((u-.5)*2,(v-.554)*2.2);
  const falloff=1-smooth(.13,.52,distance);
  const crest=Math.max(Math.sin(distance*34-t*2.8+Math.sin(u*19+t*.3)*.28),0)**3;
  return .010*crest*falloff*hold;
}

test('Temple physical impact shares its pre-existing receiving-pool footprint and fragment impact center',()=>{
  const a=build(),pool=a.water.find(w=>w.kind==='pool');
  assert.deepEqual(a.locations.map(x=>x.id),ids);
  assert.equal(atlas.locations.find(s=>s.id===ids[0]).physical_zone_id,'REG-SOUTHERN-WETLANDS');
  assert.ok(pool&&a.water.find(w=>w.kind==='river')&&a.water.find(w=>w.kind==='waterfall'));
  assert.equal(pool.mesh.parent,a.locations[0].group);
  assert.deepEqual(pool.mesh.position.toArray(),[-5.8,.30,3]);
  assert.deepEqual(pool.mesh.scale.toArray(),[3.8,2.8,1]);
  assert.equal(pool.mesh.geometry.getAttribute('position').count,321);
  assert.equal(pool.mesh.geometry.index.count,1800);
  const vertex=pool.material.vertexShader,fragment=pool.material.fragmentShader;
  assert.match(fragment,/vec2 impactUv=vec2\(\.5,\.554\)/,'existing impact visual center retained');
  assert.match(vertex,/if\(uPlunge>\.5\)/);
  assert.match(vertex,/impactDistance=length\(\(uv-vec2\(\.5,\.554\)\)\*vec2\(2\.,2\.2\)\)/);
  assert.match(vertex,/impactFalloff=1\.-smoothstep\(\.13,\.52,impactDistance\)/);
  assert.match(vertex,/p\.z\+=\.010\*impactCrest\*impactFalloff\*plungeHold/);
  assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  a.dispose();
});

test('Same pool geometry has bounded changing physical impact ripples without moving its perimeter',()=>{
  const a=build(),pool=a.water.find(w=>w.kind==='pool');
  const p=pool.mesh.geometry.getAttribute('position'),uv=pool.mesh.geometry.getAttribute('uv');
  let edge=0,interior=0,changed=0,peak=0;
  for(let i=0;i<uv.count;i++){
    const u=uv.getX(i),v=uv.getY(i),r=Math.hypot((u-.5)*2,(v-.5)*2);
    const h0=impact(u,v,.35),h1=impact(u,v,1.45);
    assert.ok(Number.isFinite(h0)&&Number.isFinite(h1));
    assert.ok(h0>=0&&h0<=.01000001&&h1>=0&&h1<=.01000001);
    assert.ok(Math.abs(p.getZ(i))<1e-12,'rest pool still planar');
    peak=Math.max(peak,h0,h1);
    if(r>=.999999){edge++;assert.ok(h0<1e-12&&h1<1e-12,'fixed old shoreline');}
    if(r<.60){interior++;if(Math.abs(h0-h1)>.001)changed++;}
  }
  assert.ok(edge>=40&&interior>20);
  assert.ok(changed>=8&&peak>.002,'actual original surface vertices animate near fall');
  assert.equal(JSON.stringify(atlas),frozenSources[0]);
  assert.equal(JSON.stringify(bindings),frozenSources[1]);
  a.dispose();
});

test('Existing ordinary water clock continues under global calm; paused replay, budget and disposal are unchanged',()=>{
  const a=build(),pool=a.water.find(w=>w.kind==='pool');
  const river=a.water.find(w=>w.kind==='river'),swamp=a.water.find(w=>w.kind==='swamp');
  assert.deepEqual(Object.keys(pool.material.uniforms).sort(),Object.keys(river.material.uniforms).sort(),
    'no extra uniform, external signal, or paid renderer');
  assert.equal(a.water.filter(w=>w.kind==='pool').length,1);
  assert.equal(swamp.material.uniforms.uPlunge.value,0);
  const impactBlock=pool.material.vertexShader.split('if(uPlunge>.5){')[1].split('if(uPond>.5){')[0];
  assert.doesNotMatch(impactBlock,/\buStorm\b|\buWeather\b|\buGlobalCalm\b/i);
  for(const t of [1,3.4,7.2]){
    a.tick(t,{globalCalm:true,weatherMode:'GLOBAL_CALM',storm:0});
    assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===t));
  }
  a.tick(14,{paused:true,globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===7.2));
  let disposed=0;
  pool.mesh.geometry.addEventListener('dispose',()=>disposed++);
  a.dispose();a.dispose();
  assert.equal(disposed,1);
  assert.equal(JSON.stringify(bindings),frozenSources[1]);
});
