import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall','temple stone','dense vegetation']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','golf grounds','water hazards']}
];
const before=JSON.stringify(bindings);
const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const alpha=(u,v,t)=>{
 const lateralEdge=smooth(0,.16,u)*(1-smooth(.84,1,u));
 const spanHold=smooth(.02,.12,v)*(1-smooth(.88,.98,v));
 const edgeFlutter=.55+.45*Math.sin(v*31-t*2.1+Math.sin(u*9)*.65);
 return .88*(1-.50*(1-lateralEdge)*spanHold*edgeFlutter);
};

test('Three/WebGL2 Temple waterfall source has bounded lateral alpha with unchanged sheet geometry',()=>{
 const a=buildRegionalAssets(THREE,bindings,()=>2);
 const fall=a.water.find(w=>w.kind==='waterfall');
 assert.ok(fall);
 assert.equal(a.water.filter(w=>w.kind==='waterfall').length,1);
 assert.deepEqual(fall.mesh.userData.originalDimensions,[2.15,6.9]);
 assert.equal(fall.mesh.userData.originalPerimeterPreserved,true);
 assert.deepEqual(fall.mesh.position.toArray(),[-5.8,3.75,1.8]);
 assert.equal(fall.mesh.geometry.parameters.widthSegments,24);
 assert.equal(fall.mesh.geometry.parameters.heightSegments,32);
 assert.equal(fall.mesh.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(fall.material.transparent,true);
 assert.equal(fall.material.depthWrite,false);
 const shader=fall.material.fragmentShader;
 const start=shader.indexOf('if(uFall>.5){'),stop=shader.indexOf('}else if(uWetland>.5){',start);
 assert.ok(start>0&&stop>start);
 const onlyFall=shader.slice(start,stop);
 for(const line of [
  'lateralEdge=smoothstep(0.,.16,vUv.x)',
  '(1.-smoothstep(.84,1.,vUv.x))',
  'spanHold=smoothstep(.02,.12,vUv.y)',
  '(1.-smoothstep(.88,.98,vUv.y))',
  'edgeFlutter=.55+.45*sin(vUv.y*31.-uTime*2.1+sin(vUv.x*9.)*.65)',
  'fallingAlpha=.88*(1.-.50*(1.-lateralEdge)*spanHold*edgeFlutter)',
  'gl_FragColor=vec4(fallTint,fallingAlpha)'
 ])assert.ok(onlyFall.includes(line),line);
 assert.doesNotMatch(shader.slice(stop),/lateralEdge|spanHold|edgeFlutter|fallingAlpha/);
 assert.doesNotMatch(onlyFall,/uStorm|uWeather|uRain|uGlobalCalm/);
 assert.ok(a.water.filter(w=>w.kind!=='waterfall').every(w=>(w.material.uniforms.uFall?.value??0)===0));
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('Feather is local, smoothly bounded, mobile and crest/landing edges stay at inherited alpha',()=>{
 let maxChange=0,fringeDrop=0;
 for(let i=0;i<=100;i++)for(let j=0;j<=100;j++){
  const u=i/100,v=j/100;
  for(const t of [0,1.9,8]){
   const a=alpha(u,v,t);
   assert.ok(Number.isFinite(a)&&a>=.44-1e-12&&a<=.88+1e-12);
   if(v<=.02||v>=.98||u>=.16&&u<=.84)
    assert.ok(Math.abs(a-.88)<1e-12,'crest, landing and interior stay untouched');
   if(u===0||u===1)fringeDrop=Math.max(fringeDrop,.88-a);
   maxChange=Math.max(maxChange,Math.abs(a-alpha(u,v,t+.47)));
  }
 }
 assert.ok(fringeDrop>.30,'soft lateral opacity should be visible');
 assert.ok(maxChange>.08,'ordinary water phase moves lateral breakup');
 assert.ok(Math.abs(alpha(.159,.5,0)-alpha(.16,.5,0))<.001,'opacity joins the unmodified center continuously');
});

test('Synthetic global calm does not stop waterfall-side motion; explicit pause does',()=>{
 const a=buildRegionalAssets(THREE,bindings,()=>2);
 const w=a.water.find(x=>x.kind==='waterfall');
 a.tick(1,{globalCalm:true,storm:0});
 const t1=w.material.uniforms.uTime.value;
 a.tick(5,{globalCalm:true,storm:0});
 const t2=w.material.uniforms.uTime.value;
 assert.equal(t1,1);assert.equal(t2,5);
 assert.notEqual(alpha(0,.5,t1),alpha(0,.5,t2));
 a.tick(9,{paused:true,globalCalm:true,storm:0});
 assert.equal(w.material.uniforms.uTime.value,t2);
 a.tick(12,{globalCalm:true,storm:0});
 assert.equal(w.material.uniforms.uTime.value,12);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});
