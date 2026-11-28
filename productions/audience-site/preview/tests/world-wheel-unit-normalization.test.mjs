import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {cameraStep,defaultCamera} from '../spatial.mjs';
const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
function setup(source,paused=true,enabled=true){
 const start=source.indexOf("canvas.addEventListener('wheel',"),end=source.indexOf('function handleWorldKey(',start);
 if(start<0||end<0)throw Error('Wheel handler missing');
 let handler,options;const tooltip={hidden:false},canvas={clientHeight:600,addEventListener(type,fn,opts){if(type==='wheel'){handler=fn;options=opts;}}};
 const state=new Function('canvas','$','canControl','cameraStep','defaultCamera','structuredClone','paused',
   'let camera=defaultCamera(),target={...defaultCamera(),distance:100};'+source.slice(start,end)+';return ()=>({camera,target});')(
   canvas,()=>tooltip,()=>enabled,cameraStep,defaultCamera,structuredClone,paused);
 function wheel(deltaY,deltaMode){let prevented=false;handler({deltaY,deltaMode,preventDefault(){prevented=true;}});return {prevented,tooltip:tooltip.hidden,...state()};}
 return {wheel,state,options};
}
test('pixel wheel preserves existing scale and paused camera sync',()=>{
 const x=setup(source),v=x.wheel(32,0);assert.equal(v.target.distance,102.24);assert.deepEqual(v.camera,v.target);assert.equal(v.prevented,true);assert.equal(v.tooltip,true);assert.equal(x.options.passive,false);
});
test('line wheel equals its CSS pixel equivalent in both directions',()=>{
 for(const sign of [-1,1])assert.deepEqual(setup(source).wheel(sign*3,1),setup(source).wheel(sign*48,0));
});
test('page wheel uses visible canvas height and preserves live camera easing',()=>{
 const a=setup(source,false).wheel(1,2),b=setup(source,false).wheel(600,0);assert.deepEqual(a,b);assert.equal(a.target.distance,142);assert.equal(a.camera.distance,280);
});
test('historical/fallback input ownership prevents wheel mutation and default cancellation',()=>{
 const x=setup(source,true,false),before=x.state(),v=x.wheel(3,1);assert.deepEqual(v.target,before.target);assert.deepEqual(v.camera,before.camera);assert.equal(v.prevented,false);assert.equal(v.tooltip,false);
});
test('large and invalid wheel deltas cannot escape the existing camera bounds',()=>{
 const x=setup(source);assert.equal(x.wheel(10000,1).target.distance,280);assert.equal(x.wheel(-10000,1).target.distance,12);assert.equal(x.wheel(NaN,0).target.distance,12);
});
