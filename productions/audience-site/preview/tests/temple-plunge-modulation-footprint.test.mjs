import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const places=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const smooth=x=>{const t=Math.max(0,Math.min(1,(x-.35)/.8));return t*t*(3-2*t);};
const impact=p=>.45+.55*(.5+.5*Math.sin(p));
const wake=p=>Math.sqrt(.5+.5*Math.sin(p));
const mix=(v,m,w)=>v+(m-v)*smooth(w);

test('pool-only impact and wake amplitude are filtered after nonlinear shaping',()=>{
 const a=buildRegionalAssets(THREE,places,()=>2);
 try{
 const p=a.water.find(w=>w.kind==='pool'),f=p.material.fragmentShader;
 const b=f.indexOf('}else if(uPlunge>.5){'),e=f.indexOf('}else{',b);
 assert.ok(b>=0&&e>b);const s=f.slice(b,e);
 for(const x of [
  'impactBreakupPhase=vUv.x*27.-vUv.y*17.+uTime*.57',
  'impactBreakup=.45+.55*(.5+.5*sin(impactBreakupPhase))',
  'impactBreakup=mix(impactBreakup,.725,smoothstep(.35,1.15,fwidth(impactBreakupPhase)))',
  'impactFoam=impactCrest*impactBreakup*impactField',
  'wakeBreakPhase=impactRadius*37.-uTime*2.28+vUv.x*19.',
  'wakeBreak=.5+.5*sin(wakeBreakPhase)',
  'wakeAmplitude=mix(sqrt(wakeBreak),.6366197724,smoothstep(.35,1.15,fwidth(wakeBreakPhase)))',
  'wakeGlint=wakeSpoke*wakeAmplitude*wakeField'
 ])assert.ok(s.includes(x),x);
 assert.doesNotMatch(f.slice(0,b)+f.slice(e)+p.material.vertexShader,/impactBreakupPhase|wakeBreakPhase|wakeAmplitude/);
 assert.doesNotMatch(s,/uStorm|uWeather|uGlobalCalm|uRain/);
 a.tick(2,{globalCalm:true});assert.equal(p.material.uniforms.uTime.value,2);
 a.tick(5,{globalCalm:true,paused:true});assert.equal(p.material.uniforms.uTime.value,2);
 }finally{a.dispose();}
});

test('modulator filtering preserves periodic means, bounds and resolved time variation',()=>{
 let samples=0;
 for(const [raw,mean,speed] of [[impact,.725,.57],[wake,2/Math.PI,2.28]]){
  let sum=0,halfSum=0,nearDelta=0;
  for(let i=0;i<4096;i++){
   const p=2*Math.PI*(i+.5)/4096;
   sum+=raw(p)/4096;halfSum+=mix(raw(p),mean,.75)/4096;
   assert.equal(mix(raw(p),mean,.1),raw(p));
   assert.ok(Math.abs(mix(raw(p),mean,2)-mean)<1e-15);
   for(const w of [.1,.35,.55,.75,1.15,2]){
    const v=mix(raw(p),mean,w);
    assert.ok(v>=0&&v<=1);
    assert.ok(Math.abs(v-mean)<=Math.abs(raw(p)-mean)+1e-15);
    samples++;
   }
   nearDelta=Math.max(nearDelta,Math.abs(raw(p)-raw(p+speed*.43)));
  }
  assert.ok(Math.abs(sum-mean)<1e-6);
  assert.ok(Math.abs(halfSum-mean)<1e-6);
  assert.ok(nearDelta>.05);
  console.log(JSON.stringify({mean,observedMean:sum,halfFilteredMean:halfSum,nearDelta}));
 }
 console.log(JSON.stringify({samples}));
});
