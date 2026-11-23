import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildWorldGeometry,nextWaterPhase} from '../renderer.mjs';

const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
const STEP=9;
function vertex(mesh,index){
 const start=index*STEP;
 return {
  position:mesh.values.slice(start,start+3),
  normal:mesh.values.slice(start+3,start+6),
  color:mesh.values.slice(start+6,start+9),
 };
}

test('native-WebGL terrain shares normalized height-derived corner normals across existing triangles',()=>{
 const grid=12,{mesh}=buildWorldGeometry([],grid,0);
 assert.equal(mesh.values.length,grid*grid*6*STEP,'same exact unindexed terrain vertex budget');
 const shared=new Map(),different=new Set();
 for(let i=0;i<grid*grid*6;i++){
  const {position,normal}=vertex(mesh,i);
  assert.ok([...position,...normal].every(Number.isFinite));
  assert.ok(Math.abs(Math.hypot(...normal)-1)<1e-6,'unit surface normal');
  assert.ok(normal[1]>0,'terrain normal remains upright');
  const key=position.join(',');
  if(shared.has(key))assert.deepEqual(normal,shared.get(key),'same world vertex must shade seamlessly across cell boundary');
  else shared.set(key,normal);
  different.add(normal.map(n=>n.toFixed(5)).join(','));
 }
 assert.equal(shared.size,(grid+1)*(grid+1),'same terrain positions and grid footprint');
 assert.ok(different.size>grid,'shading is actually interpolated rather than one flat normal');
 // Existing diagonal and cross-cell shared corners are byte-identical.
 assert.deepEqual(vertex(mesh,0).normal,vertex(mesh,3).normal);
 assert.deepEqual(vertex(mesh,1).normal,vertex(mesh,5).normal);
 assert.deepEqual(vertex(mesh,2).normal,vertex(mesh,grid*6).normal);
 assert.deepEqual(vertex(mesh,4).normal,vertex(mesh,6).normal);
});

test('terrain smooth shading leaves canonical footprint, existing water, and source anchors untouched',()=>{
 const grid=8,binding={id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[12,0,14]};
 const anchorBefore=JSON.stringify(binding.anchor);
 const a=buildWorldGeometry([binding],grid,0);
 const b=buildWorldGeometry([{id:binding.id,anchor:[12,0,14]}],grid,0);
 assert.deepEqual(a.mesh.values,b.mesh.values,'deterministic scene geometry');
 assert.deepEqual(a.water.values,b.water.values,'ordinary-water mesh untouched');
 assert.equal(a.water.values.length,40*40*6*STEP,'same 16-unit source water footprint');
 assert.equal(JSON.stringify(binding.anchor),anchorBefore);
 assert.equal(binding.renderAnchor[0],12);
 assert.equal(binding.renderAnchor[2],14);
 assert.ok(binding.renderAnchor.every(Number.isFinite));
 const waterVertices=a.water.values;
 assert.equal(Math.min(...waterVertices.filter((_,i)=>i%STEP===0)),-320);
 assert.equal(Math.max(...waterVertices.filter((_,i)=>i%STEP===0)),320);
 assert.equal(Math.min(...waterVertices.filter((_,i)=>i%STEP===2)),-320);
 assert.equal(Math.max(...waterVertices.filter((_,i)=>i%STEP===2)),320);
});

test('native shading update introduces no new draw pass, weather authority, or water phase coupling',()=>{
 assert.match(source,/triSmooth\(a\.position,c\.position,b\.position,col,a\.normal,c\.normal,b\.normal\)/);
 assert.match(source,/terrainVertices\.set\(key,vertex\)/);
 assert.match(source,/mesh\.triSmooth\(a\.position,d\.position,c\.position,col,a\.normal,d\.normal,c\.normal\)/);
 assert.match(source,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uStorm,storm\)/);
 assert.match(source,/gl\.drawArrays\(gl\.TRIANGLES,0,terrain\.count\)/);
 assert.match(source,/gl\.drawArrays\(gl\.TRIANGLES,0,ocean\.count\)/);
 assert.equal(nextWaterPhase(1,4,false),4,'global calm must not freeze ordinary water');
 assert.equal(nextWaterPhase(4,9,true),4,'explicit pause must freeze ordinary water');
 assert.doesNotMatch(source,/fetch\(|writeWorldState|publishObserver|createPrincipalCharacter/);
});
