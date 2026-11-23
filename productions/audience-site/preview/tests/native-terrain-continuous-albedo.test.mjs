import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildWorldGeometry,nextWaterPhase} from '../renderer.mjs';

const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
const STRIDE=9;
const readVertex=(mesh,index)=>{
 const start=index*STRIDE;
 return {position:mesh.values.slice(start,start+3),
  normal:mesh.values.slice(start+3,start+6),
  color:mesh.values.slice(start+6,start+9)};
};

test('secondary native-WebGL terrain interpolates one identical albedo at every shared corner',()=>{
 const grid=16,{mesh}=buildWorldGeometry([],grid,0);
 assert.equal(mesh.values.length,grid*grid*6*STRIDE,'no added terrain triangles or attributes');
 const shared=new Map(),distinct=new Set();
 for(let i=0;i<grid*grid*6;i++){
  const {position,color}=readVertex(mesh,i);
  assert.ok(color.every(v=>Number.isFinite(v)&&v>=0&&v<=1),'finite bounded terrain RGB');
  const key=position.join(',');
  if(shared.has(key))assert.deepEqual(color,shared.get(key),'shared terrain corners have no cell-color discontinuity');
  else shared.set(key,color);
  distinct.add(color.map(v=>v.toFixed(6)).join(','));
 }
 assert.equal(shared.size,(grid+1)*(grid+1),'all original grid corners remain');
 assert.ok(distinct.size>grid,'terrain albedo responds to relief and zones rather than a fixed swatch');
 assert.notDeepEqual(readVertex(mesh,0).color,readVertex(mesh,1).color,'albedo is truly per corner, not a cell constant');
});

test('terrain-color interpolation does not move source-bound places or affect physical water',()=>{
 const grid=9,binding={id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[12,0,14]};
 const immutableSource=JSON.stringify(binding.anchor);
 const one=buildWorldGeometry([binding],grid,0);
 const two=buildWorldGeometry([{id:binding.id,anchor:[12,0,14]}],grid,0);
 assert.deepEqual(one.mesh.values,two.mesh.values,'entire scene remains deterministic');
 assert.deepEqual(one.water.values,two.water.values,'existing water mesh is unchanged');
 assert.equal(one.mesh.values.length>grid*grid*6*STRIDE,true);
 assert.equal(one.water.values.length,40*40*6*STRIDE,'existing water grid stays unchanged');
 assert.equal(JSON.stringify(binding.anchor),immutableSource,'source coordinates remain immutable');
 assert.equal(binding.renderAnchor[0],12);
 assert.equal(binding.renderAnchor[2],14);
 assert.ok(binding.renderAnchor.every(Number.isFinite));
});

test('color smoothing is a buffer-only native adapter improvement, never a new weather or history authority',()=>{
 assert.match(source,/color:terrainColor\(x,y,z\)/);
 assert.match(source,/\[\[a,na,colorA\],\[b,nb,colorB\],\[c,nc,colorC\]\]/);
 assert.match(source,/mesh\.triSmooth\(a\.position,c\.position,b\.position,a\.color,a\.normal,c\.normal,b\.normal,c\.color,b\.color\)/);
 assert.match(source,/mesh\.triSmooth\(a\.position,d\.position,c\.position,a\.color,a\.normal,d\.normal,c\.normal,d\.color,c\.color\)/);
 assert.match(source,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
 assert.match(source,/gl\.drawArrays\(gl\.TRIANGLES,0,ocean\.count\)/);
 assert.equal(nextWaterPhase(4,9,false),9,'ordinary water moves even under global calm');
 assert.equal(nextWaterPhase(9,15,true),9,'explicit pause freezes water');
 assert.doesNotMatch(source,/fetch\(|writeWorldState|publishObserver|createPrincipalCharacter/);
});
