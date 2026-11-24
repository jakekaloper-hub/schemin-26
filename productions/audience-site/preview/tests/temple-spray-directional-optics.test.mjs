import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const p=atlas.locations.find(place=>place.id===id);
  assert.ok(p,'missing source Atlas location '+id);
  return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
    canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const beforeAtlas=JSON.stringify(atlas),beforeBindings=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const mist=a=>a.locations.find(l=>l.id===ids[0]).group.getObjectByName('Candidate waterfall plunge mist');
const clamp=x=>Math.max(0,Math.min(1,x));
const smooth=(a,b,x)=>{const t=clamp((x-a)/(b-a));return t*t*(3-2*t);};
// Screen axes use square pixels and the upper-left point-coordinate origin.
function projectedAxis(age,drift,viewYaw=0,view=[0,0,-12],time=0,phase=0){
  const rate=.105+.048*drift[1],osc=time*.31+phase*35;
  const tangent=[
    drift[0]*(.12+.68*age)+.08*Math.sin(osc)+.08*age*.31*Math.cos(osc)/rate,
    (.95+.35*drift[1])-2*age*(.90+.20*drift[1]),
    drift[2]*(.10+.64*age)
  ];
  const vx=tangent[0]*Math.cos(viewYaw)-tangent[2]*Math.sin(viewYaw);
  const vz=tangent[0]*Math.sin(viewYaw)+tangent[2]*Math.cos(viewYaw);
  const sx=vx+view[0]*vz/Math.max(.001,-view[2]);
  const sy=-(tangent[1]+view[1]*vz/Math.max(.001,-view[2]));
  const length=Math.hypot(sx,sy);
  return length>.0001?[sx/length,sy/length]:[0,1];
}
function optical(point,axis,age,driftY,depth=12){
  const coord=[point[0]-.5,point[1]-.5];
  const normal=[-axis[1],axis[0]];
  const radial=Math.hypot((coord[0]*axis[0]+coord[1]*axis[1])*.98,
    (coord[0]*normal[0]+coord[1]*normal[1])*1.45);
  const core=1-smooth(.02,.30,radial);
  const feather=1-smooth(.08,.49,radial);
  const opacity=Math.pow(Math.max(Math.sin(age*Math.PI),0),.75)*(.50+.38*driftY);
  return feather*opacity*(.16+.07*core)*(1-.25*smooth(7,85,depth));
}

test('source-bound Temple mist remains one original 144-point draw with unchanged materials and climate authority',()=>{
  const a=build(),o=mist(a),g=o.geometry;
  assert.equal(atlas.locations.find(l=>l.id===ids[0]).canon_status,'PERMANENT_CANON');
  assert.ok(atlas.locations.find(l=>l.id===ids[0]).persistent_landmarks.includes('waterfall'));
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(a.root.getObjectsByProperty('name',o.name).length,1);
  assert.ok(o.isPoints);
  assert.equal(g.getAttribute('position').count,144);
  assert.equal(g.getAttribute('aPhase').count,144);
  assert.equal(g.getAttribute('aDrift').count,144);
  assert.deepEqual(Object.keys(o.material.uniforms),['uTime','uLightLevel','uPixelRatio']);
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(o.userData.navigable,false);
  assert.deepEqual(o.userData.routeIds,[]);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(a.worldMutationAllowed,false);
  for(const l of a.locations.filter(l=>l.id!==ids[0]))assert.equal(l.group.getObjectByName(o.name),undefined);
  assert.equal(JSON.stringify(bindings),beforeBindings);
  assert.equal(JSON.stringify(atlas),beforeAtlas);
  a.dispose();
});

