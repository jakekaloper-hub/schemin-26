import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const places=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,places,()=>2);
const bank=a=>a.locations[0].group.getObjectByName('Candidate wetland shoreline transition');
const baseline=i=>{
 const a=i/96*Math.PI*2,w=Math.sin(a*7+.3)*.018+Math.sin(a*13-.8)*.009;
 return {a,r:[1.019+Math.sin(a*11)*.006,1.079+w,1.188+w*1.6+Math.sin(a*5)*.012],
 y:[.102,.235+Math.sin(a*9)*.018,.105+Math.cos(a*6)*.018]};
};
const close=(a,b)=>assert.ok(Math.abs(a-b)<2e-6,`${a} != ${b}`);
test('sediment bands interpolate existing bank footprint with bounded inward relief and upward normals',()=>{
 const a=build();
 try{
  const b=bank(a),g=b.geometry,p=g.getAttribute('position'),n=g.getAttribute('normal'),c=g.getAttribute('color');
  assert.equal(p.count,485);assert.equal(g.index.count,2304);
  assert.equal(n.count,p.count);assert.equal(c.count,p.count);
  const depths=new Set();
  for(let i=0;i<=96;i++){
   const {a:angle,r,y}=baseline(i);
   for(let j=0;j<5;j++){
    const k=i*5+j,lo=Math.floor(j/2),hi=Math.ceil(j/2);
    const rad=(r[lo]+r[hi])/2,h=(y[lo]+y[hi])/2;
    close(p.getX(k),Math.cos(angle)*10.5*rad);close(p.getZ(k),Math.sin(angle)*8.2*rad);
    if(j%2===0)close(p.getY(k),h);
    else {
     const depth=h-p.getY(k);assert.ok(depth>=.003&&depth<=.045);depths.add(depth.toFixed(4));
    }
    assert.ok(n.getY(k)>.70);
    assert.ok([c.getX(k),c.getY(k),c.getZ(k)].every(x=>Number.isFinite(x)&&x>=0&&x<=1));
   }
  }
  assert.ok(depths.size>50);
  for(let j=0;j<5;j++){
   for(const axis of ['getX','getY','getZ']){close(p[axis](j),p[axis](480+j));close(n[axis](j),n[axis](480+j));close(c[axis](j),c[axis](480+j));}
  }
  assert.equal(b.material.vertexColors,true);
  assert.equal(b.material,a.locations[0].group.getObjectByName('Candidate wetland raised-ground relief').material);
  assert.equal(b.castShadow,false);assert.equal(b.renderOrder,1);
 }finally{a.dispose();}
});
test('shoreline sediment candidate is deterministic, local and leaves source and water motion intact',()=>{
 const original=JSON.stringify(places),a=build(),b=build();
 try{
  const x=bank(a),y=bank(b);
  for(const name of ['position','normal','color'])assert.deepEqual(x.geometry.getAttribute(name).array,y.geometry.getAttribute(name).array);
  assert.deepEqual(x.userData.sourceLandmarks,['mud channels','raised ground']);
  assert.equal(x.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(x.userData.navigable,false);assert.deepEqual(x.userData.routeIds,[]);
  for(const l of a.locations.slice(1))assert.equal(l.group.getObjectByName(x.name),undefined);
  const w=a.water.find(w=>w.kind==='swamp');
  assert.equal(w.mesh.geometry.getAttribute('position').count,385);
  a.tick(2,{globalCalm:true});a.tick(6,{globalCalm:true});assert.equal(w.material.uniforms.uTime.value,6);
  a.tick(9,{globalCalm:true,paused:true});assert.equal(w.material.uniforms.uTime.value,6);
  assert.equal(JSON.stringify(places),original);assert.equal(a.worldMutationAllowed,false);
 }finally{a.dispose();b.dispose();}
});
