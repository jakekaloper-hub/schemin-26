import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const smooth=(a,b,x)=>{
  const q=Math.max(0,Math.min(1,(x-a)/(b-a)));
  return q*q*(3-2*q);
};
const relief=(u,v,t,sites)=>{
  let padRelief=0;
  for(const site of sites){
    const d=Math.hypot((u-site[0])*21,(v-site[1])*16.4);
    if(d>=1.05)continue;
    const interior=1-smooth(.32,1.05,d);
    const crest=Math.max(0,Math.sin(d*12-t*2.05))**8;
    padRelief=Math.max(padRelief,interior*crest);
  }
  const shore=1-smooth(.65,.96,Math.hypot((u-.5)*2,(v-.5)*2));
  return .0045*padRelief*shore;
};
const snapshots=sites=>sites.map(s=>[s.x,s.y]);

test('floating contact displacement shares the exact twelve existing light sites and phase, not a new water mesh',()=>{
  const before=JSON.stringify(bindings),a=build();
  const swamp=a.water.find(x=>x.kind==='swamp');
  const vertex=swamp.material.vertexShader,fragment=swamp.material.fragmentShader;
  assert.match(vertex,/uniform float uPadSiteCount;uniform vec2 uPadSites\[12\]/);
  assert.match(vertex,/if\(uPadSiteCount>\.5\)/);
  assert.match(vertex,/for\(int i=0;i<12;i\+\+\)/);
  assert.match(vertex,/padDistance=length\(\(uv-uPadSites\[i\]\)\*vec2\(21\.,16\.4\)\)/);
  assert.match(vertex,/padInterior=1\.-smoothstep\(\.32,1\.05,padDistance\)/);
  assert.match(vertex,/padCrest=pow\(max\(sin\(padDistance\*12\.-uTime\*2\.05\),0\.\),8\.\)/);
  assert.match(vertex,/p\.z\+=\.0045\*padRelief\*shoreHold/);
  assert.match(fragment,/padContactWake=max\(padContactWake,padInterior\*padCrest\)/);
  assert.equal(swamp.material.uniforms.uPadSiteCount.value,12);
  assert.equal(swamp.material.uniforms.uPadSites.value.length,12);
  assert.ok(a.water.filter(x=>x.kind!=='swamp').every(x=>(x.material.uniforms.uPadSiteCount?.value??0)===0));
  assert.equal(swamp.mesh.geometry.getAttribute('position').count,385);
  assert.equal(swamp.mesh.geometry.index.count,2160);
  assert.deepEqual(swamp.mesh.scale.toArray(),[10.5,8.2,1]);
  assert.equal(JSON.stringify(bindings),before);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  a.dispose();
});

test('physical wake moves real inherited disk vertices within local amplitude, keeps all rim vertices fixed',()=>{
  const a=build(),w=a.water.find(x=>x.kind==='swamp'),uv=w.mesh.geometry.getAttribute('uv');
  let peak=0,delta=0,interior=0;
  const samples=[];
  for(const t of [0,1.7,4.4]){
    a.tick(t,{storm:0});
    const sites=snapshots(w.material.uniforms.uPadSites.value);
    const vals=[];
    for(let i=0;i<uv.count;i++){
      const u=uv.getX(i),v=uv.getY(i),r=Math.hypot((u-.5)*2,(v-.5)*2);
      const z=relief(u,v,t,sites);
      assert.ok(Number.isFinite(z)&&z>=0&&z<=.004500001,'finite, bounded existing-vertex motion');
      if(r>.96)assert.ok(z<1e-11,'original water rim is stationary');
      if(r<.80&&z>.00001)interior++;
      peak=Math.max(peak,z);
      vals.push(z);
    }
    samples.push(vals);
  }
  for(let i=0;i<uv.count;i++)delta=Math.max(delta,Math.abs(samples[0][i]-samples[1][i]),Math.abs(samples[1][i]-samples[2][i]));
  assert.ok(peak>.00005,'contact relief must displace real interior vertices');
  assert.ok(delta>.00005,'ordinary time and shared moving centers change actual vertices');
  assert.ok(interior>0,'some real samples lie beneath moving pad contact');
  assert.equal(relief(.5,.5,3,[]),0,'no pad sites means no displacement');
  assert.equal(relief(.99,.99,1,[[.99,.99]]),0,'water boundary remains fixed');
  a.dispose();
});

test('global calm preserves ordinary foliage and contact motion; explicit pause freezes all uniforms',()=>{
  const before=JSON.stringify(bindings),a=build(),w=a.water.find(x=>x.kind==='swamp');
  const foliage=a.locations.find(x=>x.id==='LOC-MUD-DOGS-SWAMP').group.getObjectByName('Candidate Mud Dogs floating foliage');
  a.tick(2,{storm:0});const sites=snapshots(w.material.uniforms.uPadSites.value);
  a.tick(13,{storm:0,paused:true});
  assert.equal(w.material.uniforms.uTime.value,2);
  assert.equal(foliage.material.uniforms.uTime.value,2);
  assert.deepEqual(snapshots(w.material.uniforms.uPadSites.value),sites);
  a.tick(13,{storm:0});
  assert.equal(w.material.uniforms.uTime.value,13);
  assert.equal(foliage.material.uniforms.uTime.value,13);
  assert.ok(snapshots(w.material.uniforms.uPadSites.value).some((p,i)=>Math.hypot(p[0]-sites[i][0],p[1]-sites[i][1])>.00001));
  for(const water of a.water.filter(x=>x.kind!=='swamp'))assert.equal(water.material.uniforms.uPadSiteCount?.value??0,0);
  assert.equal(JSON.stringify(bindings),before);
  let disposed=0;w.material.addEventListener('dispose',()=>disposed++);
  a.dispose();a.dispose();assert.equal(disposed,1);
});
