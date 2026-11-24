import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(place=>place.id===id);
  assert.ok(p,'missing source Atlas location '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const beforeAtlas=JSON.stringify(atlas),beforeBindings=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const mist=a=>a.locations.find(l=>l.id===ids[0]).group.getObjectByName('Candidate waterfall plunge mist');
const clamp=x=>Math.max(0,Math.min(1,x));
const smooth=(a,b,x)=>{const t=clamp((x-a)/(b-a));return t*t*(3-2*t);};
function projectedAxis(age,drift,viewYaw=0){
  const tangent=[
    drift[0]*(.12+.68*age),
    (.95+.35*drift[1])-2*age*(.90+.20*drift[1]),
    drift[2]*(.10+.64*age)
  ];
  const horizontal=tangent[0]*Math.cos(viewYaw)-tangent[2]*Math.sin(viewYaw);
  const length=Math.hypot(horizontal,tangent[1]);
  return length>.0001?[horizontal/length,tangent[1]/length]:[0,1];
}
function optical(point,axis,age,driftY,depth=12){
  const coord=[point[0]-.5,point[1]-.5];
  const normal=[-axis[1],axis[0]];
  const radial=Math.hypot((coord[0]*axis[0]+coord[1]*axis[1])*.98,
    (coord[0]*normal[0]+coord[1]*normal[1])*1.45);
  const core=1-smooth(.02,.30,radial);
  const feather=1-smooth(.08,.49,radial);
  const opacity=Math.pow(Math.max(Math.sin(age*Math.PI),0),.75)*(.50+.38*driftY);
  return feather*opacity*(.16+.07*core)*(1-.25*smooth(7,85,depth));
}

test('source-bound Temple mist remains one original 144-point draw with unchanged materials and climate authority',()=>{
  const a=build(),o=mist(a),g=o.geometry;
  assert.equal(atlas.locations.find(l=>l.id===ids[0]).canon_status,'PERMANENT_CANON');
  assert.ok(atlas.locations.find(l=>l.id===ids[0]).persistent_landmarks.includes('waterfall'));
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(a.root.getObjectsByProperty('name',o.name).length,1);
  assert.ok(o.isPoints);
  assert.equal(g.getAttribute('position').count,144);
  assert.equal(g.getAttribute('aPhase').count,144);
  assert.equal(g.getAttribute('aDrift').count,144);
  assert.deepEqual(Object.keys(o.material.uniforms),['uTime','uLightLevel']);
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(o.userData.navigable,false);
  assert.deepEqual(o.userData.routeIds,[]);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(a.worldMutationAllowed,false);
  for(const l of a.locations.filter(l=>l.id!==ids[0]))assert.equal(l.group.getObjectByName(o.name),undefined);
  assert.equal(JSON.stringify(bindings),beforeBindings);
  assert.equal(JSON.stringify(atlas),beforeAtlas);
  a.dispose();
});

test('imported shaders orient the existing soft droplet along projected ballistic velocity with finite, fully feathered bounds',()=>{
  const a=build(),o=mist(a),v=o.material.vertexShader,f=o.material.fragmentShader;
  for(const fragment of ['varying vec2 vSprayAxis',
    'vec3 tangent=vec3(aDrift.x*(.12+.68*age)',
    'vec2 screenTangent=(modelViewMatrix*vec4(tangent,0.)).xy',
    'vSprayAxis=length(screenTangent)>.0001?normalize(screenTangent):vec2(0.,1.)',
    'dot(drop,vSprayAxis)*.98','dot(drop,transverse)*1.45',
    'float core=1.-smoothstep(.02,.30,radial)',
    'float feather=1.-smoothstep(.08,.49,radial)']){
    assert.ok((v+f).includes(fragment),'missing physically oriented optical contract: '+fragment);
  }
  assert.doesNotMatch(v+f,/\buStorm\b|\buWeather\b|\buRain\b|\buGlobalCalm\b/);
  const drift=o.geometry.getAttribute('aDrift');
  let ageShift=false,viewShift=false,nonzero=0;
  for(let i=0;i<drift.count;i++){
    const d=[drift.getX(i),drift.getY(i),drift.getZ(i)];
    const early=projectedAxis(.2,d),late=projectedAxis(.85,d),yaw=projectedAxis(.2,d,.75);
    assert.ok([...early,...late,...yaw].every(Number.isFinite));
    assert.ok(Math.abs(Math.hypot(...early)-1)<.000001);
    if(Math.hypot(early[0]-late[0],early[1]-late[1])>.06)ageShift=true;
    if(Math.hypot(early[0]-yaw[0],early[1]-yaw[1])>.06)viewShift=true;
    for(const age of [.2,.48,.85])for(const point of [[.5,.5],[.5,.25],[.75,.5],[.33,.67],[0,.5],[1,.5],[.5,0],[.5,1],[0,0],[1,1]]){
      const alpha=optical(point,projectedAxis(age,d),age,d[1]);
      assert.ok(Number.isFinite(alpha)&&alpha>=0&&alpha<=.230001,'finite bounded optical sprite');
      if(point[0]===0||point[0]===1||point[1]===0||point[1]===1)
        assert.ok(alpha<1e-10,'no squared point boundary bleed');
      if(alpha>.01)nonzero++;
    }
  }
  assert.ok(ageShift,'projected droplet tilts with ballistic phase');
  assert.ok(viewShift,'same source droplet responds to spectator viewpoint');
  assert.ok(nonzero>300,'nontrivial visible feathered sprite interior');
  a.dispose();
});

test('one-draw sprite survives batching; global weather calm does not freeze spray/water and explicit pause/disposal still work',()=>{
  const a=build(),o=mist(a),temple=a.locations.find(l=>l.id===ids[0]).group;
  const startCount=temple.children.length;
  const batches=batchStaticGeometry(THREE,temple);
  assert.ok(temple.children.length<startCount);
  assert.ok(temple.children.includes(o));
  for(const geo of batches.geometries)geo.dispose();
  let gDisposed=0,mDisposed=0;
  o.geometry.addEventListener('dispose',()=>gDisposed++);
  o.material.addEventListener('dispose',()=>mDisposed++);
  const ordinary=a.water.filter(w=>['waterfall','river','pool','swamp','channel','pond'].includes(w.kind));
  assert.equal(ordinary.length,6);
  a.tick(3,{globalCalm:true,storm:0});
  a.tick(9,{globalCalm:true,storm:0});
  assert.equal(o.material.uniforms.uTime.value,9);
  assert.ok(ordinary.every(w=>w.material.uniforms.uTime.value===9));
  a.tick(13,{globalCalm:true,storm:0,paused:true});
  assert.equal(o.material.uniforms.uTime.value,9);
  a.tick(17,{globalCalm:true,storm:0});
  assert.equal(o.material.uniforms.uTime.value,17);
  assert.ok(ordinary.every(w=>w.material.uniforms.uTime.value===17));
  a.dispose();a.dispose();a.tick(30);
  assert.equal(gDisposed,1);assert.equal(mDisposed,1);
  assert.equal(JSON.stringify(atlas),beforeAtlas);
  assert.equal(JSON.stringify(bindings),beforeBindings);
});
