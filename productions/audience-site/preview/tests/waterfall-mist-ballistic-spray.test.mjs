import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(entry=>entry.id===id);
  assert.ok(p, 'missing authoritative Atlas place: '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const temple=a=>a.locations.find(l=>l.id===ids[0]).group;
const mist=a=>temple(a).getObjectByName('Candidate waterfall plunge mist');
const sprayHeight=(age,driftY)=>age*(.95+.35*driftY)-age*age*(.90+.20*driftY);
function displacement(phase,drift,time){
  const age=((phase+time*(.105+.048*drift[1]))%1+1)%1;
  return [
    drift[0]*age*(.12+.34*age)+Math.sin(time*.31+phase*35)*.08*age,
    sprayHeight(age,drift[1]),
    drift[2]*age*(.10+.32*age)
  ];
}

test('Temple uses the SAME one-draw localized mist emitter and keeps Atlas identity immutable',()=>{
  const before=JSON.stringify(atlas),bindingBefore=JSON.stringify(bindings),a=build(),m=mist(a);
  const p=m.geometry.getAttribute('position'),phase=m.geometry.getAttribute('aPhase'),drift=m.geometry.getAttribute('aDrift');
  assert.equal(atlas.locations.find(l=>l.id===ids[0]).canon_status,'PERMANENT_CANON');
  assert.ok(atlas.locations.find(l=>l.id===ids[0]).persistent_landmarks.includes('waterfall'));
  assert.ok(m.isPoints);assert.equal(p.count,144);assert.equal(phase.count,144);assert.equal(drift.count,144);
  assert.equal(m.material.isShaderMaterial,true);
  assert.deepEqual(Object.keys(m.material.uniforms),['uTime','uLightLevel','uPixelRatio']);
  assert.equal(a.root.getObjectsByProperty('name','Candidate waterfall plunge mist').length,1);
  assert.equal(m.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(m.userData.sourceLandmark,'waterfall');
  assert.equal(m.userData.navigable,false);assert.deepEqual(m.userData.routeIds,[]);
  for(const l of a.locations.filter(l=>l.id!==ids[0]))
    assert.equal(l.group.getObjectByName(m.name),undefined);
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),before);assert.equal(JSON.stringify(bindings),bindingBefore);
  a.dispose();
});

test('real imported mist shader launches and falls, within the previous local spray envelope',()=>{
  const a=build(),m=mist(a),v=m.material.vertexShader,f=m.material.fragmentShader;
  for(const s of [
    'float age=fract(aPhase+uTime*(.105+.048*aDrift.y))',
    'float launch=age*(.95+.35*aDrift.y)',
    'float fall=age*age*(.90+.20*aDrift.y)',
    'p.x+=aDrift.x*age*(.12+.34*age)',
    '+sin(uTime*.31+aPhase*35.)*.08*age',
    'p.y+=launch-fall',
    'p.z+=aDrift.z*age*(.10+.32*age)'
  ])assert.ok(v.includes(s),s);
  assert.doesNotMatch(v,/\buStorm\b|\buWeather\b|\buGlobalCalm\b|\buRain\b/);
  assert.match(f,/gl_PointCoord/);
  assert.match(f,/smoothstep\(\.08,\.49,radial\)/);
  for(let driftY=0;driftY<=1;driftY+=.05){
    assert.equal(sprayHeight(0,driftY),0,'new particle starts at its existing emitter');
    assert.ok(sprayHeight(.4,driftY)>sprayHeight(.9,driftY),'droplets descend after their apex');
    assert.ok(sprayHeight(1,driftY)>=.049999,'short lifetime ends near its original emitter');
  }
  const positions=m.geometry.getAttribute('position'),phases=m.geometry.getAttribute('aPhase'),
    drifts=m.geometry.getAttribute('aDrift');
  let changed=false,highest=0;
  for(let i=0;i<positions.count;i++){
    const phase=phases.getX(i),d=[drifts.getX(i),drifts.getY(i),drifts.getZ(i)];
    assert.ok(d[1]>=0&&d[1]<=1);
    for(const time of [0,.4,2.1,7.4,19.3,40.9]){
      const p=displacement(phase,d,time),again=displacement(phase,d,time);
      assert.deepEqual(p,again,'reproducible shader-time trajectory');
      assert.ok(p.every(Number.isFinite));
      assert.ok(Math.abs(p[0])<=.540001&&p[1]>=0&&p[1]<=.400001&&Math.abs(p[2])<=.420001,
        'spray displacement remains inside a tightly bounded local envelope');
      highest=Math.max(highest,p[1]);
    }
    const a1=displacement(phase,d,1.8),b=displacement(phase,d,2.8);
    if(Math.abs(a1[1]-b[1])>.0001)changed=true;
  }
  assert.ok(changed,'spray movement is not frozen');
  assert.ok(highest>.25,'visible upward and falling mist span');
  assert.equal(m.material.transparent,true);assert.equal(m.material.depthWrite,false);
  a.dispose();
});

test('El Niño global calm preserves ordinary spray/fall/pool motion; explicit pause freezes, disposal is once',()=>{
  const before=JSON.stringify(bindings),a=build(),m=mist(a);
  const templeWater=a.water.filter(w=>['waterfall','pool','landing-ripple'].includes(w.kind));
  assert.equal(templeWater.length,6);
  let geoDisposals=0,materialDisposals=0;
  m.geometry.addEventListener('dispose',()=>geoDisposals++);
  m.material.addEventListener('dispose',()=>materialDisposals++);
  a.tick(2,{storm:0,globalCalm:true});
  assert.equal(m.material.uniforms.uTime.value,2);
  for(const w of templeWater)assert.equal(w.material.uniforms.uTime.value,2);
  a.tick(8,{storm:0,globalCalm:true});
  assert.equal(m.material.uniforms.uTime.value,8);
  for(const w of templeWater)assert.equal(w.material.uniforms.uTime.value,8);
  a.tick(12,{storm:0,globalCalm:true,paused:true});
  assert.equal(m.material.uniforms.uTime.value,8);
  for(const w of templeWater)assert.equal(w.material.uniforms.uTime.value,8);
  a.tick(16,{storm:0,globalCalm:true});
  assert.equal(m.material.uniforms.uTime.value,16);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();a.dispose();
  assert.equal(geoDisposals,1);assert.equal(materialDisposals,1);
});
