import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

test('wetland bank contact filters only the signed optical crest footprint',()=>{
 const bindings=[{id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'}];
 const before=JSON.stringify(bindings),a=buildRegionalAssets(THREE,bindings,()=>2);
 try{
  const wet=a.water.filter(w=>['swamp','channel'].includes(w.kind));
  assert.deepEqual(wet.map(w=>w.kind),['swamp','channel']);
  for(const w of wet){
   const s=w.material.fragmentShader;
   assert.match(s,/float bankDistance=bankRadius-\(\.90\+bankWobble\);/);
   assert.match(s,/float bankOpticalGain=1\.-smoothstep\(\.35,1\.15,fwidth\(bankDistance\/\.022\)\);/);
   assert.match(s,/bankCrest=1\.-smoothstep\(\.0,\.022,abs\(bankRadius-\(\.90\+bankWobble\)\)\);/);
   assert.match(s,/contactLight=vec3\(\.09,\.12,\.073\)\*bankCrest\*bankOpticalGain\*bankBreakup\*bankMask\*uBankContact/);
   assert.doesNotMatch(w.material.vertexShader,/bankOpticalGain|bankDistance/);
   assert.equal(w.mesh.geometry.getAttribute('position').count,385);
  }
  assert.equal(a.worldMutationAllowed,false);
  assert.equal(JSON.stringify(bindings),before);
 }finally{a.dispose();}
});
const smooth=(a,b,v)=>{const t=Math.max(0,Math.min(1,(v-a)/(b-a)));return t*t*(3-2*t);};
test('signed distance footprint preserves resolved crest motion and rejects coarse aliasing',()=>{
 const distance=(x,y,t)=>{
  const angle=Math.atan2(y,x);
  return Math.hypot(x,y)-(.90+Math.sin(angle*9+t*.31)*.009+Math.sin(angle*17-t*.20)*.006);
 };
 const gain=(x,y,t,h)=>1-smooth(.35,1.15,(Math.abs(distance(x+h,y,t)-distance(x,y,t))+Math.abs(distance(x,y+h,t)-distance(x,y,t)))/.022);
 let n=0,coarse=0,motion=0;
 for(let i=0;i<72;i++)for(const r of [.885,.90,.915])for(const t of [0,2,6]){
  const angle=i*Math.PI/36,x=r*Math.cos(angle),y=r*Math.sin(angle);
  const resolved=gain(x,y,t,.002),unresolved=gain(x,y,t,.06);
  assert.equal(resolved,1);
  assert.ok(unresolved>=0&&unresolved<=1);
  n++;if(unresolved<.1)coarse++;
  const crest=tt=>(1-smooth(0,.022,Math.abs(distance(x,y,tt))))*gain(x,y,tt,.002);
  motion=Math.max(motion,Math.abs(crest(t)-crest(t+1)));
 }
 assert.ok(coarse/n>.95);assert.ok(motion>.1);
 console.log('bank distance samples',n,'coarse suppressed',coarse,'resolved temporal change',motion);
});
