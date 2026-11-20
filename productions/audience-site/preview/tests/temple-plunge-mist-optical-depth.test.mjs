import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
 const p=atlas.locations.find(x=>x.id===id);
 assert.ok(p,'Missing source Atlas place '+id);
 return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
   canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const oldAtlas=JSON.stringify(atlas),oldBindings=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const temple=a=>a.locations.find(x=>x.id===ids[0]).group;
const mist=a=>temple(a).getObjectByName('Candidate waterfall plunge mist');
const clamp=x=>Math.max(0,Math.min(1,x));
const smooth=(a,b,x)=>{const t=clamp((x-a)/(b-a));return t*t*(3-2*t);};
function optical(radial,depth,age,driftY){
 const core=1-smooth(.02,.30,radial),feather=1-smooth(.08,.49,radial);
 const vOpacity=Math.pow(Math.max(Math.sin(age*Math.PI),0),.75)*(.50+.38*driftY);
 const vViewFade=1-.25*smooth(7,85,depth);
 const rgb=[.68,.82,.78].map((v,i)=>v+([.91,.96,.88][i]-v)*(core*.42));
 return {rgb,alpha:feather*vOpacity*(.16+.07*core)*vViewFade,core,vViewFade};
}

test('Existing Waterfall Temple emitter remains exactly one source-local 144-point layer with zero new uniforms',()=>{
 const a=build(),o=mist(a),geo=o.geometry;
 assert.equal(atlas.locations.find(p=>p.id===ids[0]).canon_status,'PERMANENT_CANON');
 assert.ok(atlas.locations.find(p=>p.id===ids[0]).persistent_landmarks.includes('waterfall'));
 assert.deepEqual(a.locations.map(x=>x.id),ids);
 assert.equal(temple(a).userData.locationId,ids[0]);
 assert.equal(a.root.getObjectsByProperty('name',o.name).length,1);
 assert.equal(o.isPoints,true);
 assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(o.userData.sourceLandmark,'waterfall');
 assert.equal(o.userData.navigable,false);
 assert.deepEqual(o.userData.routeIds,[]);
 assert.equal(geo.getAttribute('position').count,144);
 assert.equal(geo.getAttribute('aPhase').count,144);
 assert.equal(geo.getAttribute('aDrift').count,144);
 assert.deepEqual(Object.keys(o.material.uniforms),['uTime']);
 assert.equal(o.material.transparent,true);
 assert.equal(o.material.depthWrite,false);
 const pts=geo.getAttribute('position');
 for(let i=0;i<pts.count;i++){
   assert.ok(pts.getX(i)>-7.65&&pts.getX(i)<-3.95);
   assert.ok(pts.getY(i)>=.18&&pts.getY(i)<1.3);
   assert.ok(pts.getZ(i)>1.5&&pts.getZ(i)<4.4);
 }
 for(const other of a.locations.filter(x=>x.id!==ids[0]))
   assert.equal(other.group.getObjectByName(o.name),undefined);
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(atlas),oldAtlas);
 assert.equal(JSON.stringify(bindings),oldBindings);
 a.dispose();
});

test('Imported mist shaders compute bounded view extinction and feathered translucent scattering, no climate inputs',()=>{
 const a=build(),m=mist(a),v=m.material.vertexShader,f=m.material.fragmentShader;
 assert.match(v,/vViewFade=1\.-\.25\*smoothstep\(7\.,85\.,-view\.z\)/);
 assert.match(v,/float age=fract\(aPhase\+uTime\*\(\.105\+\.048\*aDrift\.y\)\)/);
 assert.match(v,/p\.y\+=launch-fall/);
 assert.match(f,/float core=1\.-smoothstep\(\.02,\.30,radial\)/);
 assert.match(f,/float feather=1\.-smoothstep\(\.08,\.49,radial\)/);
 assert.match(f,/vec3 scatter=mix\(vec3\(\.68,\.82,\.78\),vec3\(\.91,\.96,\.88\),core\*\.42\)/);
 assert.match(f,/float alpha=feather\*vOpacity\*\(\.16\+\.07\*core\)\*vViewFade/);
 assert.match(f,/gl_FragColor=vec4\(scatter,alpha\)/);
 assert.doesNotMatch(v+f,/\buStorm\b|\buRain\b|\buGlobalCalm\b|\buWeather\b/);
 const center=optical(0,8,.5,.8),middle=optical(.21,8,.5,.8),
       rim=optical(.5,8,.5,.8),far=optical(0,100,.5,.8);
 assert.ok(center.alpha>middle.alpha&&middle.alpha>rim.alpha);
 assert.equal(rim.alpha,0,'Finite soft radial edge');
 assert.ok(center.alpha>far.alpha&&far.alpha>0);
 assert.ok(center.rgb.every((c,i)=>c>=0&&c<1&&c>far.rgb[i]-.00001));
 assert.ok(center.rgb[0]>middle.rgb[0],'Core brighter than outer spray');
 assert.ok(center.vViewFade>far.vViewFade&&far.vViewFade===.75);
 let nonzero=0;
 for(let ri=0;ri<=50;ri++)for(const depth of [0,7,20,60,85,200]){
   const r=ri/100,z=optical(r,depth,.41,.7);
   assert.ok(Number.isFinite(z.alpha)&&z.alpha>=0&&z.alpha<=.230001);
   assert.ok(z.rgb.every(c=>Number.isFinite(c)&&c>=0&&c<=1));
   assert.ok(z.vViewFade>=.75&&z.vViewFade<=1);
   if(z.alpha>.005)nonzero++;
 }
 assert.ok(nonzero>80,'Nontrivial partially transparent sprite area');
 a.dispose();
});

test('Mist stays unbatched and advances with all original waters under global calm, freezes on pause, disposes once',()=>{
 const a=build(),g=temple(a),o=mist(a),initial=g.children.length;
 const batches=batchStaticGeometry(THREE,g);
 assert.ok(g.children.length<initial);
 assert.ok(g.children.includes(o),'Animated points must not enter opaque mesh batches');
 for(const geo of batches.geometries)geo.dispose();
 const water=a.water.filter(w=>['waterfall','river','pool','swamp','channel','pond'].includes(w.kind));
 assert.equal(water.length,6);
 let geoDisposals=0,matDisposals=0;
 o.geometry.addEventListener('dispose',()=>geoDisposals++);
 o.material.addEventListener('dispose',()=>matDisposals++);
 a.tick(2,{globalCalm:true,storm:0});
 a.tick(9,{globalCalm:true,storm:0});
 assert.equal(o.material.uniforms.uTime.value,9);
 assert.ok(water.every(w=>w.material.uniforms.uTime.value===9));
 a.tick(13,{globalCalm:true,storm:0,paused:true});
 assert.equal(o.material.uniforms.uTime.value,9);
 assert.ok(water.every(w=>w.material.uniforms.uTime.value===9));
 a.tick(18,{globalCalm:true,storm:0});
 assert.equal(o.material.uniforms.uTime.value,18);
 assert.ok(water.every(w=>w.material.uniforms.uTime.value===18));
 a.dispose();a.dispose();a.tick(40);
 assert.equal(geoDisposals,1);
 assert.equal(matDisposals,1);
 assert.equal(JSON.stringify(atlas),oldAtlas);
 assert.equal(JSON.stringify(bindings),oldBindings);
});
