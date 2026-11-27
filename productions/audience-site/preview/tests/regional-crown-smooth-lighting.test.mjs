import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{const p=atlas.locations.find(x=>x.id===id);return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],canonStatus:p.canon_status,landmarks:p.persistent_landmarks};});
for(const [index,key,count] of [[0,'templeCanopyPart',21],[2,'estateTreePart',49]]){
  test(`${ids[index]} crowns retain smooth incident-area normals across coincident corners`,()=>{
    const a=buildRegionalAssets(THREE,bindings,()=>2);
    try{
      const crowns=a.locations.find(l=>l.id===ids[index]).group.children.filter(o=>o.userData[key]==='crown');
      assert.equal(crowns.length,count);
      let groups=0,vertices=0,maxError=0,maxAngle=0;
      for(const o of crowns){
        const g=o.geometry,p=g.attributes.position,n=g.attributes.normal,corners=new Map();
        assert.equal(g.index,null);assert.equal(p.count,540);
        const pos=i=>new THREE.Vector3().fromBufferAttribute(p,i);
        const normal=i=>new THREE.Vector3().fromBufferAttribute(n,i);
        for(let i=0;i<p.count;i++){
          const key=pos(i).toArray().join(',');
          if(!corners.has(key))corners.set(key,[]);
          corners.get(key).push(i);
        }
        for(const members of corners.values()){
          assert.ok(members.length>=3);
          const expected=new THREE.Vector3();
          for(const i of members){const k=i-i%3,[x,y,z]=[pos(k),pos(k+1),pos(k+2)];expected.add(y.sub(x).cross(z.sub(x)));}
          expected.normalize();groups++;vertices+=members.length;
          for(const i of members){
            const v=normal(i);assert.ok(v.dot(pos(i))>0);assert.ok(Math.abs(v.length()-1)<1e-6);
            maxError=Math.max(maxError,v.distanceTo(expected));
            for(const j of members)maxAngle=Math.max(maxAngle,v.angleTo(normal(j))*180/Math.PI);
          }
        }
      }
      console.log('REGIONAL_CROWN_LIGHTING',JSON.stringify({id:ids[index],groups,vertices,maxError,maxAngle}));
      assert.equal(groups,count*92);assert.equal(vertices,count*540);
      assert.ok(maxError<1e-6);assert.ok(maxAngle<1e-5);
    }finally{a.dispose();}
  });
}
