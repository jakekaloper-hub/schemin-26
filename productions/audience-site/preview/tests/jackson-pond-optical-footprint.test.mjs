import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const place=source.locations.find(p=>p.id==='LOC-COUNTRY-CLUB-JACKSON');
const bindings=[{id:place.id,anchor:[place.abstract_position[0],0,place.abstract_position[1]],canonStatus:place.canon_status,landmarks:place.persistent_landmarks}];
test('Jackson four radial crests have independent continuous optical footprints only',()=>{
 const before=JSON.stringify(bindings),a=buildRegionalAssets(THREE,bindings,()=>2);
 try{
  const ponds=a.water.filter(w=>w.kind==='pond');assert.equal(ponds.length,1);
  const p=ponds[0],s=p.material.fragmentShader;
  const region=s.slice(s.indexOf('}else if(uPond>.5){'),s.indexOf('}else if(uPlunge>.5){'));
  for(const [phase,formula,output,power] of [
   ['pondWaveCoordinateA','r1*33.0-uTime*2.4','wave1',12],
   ['pondWaveCoordinateB','r2*25.0-uTime*1.75','wave2',12],
   ['bridgeWaveCoordinateA','bridgeDistA*37.-uTime*2.05','bridgeCrestA',10],
   ['bridgeWaveCoordinateB','bridgeDistB*33.-uTime*1.82+1.2','bridgeCrestB',10]
  ]){
   assert.ok(region.includes('float '+phase+'='+formula+';'),phase);
   const statement=region.slice(region.indexOf('float '+output+'=')).split(';')[0];
   assert.ok(statement.includes('pow(max(sin('+phase+'),0.),'+power+'.)'),output);
   assert.ok(statement.includes('*(1.-smoothstep(.35,1.15,fwidth('+phase+')))'),output+' footprint');
   assert.ok(!p.material.vertexShader.includes(phase));
  }
  assert.ok(region.includes('ripple=(wave1*.6+wave2*.4)*bank'));
  assert.ok(region.includes('bridgeContact=clamp((bridgeCrestA+bridgeCrestB)*bridgeBreak*bank,0.,1.)'));
  assert.doesNotMatch(region,/uStorm|uWeather|uGlobalCalm/);
  assert.equal(p.mesh.geometry.getAttribute('position').count,321);
  assert.equal(p.mesh.geometry.index.count,1800);
  assert.equal(p.material.uniforms.uFlow.value.length(),0);
  a.tick(3,{storm:0,globalCalm:true});a.tick(5,{storm:0,globalCalm:true});
  assert.equal(p.material.uniforms.uTime.value,5);
  a.tick(9,{storm:0,globalCalm:true,paused:true});assert.equal(p.material.uniforms.uTime.value,5);
  assert.equal(a.worldMutationAllowed,false);assert.equal(JSON.stringify(bindings),before);
 }finally{a.dispose();}
});
const smooth=(a,b,v)=>{const q=Math.max(0,Math.min(1,(v-a)/(b-a)));return q*q*(3-2*q);};
const phases=[
 (x,y,t)=>Math.hypot(x+.19,(y-.08)*1.25)*33-t*2.4,
 (x,y,t)=>Math.hypot((x-.25)*1.2,y+.18)*25-t*1.75,
 (x,y,t)=>Math.hypot(x+.88/3.8,y*1.28)*37-t*2.05,
 (x,y,t)=>Math.hypot(x-.71/3.8,y*1.28)*33-t*1.82+1.2
];
const gain=(f,x,y,t,h)=>1-smooth(.35,1.15,Math.abs(f(x+h,y,t)-f(x,y,t))+Math.abs(f(x,y+h,t)-f(x,y,t)));
test('four radial phases preserve resolved moving crests and attenuate coarse footprints',()=>{
 for(const [i,f] of phases.entries()){
  const power=i<2?12:10,crest=(x,y,t)=>Math.max(Math.sin(f(x,y,t)),0)**power;
  let samples=0,suppressed=0,motion=0;
  for(let ix=-12;ix<=12;ix++)for(let iy=-12;iy<=12;iy++)for(const t of [0,2,6]){
   const x=ix/24,y=iy/24,near=gain(f,x,y,t,.002),far=gain(f,x,y,t,.08);
   assert.equal(near,1);assert.ok(far>=0&&far<=1);
   samples++;if(far<.1)suppressed++;
   motion=Math.max(motion,Math.abs(crest(x,y,t)*near-crest(x,y,t+.5)*gain(f,x,y,t+.5,.002)));
  }
  assert.ok(suppressed/samples>.95,'phase '+i+' coarse suppression');
  assert.ok(motion>.1,'phase '+i+' retained temporal variation');
  console.log('pond phase',i,'samples',samples,'suppressed',suppressed,'resolved change',motion);
 }
});
