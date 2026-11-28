/** Offline mesh inspection only; never a GPU, weather, canon or art acceptance gate. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {join} from 'node:path';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const [catalogPath,out]=process.argv.slice(2);
assert.ok(catalogPath&&out,'usage: node mud-dogs-nominal-contact.mjs CATALOG NEW_OUTPUT_DIR');
const bytes=readFileSync(catalogPath),catalog=JSON.parse(bytes);
const hash=b=>createHash('sha256').update(b).digest('hex');
assert.match(catalog.sourceRevision,/^[a-f0-9]{40}$/);
assert.equal(catalog.publicationAuthorized,false);
const place=catalog.locations.find(p=>p.id==='LOC-MUD-DOGS-SWAMP');
assert.equal(place?.canonStatus,'PERMANENT_CANON');
assert.equal(place.visible,true);
const bindings=[{id:place.id,anchor:[place.position[0],0,place.position[1]],canonStatus:place.canonStatus,landmarks:place.landmarks}];
const before=JSON.stringify(bindings),assets=buildRegionalAssets(THREE,bindings,()=>2);
try{
 const relief=assets.locations[0].group.getObjectByName('Candidate wetland raised-ground relief');
 const water=assets.water.find(w=>w.kind==='swamp');
 assert.equal(relief.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(relief.userData.navigable,false);
 assert.equal(water.mesh.rotation.x,-Math.PI/2);
 const y=water.mesh.position.y,[sx,sz]=water.mesh.scale.toArray();
 const sites=water.material.uniforms.uIslandSites.value;
 assert.equal(sites.length,4);
 for(const shader of [water.material.vertexShader,water.material.fragmentShader]){
  assert.match(shader,/smoothstep\(\.86,\.97,islandRadius\)/);
  assert.match(shader,/smoothstep\(1\.04,1\.22,islandRadius\)/);
 }
 const {position:p,aIsland:id}=relief.geometry.attributes,idx=relief.geometry.index;
 const segments=sites.map(()=>[]);
 const normalized=(v,k)=>[(.5+(v.x-water.mesh.position.x)/(2*sx)-sites[k].x)/sites[k].z,(.5-(v.z-water.mesh.position.z)/(2*sz)-sites[k].y)/sites[k].w];
 for(let i=0;i<idx.count;i+=3){
  const ii=[0,1,2].map(j=>idx.getX(i+j)),k=id.getX(ii[0]);
  assert.ok(ii.every(j=>id.getX(j)===k));
  const v=ii.map(j=>new THREE.Vector3().fromBufferAttribute(p,j)),hits=[];
  for(let j=0;j<3;j++){
   const a=v[j],b=v[(j+1)%3];
   assert.ok(Math.abs(a.y-y)>1e-8,'exact vertex-plane tie requires explicit treatment');
   if((a.y-y)*(b.y-y)<0)hits.push(normalized(a.clone().lerp(b,(y-a.y)/(b.y-a.y)),k));
  }
  assert.ok(hits.length===0||hits.length===2);
  if(hits.length)segments[k].push(hits);
 }
 const key=p=>p.map(n=>n.toFixed(8)).join(','),radius=p=>Math.hypot(...p);
 const round=n=>Number(n.toFixed(6)),smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
 const loops=[];
 const metrics=segments.map((ss,k)=>{
  const graph=new Map();
  for(const [a,b] of ss){for(const [u,v] of [[a,b],[b,a]]){const q=key(u);if(!graph.has(q))graph.set(q,new Set());graph.get(q).add(key(v));}}
  assert.ok(graph.size>0&&[...graph.values()].every(n=>n.size===2),'contour must be a closed, unbranched loop');
  const seen=new Set(),stack=[graph.keys().next().value];
  while(stack.length){const n=stack.pop();if(seen.has(n))continue;seen.add(n);stack.push(...graph.get(n));}
  assert.equal(seen.size,graph.size,'one connected loop per island');
  assert.equal(ss.length,graph.size);
  const first=[...graph.keys()].sort()[0],loop=[];let current=first,prior=null;
  do{loop.push(current);const next=[...graph.get(current)].sort().find(n=>n!==prior);prior=current;current=next;assert.ok(loop.length<=graph.size);}while(current!==first);
  assert.equal(loop.length,graph.size);loops.push(loop.map(q=>q.split(',').map(Number)));
  let lo=Infinity,hi=0;
  for(const [a,b] of ss){const d=b.map((x,i)=>x-a[i]),t=Math.max(0,Math.min(1,-(a[0]*d[0]+a[1]*d[1])/(d[0]**2+d[1]**2)));lo=Math.min(lo,radius(a.map((x,i)=>x+t*d[i])));hi=Math.max(hi,radius(a),radius(b));}
  assert.ok(lo>.86&&hi<1.22,'nominal contact leaves active band');
  const gain=x=>smooth(.86,.97,x)*(1-smooth(1.04,1.22,x));
  return {island:k+1,segments:ss.length,closedLoop:true,minRadius:round(lo),maxRadius:round(hi),minRadialEnvelope:round(Math.min(gain(lo),gain(hi)))};
 });
 assert.equal(JSON.stringify(bindings),before);assert.equal(assets.worldMutationAllowed,false);
 const receipt={sourceRevision:catalog.sourceRevision,catalogSha256:hash(bytes),regionalSourceSha256:hash(readFileSync(new URL('../regional-assets.mjs',import.meta.url))),locationId:place.id,nominalLocalWaterY:y,authority:'CANDIDATE_NOT_APPROVED',method:'CPU triangle-plane intersection; normalized shader-site coordinates; radial envelope only; no wave phase, shader execution, camera, pixels or GPU',metrics};
 const panels=loops.map((loop,k)=>{
  const x=250+500*(k%2),cy=186+286*Math.floor(k/2),m=metrics[k];
  const path='M'+loop.map(a=>a.map(n=>n.toFixed(4)).join(' ')).join('L')+'Z';
  return `<g transform="translate(${x} ${cy})"><g transform="scale(87 -87)"><circle r="1.22" fill="#426c5e" opacity=".30"/><circle r=".86" fill="#172e31"/><circle r=".97" fill="none" stroke="#83b6a3" stroke-width=".008" stroke-dasharray=".035 .025"/><circle r="1.04" fill="none" stroke="#83b6a3" stroke-width=".008" stroke-dasharray=".035 .025"/><circle r="1.22" fill="none" stroke="#426c5e" stroke-width=".012"/><path d="${path}" fill="none" stroke="#ffc77a" stroke-width=".018" stroke-linecap="round"/></g><text y="-119" class="head">ILLUSTRATIVE ISLAND ${k+1}</text><text y="124">r ${m.minRadius.toFixed(3)}–${m.maxRadius.toFixed(3)} | ${m.segments} contour segments</text><text y="144">minimum radial envelope ${m.minRadialEnvelope.toFixed(3)}</text></g>`;
 }).join('');
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 745" width="1000" height="745"><style>text{font:14px sans-serif;fill:#d4e4de;text-anchor:middle}.head{font-weight:bold;font-size:15px;letter-spacing:1px}</style><rect width="1000" height="745" fill="#172e31"/><text x="500" y="31" style="font-size:22px;font-weight:bold">MUD DOGS SWAMP · NOMINAL WATER CONTACT</text><text x="500" y="53">Exact candidate mesh / local shader-site coordinates / not a scene render</text>${panels}<text x="500" y="650" fill="#ffc77a">Amber: actual mesh-plane contour · dashed: full radial envelope · green: active envelope</text><text x="500" y="672">Nominal local water y = ${y} · no animated displacement or shader execution · each panel independently normalized</text><text x="500" y="697">CANDIDATE_NOT_APPROVED · ${catalog.sourceRevision.slice(0,12)} · CPU geometry diagnostic</text></svg>\n`;
 mkdirSync(out);writeFileSync(join(out,'inspection.svg'),svg);writeFileSync(join(out,'manifest.json'),JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt));
}finally{assets.dispose();}
