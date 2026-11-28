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
const id='LOC-DK-HIGHLAND-STRONGHOLD';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(l=>l.id===id);
const court=a=>site(a)?.group.children.find(o=>o.name==='Training court');

test('only source-recorded Highland Stronghold training court receives the sculpted static sand',()=>{
 const record=source.locations.find(l=>l.id===id);
 assert.deepEqual(record.persistent_landmarks,['highland stronghold','training court','road approach']);
 const a=build(),s=site(a),c=court(a);
 assert.ok(s&&c);assert.equal(a.locations.length,20);
 assert.equal(s.group.children.filter(o=>o.name==='Training court').length,1);
 assert.equal(c.userData.sourceLandmark,'training court');
 for(const landmark of record.persistent_landmarks)assert.ok(s.group.children.some(o=>o.userData?.sourceLandmark===landmark),landmark);
 assert.ok(s.group.children.some(o=>o.name==='Hall candidate'));
 assert.ok(s.group.children.some(o=>o.name==='Approach step'));
 for(const other of a.locations.filter(l=>l.id!==id))assert.equal(other.group.children.filter(o=>o.name==='Training court').length,0,other.id);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('static court retains exact mesh transform, footprint and budget while physically varying worn sand',()=>{
 const a=build(),c=court(a),geo=c.geometry,p=geo.getAttribute('position'),color=geo.getAttribute('color');
 assert.equal(geo.type,'BoxGeometry');
 assert.deepEqual([geo.parameters.width,geo.parameters.height,geo.parameters.depth],[7.8,.1,5]);
 assert.deepEqual([geo.parameters.widthSegments,geo.parameters.heightSegments,geo.parameters.depthSegments],[48,1,32]);
 assert.deepEqual(c.position.toArray(),[0,.86,1.2]);
 assert.deepEqual(c.scale.toArray(),[1,1,1]);
 assert.equal(p.count,color.count);assert.ok(p.count>=3200&&p.count<=3800);
 assert.equal(c.material.vertexColors,true);assert.equal(c.material.roughness,.99);
 let lowered=0,edgeTop=0,minY=Infinity,maxY=-Infinity,low=Infinity,high=-Infinity;
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  assert.ok([x,y,z].every(Number.isFinite));
  assert.ok(Math.abs(x)<=3.900001&&Math.abs(z)<=2.500001);
  assert.ok(y>=-.050001&&y<=.050001);
  if(y<.049&&y>-.049)lowered++;
  if((Math.abs(x)>3.899||Math.abs(z)>2.499)&&Math.abs(y-.05)<.00001)edgeTop++;
  const channels=[color.getX(i),color.getY(i),color.getZ(i)];
  assert.ok(channels.every(v=>Number.isFinite(v)&&v>.11&&v<.75));
  low=Math.min(low,...channels);high=Math.max(high,...channels);
  minY=Math.min(minY,y);maxY=Math.max(maxY,y);
 }
 assert.ok(lowered>600,'dense top surface contains physical compacted relief');
 assert.ok(edgeTop>100,'all original top outer edges remain at original elevation');
 assert.equal(minY,-.05000000074505806); // Float32 position representation of -0.05
 assert.ok(maxY>.049&&maxY<.051);
 assert.ok(high-low>.25,'colored sand lanes and granular tonal variation');
 assert.ok(geo.getAttribute('normal'));
 const b=build(),other=court(b);
 assert.deepEqual(p.array,other.geometry.getAttribute('position').array,'repeatable surface geometry');
 assert.deepEqual(color.array,other.geometry.getAttribute('color').array,'repeatable surface tones');
 a.dispose();b.dispose();
});

test('worn-sand visualization cannot create weather or history events and preserves calm-water motion, pause and disposal',()=>{
 const a=build(),c=court(a),snapshot=c.geometry.getAttribute('position').array.slice();
 a.tick(1.2,{globalCalm:true,storm:0});
 assert.ok(a.water.length>=4&&a.water.every(w=>w.material.uniforms.uTime.value===1.2));
 a.tick(3.6,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.6));
 a.tick(5,{paused:true,storm:4});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.6));
 assert.deepEqual(c.geometry.getAttribute('position').array,snapshot);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),before);
 let disposed=0;c.material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,1);
});
