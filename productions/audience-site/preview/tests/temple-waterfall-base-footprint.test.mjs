import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const raw=(phase,n)=>(.5+.5*Math.sin(phase))**n;
const filtered=(phase,n,mean,w)=>{const a=smooth(.35,1.15,w);return raw(phase,n)*(1-a)+mean*a;};
test('falling sheet filters only broad optical pattern phases, preserving physical time',()=>{
 const a=buildRegionalAssets(THREE,[
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall','temple stone','dense vegetation']},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','golf grounds','water hazards']}
 ],()=>2);
 const p=a.water.find(w=>w.kind==='waterfall'),f=p.material.fragmentShader;
 const start=f.indexOf('if(uFall>.5){'),end=f.indexOf('}else if(uWetland>.5)',start);
 const s=f.slice(start,end);
 for(const fragment of [
  'fallStripePhase=vUv.x*21.+sin(vUv.y*9.-uTime*3.8)*1.9',
  'fallFoamPhase=vUv.y*35.+uTime*9.+sin(vUv.x*13.)',
  'stripe=mix(stripe,.3125,smoothstep(.35,1.15,fwidth(fallStripePhase)))',
  'foam=mix(foam,.2734375,smoothstep(.35,1.15,fwidth(fallFoamPhase)))'
 ]) assert.ok(s.includes(fragment),fragment);
 assert.ok(!p.material.vertexShader.includes('fallStripePhase'));
 assert.ok(!f.slice(end).includes('fallFoamPhase'));
 assert.doesNotMatch(s,/\buStorm\b|\buWeather\b|\buRain\b|\buGlobalCalm\b/);
 a.tick(2,{globalCalm:true,storm:0});assert.equal(p.material.uniforms.uTime.value,2);
 a.tick(5,{paused:true,globalCalm:true,storm:0});assert.equal(p.material.uniforms.uTime.value,2);
 a.dispose();
});
test('periodic means preserve foam energy and resolved temporal variation',()=>{
 let samples=0,maxNear=0,maxError=0;
 for(const [n,mean] of [[3,.3125],[4,.2734375]]){
  let actual=0;
  for(let i=0;i<1024;i++) actual+=raw(i*Math.PI/512,n)/1024;
  maxError=Math.max(maxError,Math.abs(actual-mean));
  for(let i=0;i<256;i++){
   const p=i*.071;
   assert.equal(filtered(p,n,mean,.1),raw(p,n));
   assert.equal(filtered(p,n,mean,2),mean);
   maxNear=Math.max(maxNear,Math.abs(filtered(p,n,mean,.1)-filtered(p+.43,n,mean,.1)));
   for(const w of [.1,.35,.6,.9,1.15,3]){const z=filtered(p,n,mean,w);assert.ok(z>=0&&z<=1);samples++;}
  }
 }
 assert.ok(maxError<1e-12);assert.ok(maxNear>.1);
 console.log(JSON.stringify({samples,maxNear,maxError}));
});
