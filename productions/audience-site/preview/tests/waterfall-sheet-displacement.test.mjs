import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON',landmarks:['waterfall','temple stone']},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['water hazards']},
];
const create=()=>buildRegionalAssets(THREE,bindings,()=>2);

test('falling Temple sheet preserves original position, dimensions, and fixed boundaries',()=>{
 const a=create(),fall=a.water.filter(w=>w.kind==='waterfall');
 assert.equal(fall.length,1,'one inherited falling waterfall');
 const {mesh,material}=fall[0],geo=mesh.geometry;
 assert.equal(geo.type,'PlaneGeometry');
 assert.deepEqual([geo.parameters.width,geo.parameters.height,geo.parameters.widthSegments,geo.parameters.heightSegments],[2.15,6.9,24,32]);
 assert.deepEqual(mesh.position.toArray(),[-5.8,7.2-6.9/2,1.8]);
 assert.equal(mesh.renderOrder,2);assert.equal(material.uniforms.uFall.value,1);
 assert.equal(geo.getAttribute('position').count,25*33);
 const uv=geo.getAttribute('uv'),pos=geo.getAttribute('position');
 let perimeter=0,interior=0,folded=0;
 for(let i=0;i<uv.count;i++){
   const depth=pos.getZ(i);
   assert.ok(Number.isFinite(depth)&&depth>=-1e-6&&depth<=.17001,
     'candidate rest contour is bounded, finite and cannot expand the inherited sheet');
   if([0,1].some(n=>Math.abs(uv.getX(i)-n)<1e-6||Math.abs(uv.getY(i)-n)<1e-6)){
     assert.ok(Math.abs(depth)<1e-6,'source crest, landing and both side boundaries immovable');
     perimeter++;
   }else{
     interior++;
     if(depth>.04)folded++;
   }
 }
 assert.ok(perimeter>100&&interior>0,'sheet has physical border and animated interior vertices');
 assert.ok(folded>200,'candidate rest geometry provides true interior depth contour');
 a.dispose();
});

test('only waterfall sheet receives small time-varying interior vertex-normal displacement',()=>{
 const a=create(),fall=a.water.find(w=>w.kind==='waterfall');
 const shader=fall.material.vertexShader;
 assert.match(shader,/uniform float uFall;/,'the selector is declared in vertex GLSL');
 assert.match(shader,/if\(uFall>\.5\)/,'sheet-only conditional');
 assert.match(shader,/sideHold=sin\(uv\.x\*3\.14159265\)/,'both sides pinned');
 assert.match(shader,/endHold=sin\(uv\.y\*3\.14159265\)/,'top and bottom pinned');
 assert.match(shader,/p\.z\+=\.10\*sideHold\*endHold\*folds/,'bounded displacement along local normal');
 assert.match(shader,/uTime\*2\.2/,'motion evolves with the existing environmental time');
 assert.doesNotMatch(shader,/\buStorm\b|\buWeather\b/i,'sheet movement is not storm-driven');
 const envelope=(u,v,t)=>.10*Math.sin(u*Math.PI)*Math.sin(v*Math.PI)*
    (Math.sin(u*17-t*2.2+v*7.8)+.38*Math.sin(u*29+t*1.45-v*9.3));
 for(const t of [0,1.4,13]){
   for(const u of [0,.125,.5,.875,1])for(const v of [0,.25,.5,.75,1]){
     assert.ok(Math.abs(envelope(u,v,t))<=.139,'deformation amplitude stays bounded');
     if(u===0||u===1||v===0||v===1)assert.ok(Math.abs(envelope(u,v,t))<1e-12,'all boundary vertices stationary');
   }
 }
 assert.ok(Math.abs(envelope(.375,.5,0)-envelope(.375,.5,1.4))>.001,'interior actually moves');
 for(const w of a.water.filter(w=>w.kind!=='waterfall'))assert.equal(w.material.uniforms.uFall?.value??0,0);
 a.dispose();
});

test('global weather calm cannot freeze falling water; pause does and source remains untouched',()=>{
 const before=JSON.stringify(bindings),a=create(),fall=a.water.find(w=>w.kind==='waterfall');
 a.tick(3,{storm:0});assert.equal(fall.material.uniforms.uTime.value,3);
 a.tick(9,{storm:0});assert.equal(fall.material.uniforms.uTime.value,9);
 a.tick(24,{storm:0,paused:true});assert.equal(fall.material.uniforms.uTime.value,9);
 a.tick(24,{storm:0});assert.equal(fall.material.uniforms.uTime.value,24);
 assert.ok(a.water.some(w=>w.kind==='swamp')&&a.water.some(w=>w.kind==='pond'));
 assert.deepEqual(a.locations.map(l=>l.id),bindings.map(b=>b.id));
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('higher-density Temple sheet resolves both inherited fold harmonics without added draw instances',()=>{
 const before=JSON.stringify(bindings),a=create(),fall=a.water.find(w=>w.kind==='waterfall'),geo=fall.mesh.geometry;
 const uv=geo.getAttribute('uv'),p=geo.getAttribute('position');
 const samplesX=new Set(),samplesY=new Set(),boundary=[];
 let contouredInterior=0;
 for(let i=0;i<uv.count;i++){
  const u=uv.getX(i),v=uv.getY(i),depth=p.getZ(i);
  samplesX.add(u.toFixed(6));samplesY.add(v.toFixed(6));
  const isBoundary=u<1e-6||u>1-1e-6||v<1e-6||v>1-1e-6;
  if(isBoundary){
   boundary.push(i);
   assert.ok(Math.abs(depth)<1e-6,'animated and resting waterfall have pinned borders');
  }else{
   assert.ok(depth>=-1e-6&&depth<=.17001,'rest contour remains within bounded sheet');
   if(depth>.04)contouredInterior++;
  }
 }
 assert.ok(contouredInterior>200,'physical resting contour augments (not replaces) animated folds');
 assert.equal(samplesX.size,25);assert.equal(samplesY.size,33);
 assert.equal(geo.index.count,24*32*6);
 assert.ok(geo.getAttribute('position').count<900,'bounded one-sheet mobile vertex budget');
 // The 29-radian cross-sheet harmonic requires >9 segments by Nyquist;
 // preserve additional headroom for view-dependent folds and two-band layering.
 assert.ok(geo.parameters.widthSegments>=20);
 assert.ok(boundary.length>100,'all four sheet edges have physical vertices');
 const shader=fall.material.vertexShader;
 assert.ok(shader.includes('uv.x*29.'),'first high-frequency fold harmonic preserved');
 assert.ok(shader.includes('uv.x*17.'),'second fold harmonic preserved');
 assert.ok(shader.includes('sideHold*endHold*folds'),'fixed edges still modulate folds');
 assert.equal(a.water.filter(w=>w.kind==='waterfall').length,1);
 a.tick(1.2,{globalCalm:true,storm:0});
 a.tick(5.6,{globalCalm:true,storm:0});
 assert.equal(fall.material.uniforms.uTime.value,5.6);
 a.tick(8,{paused:true,storm:9});
 assert.equal(fall.material.uniforms.uTime.value,5.6);
 let disposalCount=0;geo.addEventListener('dispose',()=>disposalCount++);
 a.dispose();a.dispose();
 assert.equal(disposalCount,1);
 assert.equal(JSON.stringify(bindings),before);
});
