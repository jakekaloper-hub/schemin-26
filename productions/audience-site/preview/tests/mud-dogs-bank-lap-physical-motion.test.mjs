import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const loc=atlas.locations.find(s=>s.id===id);
  assert.ok(loc, 'Established Atlas location: '+id);
  return {id,anchor:[loc.abstract_position[0],0,loc.abstract_position[1]],
    canonStatus:loc.canon_status,landmarks:loc.persistent_landmarks};
});
const originals=[JSON.stringify(atlas),JSON.stringify(bindings)];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function shorelineLap(u,v,time){
  const x=(u-.5)*2,y=(v-.5)*2,r=Math.hypot(x,y),angle=Math.atan2(y,x);
  const band=smooth(.76,.84,r)*(1-smooth(.94,.99,r));
  const phase=r*55-time*2.15-1.7+.43*Math.sin(angle*7+time*.27);
  const broken=.55+.45*Math.sin(angle*11-time*.43);
  return .010*band*broken*Math.max(Math.sin(phase),0)**3;
}

test('Only source-defined Mud Dogs Swamp receives a physical bank lap on its unchanged surface',()=>{
  const a=build();
  const site=atlas.locations.find(s=>s.id==='LOC-MUD-DOGS-SWAMP');
  assert.equal(site.physical_zone_id,'REG-SOUTHERN-WETLANDS');
  assert.equal(site.canon_status,'PERMANENT_CANON');
  assert.deepEqual(a.locations.map(x=>x.id),ids);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  const swamp=a.water.find(w=>w.kind==='swamp');
  const channel=a.water.find(w=>w.kind==='channel');
  assert.ok(swamp&&channel);
  assert.equal(swamp.mesh.parent,a.locations[1].group);
  assert.deepEqual(swamp.mesh.position.toArray(),[0,.12,0]);
  assert.deepEqual(swamp.mesh.scale.toArray(),[10.5,8.2,1]);
  assert.equal(swamp.mesh.rotation.x,-Math.PI/2);
  assert.equal(swamp.mesh.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(swamp.material.uniforms.uRootSiteCount.value,5);
  assert.equal(channel.material.uniforms.uRootSiteCount.value,0);
  assert.ok(a.water.filter(w=>w.kind!=='swamp')
    .every(w=>(w.material.uniforms.uRootSiteCount?.value??0)===0));
  const shader=swamp.material.vertexShader;
  assert.match(shader,/if\(uRootSiteCount>\.5\)\{\s*vec2 bankPoint=/);
  assert.match(shader,/lapBand=smoothstep\(\.76,\.84,lapRadius\)/);
  assert.match(shader,/lapPhase=lapRadius\*55\.-uTime\*2\.15/);
  assert.match(shader,/p\.z\+=\.010\*lapBand\*lapBreak\*lapCrest/);
  assert.ok(shader.indexOf('lapBand=smoothstep')>shader.indexOf('if(uWetland>.5){'));
  assert.ok(shader.indexOf('lapBand=smoothstep')<shader.indexOf('if(uRiver>.5){'));
  assert.doesNotMatch(shader.slice(shader.indexOf('lapBand=smoothstep'),
    shader.indexOf('// Root ripples physically affect')), /\buStorm\b|\buWeather\b|\buGlobalCalm\b/);
  assert.equal(swamp.mesh.geometry.getAttribute('position').count,385);
  assert.equal(swamp.mesh.geometry.index.count,2160);
  assert.equal(JSON.stringify(atlas),originals[0]);
  assert.equal(JSON.stringify(bindings),originals[1]);
  a.dispose();
});

test('Original bank vertices have deterministic nonzero ordinary-time relief while perimeter stays fixed',()=>{
  const a=build(),b=build();
  const swamp=a.water.find(w=>w.kind==='swamp');
  const identical=b.water.find(w=>w.kind==='swamp');
  assert.equal(swamp.material.vertexShader,identical.material.vertexShader);
  const geo=swamp.mesh.geometry,uv=geo.getAttribute('uv'),pos=geo.getAttribute('position');
  let edge=0,bank=0,changed=0,peak=0;
  for(let i=0;i<uv.count;i++){
    const u=uv.getX(i),v=uv.getY(i),r=Math.hypot((u-.5)*2,(v-.5)*2);
    const h0=shorelineLap(u,v,.4),h1=shorelineLap(u,v,2.15);
    assert.ok(Number.isFinite(h0)&&Number.isFinite(h1));
    assert.ok(h0>=0&&h0<=.010000001&&h1>=0&&h1<=.010000001);
    peak=Math.max(peak,h0,h1);
    if(r>.84&&r<.94){bank++;if(Math.abs(h0-h1)>.002)changed++;}
    if(r>=.999999){edge++;assert.ok(Math.abs(h0)<1e-12&&Math.abs(h1)<1e-12);}
    assert.ok(Math.abs(pos.getZ(i))<1e-12);
  }
  assert.ok(edge>=48,'Original 48 perimeter vertices retained and still');
  assert.ok(bank>=40&&changed>=12,'Shoreline vertices actually move with local water clock');
  assert.ok(peak>.005,'Relief magnitude visible on real existing bank vertices');
  assert.equal(JSON.stringify(atlas),originals[0]);
  a.dispose();b.dispose();
});

test('Calm weather never freezes water; pause, static batching and disposal remain bounded',()=>{
  const a=build(),swamp=a.water.find(w=>w.kind==='swamp');
  const group=a.locations[1].group,childCount=group.children.length;
  const batches=batchStaticGeometry(THREE,group);
  assert.ok(group.children.length<childCount);
  assert.ok(group.children.includes(swamp.mesh),'Animated swamp stays outside static geometry batches');
  batches.geometries.forEach(g=>g.dispose());
  assert.deepEqual(a.water.map(w=>w.kind),[
    'river','waterfall','landing-ripple','landing-ripple','landing-ripple','landing-ripple',
    'pool','swamp','channel','pond'
  ]);
  for(const t of [1,3.5,8.75]){
    a.tick(t,{weatherMode:'GLOBAL_CALM',storm:0});
    assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===t));
  }
  a.tick(19,{weatherMode:'GLOBAL_CALM',storm:0,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===8.75));
  let disposals=0,geos=0;
  swamp.material.addEventListener('dispose',()=>disposals++);
  swamp.mesh.geometry.addEventListener('dispose',()=>geos++);
  a.dispose();a.dispose();a.tick(30);
  assert.equal(disposals,1);assert.equal(geos,1);
  assert.equal(JSON.stringify(atlas),originals[0]);
  assert.equal(JSON.stringify(bindings),originals[1]);
});
