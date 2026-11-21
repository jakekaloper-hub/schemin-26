import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const places=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall','temple stone','dense vegetation']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','golf grounds','water hazards']}
];
const build=()=>buildRegionalAssets(THREE,places,()=>2);
const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const threads=(u,v,t)=>{
 const coordinate=u*47+Math.sin(v*13-t*1.17)*1.1;
 return Math.max(Math.sin(coordinate),0)**10
   *(.5+.5*Math.sin(v*25-t*3.6+u*8))
   *smooth(.02,.13,u)*(1-smooth(.87,.98,u))
   *smooth(.025,.16,v)*(1-smooth(.86,.985,v));
};

test('Temple foam threads shade the one existing sheet, not other waters or climate',()=>{
 const a=build(),waterfall=a.water.filter(w=>w.kind==='waterfall');
 assert.equal(waterfall.length,1);
 const {mesh,material}=waterfall[0];
 assert.deepEqual([mesh.geometry.parameters.width,mesh.geometry.parameters.height,mesh.geometry.parameters.widthSegments,mesh.geometry.parameters.heightSegments],[2.15,6.9,24,32]);
 assert.deepEqual(mesh.position.toArray(),[-5.8,3.75,1.8]);
 assert.equal(mesh.geometry.type,'PlaneGeometry');
 assert.equal(material.uniforms.uFall.value,1);
 const shader=material.fragmentShader;
 const start=shader.indexOf('if(uFall>.5){'),end=shader.indexOf('}else if(uWetland>.5){',start);
 assert.ok(start>0&&end>start);
 const fall=shader.slice(start,end);
 for(const fragment of [
  'threadCoordinate=vUv.x*47.+sin(vUv.y*13.-uTime*1.17)*1.1',
  'foamThread=pow(max(sin(threadCoordinate),0.),10.)',
  'brokenThread=.5+.5*sin(vUv.y*25.-uTime*3.6+vUv.x*8.)',
  'sideFade=smoothstep(.02,.13,vUv.x)*(1.-smoothstep(.87,.98,vUv.x))',
  'endFade=smoothstep(.025,.16,vUv.y)*(1.-smoothstep(.86,.985,vUv.y))',
  'threadLight=foamThread*brokenThread*sideFade*endFade',
  'fallTint=clamp(fallTint+vec3(.055,.071,.061)*threadLight,0.,1.)',
  'gl_FragColor=vec4(fallTint,.88)'
 ]) assert.ok(fall.includes(fragment),fragment);
 assert.doesNotMatch(shader.slice(end),/foamThread|threadLight|threadCoordinate/);
 assert.doesNotMatch(fall,/\buStorm\b|\buWeather\b|\buRain\b|\buGlobalCalm\b/);
 for(const w of a.water.filter(w=>w.kind!=='waterfall'))assert.equal(w.material.uniforms.uFall?.value??0,0);
 a.dispose();
});

test('bounded deterministic interior threads actually move while all four edges remain clean',()=>{
 let max=0,maxChange=0;
 for(let i=0;i<=40;i++)for(let j=0;j<=40;j++){
  const u=i/40,v=j/40;
  for(const t of [0,1.9,8]){
   const value=threads(u,v,t);
   assert.ok(Number.isFinite(value)&&value>=0&&value<=1.000001);
   if(i===0||i===40||j===0||j===40)assert.ok(Math.abs(value)<1e-12,'perimeter remains unaffected');
   max=Math.max(max,value);
   maxChange=Math.max(maxChange,Math.abs(value-threads(u,v,t+.31)));
  }
 }
 assert.ok(max>.4,'candidate foam is not merely an inert shader declaration');
 assert.ok(maxChange>.1,'threads visibly advect within the existing water');
 assert.ok(max*.071<=.0710001,'bounded additive highlight strength');
});

test('El Nino synthetic global calm preserves foam clock; only explicit pause freezes',()=>{
 const before=JSON.stringify(places),a=build(),w=a.water.find(w=>w.kind==='waterfall');
 let geometryDisposals=0,materialDisposals=0;
 w.mesh.geometry.addEventListener('dispose',()=>geometryDisposals++);
 w.material.addEventListener('dispose',()=>materialDisposals++);
 a.tick(1,{globalCalm:true,storm:0});assert.equal(w.material.uniforms.uTime.value,1);
 a.tick(4.4,{globalCalm:true,storm:0});assert.equal(w.material.uniforms.uTime.value,4.4);
 a.tick(7.7,{paused:true,globalCalm:true,storm:0});assert.equal(w.material.uniforms.uTime.value,4.4);
 a.tick(11,{globalCalm:true,storm:0});assert.equal(w.material.uniforms.uTime.value,11);
 assert.deepEqual(a.locations.map(l=>l.id),places.map(l=>l.id));
 assert.ok(a.locations.every(l=>l.group.userData.visualAuthority==='CANDIDATE_NOT_APPROVED'));
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(places),before);
 a.dispose();a.dispose();
 assert.equal(geometryDisposals,1);assert.equal(materialDisposals,1);
});
