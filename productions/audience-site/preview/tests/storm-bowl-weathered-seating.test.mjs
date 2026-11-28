import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const before=JSON.stringify(bindings);
const placeId='LOC-STORM-BOWL';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const getSite=a=>a.locations.find(l=>l.id===placeId);
const getSeats=a=>getSite(a).group.children.filter(o=>o.name==='Broken-ring seating');

test('only source-provisional Storm Bowl uses 17 weathered static seating surfaces',()=>{
 const authoritative=source.locations.find(l=>l.id===placeId);
 assert.equal(authoritative.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(authoritative.persistent_landmarks,['weather-exposed venue','service counter']);
 const a=build(),site=getSite(a),seats=getSeats(a);
 assert.ok(site);assert.equal(a.locations.length,20);assert.equal(seats.length,17);
 assert.deepEqual(site.sourceLandmarks,authoritative.persistent_landmarks);
 assert.equal(site.group.userData.canonStatus,'PROVISIONAL_CANON');
 assert.equal(site.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 for(const landmark of authoritative.persistent_landmarks)
  assert.ok(site.group.children.some(o=>o.userData?.sourceLandmark===landmark),landmark);
 assert.equal(site.group.children.filter(o=>o.name==='Illustrative rock').length,17);
 for(const other of a.locations.filter(l=>l.id!==placeId))
  assert.equal(other.group.children.filter(o=>o.name==='Broken-ring seating').length,0,other.id);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('17 seats preserve positions, one-mesh footprints and material budget with bounded chipped stone',()=>{
 const a=build(),seats=getSeats(a),m=seats[0].material;
 assert.equal(new Set(seats.map(o=>o.material)).size,1,'one shared static masonry material');
 assert.equal(m.vertexColors,true);assert.equal(m.roughness,.97);
 assert.equal(m.isMeshStandardMaterial,true);
 let minTop=Infinity,maxTop=-Infinity,low=Infinity,high=-Infinity,positions=0;
 const sectors=[];
 for(let i=0;i<20;i++){const ang=i*Math.PI*2/20;if(!(ang>1.1&&ang<2.0))sectors.push(ang);}
 assert.equal(sectors.length,17);
 for(let k=0;k<seats.length;k++){
  const seat=seats[k],ang=sectors[k],g=seat.geometry,p=g.getAttribute('position'),c=g.getAttribute('color');
  assert.equal(g.type,'BoxGeometry');
  assert.equal(g.parameters.width,1.9);assert.equal(g.parameters.height,.7);assert.equal(g.parameters.depth,1.4);
  assert.equal(g.parameters.widthSegments,6);assert.equal(g.parameters.heightSegments,3);assert.equal(g.parameters.depthSegments,4);
  assert.equal(p.count,c.count);assert.ok(p.count>=140&&p.count<=220);
  assert.ok(Math.abs(seat.position.x-Math.cos(ang)*6.3)<1e-5);
  assert.ok(Math.abs(seat.position.z-Math.sin(ang)*6.3)<1e-5);
  assert.equal(seat.position.y,.8);assert.ok(Math.abs(seat.rotation.y+ang)<1e-5);
  assert.ok(g.getAttribute('normal'));
  for(let i=0;i<p.count;i++){
   const [x,y,z]=[p.getX(i),p.getY(i),p.getZ(i)];
   assert.ok([x,y,z].every(Number.isFinite));
   assert.ok(Math.abs(x)<=.950001&&Math.abs(z)<=.700001,'original horizontal footprint');
   assert.ok(y>=-.350001&&y<=.350001,'original vertical bounds');
   if(y>0){minTop=Math.min(minTop,y);maxTop=Math.max(maxTop,y);}
   const channels=[c.getX(i),c.getY(i),c.getZ(i)];
   assert.ok(channels.every(n=>Number.isFinite(n)&&n>0&&n<1),'bounded nonflat mineral color');
   low=Math.min(low,...channels);high=Math.max(high,...channels);positions++;
  }
 }
 assert.ok(positions>2400,'physically subdivided surfaces');
 assert.ok(minTop<.11&&maxTop>.29,'visible physical surface wear remains shallow');
 assert.ok(high-low>.05,'mineral tonality varies across existing seating');
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('static presentation cannot mutate world/weather; calm-water time and pause retain existing semantics',()=>{
 const a=build(),seats=getSeats(a),material=seats[0].material;
 const snapshot=seats.map(o=>o.geometry.getAttribute('position').array.slice());
 a.tick(1.5,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.5));
 a.tick(3.25,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.25));
 a.tick(4,{paused:true,storm:3});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.25));
 for(let i=0;i<seats.length;i++)
  assert.deepEqual(seats[i].geometry.getAttribute('position').array,snapshot[i],'no unsourced event deformation');
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),before);
 let disposals=0;material.addEventListener('dispose',()=>disposals++);
 a.dispose();a.dispose();assert.equal(disposals,1);
});
