import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(atlas.locations)});
const sourceSnapshot=JSON.stringify(bindings);

function assertMainIntegrity(glsl,kind,label) {
 const cleaned=glsl.replace(/\/\/[^\n]*/g,'').replace(/\/\*[\s\S]*?\*\//g,'');
 assert.equal((cleaned.match(/\bvoid\s+main\s*\(\s*(?:void\s*)?\)\s*\{/g)||[]).length,1,`${label} ${kind}: exactly one main()`);
 let depth=0;
 for(const ch of cleaned){
  if(ch==='{')depth++;
  if(ch==='}')depth--;
  assert.ok(depth>=0,`${label} ${kind}: closing brace before opening brace`);
 }
 assert.equal(depth,0,`${label} ${kind}: unclosed GLSL brace (headless WebGL2 compile gate)`);
 assert.ok(cleaned.trimEnd().endsWith('}'),`${label} ${kind}: shader ends after closed main`);
 assert.match(cleaned,kind==='vertex'?/\bgl_Position\s*=/:/\bgl_FragColor\s*=/,`${label} ${kind}: output assignment`);
}

test('all current Atlas site ShaderMaterials close their GLSL main functions before GPU compilation',()=>{
 assert.equal(THREE.REVISION,'187');
 const scene=buildAtlasSiteAssets(THREE,bindings,()=>4);
 assert.equal(scene.locations.length,20);
 assert.equal(scene.principalCharacters.length,0);
 assert.equal(scene.worldMutationAllowed,false);
 assert.equal(scene.weatherMutationAllowed,false);
 const shaders=new Map();
 for(const site of scene.locations){
  site.group.traverse(object=>{
   if(!object.isMesh||!object.material?.isShaderMaterial)return;
   const m=object.material;
   if(!shaders.has(m))shaders.set(m,new Set());
   shaders.get(m).add(site.id+'/'+object.name);
  });
 }
 assert.ok(shaders.size>=4,'source-backed candidate environment animation materials are inspected');
 for(const [material,placements] of shaders){
  const label=[...placements].join(' | ');
  assertMainIntegrity(material.vertexShader,'vertex',label);
  assertMainIntegrity(material.fragmentShader,'fragment',label);
 }
 const march=scene.locations.find(l=>l.id==='LOC-TDS-CHILI-SHARED-MARCH');
 const reeds=march.group.children.find(o=>o.name==='Shared March swaying bank reeds · candidate');
 assert.ok(reeds?.material?.isShaderMaterial,'the source-exact watercourse bank reeds are covered');
 assert.equal(JSON.stringify(bindings),sourceSnapshot,'shader audit cannot mutate Atlas inputs');
 scene.dispose();
});
