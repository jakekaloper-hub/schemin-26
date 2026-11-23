import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const start=source.indexOf('function projectedStormRain(');
const end=source.indexOf('\nconst zoneBounds=',start);
assert.ok(start>=0&&end>start,'Expected actual bounded weather projection source');
const projectedStormRain=vm.runInNewContext(source.slice(start,end)+'\nprojectedStormRain');

const cameraProjection=p=>({x:p[0]*3,y:p[1]*3,depth:0,world:p});

test('synthetic storm columns are anchored to existing affected region geometry and terrain',()=>{
 const bounds=[68,25,100,88],samples=projectedStormRain(bounds,0,()=>2,cameraProjection);
 assert.equal(samples.length,110);
 for(const {a,b} of samples){
  const [x,top,z]=a.world,[tailX,bottom,tailZ]=b.world;
  assert.ok(tailX>=36&&tailX<=100&&tailZ>=-76&&tailZ<=50);
  assert.ok(Math.abs(x-tailX+.22)<1e-10);
  assert.ok(Math.abs(z-tailZ-.1)<1e-10);
  assert.ok(Math.abs(top-bottom-1.4)<1e-10);
  assert.ok(bottom>=4&&bottom<18);
 }
});

test('camera motion reprojects fixed drops while ordinary time advances falling positions',()=>{
 const region=[25,30,72,58],ground=(x,z)=>Math.sin(x*.01)+Math.cos(z*.01);
 const a=projectedStormRain(region,1,ground,cameraProjection),b=projectedStormRain(region,1,ground,cameraProjection);
 const moving=projectedStormRain(region,2,ground,cameraProjection);
 const rotated=projectedStormRain(region,1,ground,p=>({x:p[2]*2,y:p[1],depth:0,world:p}));
 assert.equal(JSON.stringify(a),JSON.stringify(b),'explicit pause holds same frame');
 assert.notEqual(JSON.stringify(a),JSON.stringify(moving),'ordinary clock moves precipitation');
 assert.notEqual(JSON.stringify(a.map(s=>s.a.x)),JSON.stringify(rotated.map(s=>s.a.x)),'camera moves in world, not screen coordinates');
 assert.equal(a.length,110);
});

test('samples fail closed for invalid zones, clocks and out-of-frustum projections',()=>{
 const p=p=>({x:p[0],y:p[1],depth:0});
 for(const bad of [[1,2,1,3],[0,3,2,2],[NaN,0,1,1],[0,1,2]]){
  assert.throws(()=>projectedStormRain(bad,0,()=>0,p),/INVALID_STORM_RAIN_SAMPLE/);
 }
 assert.throws(()=>projectedStormRain([0,0,1,1],NaN,()=>0,p),/INVALID_STORM_RAIN_SAMPLE/);
 assert.throws(()=>projectedStormRain([0,0,1,1],1,()=>0,p,111),/INVALID_STORM_RAIN_SAMPLE/);
 assert.equal(projectedStormRain([0,0,1,1],1,()=>NaN,p).length,0);
 assert.equal(projectedStormRain([0,0,1,1],1,()=>0,()=>({x:0,y:0,depth:2})).length,0);
 assert.equal(projectedStormRain([0,0,1,1],1,()=>0,()=>null).length,0);
});

test('existing world, history and weather authority remain independent of preview optical rain',()=>{
 assert.match(source,/if\(demo>0\)for\(const id of weather\.affectedZoneIds\)/);
 assert.match(source,/projectedStormRain\(bounds,t,\(x,z\)=>renderer\.height\(x,z\),point=>renderer\.project\(point\)\)/);
 assert.match(source,/renderer\.render\(camera,animationTime,\{strength:light\.strength,storm:demo\|\|0,paused\}\)/);
 assert.match(source,/if\(!paused&&!document\.hidden\)animationTime\+=dt/);
 assert.match(source,/function syntheticWeather\(wins\)/);
 assert.doesNotMatch(source,/\(\(i\*127\.3\+t\*12\)%w/,'screen-anchored moving rain must be removed');
 assert.doesNotMatch(source,/projectedStormRain\([\s\S]*?fetch\(/,'rain projection may not request live data');
});
