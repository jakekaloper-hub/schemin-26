import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {batchStaticGeometry} from '../three-world.mjs';
import {buildRegionalAssets} from '../regional-assets.mjs';

const ids=['LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map((id,i)=>({id,anchor:[i*15,0,25],canonStatus:'PERMANENT_CANON'}));

test('opaque batching retains every linear vertex-color triple and object-space placement',()=>{
 const root=new THREE.Group(),mat=new THREE.MeshStandardMaterial({vertexColors:true,side:THREE.DoubleSide});
 const colors=[new THREE.Color('#3c543c'),new THREE.Color('#8e7655')];
 for(let i=0;i<2;i++){
  const geo=new THREE.BoxGeometry(1,1,1),attr=new Float32Array(geo.attributes.position.count*3);
  for(let j=0;j<geo.attributes.position.count;j++){attr[j*3]=colors[i].r;attr[j*3+1]=colors[i].g;attr[j*3+2]=colors[i].b;}
  geo.setAttribute('color',new THREE.BufferAttribute(attr,3));
  const mesh=new THREE.Mesh(geo,mat);mesh.position.set(i*4,0,0);root.add(mesh);
 }
 const result=batchStaticGeometry(THREE,root);
 assert.equal(result.geometries.length,1);assert.equal(root.children.length,1);
 const batch=root.children[0],c=batch.geometry.getAttribute('color'),p=batch.geometry.getAttribute('position');
 assert.ok(c,'Vertex colors must not disappear from the draw-call reduction');
 assert.equal(c.count,p.count);assert.equal(batch.material.vertexColors,true);
 assert.ok(p.getX(0)<2 && p.getX(p.count-1)>3,'mesh transforms preserved');
 assert.ok(Math.abs(c.getX(0)-colors[0].r)<1e-6);
 assert.ok(Math.abs(c.getX(c.count-1)-colors[1].r)<1e-6);
 for(const g of result.geometries)g.dispose();mat.dispose();
});

test('existing wetland shoreline and raised-ground share one opaque vertex-color material, without source mutation',()=>{
 const before=JSON.stringify(bindings),a=buildRegionalAssets(THREE,bindings,()=>3);
 const swamp=a.locations.find(l=>l.id==='LOC-MUD-DOGS-SWAMP').group;
 const bank=swamp.getObjectByName('Candidate wetland shoreline transition');
 const ground=swamp.getObjectByName('Candidate wetland raised-ground relief');
 assert.ok(bank&&ground);
 assert.equal(bank.material,ground.material,'share a static candidate landform material');
 assert.equal(bank.material.vertexColors,true);
 assert.equal(bank.material.transparent,false,'terrain must be opaque, not painted in the transparency pass');
 const expected=(bank.geometry.index?.count??bank.geometry.getAttribute('position').count)+(ground.geometry.index?.count??ground.geometry.getAttribute('position').count);
 const result=batchStaticGeometry(THREE,swamp);
 const batches=swamp.children.filter(x=>x.isMesh&&x.material===ground.material);
 assert.equal(batches.length,1,'two existing landforms should compile to one opaque draw');
 assert.equal(batches[0].geometry.getAttribute('color').count,expected,'candidate landform colors survive compilation');
 assert.equal(JSON.stringify(bindings),before);
 assert.equal(a.water.find(w=>w.kind==='swamp').material.uniforms.uTime.value,0);
 a.tick(2,{storm:0});assert.equal(a.water.find(w=>w.kind==='swamp').material.uniforms.uTime.value,2);
 a.tick(5,{paused:true,storm:0});assert.equal(a.water.find(w=>w.kind==='swamp').material.uniforms.uTime.value,2);
 for(const g of result.geometries)g.dispose();a.dispose();
});
