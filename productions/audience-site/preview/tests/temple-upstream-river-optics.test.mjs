import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const places=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall','temple stone','dense vegetation']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','golf grounds','water hazards']}
];
const build=()=>buildRegionalAssets(THREE,places,()=>2);
const smooth=(a,b,v)=>{const p=Math.max(0,Math.min(1,(v-a)/(b-a)));return p*p*(3-2*p);};
const foam=(u,v,t)=>{
 const y=v-t*.023;
 const interior=1-smooth(.72,.96,Math.hypot((u-.5)*2,(v-.5)*2));
 return Math.max(Math.sin(u*42+Math.sin(y*13)*.7),0)**14
   *smooth(.47,.86,.5+.5*Math.sin(y*29+u*6-t*.72))*interior;
};
const slope=normal=>{
 const mag=Math.hypot(...normal),y=mag>.00001?normal[1]/mag:1;
 return Math.min(.32,Math.max(0,(1-Math.min(1,Math.abs(y)))*12));
};

test('Temple upstream river optical flow stays inside one source-bounded existing water body',()=>{
 const before=JSON.stringify(places),a=build(),rivers=a.water.filter(w=>w.kind==='river');
 assert.equal(rivers.length,1);
 const {mesh,material}=rivers[0];
 assert.deepEqual(mesh.position.toArray(),[-5.8,7.2,-1.5]);
 assert.deepEqual(mesh.scale.toArray(),[2.2,2.6,1]);
 assert.equal(mesh.rotation.x,-Math.PI/2);
 assert.equal(mesh.geometry.name,'Candidate Temple upstream river surface');
 assert.equal(mesh.geometry.getAttribute('position').count,385);
 assert.equal(mesh.geometry.index.count,2160);
 assert.equal(material.transparent,true);assert.equal(material.depthWrite,false);
 assert.equal(material.uniforms.uRiver.value,1);
 const shader=material.fragmentShader;
 const start=shader.indexOf('}else if(uRiver>.5){'),end=shader.indexOf('}else if(uPond>.5){',start);
 assert.ok(start>=0&&end>start);
 const region=shader.slice(start,end);
 for(const fragment of [
   'runningUv=vUv+vec2(0.,-uTime*.023)',
   'riverInterior=1.-smoothstep(.72,.96,length((vUv-vec2(.5))*2.))',
   'riverFace=cross(dFdx(vWorld),dFdy(vWorld))',
   'riverNormal=riverFaceSize>.00001?riverFace/riverFaceSize:vec3(0.,1.,0.)',
   'riverSlope=clamp((1.-clamp(abs(riverNormal.y),0.,1.))*12.,0.,.32)',
   'riverGrazing=pow(1.-clamp(abs(dot(riverNormal,riverEye)),0.,1.),2.)',
   'runCoordinate=runningUv.y*44.+sin(runningUv.x*11.)*1.15',
   'runGlint=pow(max(broken,0.),11.)',
   '*(1.-smoothstep(.35,1.15,fwidth(runCoordinate)))',
   'riverFoamCoordinate=runningUv.x*42.+sin(runningUv.y*13.)*.7',
   'riverFoamLine=pow(max(sin(riverFoamCoordinate),0.),14.)',
   '*(1.-smoothstep(.35,1.15,fwidth(riverFoamCoordinate)))',
   'riverFoamBreak=smoothstep(.47,.86,.5+.5*sin(runningUv.y*29.+vUv.x*6.-uTime*.72))',
   'riverFoam=riverFoamLine*riverFoamBreak*riverInterior',
   'gl_FragColor=vec4(clamp(uColor+vec3(.10,.15,.13)*(runGlint*riverInterior)+riverOptics,0.,1.),.88)'
 ])assert.ok(region.includes(fragment),fragment);
 for(const term of ['uStorm','uWeather','uRain','uGlobalCalm'])assert.ok(!region.includes(term),term);
 for(const w of a.water.filter(w=>w.kind!=='river'))assert.equal(w.material.uniforms.uRiver?.value??0,0);
 assert.deepEqual(a.locations.map(l=>l.id),places.map(p=>p.id));
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(places),before);
 a.dispose();
});

