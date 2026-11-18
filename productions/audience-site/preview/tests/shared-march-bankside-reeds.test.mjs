import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),before=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const id='LOC-TDS-CHILI-SHARED-MARCH',label='Shared March swaying bank reeds · candidate';
const reed=a=>a.locations.find(x=>x.id===id)?.group.children.find(x=>x.name===label);
function delta(rise,phase,time){
 const bend=Math.sin(time*.73+phase)+.3*Math.sin(time*1.21+phase*1.73);
 return [Math.pow(rise,1.7)*.16*bend,Math.pow(rise,1.6)*.035*Math.sin(time*.51+phase*1.31)];
}

test('source-exact Shared March alone retains the existing crossing and adds one candidate reed mesh',()=>{
 const upstream=source.locations.find(x=>x.id===id);
 assert.ok(upstream.persistent_landmarks.includes('watercourse crossing'));
 assert.equal(upstream.physical_zone_id,'REG-WESTERN-TABLELANDS');
 const a=build(),site=a.locations.find(x=>x.id===id),r=reed(a);
 assert.ok(site&&r);
 assert.equal(site.group.children.filter(x=>x.name===label).length,1);
 assert.equal(r.geometry.type,'BufferGeometry');
 assert.equal(r.material.isShaderMaterial,true);
 assert.equal(r.castShadow,false);
 assert.equal(r.receiveShadow,false);
 assert.ok(site.group.children.some(x=>x.name==='Watercourse crossing'));
 assert.equal(a.water.filter(x=>x.kind==='watercourse crossing').length,1);
 assert.equal(a.water.length,4);assert.equal(a.locations.length,20);
 for(const other of a.locations.filter(x=>x.id!==id))assert.equal(other.group.children.filter(x=>x.name===label).length,0,other.id);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(a.worldMutationAllowed,false);
 assert.equal(a.weatherMutationAllowed,false);assert.equal(JSON.stringify(bindings),before);a.dispose();
});
test('bankside strips reuse one mesh, keep bridge approach clear and pin every stem base',()=>{
 const a=build(),r=reed(a),geo=r.geometry,pos=geo.getAttribute('position'),uv=geo.getAttribute('uv'),phase=geo.getAttribute('aPhase');
 assert.equal(pos.count,120,'20 stems with six vertices each');
 assert.equal(phase.count,120);assert.equal(geo.index.count,240);
 assert.ok(geo.getAttribute('normal'));
 let bases=0,topMotion=0,change=0;const zBands=new Set();
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),z=pos.getZ(i),rise=uv.getY(i),ph=phase.getX(i);
  assert.ok([x,y,z,rise,ph].every(Number.isFinite));
  assert.ok(Math.abs(x)>=1.35,'reed candidate outside crossing corridor');
  assert.ok(z>0.9&&z<4.75,'reeds flank existing modeled water disk');
  zBands.add(z<2?'south':'north');
  const p=delta(rise,ph,1.2),q=delta(rise,ph,3.8);
  for(const [dx,dz] of [p,q]){assert.ok(Math.abs(dx)<=.2080001);assert.ok(Math.abs(dz)<=.0350001);}
  if(rise===0){bases++;assert.ok(p.every(v=>Math.abs(v)===0)&&q.every(v=>Math.abs(v)===0),'base stays pinned, including signed zero');}
  if(rise===1){topMotion=Math.max(topMotion,Math.abs(p[0]),Math.abs(q[0]));change=Math.max(change,Math.abs(p[0]-q[0]));}
 }
 assert.equal(bases,40);assert.equal(zBands.size,2);assert.ok(topMotion>.1&&change>.11);
 for(const term of ['float bend=sin(uTime*.73+aPhase)+.3*sin(uTime*1.21+aPhase*1.73);','p.x+=pow(rise,1.7)*.16*bend;','p.z+=pow(rise,1.6)*.035*sin(uTime*.51+aPhase*1.31);'])assert.ok(r.material.vertexShader.includes(term),term);
 assert.ok(r.material.fragmentShader.includes('vec3 base=mix(vec3(.18,.24,.12),vec3(.39,.49,.21),vRise);'));
 assert.equal(JSON.stringify(bindings),before);a.dispose();
});
test('reed motion follows ordinary clock through calm, freezes on explicit pause and disposes once',()=>{
 const a=build(),r=reed(a),mat=r.material;
 a.tick(1.4,{storm:0,globalCalm:true});assert.equal(mat.uniforms.uTime.value,1.4);
 a.tick(3.7,{storm:0,globalCalm:true});assert.equal(mat.uniforms.uTime.value,3.7);
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.7));
 a.tick(9.2,{paused:true,storm:3});assert.equal(mat.uniforms.uTime.value,3.7);
 let count=0;mat.addEventListener('dispose',()=>count++);
 a.dispose();a.dispose();assert.equal(count,1);a.tick(15);assert.equal(mat.uniforms.uTime.value,3.7);
 assert.equal(JSON.stringify(bindings),before);
});
