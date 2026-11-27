import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const world=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=world.locations.find(x=>x.id===id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});

test('Mud Dogs bark UV wrap shares true area-weighted side normals, not cap or adjacent faces',()=>{
  const snapshot=JSON.stringify(bindings),a=buildRegionalAssets(THREE,bindings,()=>2);
  try {
    const group=a.locations.find(l=>l.id===ids[0]).group;
    for(const [part,count] of [['trunk',14],['buttress-root',56]]){
      const meshes=group.children.filter(o=>o.userData.wetlandPart===part);
      assert.equal(meshes.length,count);
      for(const o of meshes){
        assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
        const g=o.geometry,p=g.getAttribute('position'),n=g.getAttribute('normal'),uv=g.getAttribute('uv');
        const {radialSegments:r,heightSegments:h}=g.parameters,stride=r+1,sideCount=stride*(h+1);
        const raw=g.clone();raw.computeVertexNormals();
        const original=raw.getAttribute('normal'),idx=g.getIndex();
        for(let row=0;row<=h;row++){
          const first=row*stride,last=first+r;
          const normal=v=>new THREE.Vector3().fromBufferAttribute(n,v);
          const pos=v=>new THREE.Vector3().fromBufferAttribute(p,v);
          assert.ok(pos(first).distanceTo(pos(last))<1e-6,'UV seam positions coincide');
          assert.equal(uv.getX(first),0);assert.equal(uv.getX(last),1);
          const sum=new THREE.Vector3();
          for(let k=0;k<idx.count;k+=3){
            const tri=[idx.getX(k),idx.getX(k+1),idx.getX(k+2)];
            if(tri.some(v=>v>=sideCount)||!tri.some(v=>v===first||v===last))continue;
            const [x,y,z]=tri.map(pos);sum.add(y.sub(x).cross(z.sub(x)));
          }
          sum.normalize();
          assert.ok(normal(first).distanceTo(normal(last))<1e-6,part+' UV lighting seam');
          assert.ok(normal(first).distanceTo(sum)<1e-6,part+' area-weighted side normal');
          assert.ok(Math.abs(normal(first).length()-1)<1e-6);
        }
        for(let v=0;v<p.count;v++){
          if(v<sideCount&&(v%stride===0||v%stride===r))continue;
          assert.deepEqual([n.getX(v),n.getY(v),n.getZ(v)],[original.getX(v),original.getY(v),original.getZ(v)],'non-seam and cap normals unchanged');
        }
        raw.dispose();
      }
    }
    assert.equal(a.worldMutationAllowed,false);assert.equal(JSON.stringify(bindings),snapshot);
  } finally {a.dispose();}
});
