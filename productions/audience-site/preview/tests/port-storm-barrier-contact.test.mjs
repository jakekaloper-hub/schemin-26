import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(atlas.locations)}),before=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function smooth(a,b,v){const t=Math.max(0,Math.min(1,(v-a)/(b-a)));return t*t*(3-2*t);}
function portRelief(w,x,y,t){
 const edge=1-smooth(.58,.95,Math.hypot(x,y)),axis=Math.abs(y+.016);
 const span=smooth(-.85,-.62,x)*(1-smooth(.45,.65,x));
 return w.material.uniforms.uBarrier.value*w.material.uniforms.uAmplitude.value*.20*edge*Math.exp(-axis*13)*span*Math.sin(axis*26-t*1.35+x*3.1);
}
test('only source LLC port barrier produces candidate water-contact motion with original mesh',()=>{
 const a=build(),site=a.locations.find(x=>x.id==='LOC-LLC-STORM-CITY');
 const port=a.water.find(x=>x.kind==='sheltered port');
 assert.ok(site&&port&&site.group.children.includes(port.mesh));
 assert.ok(atlas.locations.find(x=>x.id==='LOC-LLC-STORM-CITY').persistent_landmarks.includes('storm barriers'));
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(new Set(a.water.map(w=>w.kind)),new Set(['mountain lake','mire','sheltered port','watercourse crossing']));
 assert.deepEqual(a.water.filter(w=>w.material.uniforms.uBarrier.value===1).map(w=>w.kind),['sheltered port']);
 for(const w of a.water){
  assert.equal(w.material.uniforms.uBarrier.value,w===port?1:0);
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.mesh.children.length,0);assert.equal(w.material.depthWrite,false);
 }
 assert.deepEqual(a.principalCharacters,[]);assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),before);a.dispose();
});
test('port shader has synchronized physical and optical water waves within the original fixed shoreline',()=>{
 const a=build(),port=a.water.find(w=>w.kind==='sheltered port');
 for(const s of ['uniform float uBarrier;','float barrierAxis=abs(position.y+.016);','float barrierBand=exp(-barrierAxis*13.)*barrierSpan;','float barrierWave=sin(barrierAxis*26.-uTime*1.35+position.x*3.1);','p.z+=uBarrier*uAmplitude*.20*interior*barrierBand*barrierWave;'])assert.ok(port.material.vertexShader.includes(s),s);
 for(const s of ['float barrierSheen=uBarrier*exp(-barrierAxis*13.)*barrierSpan*pow(max(sin(barrierAxis*26.-uTime*1.35+barrierXY.x*3.1),0.),8.)','c=clamp(c+vec3(.045,.075,.074)*barrierSheen,0.,1.);'])assert.ok(port.material.fragmentShader.includes(s),s);
 const pos=port.mesh.geometry.getAttribute('position');let peak=0,delta=0;
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),v1=portRelief(port,x,y,1.2),v2=portRelief(port,x,y,3.7);
  assert.ok(Number.isFinite(v1)&&Number.isFinite(v2));
  peak=Math.max(peak,Math.abs(v1),Math.abs(v2));delta=Math.max(delta,Math.abs(v1-v2));
  assert.ok(Math.abs(v1)<=.0042+1e-8 && Math.abs(v2)<=.0042+1e-8);
  if(Math.hypot(x,y)>.95)assert.ok(Math.abs(v1)<1e-12 && Math.abs(v2)<1e-12);
 }
 assert.ok(peak>.001 && delta>.002);
 assert.ok(Math.abs(portRelief(port,0,-.016,1.2)-portRelief(port,0,-.016,3.7))>.002);
 for(const w of a.water.filter(w=>w!==port)){assert.equal(w.material.uniforms.uBarrier.value,0);assert.equal(portRelief(w,0,-.016,1.2),0);}
 assert.equal(JSON.stringify(bindings),before);a.dispose();
});
test('global calm keeps ordinary port motion; explicit pause freezes and disposal remains idempotent',()=>{
 const a=build(),port=a.water.find(w=>w.kind==='sheltered port');
 a.tick(2,{storm:0,globalCalm:true});assert.equal(port.material.uniforms.uTime.value,2);
 a.tick(4.5,{storm:0,globalCalm:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.5));
 a.tick(10,{paused:true,storm:0,globalCalm:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.5));
 assert.ok(a.locations.every(l=>l.group.userData.visualAuthority==='CANDIDATE_NOT_APPROVED'));
 assert.equal(JSON.stringify(bindings),before);
 let disposed=0;port.mesh.geometry.addEventListener('dispose',()=>disposed++);port.material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,2);a.tick(33);assert.equal(port.material.uniforms.uTime.value,4.5);
});
