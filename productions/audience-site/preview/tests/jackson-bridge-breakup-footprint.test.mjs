import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const place=source.locations.find(p=>p.id==='LOC-COUNTRY-CLUB-JACKSON');
const bindings=[{id:place.id,anchor:[place.abstract_position[0],0,place.abstract_position[1]],canonStatus:place.canon_status,landmarks:place.persistent_landmarks}];

const terms=[
 ['bridgeShadowPhase','p.y*27.-uTime*.59+p.x*13.','bridgeShadowDapple',.95,.05,13,27,.59],
 ['bridgeContactPhase','p.y*27.+uTime*.68+p.x*11.','bridgeBreak',.5,.5,11,27,-.68],
 ['bridgeMirrorPhase','p.y*42.-uTime*.84+p.x*12.','bridgeMirrorBreak',.74,.26,12,42,.84]
];
test('Jackson bridge modulation retains broad energy at coarse fragment footprints',()=>{
 const original=JSON.stringify(bindings),a=buildRegionalAssets(THREE,bindings,()=>2);
 try{
  const p=a.water.find(w=>w.kind==='pond');
  const f=p.material.fragmentShader;
  for(const [phase,formula,output,mean] of terms){
   assert.ok(f.includes('float '+phase+'='+formula+';'),phase);
   assert.ok(f.includes(output+'=mix('+output+','+String(mean).replace(/^0/,'')+',smoothstep(.35,1.15,fwidth('+phase+')));'),output);
   assert.ok(!p.material.vertexShader.includes(phase));
  }
  assert.equal(p.mesh.geometry.getAttribute('position').count,321);
  assert.equal(p.mesh.geometry.index.count,1800);
  assert.equal(a.water.filter(w=>w.kind==='pond').length,1);
  assert.equal(a.worldMutationAllowed,false);
  a.tick(3,{globalCalm:true,storm:0});a.tick(6,{globalCalm:true,storm:0});
  assert.equal(p.material.uniforms.uTime.value,6);
  a.tick(8,{paused:true,globalCalm:true,storm:0});
  assert.equal(p.material.uniforms.uTime.value,6);
  assert.equal(JSON.stringify(bindings),original);
 }finally{a.dispose();}
});
const smooth=(v)=>{const t=Math.max(0,Math.min(1,(v-.35)/.8));return t*t*(3-2*t);};
test('all three breakup terms conserve periodic means and retain resolved time variation',()=>{
 for(const [phase,,,mean,amp,kx,ky,kt] of terms){
  let count=0,maxMotion=0;
  for(const step of [.001,.012,.06,.12]){
   const gain=1-smooth(step*(Math.abs(kx)+Math.abs(ky)));
   let sum=0;
   for(let i=0;i<512;i++){
    const phi=i*2*Math.PI/512;
    const value=mean+amp*Math.sin(phi)*gain;
    assert.ok(value>=mean-amp-1e-12&&value<=mean+amp+1e-12);
    if(step===.001){assert.equal(gain,1);maxMotion=Math.max(maxMotion,Math.abs(value-(mean+amp*Math.sin(phi-kt*.8))));}
    if(step>=.06){assert.equal(gain,0);assert.equal(value,mean);}
    sum+=value;count++;
   }
   assert.ok(Math.abs(sum/512-mean)<1e-12,phase+' periodic mean');
  }
  assert.ok(maxMotion>.01,phase+' resolved motion');
  console.log(phase,'samples',count,'resolved max delta',maxMotion);
 }
});
