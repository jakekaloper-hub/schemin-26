import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[{id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'}];
const near=(a,b)=>assert.ok(Math.abs(a-b)<.00001,`${a} != ${b}`);
const get=()=>{
  const assets=buildRegionalAssets(THREE,bindings,()=>2);
  const blade=assets.locations[0].group.getObjectByName('Candidate wetland emergent vegetation');
  return {assets,blade};
};

test('all 384 original bank blades retain both roots and tip while gaining a bounded folded midrib',()=>{
  const {assets,blade}=get();
  try {
    const p=blade.geometry.getAttribute('position'),s=blade.geometry.getAttribute('aSway');
    const idx=blade.geometry.getIndex(),v=new THREE.Vector3();
    assert.equal(p.count,384*6);assert.equal(idx.count,384*15);
    for(let i=0;i<96;i++)for(let j=0;j<4;j++){
      const a=Math.floor(i/6)/16*Math.PI*2+(i%6-2.5)*.033+Math.sin(i*7.17)*.009;
      const r=1.105+.067*(.5+.5*Math.sin(i*2.19));
      const x=Math.cos(a)*10.5*r,z=Math.sin(a)*8.2*r,y=.175+.042*(.5+.5*Math.sin(a*9.));
      const b=a+j*2.094+Math.sin(i*.82)*.25,dx=Math.cos(b),dz=Math.sin(b);
      const h=.38+((i*13+j*7)%19)*.043,w=.047+(i+j*3)%5*.012;
      const tx=x+Math.sin(b*2.+i)*.10,tz=z+Math.cos(b*2.+i)*.07;
      const k=(i*4+j)*6;
      for(const [off,expected] of [[0,[x-dx*w,y,z-dz*w]],[1,[x+dx*w,y,z+dz*w]],[5,[tx,y+h,tz]]]){
        v.fromBufferAttribute(p,k+off);expected.forEach((n,m)=>near(v.getComponent(m),n));
      }
      for(let off=0;off<6;off++){
        near(s.getX(k+off),i*2.399+j*2.04);near(s.getY(k+off),[0,0,.5,.5,.5,1][off]);
      }
      const left=new THREE.Vector3().fromBufferAttribute(p,k+2),right=new THREE.Vector3().fromBufferAttribute(p,k+3),ridge=new THREE.Vector3().fromBufferAttribute(p,k+4);
      const mid=left.clone().lerp(right,.5),relief=ridge.distanceTo(mid);
      assert.ok(relief>=.0179&&relief<=.0341);
      near(left.distanceTo(right),w);near(ridge.y,y+h*.5);
      const base=(i*4+j)*15;
      for(let n=0;n<15;n++)assert.ok(idx.getX(base+n)>=k&&idx.getX(base+n)<k+6);
      for(let n=0;n<15;n+=3){
        const [u,vv,ww]=[0,1,2].map(q=>new THREE.Vector3().fromBufferAttribute(p,idx.getX(base+n+q)));
        assert.ok(vv.sub(u).cross(ww.sub(u)).length()>.00001,'degenerate fold');
      }
    }
  } finally {assets.dispose();}
});

test('folds add muted face variation, retain one ordinary-motion draw and expanded culling bounds',()=>{
  const {assets,blade}=get();
  try {
    const p=blade.geometry.getAttribute('position'),c=blade.geometry.getAttribute('aTint');
    assert.equal(c.count,p.count);assert.equal(blade.geometry.getIndex().count,5760);
    for(let k=0;k<p.count;k+=6){
      const lum=i=>c.getX(i)+c.getY(i)+c.getZ(i);
      assert.ok(lum(k+2)<lum(k+3));assert.ok(lum(k+4)>lum(k+2));
      for(let j=0;j<6;j++)assert.ok(lum(k+j)/3<.33);
    }
    const raw=new THREE.Sphere().setFromPoints(Array.from({length:p.count},(_,i)=>new THREE.Vector3().fromBufferAttribute(p,i)));
    assert.ok(blade.geometry.boundingSphere.radius>=raw.radius+.23);
    assert.equal(blade.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(blade.userData.navigable,false);assert.deepEqual(blade.userData.routeIds,[]);
    assert.equal(blade.castShadow,false);assert.equal(blade.receiveShadow,false);
    assert.equal(blade.material.transparent,false);assert.equal(blade.material.depthWrite,true);
    assets.tick(2,{storm:0});assert.equal(blade.material.uniforms.uTime.value,2);
    assets.tick(5,{storm:0,paused:true});assert.equal(blade.material.uniforms.uTime.value,2);
    assert.equal(assets.water.find(w=>w.kind==='swamp').material.uniforms.uTime.value,2);
  } finally {assets.dispose();}
});