test('imported shaders orient the existing soft droplet along projected ballistic velocity with finite, fully feathered bounds',()=>{
  const a=build(),o=mist(a),v=o.material.vertexShader,f=o.material.fragmentShader;
  for(const fragment of ['varying vec2 vSprayAxis',
    'vec3 tangent=vec3(aDrift.x*(.12+.68*age)',
    'vec3 viewTangent=(modelViewMatrix*vec4(tangent,0.)).xyz',
    '+.08*sin(oscillation)+.08*age*.31*cos(oscillation)/ageRate',
    'vec2 screenTangent=viewTangent.xy+view.xy*viewTangent.z/max(.001,-view.z)',
    'screenTangent.y=-screenTangent.y',
    'vSprayAxis=length(screenTangent)>.0001?normalize(screenTangent):vec2(0.,1.)',
    'dot(drop,vSprayAxis)*.98','dot(drop,transverse)*1.45',
    'float core=1.-smoothstep(.02,.30,radial)',
    'float feather=1.-smoothstep(.08,.49,radial)']){
    assert.ok((v+f).includes(fragment),'missing physically oriented optical contract: '+fragment);
  }
  assert.doesNotMatch(v+f,/\buStorm\b|\buWeather\b|\buRain\b|\buGlobalCalm\b/);
  const drift=o.geometry.getAttribute('aDrift');
  let ageShift=false,viewShift=false,nonzero=0;
  for(let i=0;i<drift.count;i++){
    const d=[drift.getX(i),drift.getY(i),drift.getZ(i)];
    const early=projectedAxis(.2,d),late=projectedAxis(.85,d),yaw=projectedAxis(.2,d,.75);
    assert.ok([...early,...late,...yaw].every(Number.isFinite));
    assert.ok(Math.abs(Math.hypot(...early)-1)<.000001);
    if(Math.hypot(early[0]-late[0],early[1]-late[1])>.06)ageShift=true;
    if(Math.hypot(early[0]-yaw[0],early[1]-yaw[1])>.06)viewShift=true;
    for(const age of [.2,.48,.85])for(const point of [[.5,.5],[.5,.25],[.75,.5],[.33,.67],[0,.5],[1,.5],[.5,0],[.5,1],[0,0],[1,1]]){
      const alpha=optical(point,projectedAxis(age,d),age,d[1]);
      assert.ok(Number.isFinite(alpha)&&alpha>=0&&alpha<=.230001,'finite bounded optical sprite');
      if(point[0]===0||point[0]===1||point[1]===0||point[1]===1)
        assert.ok(alpha<1e-10,'no squared point boundary bleed');
      if(alpha>.01)nonzero++;
    }
  }
  assert.ok(ageShift,'projected droplet tilts with ballistic phase');
  assert.ok(viewShift,'same source droplet responds to spectator viewpoint');
  assert.ok(nonzero>300,'nontrivial visible feathered sprite interior');
  a.dispose();
});

test('one-draw sprite survives batching; global weather calm does not freeze spray/water and explicit pause/disposal still work',()=>{
  const a=build(),o=mist(a),temple=a.locations.find(l=>l.id===ids[0]).group;
  const startCount=temple.children.length;
  const batches=batchStaticGeometry(THREE,temple);
  assert.ok(temple.children.length<startCount);
  assert.ok(temple.children.includes(o));
  for(const geo of batches.geometries)geo.dispose();
  let gDisposed=0,mDisposed=0;
  o.geometry.addEventListener('dispose',()=>gDisposed++);
  o.material.addEventListener('dispose',()=>mDisposed++);
  const ordinary=a.water.filter(w=>['waterfall','river','pool','swamp','channel','pond'].includes(w.kind));
  assert.equal(ordinary.length,6);
  a.tick(3,{globalCalm:true,storm:0});
  a.tick(9,{globalCalm:true,storm:0});
  assert.equal(o.material.uniforms.uTime.value,9);
  assert.ok(ordinary.every(w=>w.material.uniforms.uTime.value===9));
  a.tick(13,{globalCalm:true,storm:0,paused:true});
  assert.equal(o.material.uniforms.uTime.value,9);
  a.tick(17,{globalCalm:true,storm:0});
  assert.equal(o.material.uniforms.uTime.value,17);
  assert.ok(ordinary.every(w=>w.material.uniforms.uTime.value===17));
  a.dispose();a.dispose();a.tick(30);
  assert.equal(gDisposed,1);assert.equal(mDisposed,1);
  assert.equal(JSON.stringify(atlas),beforeAtlas);
  assert.equal(JSON.stringify(bindings),beforeBindings);
});

