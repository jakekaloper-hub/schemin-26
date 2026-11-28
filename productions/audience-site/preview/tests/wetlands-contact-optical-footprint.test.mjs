import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const places=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
test('root and pad optical crest phases are filtered before any varying branch',()=>{
 const before=JSON.stringify(places),a=buildRegionalAssets(THREE,places,()=>2);
 try{
  const swamp=a.water.find(w=>w.kind==='swamp'),channel=a.water.find(w=>w.kind==='channel'),s=swamp.material.fragmentShader;
  assert.match(s,/float rootWakeCoordinate=rootDistance\*7\.1-uTime\*1\.6;/);
  assert.match(s,/wakeCrest=pow\(max\(sin\(rootWakeCoordinate\),0\.\),6\.\)\s*\*\(1\.-smoothstep\(\.35,1\.15,fwidth\(rootWakeCoordinate\)\)\)/);
  assert.match(s,/float padWakeCoordinate=padDistance\*12\.-uTime\*2\.05;/);
  assert.match(s,/float padWakeGain=1\.-smoothstep\(\.35,1\.15,fwidth\(padWakeCoordinate\)\);\s*if\(padDistance<1\.05\)/);
  assert.match(s,/padCrest=pow\(max\(sin\(padWakeCoordinate\),0\.\),8\.\)\*padWakeGain/);
  assert.match(s,/rootWake=max\(rootWake,wakeFade\*wakeCrest\)/);
  assert.match(s,/padContactWake=max\(padContactWake,padInterior\*padCrest\)/);
  assert.doesNotMatch(swamp.material.vertexShader,/rootWakeCoordinate|padWakeCoordinate/);
  assert.equal(swamp.material.uniforms.uRootSiteCount.value,5);
  assert.equal(swamp.material.uniforms.uPadSiteCount.value,12);
  assert.equal(channel.material.uniforms.uRootSiteCount.value,0);
  assert.equal(channel.material.uniforms.uPadSiteCount.value,0);
  a.tick(4,{storm:0});a.tick(9,{storm:0,paused:true});
  assert.equal(swamp.material.uniforms.uTime.value,4);
  a.tick(9,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,9);
  assert.equal(a.worldMutationAllowed,false);assert.equal(JSON.stringify(places),before);
 }finally{a.dispose();}
});

const smooth=(a,b,v)=>{const t=Math.max(0,Math.min(1,(v-a)/(b-a)));return t*t*(3-2*t);};
test('radial contact optics retain resolved movement and suppress undersampled detail',()=>{
 for(const [frequency,speed,power,radius] of [[7.1,1.6,6,3.25],[12,2.05,8,1.05]]){
  const phase=(x,y,t)=>Math.hypot(x,y)*frequency-t*speed;
  const gain=(x,y,t,step)=>1-smooth(.35,1.15,Math.abs(phase(x+step,y,t)-phase(x,y,t))+Math.abs(phase(x,y+step,t)-phase(x,y,t)));
  let n=0,suppressed=0,motion=0;
  for(let i=-12;i<=12;i++)for(let j=-12;j<=12;j++)for(const t of [0,2,6]){
   const x=i*radius/12,y=j*radius/12;if(Math.hypot(x,y)>radius)continue;
   const near=gain(x,y,t,.008),far=gain(x,y,t,.24);
   assert.ok(near>.99);assert.ok(far>=0&&far<=1);
   n++;if(far<.1)suppressed++;
   const crest=tt=>Math.max(0,Math.sin(phase(x,y,tt)))**power*gain(x,y,tt,.008);
   motion=Math.max(motion,Math.abs(crest(t)-crest(t+.5)));
  }
  assert.ok(suppressed/n>.90,'coarse suppression '+suppressed+'/'+n);
  assert.ok(motion>.1);
  console.log('contact phase',frequency,'samples',n,'coarse suppressed',suppressed,'near motion',motion);
 }
});
