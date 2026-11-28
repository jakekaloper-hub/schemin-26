import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const places=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const smooth=(a,b,v)=>{const t=Math.max(0,Math.min(1,(v-a)/(b-a)));return t*t*(3-2*t);};
const flow=[-.034,.013],mag=Math.hypot(...flow),alongAxis=flow.map(v=>v/mag),crossAxis=[-alongAxis[1],alongAxis[0]];
const phases=[
 (u,v,t)=>{const x=u+.012*t,y=v-.009*t;return (x+Math.sin(y*10+Math.sin(x*6)*.5)*.024)*44+y*11+Math.sin(x*9)*.8;},
 (u,v,t)=>Math.hypot(u-.52,(v-.44)*1.4)*30-t*.15,
 (u,v,t)=>{const x=(u-.5)*2,y=(v-.5)*2,along=x*alongAxis[0]+y*alongAxis[1],across=x*crossAxis[0]+y*crossAxis[1];return (across+Math.sin(along*8-t*.26)*.036)*31+along*7-t*.90;}
];
const gain=(f,u,v,t,step)=>1-smooth(.35,1.15,Math.abs(f(u+step,v,t)-f(u,v,t))+Math.abs(f(u,v+step,t)-f(u,v,t)));

test('Existing Mud Dogs current, eddy and channel ribbon optical phases are footprint-filtered; physical water remains separate',()=>{
 const before=JSON.stringify(places),a=buildRegionalAssets(THREE,places,()=>2);
 try {
  for(const kind of ['swamp','channel']){
   const w=a.water.find(w=>w.kind===kind),s=w.material.fragmentShader;
   const region=s.slice(s.indexOf('}else if(uWetland>.5){'),s.indexOf('}else if(uRiver>.5){'));
   for(const phase of ['currentCoordinate','eddyCoordinate','channelRibbonCoordinate']){
    assert.ok(region.includes('fwidth('+phase+')'),phase);
    assert.ok(!w.material.vertexShader.includes(phase),phase+' must remain optical');
   }
   for(const term of ['currentSheen * uSheenGain','eddy*eddyFade*.5*uSheenGain','channelRibbons=fineLine*smoothstep','reliefLight+padContactSheen+islandSheen','rootSheen+contactLight+channelSheen'])assert.ok(region.includes(term),term);
   assert.equal(w.material.uniforms.uChannel.value,kind==='channel'?1:0);
   assert.equal(w.material.uniforms.uWetland.value,1);
   assert.doesNotMatch(region,/uStorm|uWeather|uGlobalCalm/);
  }
  a.tick(4,{storm:0,globalCalm:true});
  assert.deepEqual(a.water.filter(w=>['swamp','channel'].includes(w.kind)).map(w=>w.material.uniforms.uTime.value),[4,4]);
  a.tick(8,{storm:0,globalCalm:true,paused:true});
  assert.deepEqual(a.water.filter(w=>['swamp','channel'].includes(w.kind)).map(w=>w.material.uniforms.uTime.value),[4,4]);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(places),before);
 }finally{a.dispose();}
});

test('Continuous optical phases retain resolved detail and motion while attenuating coarse footprints',()=>{
 for(const [index,f] of phases.entries()){
  let samples=0,coarseSuppressed=0,temporalChange=0;
  const power=[13,12,12][index],crest=(u,v,t)=>Math.max(Math.sin(f(u,v,t)),0)**power;
  for(let i=8;i<33;i++)for(let j=8;j<33;j++)for(const t of [0,2,6]){
   const u=i/40,v=j/40,near=gain(f,u,v,t,.001),far=gain(f,u,v,t,.05);
   assert.ok(near>.99);assert.ok(far>=0&&far<=1);
   samples++;if(far<.1)coarseSuppressed++;
   temporalChange=Math.max(temporalChange,Math.abs(crest(u,v,t)*near-crest(u,v,t+.5)*gain(f,u,v,t+.5,.001)));
  }
  assert.ok(coarseSuppressed/samples>.90,'phase '+index+' coarse suppression '+coarseSuppressed/samples);
  assert.ok(temporalChange>.1,'phase '+index+' retains moving near detail');
 }
});
