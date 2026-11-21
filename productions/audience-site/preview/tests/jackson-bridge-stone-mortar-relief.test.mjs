import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(l=>l.id===id);
  assert.ok(p,'canonical Atlas location missing: '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const sourceBefore=JSON.stringify(atlas),bindingsBefore=JSON.stringify(bindings);
const make=()=>buildRegionalAssets(THREE,bindings,()=>2);
const arches=a=>a.locations.find(p=>p.id===ids[2]).group
  .getObjectByName('Candidate Week 9 pond-side stone arch').children
  .filter(m=>m.userData.bridgePart==='stone-arch');

function originalArch(){
  const s=new THREE.Shape();
  s.moveTo(-2.65,0);s.lineTo(-1.73,0);
  s.bezierCurveTo(-1.58,1.30,1.58,1.30,1.73,0);
  s.lineTo(2.65,0);s.lineTo(2.65,1.48);
  s.lineTo(-2.65,1.48);s.closePath();
  const g=new THREE.ExtrudeGeometry(s,{depth:.17,steps:1,bevelEnabled:false,curveSegments:16});
  g.rotateY(Math.PI/2);g.computeBoundingBox();return g;
}
const close=(a,b,tol=1e-5)=>Math.abs(a-b)<=tol;

test('only the two existing sourced Jackson masonry arches receive carved facade detail',()=>{
  const a=make(),existing=arches(a),country=a.locations.find(p=>p.id===ids[2]);
  const world=atlas.locations.find(p=>p.id===ids[2]);
  assert.deepEqual(a.locations.map(p=>p.id),ids);
  assert.ok(world.persistent_landmarks.includes('water hazards'));
  assert.ok(world.current_state.some(s=>s.includes('chili contamination')));
  assert.ok(world.current_state.some(s=>s.includes('cleanup state')));
  assert.equal(country.group.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.deepEqual(existing.map(o=>o.position.x),[-.88,.71]);
  assert.equal(existing.length,2);
  assert.equal(existing[0].material,existing[1].material,'original shared stone');
  for(const arch of existing){
    assert.equal(arch.geometry.type,'ExtrudeGeometry');
    assert.equal(arch.geometry.parameters.options.depth,.17);
    assert.equal(arch.userData.stoneDetail,'inward-jointed-original-facade');
    assert.equal(arch.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
    assert.equal(arch.userData.navigable,false);
    assert.deepEqual(arch.userData.routeIds,[]);
    assert.deepEqual(arch.userData.principalCharacters,[]);
  }
  assert.ok(a.locations.slice(0,2).every(p=>
    !p.group.getObjectByName('Candidate Week 9 pond-side stone arch')));
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
  a.dispose();
});

test('inward-only physical stone joints are deterministic and retain the exact original arch contour',()=>{
  const a=make(),b=make(),faces=arches(a),replicas=arches(b),old=originalArch();
  const base=old.getAttribute('position'),beforeBox=old.boundingBox;
  assert.equal(base.count,240);
  for(let k=0;k<2;k++){
    const g=faces[k].geometry,p=g.getAttribute('position'),n=g.getAttribute('normal');
    assert.equal(p.count,2976,'38 existing face triangles subdivided 5x5; side faces unchanged');
    assert.equal(p.count,g.getAttribute('uv').count);
    assert.deepEqual(p.array,replicas[k].geometry.getAttribute('position').array);
    assert.deepEqual(faces[k].position.toArray(),[-.88,.71].slice(k,k+1).concat([0,0]));
    assert.ok(close(g.boundingBox.min.x,beforeBox.min.x)&&close(g.boundingBox.max.x,beforeBox.max.x));
    assert.ok(close(g.boundingBox.min.y,beforeBox.min.y)&&close(g.boundingBox.max.y,beforeBox.max.y));
    assert.ok(close(g.boundingBox.min.z,beforeBox.min.z)&&close(g.boundingBox.max.z,beforeBox.max.z));
    let recessed=0,deep=0;
    for(let i=0;i<p.count;i++){
      const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
      assert.ok([x,y,z,n.getX(i),n.getY(i),n.getZ(i)].every(Number.isFinite));
      assert.ok(x>=-.000001&&x<=.170001,'inward-only within original extrusion');
      assert.ok(y>=-.000001&&y<=1.480001);
      assert.ok(Math.abs(z)<=2.650001);
      if(x>.0005&&x<.0141||x>.1559&&x<.1695){
        recessed++;
        if(x>.003&&x<.0141||x>.1559&&x<.167)deep++;
      }
    }
    assert.ok(recessed>20&&deep>5,'real recess geometry rather than material-only paint');
    // Every previously defined triangular facade boundary vertex remains
    // represented on BOTH physical cap planes with no outward deformation.
    for(let i=0;i<base.count;i++){
      const x=base.getX(i),y=base.getY(i),z=base.getZ(i);
      let found=false;
      for(let j=0;j<p.count;j++)if(close(p.getX(j),x)&&close(p.getY(j),y)&&close(p.getZ(j),z)){found=true;break;}
      assert.ok(found,'original 3D outline vertex must remain '+i);
    }
  }
  old.dispose();a.dispose();b.dispose();
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});

test('original pond and other ordinary waters still move in El Niño calm; pause and dispose are bounded',()=>{
  const a=make(),faces=arches(a),first=faces[0],p=a.water.find(w=>w.kind==='pond');
  const originalFaces=faces.map(o=>o.geometry.getAttribute('position').array.slice());
  assert.equal(a.water.filter(w=>['river','waterfall','pool','swamp','channel','pond'].includes(w.kind)).length,6);
  assert.deepEqual(p.mesh.position.toArray(),[7,.06,6]);
  assert.deepEqual(p.mesh.scale.toArray(),[3.8,2.3,1]);
  a.tick(2,{globalCalm:true,storm:0});
  a.tick(6,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===6));
  a.tick(11,{globalCalm:true,storm:5,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===6));
  faces.forEach((o,i)=>assert.deepEqual(o.geometry.getAttribute('position').array,originalFaces[i]));
  let geoDisposals=0,materialDisposals=0;
  first.geometry.addEventListener('dispose',()=>geoDisposals++);
  first.material.addEventListener('dispose',()=>materialDisposals++);
  a.dispose();a.dispose();a.tick(20);
  assert.equal(geoDisposals,1);assert.equal(materialDisposals,1);
  assert.equal(JSON.stringify(atlas),sourceBefore);
  assert.equal(JSON.stringify(bindings),bindingsBefore);
});
