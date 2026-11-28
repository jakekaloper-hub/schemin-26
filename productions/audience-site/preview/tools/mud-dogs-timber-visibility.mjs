/** Static CPU visibility sampling of inherited candidate timber; not rendered pixels. */
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {join} from 'node:path';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const [catalogPath,out]=process.argv.slice(2);
assert.ok(catalogPath&&out,'usage: node mud-dogs-timber-visibility.mjs CATALOG NEW_OUTPUT_DIR');
const bytes=readFileSync(catalogPath),catalog=JSON.parse(bytes),hash=b=>createHash('sha256').update(b).digest('hex');
assert.equal(catalog.publicationAuthorized,false);assert.match(catalog.sourceRevision,/^[a-f0-9]{40}$/);
const place=catalog.locations.find(p=>p.id==='LOC-MUD-DOGS-SWAMP');
assert.ok(place?.visible&&place.canonStatus==='PERMANENT_CANON');
const bindings=[{id:place.id,anchor:[place.position[0],0,place.position[1]],canonStatus:place.canonStatus,landmarks:place.landmarks}];
const before=JSON.stringify(bindings),assets=buildRegionalAssets(THREE,bindings,()=>2);
const round=n=>Number(n.toFixed(5));
let baseline;
try{
 const g=assets.locations[0].group,log=g.getObjectByName('Candidate Mud Dogs recessed fallen timber');
 assert.equal(log.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');assert.equal(log.userData.navigable,false);
 const a=new THREE.Vector3(-5,.5,1),b=new THREE.Vector3(0,.8,4);
 baseline=new THREE.Mesh(new THREE.CylinderGeometry(.32*.62,.32,a.distanceTo(b),7),log.material);
 baseline.position.copy(log.position);baseline.quaternion.copy(log.quaternion);g.add(baseline);assets.root.updateMatrixWorld(true);
 const ground=['Candidate wetland raised-ground relief','Candidate wetland shoreline transition'].map(n=>g.getObjectByName(n));
 assert.ok(ground.every(Boolean));const water=assets.water.filter(w=>['swamp','channel'].includes(w.kind)).map(w=>w.mesh);assert.equal(water.length,2);
 const side=new THREE.Vector3(-(b.z-a.z),0,b.x-a.x).normalize(),ray=new THREE.Raycaster();
 function top(objects,p,up=false){ray.set(g.localToWorld(new THREE.Vector3(p.x,up?-15:15,p.z)),new THREE.Vector3(0,up?1:-1,0));const h=ray.intersectObjects(objects,false)[0];return h?g.worldToLocal(h.point.clone()).y:null;}
 const counts={old:{hit:0,above:0,terrain:0,water:0},new:{hit:0,above:0,terrain:0,water:0}};
 const profile=[];let lost=0,gained=0,maxRecess=0,clearStations=0,minGap=Infinity,maxGap=-Infinity,oldClearStations=0,oldMinGap=Infinity,oldMaxGap=-Infinity;
 function classify(h,terrain,wet,c){if(h===null)return false;c.hit++;if(terrain!==null&&terrain>=h){c.terrain++;return false;}if(wet!==null&&wet>=h){c.water++;return false;}c.above++;return true;}
 for(let i=0;i<41;i++)for(let j=-4;j<=4;j++){
  const t=.01+.98*i/40,p=a.clone().lerp(b,t).addScaledVector(side,j*.08);
  const old=top([baseline],p),next=top([log],p),terrain=top(ground,p),wet=top(water,p);
  if(next!==null){assert.ok(old!==null&&next<=old+1e-5,'refined surface outside original top envelope');maxRecess=Math.max(maxRecess,old-next);}
  const o=classify(old,terrain,wet,counts.old),n=classify(next,terrain,wet,counts.new);
  if(o&&!n)lost++;if(n&&!o)gained++;
  if(j===0){const bottom=top([log],p,true),oldBottom=top([baseline],p,true);assert.ok(old!==null&&next!==null&&bottom!==null&&oldBottom!==null&&bottom<=next);const support=Math.max(terrain??-Infinity,wet??-Infinity);if(Number.isFinite(support)){const gap=bottom-support;if(gap>0)clearStations++;minGap=Math.min(minGap,gap);maxGap=Math.max(maxGap,gap);const oldGap=oldBottom-support;if(oldGap>0)oldClearStations++;oldMinGap=Math.min(oldMinGap,oldGap);oldMaxGap=Math.max(oldMaxGap,oldGap);}profile.push([t,old,next,terrain,wet,bottom].map(v=>v===null?null:round(v)));}
 }
 assert.equal(gained,0);assert.ok(maxRecess>0&&maxRecess<.1);assert.equal(JSON.stringify(bindings),before);assert.equal(assets.worldMutationAllowed,false);
 for(const c of Object.values(counts))assert.equal(c.hit,c.above+c.terrain+c.water);
 const manifest={sourceRevision:catalog.sourceRevision,catalogSha256:hash(bytes),regionalSourceSha256:hash(readFileSync(new URL('../regional-assets.mjs',import.meta.url))),locationId:place.id,authority:'CANDIDATE_NOT_APPROVED',method:'369 sample positions with vertical CPU rays, 41 axial stations x 9 offsets at .08 local spacing, old primitive and current exact builder; compares top heights and centerline underside against existing raised ground, shoreline and nominal undisplaced water; excludes vegetation, lighting, actual camera, opacity, shaders and GPU',counts,lost,gained,maxRecess:round(maxRecess),centerline:{stations:profile.length,clearStations,minGap:round(minGap),maxGap:round(maxGap),oldClearStations,oldMinGap:round(oldMinGap),oldMaxGap:round(oldMaxGap)}};
 const x=t=>70+t*660,y=h=>300-h*180;
 const trace=(column,color,width)=>{let active=false,d='',dots='';for(const p of profile){if(p[column]===null){active=false;continue;}d+=(active?'L':'M')+Math.round(x(p[0]))+' '+Math.round(y(p[column]));active=true;if(column===3)dots+=`<circle cx="${Math.round(x(p[0]))}" cy="${Math.round(y(p[column]))}" r="2" fill="${color}"/>`;}return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}"/>${dots}`;};
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 470"><rect width="800" height="470" fill="#162925"/><g font-family="sans-serif" fill="#e3e9dc"><text x="30" y="34" font-size="20" font-weight="bold">Mud Dogs Swamp · inherited timber exposure</text><text x="30" y="56" font-size="12">CPU geometry / nominal water / local abstract dimensions</text><g stroke="#456059" stroke-width="1"><path d="M70 75V318H730 M70 300H730 M70 210H730 M70 120H730" fill="none"/></g><g font-size="11"><text x="40" y="304">0</text><text x="40" y="214">.5</text><text x="40" y="124">1</text><text x="70" y="334">start</text><text x="704" y="334">end</text></g>${trace(3,'#99bb77',3)}${trace(4,'#57c1cc',2)}${trace(1,'#eee3b4',3)}${trace(2,'#ff9861',2)}${trace(5,'#ff9861',1)}<g font-size="12"><text x="70" y="352" fill="#99bb77">Raised ground / shoreline</text><text x="245" y="352" fill="#57c1cc">Nominal water</text><text x="360" y="352" fill="#eee3b4">Original timber</text><text x="485" y="352" fill="#ff9861">Refined top / underside</text><text x="30" y="375">Exposed sample rays: ${counts.old.above} to ${counts.new.above}; max top recession ${manifest.maxRecess}</text><text x="30" y="397">Underside above nominal ground/water: ${clearStations}/${profile.length} stations; gap ${manifest.centerline.minGap} to ${manifest.centerline.maxGap}</text><text x="30" y="420">Original underside also clear: ${oldClearStations}/${profile.length}; gap ${manifest.centerline.oldMinGap} to ${manifest.centerline.oldMaxGap}</text><text x="30" y="445">Centerline profile only · not GPU pixels or art approval · ${catalog.sourceRevision.slice(0,12)}</text></g></g></svg>\n`;
 mkdirSync(out);writeFileSync(join(out,'inspection.svg'),svg);writeFileSync(join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');console.log(JSON.stringify(manifest));
}finally{if(baseline){baseline.removeFromParent();baseline.geometry.dispose();}assets.dispose();}
