import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildWorldGeometry,canvasWaterDisplacement,nextWaterPhase} from '../renderer.mjs';

function waterGrid(size){
 const {water}=buildWorldGeometry([],2,0,{waterCellSize:size});
 const vertices=water.values;
 const xs=new Set(),zs=new Set();
 for(let i=0;i<vertices.length;i+=9){
  xs.add(vertices[i]);zs.add(vertices[i+2]);
  assert.equal(vertices[i+1],-.4,'original water level preserved');
  assert.deepEqual(vertices.slice(i+6,i+9),[.115,.29,.31],'original water color preserved');
 }
 return {vertices,xs,zs};
}

test('native 8-unit water cells improve physical-wave sampling without expanding water or changing topology',()=>{
 const native=waterGrid(8),legacy=waterGrid(16);
 assert.equal(legacy.vertices.length/27,3200,'Canvas and legacy water remain 40x40 quads');
 assert.equal(native.vertices.length/27,12800,'Native water uses 80x80 original-footprint quads');
 assert.deepEqual([Math.min(...native.xs),Math.max(...native.xs),Math.min(...native.zs),Math.max(...native.zs)],[-320,320,-320,320]);
 assert.deepEqual([Math.min(...legacy.xs),Math.max(...legacy.xs),Math.min(...legacy.zs),Math.max(...legacy.zs)],[-320,320,-320,320]);
 assert.ok(native.xs.has(-312)&&!legacy.xs.has(-312),'8-unit vertices physically sample intermediate wave heights');
 assert.equal(native.xs.size,81);
 assert.equal(native.zs.size,81);
 assert.equal(legacy.xs.size,41);
 assert.equal(legacy.zs.size,41);
});

test('smaller physical cells reduce analytic water-wave chord error using the unchanged ordinary clock',()=>{
 const phase=nextWaterPhase(0,1.75,false);
 const held=nextWaterPhase(phase,40,true);
 assert.equal(held,phase,'explicit pause holds the surface');
 assert.equal(nextWaterPhase(held,2.4,false),2.4,'ordinary water advances under synthetic calm without weather input');
 const maxError=(step)=>{
  let max=0;
  for(let x=-96;x<96;x+=step){
   for(const t of [0,.75,2.2,6.1]){
    const surface=p=>canvasWaterDisplacement(p,0,t);
    const mid=surface(x+step/2),chord=(surface(x)+surface(x+step))/2;
    max=Math.max(max,Math.abs(mid-chord));
   }
  }
  return max;
 };
 assert.ok(maxError(8)<maxError(16)*.4,'denser vertices better approximate existing 3D displacement');
});

test('only native WebGL selects denser geometry; Canvas painter and GPU shaders retain authority',()=>{
 const src=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
 assert.match(src,/buildWorldGeometry\(bindings,200,4300,\{waterCellSize:8\}\)/);
 assert.match(src,/buildWorldGeometry\(bindings,100,7000\)/);
 assert.match(src,/waterFrame=Math\.floor\(lastWater\*8\)\/8/);
 assert.match(src,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
 assert.match(src,/gl\.uniform1f\(loc\.uTime,waterTime\)/);
 assert.match(src,/if\(uWater>\.5\)p\.y\+=sin\(p\.x\*\.21\+uTime\*\.55\)/);
 assert.doesNotMatch(src,/fetch\(|writeWorldState|publishObserver|createPrincipalCharacter/);
 assert.throws(()=>buildWorldGeometry([],2,0,{waterCellSize:7}),/INVALID_WATER_CELL_SIZE/);
});
