import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const mix=(a,b,t)=>a+(b-a)*t;
const raw=(x,y)=>(.5+.5*Math.sin(x)*Math.sin(y))**3;
const filtered=(x,y,wx,wy)=>{
 const ax=smooth(.35,1.15,wx),ay=smooth(.35,1.15,wy);
 const meanX=.125+.1875*Math.sin(y)**2,meanY=.125+.1875*Math.sin(x)**2;
 return mix(mix(raw(x,y),meanX,ax),mix(meanY,.21875,ax),ay);
};

test('Temple receiving-pool scatter averages independently on both unresolved phase axes',()=>{
 const a=buildRegionalAssets(THREE,[
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall','temple stone','dense vegetation']},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','golf grounds','water hazards']}
 ],()=>2);
 const p=a.water.find(w=>w.kind==='pool'),f=p.material.fragmentShader;
 const start=f.indexOf('}else if(uPlunge>.5){'),end=f.indexOf('}else{',start);
 const s=f.slice(start,end);
 for(const fragment of [
  'scatterPhaseX=p.x*34.+uTime*1.1',
  'scatterPhaseY=p.y*29.-uTime*.87',
  'smoothstep(.35,1.15,fwidth(scatterPhaseX))',
  'smoothstep(.35,1.15,fwidth(scatterPhaseY))',
  'scatterMeanX=.125+.1875*scatterY*scatterY',
  'scatterMeanY=.125+.1875*scatterX*scatterX',
  'mix(scatterMeanY,.21875,scatterBlendX)',
  'foam=mix(mix(foam,scatterMeanX*plungeCore,scatterBlendX),',
  'scatterBlendY)'
 ]) assert.ok(s.includes(fragment),fragment);
 assert.ok(!p.material.vertexShader.includes('scatterPhaseX'));
 assert.ok(!f.slice(0,start).includes('scatterPhaseX'));
 assert.ok(!f.slice(end).includes('scatterPhaseX'));
 assert.doesNotMatch(s,/\buStorm\b|\buWeather\b|\buRain\b|\buGlobalCalm\b/);
 a.tick(2,{globalCalm:true,storm:0});assert.equal(p.material.uniforms.uTime.value,2);
 a.tick(5,{paused:true,globalCalm:true,storm:0});assert.equal(p.material.uniforms.uTime.value,2);
 a.dispose();
});

test('analytic means conserve original scatter energy, retain anisotropic variation and resolved motion',()=>{
 let maxNearChange=0,maxAnisoChange=0,maxError=0,n=0;
 for(let i=0;i<40;i++)for(let j=0;j<40;j++){
  const x=i*.37,y=j*.29;
  let mx=0,my=0;
  for(let k=0;k<128;k++){const phase=2*Math.PI*k/128;mx+=raw(phase,y)/128;my+=raw(x,phase)/128;}
  maxError=Math.max(maxError,Math.abs(mx-filtered(x,y,2,0)),Math.abs(my-filtered(x,y,0,2)));
  assert.equal(filtered(x,y,.1,.1),raw(x,y));
  assert.equal(filtered(x,y,2,2),.21875);
  maxNearChange=Math.max(maxNearChange,Math.abs(filtered(x,y,.1,.1)-filtered(x+.43,y-.34,.1,.1)));
  maxAnisoChange=Math.max(maxAnisoChange,Math.abs(filtered(x,y,2,.1)-filtered(x,y-.34,2,.1)));
  for(const wx of [.1,.6,1.15,3])for(const wy of [.1,.6,1.15,3]){
   const z=filtered(x,y,wx,wy);assert.ok(z>=0&&z<=1);n++;
  }
 }
 assert.ok(maxError<1e-12);assert.ok(maxNearChange>.1);assert.ok(maxAnisoChange>.05);
 let mean=0;for(let i=0;i<64;i++)for(let j=0;j<64;j++)mean+=raw(i*Math.PI/32,j*Math.PI/32)/4096;
 assert.ok(Math.abs(mean-.21875)<1e-12);
 console.log(JSON.stringify({samples:n,maxError,maxNearChange,maxAnisoChange,mean}));
});