test('spray optical axis matches finite-differenced perspective motion including drift and screen Y',()=>{
  const a=build(),o=mist(a),drift=o.geometry.getAttribute('aDrift'),
    phases=o.geometry.getAttribute('aPhase');
  let count=0,legacyMisaligned=0;
  const yaw=.61,cos=Math.cos(yaw),sin=Math.sin(yaw),eps=1e-4;
  const rotate=([x,y,z])=>[x*cos-z*sin,y,x*sin+z*cos];
  const project=([x,y,z])=>[x/-z,-y/-z];
  for(let i=0;i<drift.count;i++){
    const d=[drift.getX(i),drift.getY(i),drift.getZ(i)],phase=phases.getX(i),rate=.105+.048*d[1];
    for(const age of [.15,.37,.65,.88]){
      // Evaluate on either side of a known non-wrap age.
      const time=(age-phase+1)/rate;
      const at=t=>{
        const ag=age+(t-time)*rate;
        return rotate([d[0]*ag*(.12+.34*ag)+Math.sin(t*.31+phase*35)*.08*ag,
          ag*(.95+.35*d[1])-ag*ag*(.90+.20*d[1]),d[2]*ag*(.10+.32*ag)]);
      };
      const pos=at(time);
      for(const offset of [[0,0,-12],[2,3,-8],[-3,1,-10]]){
        const view=pos.map((v,j)=>v+offset[j]);
        const before=project(at(time-eps).map((v,j)=>v+offset[j]));
        const after=project(at(time+eps).map((v,j)=>v+offset[j]));
        const delta=after.map((v,j)=>v-before[j]),length=Math.hypot(...delta);
        if(length<1e-8)continue;
        const expected=delta.map(v=>v/length),axis=projectedAxis(age,d,yaw,view,time,phase);
        assert.ok(Math.hypot(axis[0]-expected[0],axis[1]-expected[1])<1e-5,'projected finite-difference alignment');
        const legacy=rotate([d[0]*(.12+.68*age),(.95+.35*d[1])-2*age*(.90+.20*d[1]),d[2]*(.10+.64*age)]);
        const l=Math.hypot(legacy[0],legacy[1]);
        if(l>1e-6&&Math.abs((legacy[0]*expected[0]+legacy[1]*expected[1])/l)<.9)legacyMisaligned++;
        count++;
      }
    }
  }
  assert.ok(count>1600);
  assert.ok(legacyMisaligned>100,'old optical axis visibly diverges in sampled direction space');
  a.dispose();
});

test('Temple sprite footprint stays in CSS pixels at the existing capped renderer density',async()=>{
  const {rendererQuality}=await import('../three-world.mjs');
  const a=build(),o=mist(a),v=o.material.vertexShader;
  assert.equal(o.material.uniforms.uPixelRatio.value,1);
  assert.match(v,/uniform float uPixelRatio/);
  assert.ok(v.includes('gl_PointSize=clamp(650./max(12.,-view.z),2.4,25.)*(1.-age*.22)*uPixelRatio'));
  for(const width of [390,1440])for(const dpr of [1,1.25,1.5,2,3]){
    const ratio=rendererQuality(width,dpr).pixelRatio;
    for(const depth of [8,12,30,90,400])for(const age of [.1,.5,.9]){
      const css=Math.max(2.4,Math.min(25,650/Math.max(12,depth)))*(1-age*.22);
      assert.ok(Math.abs(css*ratio/ratio-css)<1e-12);
      assert.ok(css*ratio<=37.5);
    }
  }
  const renderer=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
  assert.match(renderer,/q.pixelRatio!==lastPixelRatio/);
  assert.match(renderer,/templeMist.material.uniforms.uPixelRatio.value=renderer.getPixelRatio\(\)/);
  assert.match(renderer,/canvas.clientHeight,rendererQuality\(Math.max\(1,canvas.clientWidth\),globalThis.devicePixelRatio\|\|1\).pixelRatio/);
  a.dispose();
});
