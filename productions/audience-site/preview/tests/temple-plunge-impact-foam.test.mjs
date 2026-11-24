import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const places=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,places,()=>2);
const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const impact=(u,v,t)=>{
 const r=Math.hypot((u-.5)*2,(v-.554)*2.2);
 const field=1-smooth(.13,.52,r);
 const crest=Math.max(0,Math.sin(r*34-t*2.8+Math.sin(u*19+t*.3)*.28))**9;
 const breakup=.45+.55*(.5+.5*Math.sin(u*27-v*17+t*.57));
 const boundary=1-smooth(.63,.94,Math.hypot((u-.5)*2,(v-.5)*2));
 return crest*breakup*field*boundary;
};

test('impact follows the existing waterfall landing rings, pool footprint and source bindings',()=>{
 const before=JSON.stringify(places),a=build();
 const pool=a.water.find(w=>w.kind==='pool');
 const fall=a.water.find(w=>w.kind==='waterfall');
 const ripples=a.water.filter(w=>w.kind==='landing-ripple');
 assert.ok(pool&&fall);assert.equal(ripples.length,4);
 assert.equal(a.water.filter(w=>w.kind==='pool').length,1);
 assert.deepEqual(pool.mesh.position.toArray(),[-5.8,.30,3]);
 assert.deepEqual(pool.mesh.scale.toArray(),[3.8,2.8,1]);
 assert.ok(Math.abs(fall.mesh.position.z-1.8)<1e-10);
 assert.ok(Math.abs(ripples[0].mesh.position.z-2.7)<1e-10);
 const landingUv=.5+(pool.mesh.position.z-ripples[0].mesh.position.z)/(2*2.8);
 assert.ok(Math.abs(landingUv-.554)<.001);
 const v=pool.mesh.geometry.getAttribute('position');
 assert.equal(v.count,321);
 assert.equal(pool.mesh.geometry.index.count,1800);
 for(let i=1+7*40;i<v.count;i++)assert.ok(Math.abs(Math.hypot(v.getX(i),v.getY(i))-1)<1e-6);
 assert.equal(JSON.stringify(places),before);
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 a.dispose();
});

test('impact foam is localized, numerically bounded, dynamic, and plunge-shader-only',()=>{
 const a=build(),pool=a.water.find(w=>w.kind==='pool'),f=pool.material.fragmentShader;
 const begin=f.indexOf('}else if(uPlunge>.5){'),end=f.indexOf('}else{',begin);
 assert.ok(begin>0&&end>begin);
 const scoped=f.slice(begin,end);
 for(const expression of [
  /impactUv=vec2\(\.5,\.554\)/,
  /impactOffset=\(vUv-impactUv\)\*vec2\(2\.,2\.2\)/,
  /impactField=1\.-smoothstep\(\.13,\.52,impactRadius\)/,
  /impactCoordinate=impactRadius\*34\.-uTime\*2\.8/,
  /impactCrest=pow\(max\(sin\(impactCoordinate\),0\.\),9\.\)/,
  /fwidth\(impactCoordinate\)/,
  /fwidth\(plungeRingCoordinate\)/,
  /impactFoam=impactCrest\*impactBreakup\*impactField/,
  /vec3\(\.10,\.15,\.13\)\*impactFoam\*boundary/,
  /gl_FragColor=vec4\(plungeTint,\.88\)/
 ]) assert.match(scoped,expression);
 assert.doesNotMatch(f.slice(0,begin)+f.slice(end),/impactFoam|impactRadius|impactOffset/);
 for(const w of a.water.filter(w=>w.kind!=='pool'))assert.equal(w.material.uniforms.uPlunge?.value??0,0);
 for(const t of [0,1.7,10.5])for(const [u,v] of [[.525,.47],[.5,.554],[.5,.62],[0,.5],[1,.5],[.5,0],[.5,1]]){
  const x=impact(u,v,t);
  assert.ok(Number.isFinite(x)&&x>=0&&x<=1.000001);
  if(u===0||u===1||v===0||v===1)assert.ok(Math.abs(x)<1e-12);
 }
 assert.ok(Math.abs(impact(.525,.47,0)-impact(.525,.47,1.7))>.01);
 assert.equal(impact(.9,.9,0),0);
 a.dispose();
});

test('Temple impact motion advances during global calm and stops only on explicit pause',()=>{
 const before=JSON.stringify(places),a=build(),pool=a.water.find(w=>w.kind==='pool');
 a.tick(2,{storm:0});assert.equal(pool.material.uniforms.uTime.value,2);
 a.tick(11,{storm:0});assert.equal(pool.material.uniforms.uTime.value,11);
 a.tick(19,{storm:0,paused:true});assert.equal(pool.material.uniforms.uTime.value,11);
 a.tick(21,{storm:0});assert.equal(pool.material.uniforms.uTime.value,21);
 assert.equal(JSON.stringify(places),before);
 a.dispose();a.dispose();
});


test('pool radial crest filtering preserves close motion and attenuates unresolved distant detail',()=>{
 const ring=(u,v,t)=>Math.hypot((u-.5)*2,(v-.5)*2*1.16)*31-t*2.1+.7*Math.sin(u*14+t*.35);
 const crest=(u,v,t)=>Math.hypot((u-.5)*2,(v-.554)*2.2)*34-t*2.8+.28*Math.sin(u*19+t*.3);
 const attenuation=(c,u,v,t,step)=>1-smooth(.35,1.15,Math.abs(c(u+step,v,t)-c(u,v,t))+Math.abs(c(u,v+step,t)-c(u,v,t)));
 let change=0;
 const samples=new Map([[ring,{n:0,filtered:0}],[crest,{n:0,filtered:0}]]);
 for(const [c,power] of [[ring,10],[crest,9]])for(let i=12;i<=28;i++)for(let j=12;j<=28;j++)for(const t of [0,1.7,8]){
  const u=i/40,v=j/40,near=attenuation(c,u,v,t,.002),far=attenuation(c,u,v,t,.05);
  assert.ok(near>.99);
  assert.ok(far>=0&&far<=1);
  const count=samples.get(c);count.n++;if(far<.1)count.filtered++;
  const optical=(time)=>Math.max(Math.sin(c(u,v,time)),0)**power*attenuation(c,u,v,time,.002);
  change=Math.max(change,Math.abs(optical(t)-optical(t+.43)));
 }
 // Radial phase can be stationary in a quad crossing the center; do not require
 // universal suppression there. On the sampled grid most coarse quads resolve neither crest.
 for(const count of samples.values())assert.ok(count.filtered/count.n>.9,JSON.stringify(count));
 assert.ok(change>.5,'ordinary water motion remains visible in resolved crests');
 const a=build(),p=a.water.find(w=>w.kind==='pool'),f=p.material.fragmentShader;
 const scoped=f.slice(f.indexOf('}else if(uPlunge>.5){'),f.indexOf('}else{',f.indexOf('}else if(uPlunge>.5){')));
 for(const coordinate of ['plungeRingCoordinate','impactCoordinate'])assert.ok(scoped.includes('*(1.-smoothstep(.35,1.15,fwidth('+coordinate+')))'));
 assert.ok(scoped.includes('foam=pow(scatter,3.)*plungeCore'));
 assert.ok(scoped.includes('plungeFacet=plungeSlope*(.35+.65*plungeGrazing)*boundary'));
 assert.ok(!p.material.vertexShader.includes('plungeRingCoordinate'));
 a.dispose();
});
