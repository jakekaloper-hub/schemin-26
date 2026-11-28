import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
const handler=source.slice(source.indexOf(' function pick(clientX,clientY)'),source.indexOf(' const lost=e=>'));
assert.ok(handler.startsWith(' function pick(clientX,clientY)'));
const place={id:'LOC-MUD-DOGS-SWAMP',anchor:[0,0,0],renderAnchor:[80,80,0]};
const make=(target=[5,5,0],{width=100,height=100,places=[place],frames={[place.id]:{target}}}={})=>{
 const canvas={clientWidth:width,clientHeight:height,getBoundingClientRect:()=>({left:40,top:60})};
 let projections=0;
 const project=p=>{projections++;return {x:p[0],y:p[1],depth:p[2]};};
 const pick=new Function('canvas','bindings','framesBySite','height','project',handler+'\nreturn pick;')(canvas,places,frames,()=>3,project);
 return {pick:(x,y)=>pick(x+40,y+60),projections:()=>projections};
};
test('candidate camera target remains the preferred source-bound hit in CSS pixels',()=>{
 const x=make([5,5,0]);assert.equal(x.pick(5,5),place);assert.equal(x.pick(0,0),place);
 assert.equal(x.pick(37,5),null,'strict 32 CSS px radius remains unchanged');
 assert.equal(x.pick(80,80),null,'does not substitute source anchor for framed candidate');
});
test('captured releases just outside each canvas edge cannot inspect nearby places',()=>{
 for(const [target,point] of [[[5,50,0],[-1,50]],[[95,50,0],[101,50]],[[50,5,0],[50,-1]],[[50,95,0],[50,101]]]){
  const x=make(target);assert.equal(x.pick(...point),null);assert.equal(x.projections(),0);
 }
});
test('nonfinite coordinates and zero-area canvas do not project or inspect',()=>{
 const x=make();for(const [a,b] of [[NaN,5],[5,Infinity],[-Infinity,5]])assert.equal(x.pick(a,b),null);
 assert.equal(x.projections(),0);
 for(const dimensions of [{width:0},{height:0}]){
  const z=make([0,0,0],dimensions);assert.equal(z.pick(0,0),null);assert.equal(z.projections(),0);
 }
});
test('only finite projections within the existing clip-depth range are selectable',()=>{
 for(const depth of [NaN,Infinity,-Infinity,-1.001,1.001])assert.equal(make([5,5,depth]).pick(5,5),null);
 for(const depth of [-1,0,1])assert.equal(make([5,5,depth]).pick(5,5),place);
});
test('source fallback and nearest valid site remain intact',()=>{
 const a={id:'LOC-A',anchor:[0,0,0],renderAnchor:[10,10,0]},b={id:'LOC-B',anchor:[0,0,0],renderAnchor:[12,12,0]};
 const x=make([5,5,0],{places:[a,b],frames:{}});
 assert.equal(x.pick(12,12),b);assert.equal(x.pick(10,10),a);
 const c={id:'LOC-C',anchor:[10,0,0]};
 assert.equal(make([5,5,0],{places:[c],frames:{}}).pick(10,5),c);
});
