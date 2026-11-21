import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';
const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),before=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const name='Moving predator banner · candidate cloth';
const get=a=>a.locations.find(x=>x.id==='LOC-RED-RUINS');
const fold=(x,y,t)=>{
 const reach=Math.max(0,Math.min(1,(x+.525)/1.05));
 const low=Math.sin(t*.87+y*2.2+reach*6.4),high=Math.sin(t*1.53-y*3.7+reach*12);
 return [reach*reach*(.085*low+.035*high),.024*reach*Math.sin(t*.89+reach*4.8)];
};
test('source-defined Red Leopard Ruins alone has two moving cloth banners and retained masts',()=>{
 const a=build(),site=get(a),upstream=source.locations.find(x=>x.id==='LOC-RED-RUINS');
 assert.ok(site&&upstream.persistent_landmarks.includes('predator banners'));
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 const cloth=site.group.children.filter(x=>x.name===name);
 assert.equal(cloth.length,2,'replace two banners, do not multiply them');
 assert.equal(site.group.children.filter(x=>x.name==='Banner mast').length,2);
 assert.equal(site.group.children.filter(x=>x.name==='Stationary authored banner').length,0);
 assert.equal(cloth[0].material,cloth[1].material,'both surfaces share one material');
 for(const face of cloth){
  assert.equal(face.geometry.type,'PlaneGeometry');
  assert.equal(face.geometry.getAttribute('position').count,77);
  assert.equal(face.material.isShaderMaterial,true);
  assert.equal(face.castShadow,false);
  assert.equal(face.children.length,0);
 }
 for(const other of a.locations.filter(x=>x!==site))assert.equal(other.group.children.filter(x=>x.name===name).length,0,other.id);
 const stormBowl=a.locations.find(x=>x.id==='LOC-STORM-BOWL');
 assert.equal(stormBowl.group.children.filter(x=>x.name==='Stationary authored banner').length,2,'unrelated inherited flags unchanged');
 assert.deepEqual(a.principalCharacters,[]);assert.equal(a.worldMutationAllowed,false);
 assert.equal(a.weatherMutationAllowed,false);assert.equal(JSON.stringify(bindings),before);a.dispose();
});
test('tessellated vertex motion is mast-pinned and numerically bounded',()=>{
 const a=build(),face=get(a).group.children.find(x=>x.name===name),pos=face.geometry.getAttribute('position'),shader=face.material.vertexShader;
 for(const term of ['float reach=clamp((position.x+.525)/1.05,0.,1.);',
  'p.z+=reach*reach*(.085*low+.035*high);',
  'p.y+=.024*reach*sin(uTime*.89+reach*4.8);'])assert.ok(shader.includes(term),term);
 assert.ok(face.material.fragmentShader.includes('float light=.77+.23*vFold;'));
 let peak=0,change=0,anchor=0;
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),a=fold(x,y,1.3),b=fold(x,y,3.7);
  assert.ok([...a,...b].every(Number.isFinite));
  assert.ok(Math.abs(a[0])<=.12000001&&Math.abs(b[0])<=.12000001);
  assert.ok(Math.abs(a[1])<=.02400001&&Math.abs(b[1])<=.02400001);
  peak=Math.max(peak,Math.abs(a[0]),Math.abs(b[0]));change=Math.max(change,Math.abs(a[0]-b[0]));
  if(Math.abs(x+.525)<.00001){assert.ok(Math.abs(a[0])<1e-8&&Math.abs(b[0])<1e-8);anchor++;}
 }
 assert.ok(anchor>=7,'mast edge pinned');
 assert.ok(peak>.04&&change>.07,'measurable physical movement');
 assert.equal(JSON.stringify(bindings),before);a.dispose();
});
test('banner animation continues through synthetic calm, stops on explicit pause and disposes once',()=>{
 const a=build(),mat=get(a).group.children.find(x=>x.name===name).material;
 a.tick(1.2,{storm:0,globalCalm:true});assert.equal(mat.uniforms.uTime.value,1.2);
 a.tick(3.4,{storm:0,globalCalm:true});assert.equal(mat.uniforms.uTime.value,3.4);
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.4),'ordinary water unaffected');
 a.tick(8,{paused:true,storm:0,globalCalm:true});assert.equal(mat.uniforms.uTime.value,3.4);
 let freed=0;mat.addEventListener('dispose',()=>freed++);
 a.dispose();a.dispose();assert.equal(freed,1);a.tick(30);
 assert.equal(mat.uniforms.uTime.value,3.4);
 assert.equal(JSON.stringify(bindings),before);
});
