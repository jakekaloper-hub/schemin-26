import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),original=JSON.stringify(bindings);
const placeId='LOC-PITTSYS-BOOK',build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(l=>l.id===placeId);
const part=(a,name)=>site(a)?.group.children.find(o=>o.name===name);
const leaves=a=>part(a,'Open ledger leaves — unlabeled');

test('Pittsy source landmarks and two older stacks remain; open pages exist at no other site',()=>{
 const place=source.locations.find(l=>l.id===placeId),a=build(),s=site(a),pages=leaves(a),cover=part(a,'Open ledger cover candidate');
 assert.equal(place.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(place.persistent_landmarks,['ledger boards','settlement desk']);
 assert.deepEqual(place.current_state,['recurring bookmaking function']);
 assert.equal(a.locations.length,20);assert.ok(s&&pages&&cover);
 assert.equal(s.group.userData.canonStatus,'PROVISIONAL_CANON');
 for(const landmark of place.persistent_landmarks)
  assert.equal(s.group.children.filter(o=>o.userData?.sourceLandmark===landmark).length,1,landmark);
 assert.equal(s.group.children.filter(o=>o.name==='Unlettered ledger').length,6);
 for(const other of a.locations.filter(l=>l.id!==placeId))
  assert.ok(!other.group.children.some(o=>o.name.startsWith('Open ledger')),other.id);
 for(const piece of [pages,cover]){
  assert.equal(piece.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(piece.userData.contentAuthority,'NONE');
 }
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),original);a.dispose();
});

test('two unlettered curved leaves are ruled, within the desk and deterministic',()=>{
 const a=build(),b=build(),o=leaves(a),q=leaves(b),cover=part(a,'Open ledger cover candidate');
 const p=o.geometry.getAttribute('position'),c=o.geometry.getAttribute('color'),i=o.geometry.getIndex();
 assert.equal(p.count,750);assert.equal(c.count,750);assert.equal(i.count,4032);
 assert.equal(o.material.vertexColors,true);assert.equal(o.material.side,THREE.DoubleSide);
 assert.equal(o.material.roughness,1);assert.ok(o.geometry.getAttribute('normal'));
 assert.ok(Math.abs(cover.position.x+.07)<1e-8&&Math.abs(cover.position.y-1.5825)<1e-6);
 assert.equal(cover.geometry.parameters.width,1.55);assert.equal(cover.geometry.parameters.depth,1.24);
 let minY=Infinity,maxY=-Infinity,low=0,high=0;
 for(let k=0;k<p.count;k++){
  const x=p.getX(k),y=p.getY(k),z=p.getZ(k),tone=c.getX(k);
  assert.ok(x>=-.800001&&x<=.660001);
  assert.ok(y>=1.600001&&y<=1.690001);
  assert.ok(z>=.629999&&z<=1.770001);
  assert.ok(Number.isFinite(tone)&&tone>.75&&tone<.91);
  assert.ok(c.getY(k)<tone&&c.getZ(k)<c.getY(k));
  minY=Math.min(minY,y);maxY=Math.max(maxY,y);
  if(tone<.82)low++;if(tone>.86)high++;
 }
 assert.ok(maxY-minY>.05,'curved leaves, not a flat sheet');
 assert.ok(low>80&&high>200,'nonverbal ruled stripes, no bookmaking text');
 assert.deepEqual(p.array,q.geometry.getAttribute('position').array);
 assert.deepEqual(c.array,q.geometry.getAttribute('color').array);
 assert.deepEqual(i.array,q.geometry.getIndex().array);
 assert.equal(JSON.stringify(bindings),original);a.dispose();b.dispose();
});

test('static book cannot write world history or weather; global calm does not stop ordinary water',()=>{
 const a=build(),page=leaves(a),before=page.geometry.getAttribute('position').array.slice();
 assert.ok(a.water.length>=4);
 a.tick(1.25,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.25));
 a.tick(3.5,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.5));
 a.tick(8,{paused:true,storm:4});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.5));
 assert.deepEqual(page.geometry.getAttribute('position').array,before);
 assert.equal(JSON.stringify(bindings),original);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 let disposed=0;page.material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,1);
});
