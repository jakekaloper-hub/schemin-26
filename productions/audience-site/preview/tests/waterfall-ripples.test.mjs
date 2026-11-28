import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const source=[{id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[10,0,20],canonStatus:'PERMANENT_CANON'}];
const create=()=>buildRegionalAssets(THREE,source,()=>1);

test('waterfall has four independently phased shader-driven landing ripples',()=>{
  const a=create();const rings=a.water.filter(w=>w.kind==='landing-ripple');
  assert.equal(rings.length,4);
  assert.equal(new Set(rings.map(r=>r.material.uniforms.uPhase.value)).size,4);
  assert.ok(rings.every(r=>r.mesh.material.isShaderMaterial&&r.mesh.geometry.type==='RingGeometry'));
  assert.ok(rings.every(r=>r.mesh.castShadow===false));
  a.dispose();
});
test('landing ripples advance in global calm but hold under pause',()=>{
  const a=create();const rings=a.water.filter(w=>w.kind==='landing-ripple');assert.equal(rings.length,4);
  a.tick(2,{storm:0});assert.ok(rings.every(w=>w.material.uniforms.uTime.value===2));
  a.tick(4,{storm:0});assert.ok(rings.every(w=>w.material.uniforms.uTime.value===4));
  a.tick(16,{paused:true});assert.ok(rings.every(w=>w.material.uniforms.uTime.value===4));
  a.dispose();
});
test('ripple candidates neither write the world nor generate unnamed new locations',()=>{
  const before=JSON.stringify(source),a=create();
  assert.deepEqual(a.locations.map(l=>l.id),['LOC-TDS-WATERFALL-TEMPLE']);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(source),before);
  a.dispose();a.dispose();
});

test('landing ripple culling bounds contain the full shader crest and preserve edge-of-view water',()=>{
  const a=create();
  try {
    a.root.updateMatrixWorld(true);
    const rings=a.water.filter(w=>w.kind==='landing-ripple');
    for(const {mesh,material} of rings){
      const g=mesh.geometry,p=g.getAttribute('position');
      assert.match(material.vertexShader,/p\.xy\*=\.55\+progress\*2\.65/);
      assert.match(material.vertexShader,/p\.z\+=\.033\*crest\*pulse\*pow\(1\.-progress,1\.6\)/);
      assert.equal(mesh.frustumCulled,true);
      if(!g.boundingSphere)g.computeBoundingSphere();
      const sphere=g.boundingSphere;
      for(const progress of [0,.25,.5,.65,.9,.999999])for(let i=0;i<p.count;i++){
        const v=new THREE.Vector3().fromBufferAttribute(p,i);
        const radial=Math.max(0,Math.min(1,(Math.hypot(v.x,v.y)-.89)/.11));
        v.multiplyScalar(.55+progress*2.65);
        v.z=.033*Math.sin(Math.PI*radial)*(1-progress)**1.6; // maximum pulse
        assert.ok(sphere.containsPoint(v),'shader-displaced vertex must be inside culling sphere');
      }
      const center=mesh.getWorldPosition(new THREE.Vector3());
      const camera=new THREE.OrthographicCamera(-.15,.15,.15,-.15,.1,20);
      const edge=mesh.localToWorld(new THREE.Vector3(2.2,0,0));
      camera.position.copy(edge).add(new THREE.Vector3(0,5,0));
      camera.up.set(0,0,-1);camera.lookAt(edge);camera.updateMatrixWorld(true);
      const frustum=new THREE.Frustum().setFromProjectionMatrix(new THREE.Matrix4().multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse));
      assert.ok(frustum.containsPoint(edge));
      assert.equal(frustum.containsPoint(center),false);
      const staticSphere=new THREE.Sphere(center,1);
      assert.equal(frustum.intersectsSphere(staticSphere),false,'original unit sphere incorrectly culled');
      assert.equal(frustum.intersectsObject(mesh),true,'visible expanding ring is submitted');
      camera.position.x+=10;camera.updateMatrixWorld(true);
      frustum.setFromProjectionMatrix(new THREE.Matrix4().multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse));
      assert.equal(frustum.intersectsObject(mesh),false,'distant ring still culled');
    }
  } finally {a.dispose();}
});
