import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const places=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall','temple stone','dense vegetation']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','water hazards']}
];
const build=()=>buildRegionalAssets(THREE,places,()=>2);
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const smooth=(a,b,x)=>{const t=clamp((x-a)/(b-a),0,1);return t*t*(3-2*t);};
const wake=(u,v,t)=>{
 const dx=(u-.5)*2,dy=(v-.554)*2.2,r=Math.hypot(dx,dy);
 const spoke=Math.max(Math.sin(Math.atan2(dy,dx)*6+r*28-t*1.64),0)**12;
 const broken=Math.sqrt(.5+.5*Math.sin(r*37-t*2.28+u*19));
 const rim=1-smooth(.63,.94,Math.hypot((u-.5)*2,(v-.5)*2));
 return spoke*broken*smooth(.20,.34,r)*(1-smooth(.59,.76,r))*rim;
};
const facet=(normal,eye=[.3,.8,.1],bank=1)=>{
 const norm=v=>{const m=Math.hypot(...v);return m>.00001?v.map(x=>x/m):[0,1,0];};
 const n=norm(normal),e=norm(eye);
 const slope=clamp((1-clamp(Math.abs(n[1]),0,1))*15,0,.34);
 const g=(1-clamp(Math.abs(n.reduce((s,x,i)=>s+x*e[i],0)),0,1))**2;
 return slope*(.35+.65*g)*bank;
};

test('Temple receiving-pool optical wake is geometrically sourced, local, with original footprint',()=>{
 const before=JSON.stringify(places),a=build(),p=a.water.find(w=>w.kind==='pool');
 assert.equal(a.water.filter(w=>w.kind==='pool').length,1);
 assert.deepEqual(p.mesh.position.toArray(),[-5.8,.30,3]);
 assert.deepEqual(p.mesh.scale.toArray(),[3.8,2.8,1]);
 assert.equal(p.mesh.geometry.name,'Candidate Temple plunge pool surface');
 assert.equal(p.mesh.geometry.getAttribute('position').count,321);
 assert.equal(p.mesh.geometry.index.count,1800);
 assert.equal(p.material.uniforms.uPlunge.value,1);
 assert.equal(p.material.transparent,true);assert.equal(p.material.depthWrite,false);
 const shader=p.material.fragmentShader,b=shader.indexOf('}else if(uPlunge>.5){'),e=shader.indexOf('}else{',b);
 assert.ok(b>=0&&e>b);const scoped=shader.slice(b,e);
 for(const x of [
  'plungeFace=cross(dFdx(vWorld),dFdy(vWorld))',
  'plungeNormal=plungeFaceSize>.00001?plungeFace/plungeFaceSize:vec3(0.,1.,0.)',
  'plungeSlope=clamp((1.-clamp(abs(plungeNormal.y),0.,1.))*15.,0.,.34)',
  'plungeGrazing=pow(1.-clamp(abs(dot(plungeNormal,plungeEye)),0.,1.),2.)',
  'plungeFacet=plungeSlope*(.35+.65*plungeGrazing)*boundary',
  'wakeUv=(vUv-impactUv)*vec2(2.,2.2)',
  'wakeSpoke=pow(max(sin(atan(wakeUv.y,wakeUv.x)*6.+impactRadius*28.-uTime*1.64),0.),12.)',
  'wakeField=smoothstep(.20,.34,impactRadius)',
  'wakeGlint=wakeSpoke*sqrt(wakeBreak)*wakeField',
  'plungeTint=clamp(plungeTint+vec3(.062,.088,.074)*plungeFacet',
  'gl_FragColor=vec4(plungeTint,.88)'
 ])assert.ok(scoped.includes(x),x);
 assert.doesNotMatch(scoped,/uStorm|uWeather|uRain|uGlobalCalm/);
 assert.doesNotMatch(shader.slice(0,b)+shader.slice(e),/plungeFacet|wakeSpoke|wakeGlint/);
 for(const w of a.water.filter(w=>w.kind!=='pool'))
  assert.equal(w.material.uniforms.uPlunge?.value??0,0,'isolation '+w.kind);
 assert.deepEqual(a.locations.map(l=>l.id),places.map(l=>l.id));
 assert.deepEqual(a.principalCharacters,[]);assert.equal(a.worldMutationAllowed,false);
 assert.equal(JSON.stringify(places),before);a.dispose();
});
test('geometry-facing highlight and water-time foam are bounded, deterministic and bank-faded',()=>{
 let peak=0,change=0;
 for(let i=0;i<=40;i++)for(let j=0;j<=40;j++){
  const u=i/40,v=j/40;
  for(const t of [0,1.7,8.1]){
   const x=wake(u,v,t),later=wake(u,v,t+.43);
   assert.ok(Number.isFinite(x)&&x>=0&&x<=1.000001);
   assert.ok(Number.isFinite(later)&&later>=0&&later<=1.000001);
   if(Math.hypot((u-.5)*2,(v-.5)*2)>=.94)assert.ok(x<1e-12);
   peak=Math.max(peak,x);change=Math.max(change,Math.abs(x-later));
  }
 }
 assert.ok(peak>.45);assert.ok(change>.2);assert.ok(peak*.063<=.0630001);
 for(const n of [[0,1,0],[0,-1,0],[.24,.95,.11],[.8,.4,.1],[0,0,0]]){
  const x=facet(n),reverse=facet(n.map(v=>-v));
  assert.ok(Number.isFinite(x)&&x>=0&&x<=.34+1e-12);
  assert.ok(Math.abs(x-reverse)<1e-12);
  assert.equal(facet(n,[.3,.8,.1],0),0);
 }
 assert.equal(facet([0,1,0]),0);assert.ok(facet([.24,.95,.11])>0);
});
test('El Niño global calm advances ordinary waterfall/river/pool water; pause and disposal safe',()=>{
 const before=JSON.stringify(places),a=build(),p=a.water.find(w=>w.kind==='pool');
 const river=a.water.find(w=>w.kind==='river'),fall=a.water.find(w=>w.kind==='waterfall');
 let ge=0,ma=0;p.mesh.geometry.addEventListener('dispose',()=>ge++);
 p.material.addEventListener('dispose',()=>ma++);
 for(const [t,opts,expected] of [
  [2,{globalCalm:true,storm:0},2],
  [6,{globalCalm:true,storm:0},6],
  [9,{globalCalm:true,paused:true},6],
  [11,{globalCalm:true},11]
 ]){
  a.tick(t,opts);assert.deepEqual([p,river,fall].map(w=>w.material.uniforms.uTime.value),[expected,expected,expected]);
 }
 a.dispose();a.dispose();assert.equal(ge,1);assert.equal(ma,1);
 assert.equal(JSON.stringify(places),before);
});
