import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const source=[
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[12,0,27],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[38,0,14],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[52,0,19],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,source,()=>2);
const crest=(radial,time,phase)=>{
  const progress=(time*.19+phase)%1;
  const azimuth=.6;
  const envelope=Math.sin(Math.PI*radial);
  const pulse=.70+.30*Math.sin(azimuth*7-time*.42+phase*Math.PI*2);
  return .033*envelope*pulse*(1-progress)**1.6;
};
const alpha=(radial,time,phase,azimuth)=>{
  const progress=(time*.19+phase)%1;
  const crown=Math.sin(Math.PI*radial);
  const foam=.5+.5*Math.sin(azimuth*9-time*.56+phase*Math.PI*2);
  return .43*(1-progress)**1.5*(.30+.70*foam**1.5)*(.24+.76*crown);
};

test('four inherited landing rings have one bounded physically subdivided crest each',()=>{
  const before=JSON.stringify(source),a=build();
  assert.deepEqual(a.locations.map(x=>x.id),source.map(x=>x.id));
  const rings=a.water.filter(w=>w.kind==='landing-ripple');
  assert.equal(rings.length,4);
  assert.equal(new Set(rings.map(w=>w.material.uniforms.uPhase.value)).size,4);
  assert.deepEqual(rings.map(w=>w.material.uniforms.uPhase.value),[0,.25,.5,.75]);
  for(const [i,w] of rings.entries()){
    const [x,y,z]=w.mesh.position.toArray();
    assert.ok(Math.abs(x+5.8)<1e-10&&Math.abs(y-(.40+i*.008))<1e-10&&Math.abs(z-2.7)<1e-10);
  }
  for(const w of rings){
    const g=w.mesh.geometry,p=g.getAttribute('position');
    assert.equal(g.type,'RingGeometry');
    assert.equal(g.parameters.innerRadius,.89);
    assert.equal(g.parameters.outerRadius,1);
    assert.equal(g.parameters.thetaSegments,48);
    assert.equal(g.parameters.phiSegments,4);
    assert.equal(p.count,245);
    assert.equal(g.index.count,1152);
    assert.equal(w.mesh.rotation.x,-Math.PI/2);
    assert.equal(w.mesh.castShadow,false);
    for(let i=0;i<p.count;i++){
      assert.ok(Math.abs(p.getZ(i))<1e-10);
      assert.ok(Math.abs(Math.hypot(p.getX(i),p.getY(i)))>=.89-1e-6);
      assert.ok(Math.hypot(p.getX(i),p.getY(i))<=1+1e-6);
    }
    assert.match(w.material.vertexShader,/p\.z\+=\.033\*crest\*pulse\*pow\(1\.-progress,1\.6\)/);
    assert.match(w.material.vertexShader,/p\.xy\*=\.55\+progress\*2\.65/);
    assert.match(w.material.vertexShader,/float crest=sin\(radial\*3\.14159265\)/);
    assert.match(w.material.fragmentShader,/float alpha=\.43\*vFade\*broken\*feather/);
    assert.equal(w.material.depthWrite,false);
  }
  assert.equal(a.water.length,10);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(source),before);
  a.dispose();a.dispose();
});

test('reconstructed GLSL crest moves in ordinary time, vanishes at both original edges, and foam fades without overshoot',()=>{
  for(const phase of [0,.25,.5,.75])for(const time of [0,.13,1.9,3.7]){
    assert.ok(Math.abs(crest(0,time,phase))<1e-10);
    assert.ok(Math.abs(crest(1,time,phase))<1e-10);
    assert.ok(crest(.5,time,phase)>0);
    for(const r of [0,.25,.5,.75,1])for(const angle of [-2.3,0,1.1,Math.PI]){
      const y=crest(r,time,phase),opacity=alpha(r,time,phase,angle);
      assert.ok(Number.isFinite(y)&&y>=0&&y<=.033001);
      assert.ok(Number.isFinite(opacity)&&opacity>=0&&opacity<=.430001);
    }
  }
  assert.ok(Math.abs(crest(.5,.13,.25)-crest(.5,1.9,.25))>.001);
  assert.ok(Math.abs(alpha(.5,.13,.25,0)-alpha(.5,1.9,.25,0))>.001);
  const a=build(),b=build();
  assert.deepEqual(a.water.filter(w=>w.kind==='landing-ripple').map(w=>w.material.vertexShader),
    b.water.filter(w=>w.kind==='landing-ripple').map(w=>w.material.vertexShader));
  assert.deepEqual(a.water.filter(w=>w.kind==='landing-ripple').map(w=>w.material.fragmentShader),
    b.water.filter(w=>w.kind==='landing-ripple').map(w=>w.material.fragmentShader));
  a.dispose();b.dispose();
});

test('landing ripples and all ordinary water continue through synthetic global calm, pause and disposal',()=>{
  const before=JSON.stringify(source),a=build(),rings=a.water.filter(w=>w.kind==='landing-ripple');
  const kinds=a.water.map(w=>w.kind);
  assert.deepEqual(kinds,['river','waterfall','landing-ripple','landing-ripple','landing-ripple','landing-ripple','pool','swamp','channel','pond']);
  const unchangedCounts=a.locations.map(l=>l.group.children.length);
  a.tick(2,{storm:0,weatherMode:'GLOBAL_CALM'});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2));
  a.tick(7.5,{storm:0,weatherMode:'GLOBAL_CALM'});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===7.5));
  a.tick(17,{paused:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===7.5));
  assert.deepEqual(a.locations.map(l=>l.group.children.length),unchangedCounts);
  assert.equal(JSON.stringify(source),before);
  const ringGeo=rings[0].mesh.geometry;
  let disposed=0,original=ringGeo.dispose.bind(ringGeo);
  ringGeo.dispose=()=>{disposed++;original();};
  a.dispose();a.dispose();
  assert.equal(disposed,1);
});
