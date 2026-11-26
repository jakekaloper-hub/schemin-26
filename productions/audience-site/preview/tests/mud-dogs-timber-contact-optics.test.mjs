import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
test('timber contact optics are anchored to the actual immersed mesh and isolated to its existing swamp',()=>{
 const before=JSON.stringify(bindings),a=buildRegionalAssets(THREE,bindings,()=>2);
 try{
  const w=a.water.find(w=>w.kind==='swamp'),u=w.material.uniforms;
  const o=a.locations.find(l=>l.id===bindings[0].id).group.getObjectByName('Candidate Mud Dogs recessed fallen timber');
  const half=o.geometry.parameters.height/2;
  const p=new THREE.Vector3(0,-half,0).applyQuaternion(o.quaternion).add(o.position);
  const q=new THREE.Vector3(0,half,0).applyQuaternion(o.quaternion).add(o.position);
  assert.equal(u.uTimberContact.value,1);
  const actual=u.uTimberSegment.value.toArray();
  [p.x,p.z,q.x,q.z].forEach((v,i)=>assert.ok(Math.abs(v-actual[i])<1e-6));
  for(const other of a.water.filter(x=>x!==w))assert.equal(other.material.uniforms.uTimberContact?.value??0,0);
  const f=w.material.fragmentShader;
  for(const part of ['if(uTimberContact>.5)','vec2(21.,-16.4)','timberDistance*15.-uTime*1.8+timberAlong*9.','fwidth(timberPhase)','contactTint*=1.-.055*timberNear*bankFade','vec3(.052,.072,.059)*timberBand*timberCrest*bankFade'])assert.ok(f.includes(part),part);
  assert.doesNotMatch(w.material.vertexShader,/uTimber|timberDistance/);
  assert.equal(w.mesh.geometry.getAttribute('position').count,385);
  assert.equal(w.mesh.geometry.index.count,2160);
  a.tick(2,{globalCalm:true,storm:0});a.tick(6,{globalCalm:true,storm:0});assert.equal(u.uTime.value,6);
  a.tick(10,{globalCalm:true,storm:0,paused:true});assert.equal(u.uTime.value,6);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 }finally{a.dispose();}
});

// Independent CPU reference of the fragment-only mask, not a rendered/GPU assertion.
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function optics(x,z,time,footprint){
 const ax=-5,az=1,dx=5,dz=3;
 const along=Math.max(0,Math.min(1,((x-ax)*dx+(z-az)*dz)/(dx*dx+dz*dz)));
 const distance=Math.hypot(x-ax-dx*along,z-az-dz*along);
 const near=1-smooth(.17,.68,distance);
 const band=smooth(.14,.27,distance)*(1-smooth(.45,.85,distance));
 const phase=distance*15-time*1.8+along*9;
 const crest=Math.max(Math.sin(phase),0)**6*(1-smooth(.35,1.15,footprint));
 const bank=1-smooth(.78,.99,Math.hypot(x/10.5,z/8.2));
 return {distance,darken:.055*near*bank,light:.072*band*crest*bank};
}
test('contact optical reference is bounded, moves on ordinary time, and vanishes off the existing timber',()=>{
 let samples=0,motion=0;
 for(let i=0;i<=40;i++)for(const sign of [-1,1])for(const offset of [0,.17,.27,.4,.55,.7,.85,1.2])for(const t of [0,1,3,8]){
  const x=-5+5*i/40-sign*offset*3/Math.sqrt(34),z=1+3*i/40+sign*offset*5/Math.sqrt(34);
  const p=optics(x,z,t,.1),q=optics(x,z,t+.5,.1);
  assert.ok(Math.abs(p.distance-offset)<1e-10);
  assert.ok(p.darken>=0&&p.darken<=.055&&p.light>=0&&p.light<=.072);
  if(offset>=.85){assert.ok(p.darken<1e-12);assert.ok(p.light<1e-12);}
  assert.equal(optics(x,z,t,1.2).light,0);
  motion=Math.max(motion,Math.abs(p.light-q.light));samples++;
 }
 assert.ok(motion>.02);
 console.log('TIMBER_OPTICS_CPU',JSON.stringify({samples,resolvedMotion:motion,maximumDarkening:.055,maximumGreenLight:.072}));
});
