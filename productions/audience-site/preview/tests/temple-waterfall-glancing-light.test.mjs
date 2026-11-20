import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
 const p=atlas.locations.find(l=>l.id===id);
 assert.ok(p,'Missing source-bound Atlas site '+id);
 return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
   canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const atlasBefore=JSON.stringify(atlas),bindingsBefore=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const waterfall=a=>a.water.find(w=>w.kind==='waterfall');
const clamp=x=>Math.max(0,Math.min(1,x));
const smooth=(a,b,x)=>{let t=clamp((x-a)/(b-a));return t*t*(3-2*t);};
const normalize=a=>{const n=Math.hypot(...a);return a.map(x=>x/n);};
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
function glint(normal,eye,u,foam){
 const sky=normalize([.19,.32,.93]),view=normalize(eye),half=normalize(view.map((x,i)=>x+sky[i]));
 const spec=Math.pow(clamp(Math.abs(dot(normalize(normal),half))),24);
 const interior=smooth(.03,.18,u)*(1-smooth(.82,.97,u));
 return spec*(.48+.52*foam)*interior;
}

test('Real imported Waterfall Temple shader adds one bounded camera-dependent glint only to the inherited sheet',()=>{
 const a=build(),w=waterfall(a),g=a.locations[0].group;
 assert.equal(atlas.locations.find(x=>x.id===ids[0]).physical_zone_id,'REG-SOUTHERN-WETLANDS');
 assert.equal(atlas.locations.find(x=>x.id===ids[0]).canon_status,'PERMANENT_CANON');
 assert.ok(atlas.locations.find(x=>x.id===ids[0]).persistent_landmarks.includes('waterfall'));
 assert.deepEqual(a.locations.map(x=>x.id),ids);
 assert.equal(a.water.filter(x=>x.kind==='waterfall').length,1);
 assert.equal(w.mesh.parent,g);
 assert.equal(w.mesh.name,'Candidate Temple contoured animated waterfall sheet');
 assert.deepEqual(w.mesh.userData.originalDimensions,[2.15,6.9]);
 assert.deepEqual([w.mesh.geometry.parameters.widthSegments,w.mesh.geometry.parameters.heightSegments],[24,32]);
 assert.deepEqual(w.mesh.position.toArray(),[-5.8,3.75,1.8]);
 assert.equal(w.mesh.userData.originalPerimeterPreserved,true);
 assert.equal(w.mesh.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(w.mesh.userData.sourceLandmark,'waterfall');
 assert.equal(w.mesh.userData.navigable,false);
 assert.deepEqual(w.mesh.userData.routeIds,[]);
 assert.deepEqual(w.mesh.userData.principalCharacters,[]);
 assert.equal(w.mesh.material.transparent,true);
 assert.equal(w.mesh.material.depthWrite,false);
 assert.deepEqual(Object.keys(w.material.uniforms).sort(),[
  'uBankContact','uChannel','uColor','uFall','uFlow','uIslandSiteCount','uIslandSites',
  'uPadSiteCount','uPadSites','uPlunge','uPond','uRiver','uRootSiteCount','uRootSites',
  'uSheenGain','uTime','uWetland'
 ].sort(),'No new uniforms added');
 const shader=w.material.fragmentShader,start=shader.indexOf('if(uFall>.5){'),
   stop=shader.indexOf('}else if(uWetland>.5){',start),fall=shader.slice(start,stop);
 assert.ok(start>0&&stop>start);
 assert.match(fall,/faceCross=cross\(dFdx\(vWorld\),dFdy\(vWorld\)\)/);
 assert.match(fall,/skyKey=normalize\(vec3\(\.19,\.32,\.93\)\)/);
 assert.match(fall,/halfRay=normalize\(eyeRay\+skyKey\)/);
 assert.match(fall,/glancingSpecular=pow\(clamp\(abs\(dot\(sheetNormal,halfRay\)\),0\.,1\.\),24\.\)/);
 assert.match(fall,/specularInterior=smoothstep\(\.03,\.18,vUv\.x\)\*\(1\.-smoothstep\(\.82,\.97,vUv\.x\)\)/);
 assert.match(fall,/sprayGlint=glancingSpecular\*\(\.48\+\.52\*foam\)\*specularInterior/);
 assert.match(fall,/fallTint=clamp\(fallTint\+vec3\(\.085,\.11,\.092\)\*sprayGlint,0\.,1\.\)/);
 assert.match(fall,/gl_FragColor=vec4\(fallTint,\.88\)/,'Original sheet alpha unchanged');
 assert.doesNotMatch(shader.slice(stop),/skyKey|halfRay|glancingSpecular|sprayGlint/);
 assert.doesNotMatch(fall,/\buStorm\b|\buWeather\b|\buRain\b|\buGlobalCalm\b/);
 assert.ok(a.water.filter(x=>x.kind!=='waterfall').every(x=>(x.material.uniforms.uFall?.value??0)===0));
 for(const other of a.locations.slice(1))assert.equal(other.group.getObjectByName(w.mesh.name),undefined);
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(atlas),atlasBefore);assert.equal(JSON.stringify(bindings),bindingsBefore);
 a.dispose();
});

