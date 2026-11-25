import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function shadowAt(x,z,time) {
  // Same normalized x/z world-to-pond footprint as the single existing pond disc.
  const p=[x/3.8,z/2.3],radius=Math.hypot(...p);
  const bank=1-smooth(.68,.95,radius);
  const bridgeDeckShadow=(1-smooth(.14,.27,Math.abs(p[0])))
    *(1-smooth(.62,.96,Math.abs(p[1])))*bank;
  const bridgeShadowDapple=.90+.10*(.5+.5*Math.sin(p[1]*27-time*.59+p[0]*13));
  return .17*bridgeDeckShadow*bridgeShadowDapple;
}

test('one original Jackson pond shades only under the inherited non-navigable arch deck',()=>{
  const source=JSON.stringify(bindings),scene=build();
  const pond=scene.water.find(w=>w.kind==='pond');
  const jackson=scene.locations.find(l=>l.id==='LOC-COUNTRY-CLUB-JACKSON');
  assert.ok(pond&&jackson);
  const bridge=jackson.group.getObjectByName('Candidate Week 9 pond-side stone arch');
  assert.ok(bridge);
  assert.deepEqual(bridge.position.toArray(),[7,.1,6]);
  assert.equal(bridge.children.length,17);
  assert.equal(bridge.userData.navigable,false);
  assert.deepEqual(bridge.userData.routeIds,[]);
  assert.deepEqual(pond.mesh.position.toArray(),[7,.06,6]);
  assert.deepEqual(pond.mesh.scale.toArray(),[3.8,2.3,1]);
  assert.equal(pond.mesh.geometry.getAttribute('position').count,321);
  assert.equal(pond.mesh.geometry.index.count,1800);
  assert.equal(scene.worldMutationAllowed,false);
  assert.deepEqual(scene.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),source);
  scene.dispose();
});

test('single-material pond underpass shade is bounded, soft, broken and isolated',()=>{
  const scene=build(),pond=scene.water.find(w=>w.kind==='pond');
  const vertex=pond.material.vertexShader,fragment=pond.material.fragmentShader;
  assert.match(fragment,/float bridgeDeckShadow=\(1\.-smoothstep\(\.14,\.27,abs\(p\.x\)\)\)/);
  assert.match(fragment,/\*\(1\.-smoothstep\(\.62,\.96,abs\(p\.y\)\)\)\*bank/);
  assert.match(fragment,/float bridgeShadowPhase=p\.y\*27\.-uTime\*\.59\+p\.x\*13\.;/);
  assert.match(fragment,/float bridgeShadowDapple=\.90\+\.10\*\(\.5\+\.5\*sin\(bridgeShadowPhase\)\)/);
  assert.match(fragment,/bridgeShadowDapple=mix\(bridgeShadowDapple,\.95,smoothstep\(\.35,1\.15,fwidth\(bridgeShadowPhase\)\)\)/);
  assert.match(fragment,/pondTint\*=1\.-\.17\*bridgeDeckShadow\*bridgeShadowDapple/);
  assert.match(fragment,/bridgeMirrorMix/);
  assert.match(vertex,/bridgeDistA/);
  const uniformNames=Object.keys(pond.material.uniforms).sort();
  const primaryWater=scene.water.filter(w=>w.kind!=='landing-ripple');
  assert.deepEqual(primaryWater.map(w=>Object.keys(w.material.uniforms).sort()),
    primaryWater.map(()=>uniformNames));
  for(const water of scene.water.filter(w=>w.kind!=='pond')) {
    assert.equal(water.material.uniforms.uPond?.value??0,0);
    assert.doesNotMatch(water.material.vertexShader,/bridgeDeckShadow/);
  }
  for(const shader of [vertex,fragment])assert.doesNotMatch(shader,/\buStorm\b|\buWeather\b/i);
  for(const time of [0,2.3,9.5]) {
    const under=shadowAt(0,.15,time),edge=shadowAt(.77,.15,time);
    assert.ok(under>.14&&under<.18);
    assert.ok(edge>0&&edge<under,'feathering on original deck width');
    assert.equal(shadowAt(1.2,.15,time),0,'outside deck');
    assert.equal(shadowAt(0,2.28,time),0,'outside inner pond bank');
    assert.ok(shadowAt(0,.15,time)<=.17,'never over-darkens');
  }
  assert.ok(Math.abs(shadowAt(0,.31,0)-shadowAt(0,.31,2.3))>.0005,
    'small ordinary-clock breakup evolves beneath stationary bridge');
  scene.dispose();
});

test('water time survives global calm, explicit pause and once-only disposal',()=>{
  const source=JSON.stringify(bindings),scene=build();
  assert.deepEqual(scene.water.filter(w=>w.kind!=='landing-ripple').map(w=>w.kind).sort(),
    ['channel','pond','pool','river','swamp','waterfall']);
  assert.equal(scene.water.filter(w=>w.kind==='landing-ripple').length,4);
  scene.tick(3,{storm:0});
  assert.ok(scene.water.every(w=>w.material.uniforms.uTime.value===3));
  scene.tick(8,{storm:0});
  assert.ok(scene.water.every(w=>w.material.uniforms.uTime.value===8));
  scene.tick(12,{storm:0,paused:true});
  assert.ok(scene.water.every(w=>w.material.uniforms.uTime.value===8));
  scene.tick(13,{storm:0});
  assert.ok(scene.water.every(w=>w.material.uniforms.uTime.value===13));
  assert.equal(JSON.stringify(bindings),source);
  scene.dispose();scene.dispose();
});