test('broken traveling sheen is bounded, animated, deterministic and leaves shoreline unlit',()=>{
 let peak=0,change=0;
 for(let i=0;i<=40;i++)for(let j=0;j<=40;j++){
  const u=i/40,v=j/40;
  for(const t of [0,1.9,8]){
   const value=foam(u,v,t),later=foam(u,v,t+.31);
   assert.ok(Number.isFinite(value)&&value>=0&&value<=1.000001);
   assert.ok(Number.isFinite(later)&&later>=0&&later<=1.000001);
   if(Math.hypot((u-.5)*2,(v-.5)*2)>=.96)assert.ok(value<1e-12);
   peak=Math.max(peak,value);change=Math.max(change,Math.abs(value-later));
  }
 }
 assert.ok(peak>.7,'thin foam exists in the river interior');
 assert.ok(change>.1,'normal water clock visibly advects the broken foam');
 assert.ok(peak*.085<=.0850001,'RGB increment remains restrained');
 for(const n of [[0,1,0],[0,-1,0],[.2,.98,.12],[.55,.72,.4],[0,0,0]]){
  assert.ok(slope(n)>=0&&slope(n)<=.32);
  assert.ok(Math.abs(slope(n)-slope(n.map(x=>-x)))<1e-12);
 }
 assert.equal(slope([0,1,0]),0);
 assert.ok(slope([.2,.98,.12])>0);
});

test('El Nino global calm does not freeze ordinary river movement; explicit pause and disposal are correct',()=>{
 const before=JSON.stringify(places),a=build(),river=a.water.find(w=>w.kind==='river');
 let geoDisposals=0,matDisposals=0;
 river.mesh.geometry.addEventListener('dispose',()=>geoDisposals++);
 river.material.addEventListener('dispose',()=>matDisposals++);
 a.tick(2,{storm:0,globalCalm:true});assert.equal(river.material.uniforms.uTime.value,2);
 a.tick(6.5,{storm:0,globalCalm:true});assert.equal(river.material.uniforms.uTime.value,6.5);
 a.tick(8,{storm:0,globalCalm:true,paused:true});assert.equal(river.material.uniforms.uTime.value,6.5);
 a.tick(11,{storm:0,globalCalm:true});assert.equal(river.material.uniforms.uTime.value,11);
 assert.equal(JSON.stringify(places),before);
 a.dispose();a.dispose();
 assert.equal(geoDisposals,1);assert.equal(matDisposals,1);
});

test('river narrow optical crests retain near detail and ordinary motion but fade at coarse footprints',()=>{
 const coordinates=[
  (u,v,t)=>(v-t*.023)*44+Math.sin(u*11)*1.15,
  (u,v,t)=>u*42+Math.sin((v-t*.023)*13)*.7
 ];
 const attenuation=(c,u,v,t,step)=>1-smooth(.35,1.15,
   Math.abs(c(u+step,v,t)-c(u,v,t))+Math.abs(c(u,v+step,t)-c(u,v,t)));
 let change=0;
 for(const c of coordinates)for(let i=8;i<33;i++)for(let j=8;j<33;j++)for(const t of [0,1.9,8]){
  const u=i/40,v=j/40,near=attenuation(c,u,v,t,.002),far=attenuation(c,u,v,t,.05);
  assert.ok(near>.99);
  assert.equal(far,0);
  change=Math.max(change,Math.abs(foam(u,v,t)*near-foam(u,v,t+.31)*attenuation(c,u,v,t+.31,.002)));
 }
 assert.ok(change>.1);
 const a=build(),w=a.water.find(w=>w.kind==='river');
 assert.ok(!w.material.vertexShader.includes('riverFoamCoordinate'));
 assert.ok(w.material.fragmentShader.includes('riverSlope*(.45+.55*riverGrazing)*riverInterior'));
 a.dispose();
});