test('Glancing light is nontrivial under camera/physical normal changes but finite, soft and edge-suppressed',()=>{
 const front=glint([0,0,1],[0,0,1],.5,.7);
 const side=glint([0,0,1],[1,0,.12],.5,.7);
 const fold=glint([.46,.25,.85],[0,0,1],.5,.7);
 assert.ok(front>.2,'Front view gives a visible physical highlight');
 assert.ok(Math.abs(front-side)>.1,'Camera actually changes lighting');
 assert.ok(Math.abs(front-fold)>.1,'Folded geometry actually changes lighting');
 assert.ok(glint([0,0,1],[0,0,1],.5,1)>glint([0,0,1],[0,0,1],.5,0));
 let visible=0;
 for(let i=0;i<=100;i++)for(const foam of [0,.5,1]){
  const u=i/100,g=glint([0,0,1],[0,0,1],u,foam);
  assert.ok(Number.isFinite(g)&&g>=0&&g<=1);
  assert.ok([.085,.11,.092].every(c=>c*g<=c+1e-12));
  if(g>.01)visible++;
  if(u===0||u===1)assert.equal(g,0,'Outer sheet edges have no extra light');
 }
 assert.ok(visible>150,'Broad interior, not a single-point optical artifact');
});

test('Original batching/water clocks remain independent of synthetic global calm; explicit pause/disposal work',()=>{
 const a=build(),temple=a.locations[0].group,w=waterfall(a),oldCount=temple.children.length;
 const batches=batchStaticGeometry(THREE,temple);
 assert.ok(temple.children.length<oldCount);
 assert.ok(temple.children.includes(w.mesh),'Dynamic water not absorbed into opaque static batches');
 for(const geometry of batches.geometries)geometry.dispose();
 const moving=a.water.filter(x=>['waterfall','river','pool','swamp','channel','pond'].includes(x.kind));
 assert.equal(moving.length,6);
 let geomDisposals=0,matDisposals=0;
 w.mesh.geometry.addEventListener('dispose',()=>geomDisposals++);
 w.material.addEventListener('dispose',()=>matDisposals++);
 a.tick(3,{globalCalm:true,storm:0});
 a.tick(11,{globalCalm:true,storm:0});
 assert.ok(moving.every(x=>x.material.uniforms.uTime.value===11));
 a.tick(16,{paused:true,globalCalm:true,storm:0});
 assert.ok(moving.every(x=>x.material.uniforms.uTime.value===11));
 a.tick(24,{globalCalm:true,storm:0});
 assert.ok(moving.every(x=>x.material.uniforms.uTime.value===24));
 a.dispose();a.dispose();a.tick(29);
 assert.equal(geomDisposals,1);assert.equal(matDisposals,1);
 assert.equal(JSON.stringify(atlas),atlasBefore);assert.equal(JSON.stringify(bindings),bindingsBefore);
});
