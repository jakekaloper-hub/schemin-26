import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const start=source.indexOf('}else if(uWetland>.5){');
const end=source.indexOf('}else if(uRiver>.5){',start);
const region=source.slice(start,end);
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};

// Read the UV operands from the actual fragment expressions, then evaluate those
// equations on CPU. This is a shader-contract regression, not a GLSL/GPU test.
const phaseMatch=region.match(/float eddyCoordinate=length\(\((vUv|wetlandUv)-vec2\(\.52,\.44\)\)\*vec2\(1\.,1\.4\)\)\*30\.-uTime\*\.15;/);
const fadeMatch=region.match(/float eddyFade=1\.-smoothstep\(\.12,\.42,length\((vUv|wetlandUv)-vec2\(\.52,\.44\)\)\);/);
function evaluate(u,v,time,flow){
 assert.ok(phaseMatch&&fadeMatch,'recognized exact source equations');
 const uv=kind=>kind==='vUv'?[u,v]:[u-flow[0]*time,v-flow[1]*time];
 const [px,py]=uv(phaseMatch[1]),[fx,fy]=uv(fadeMatch[1]);
 const phase=Math.hypot(px-.52,(py-.44)*1.4)*30-time*.15;
 const envelope=1-smooth(.12,.42,Math.hypot(fx-.52,fy-.44));
 return {phase,envelope,crest:Math.max(0,Math.sin(phase))**12*envelope};
}

test('local eddy origin and envelope stay present after long uninterrupted spectator sessions',()=>{
 for(const flow of [[.012,-.009],[-.034,.013]]){
  for(const t of [0,30,120,600,3600]){
   assert.equal(evaluate(.52,.44,t,flow).envelope,1);
   assert.equal(evaluate(.99,.44,t,flow).envelope,0);
   let brightest=0;
   for(let i=0;i<=40;i++)for(let j=0;j<=40;j++){
    const u=.2+i*.016,v=.12+j*.016;
    if(Math.hypot(u-.5,v-.5)<=.5)brightest=Math.max(brightest,evaluate(u,v,t,flow).crest);
   }
   assert.ok(brightest>.5,'local animated optical signal remains visible in disk at '+t);
  }
 }
});

test('radial phase advances under the same time while resolved startup shape is unchanged',()=>{
 const flow=[.012,-.009];
 for(const u of [.44,.52,.60,.72]){
  const a=evaluate(u,.44,0,flow),b=evaluate(u,.44,2,flow);
  assert.equal(a.phase,Math.hypot(u-.52,0)*30);
  assert.ok(Math.abs(b.phase-a.phase+.30)<1e-12);
  assert.equal(a.envelope,b.envelope);
 }
 assert.ok(Math.abs(evaluate(.58,.44,0,flow).crest-evaluate(.58,.44,2,flow).crest)>.05);
});

test('independent advected flow and optical footprint remain; no weather input',()=>{
 assert.ok(start>=0&&end>start);
 for(const term of ['wetlandUv = vUv - uFlow * uTime','currentCoordinate=(wetlandUv.x+meander)','fwidth(eddyCoordinate)','eddy*eddyFade*.5*uSheenGain','sediment=.5+.5*sin((wetlandUv.x-wetlandUv.y)'])assert.ok(region.includes(term),term);
 assert.ok(!/uStorm|uWeather|uGlobalCalm/.test(region));
 assert.ok(!source.slice(0,start).includes('float eddyCoordinate=length((vUv-vec2(.52,.44))'));
});
