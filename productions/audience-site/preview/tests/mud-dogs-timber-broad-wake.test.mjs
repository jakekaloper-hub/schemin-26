import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const vertex=source.slice(source.indexOf('vertexShader:`'),source.indexOf('fragmentShader:`'));
const wet=vertex.slice(vertex.indexOf('if(uWetland>.5)'),vertex.indexOf('if(uRiver>.5)'));
const fragment=source.slice(source.indexOf('fragmentShader:`'),source.indexOf('function wetlandWaterDisk'));
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function spec(){
 const phase=wet.match(/timberBroadPhase=timberDistance\*([\d.]+)-uTime\*([\d.]+)\+timberAlong\*([\d.]+)/);
 const env=wet.match(/timberEnvelope=smoothstep\(([\d.]+),([\d.]+),timberDistance\)\s*\*\(1\.-smoothstep\(([\d.]+),([\d.]+),timberDistance\)\)/);
 const amp=wet.match(/p\.z\+=([\d.]+)\*timberEnvelope\*timberBroadCrest\*shoreHold/);
 const endpoints=source.match(/const a=new THREE\.Vector3\(([-\d.]+),[-\d.]+,([-\d.]+)\),b=new THREE\.Vector3\(([-\d.]+),[-\d.]+,([-\d.]+)\)/);
 assert.ok(phase&&env&&amp&&endpoints,'source wake inputs must exist');
 return {phase:phase.slice(1).map(Number),env:env.slice(1).map(Number),amp:Number(amp[1]),endpoints:endpoints.slice(1).map(Number)};
}
function relief(u,v,t,s,enabled=true){
 if(!enabled)return 0;
 const [ax,az,bx,bz]=s.endpoints,dx=bx-ax,dz=bz-az;
 const x=(u-.5)*21,z=(v-.5)*-16.4;
 const along=Math.max(0,Math.min(1,((x-ax)*dx+(z-az)*dz)/Math.max(dx*dx+dz*dz,.00001)));
 const d=Math.hypot(x-ax-dx*along,z-az-dz*along);
 const [a,b,c,e]=s.env,[k,w,l]=s.phase;
 const envelope=smooth(a,b,d)*(1-smooth(c,e,d));
 return s.amp*envelope*Math.max(0,Math.sin(d*k-t*w+along*l))**2
  *(1-smooth(.65,.96,Math.hypot((u-.5)*2,(v-.5)*2)));
}
test('same timber inputs and ordinary clock affect only the existing wetland vertex branch',()=>{
 assert.match(vertex,/uniform float uTimberContact;uniform vec4 uTimberSegment/);
 assert.match(wet,/if\(uTimberContact>\.5\)/);
 assert.match(wet,/timberPoint=\(uv-vec2\(\.5\)\)\*vec2\(21\.,-16\.4\)/);
 assert.match(wet,/timberAlong=clamp\(dot\(timberPoint-uTimberSegment\.xy,timberAxis\)\/max\(dot\(timberAxis,timberAxis\),\.00001\),0\.,1\.\)/);
 assert.match(wet,/timberDistance=length\(timberPoint-\(uTimberSegment\.xy\+timberAxis\*timberAlong\)\)/);
 assert.match(wet,/timberBroadCrest=pow\(max\(sin\(timberBroadPhase\),0\.\),2\.\)/);
 assert.doesNotMatch(vertex.slice(vertex.indexOf('if(uRiver>.5)')),/timberBroad|timberEnvelope/);
 assert.match(fragment,/timberPhase=timberDistance\*15\.-uTime\*1\.8\+timberAlong\*9\./);
 assert.match(source,/uTimberContact:\{value:0\}/);
 assert.equal((source.match(/uTimberContact\.value=1/g)||[]).length,1);
 const s=spec();assert.equal(s.phase[1],1.8);assert.ok(s.phase[0]<3);
});
test('source disk vertices show bounded, local, time-varying broad wake; no additional mesh required',()=>{
 const s=spec();
 assert.match(source,/function wetlandWaterDisk\(name='Candidate wetland water surface',segments=48\)/);
 assert.match(source,/const rings=8,position=\[0,0,0\],uv=\[\.5,\.5\]/);
 assert.match(source,/uv\.push\(\.5\+\.5\*x,\.5\+\.5\*y\)/);
 const points=[[.5,.5]];
 for(let r=1;r<=8;r++)for(let i=0;i<48;i++){
  const a=i*2*Math.PI/48;
  points.push([.5+.5*r/8*Math.cos(a),.5+.5*r/8*Math.sin(a)]);
 }
 let peak=0,motion=0,active=0;
 for(const [u,v] of points){
  const vals=[0,.7,1.4,2.8,5.6].map(t=>relief(u,v,t,s));
  assert.ok(vals.every(x=>Number.isFinite(x)&&x>=0&&x<=.0080000001));
  if(Math.hypot((u-.5)*2,(v-.5)*2)>=.96)assert.ok(vals.every(x=>x===0));
  assert.equal(relief(u,v,2,s,false),0);
  const max=Math.max(...vals);peak=Math.max(peak,max);
  motion=Math.max(motion,max-Math.min(...vals));if(max>.0001)active++;
 }
 assert.equal(points.length,385);
 assert.ok(active>=8,'wake must reach multiple actual interior vertex positions');
 assert.ok(peak>.004&&motion>.004,'ordinary time produces meaningful local candidate relief');
 console.log('TIMBER_BROAD_WAKE_CPU',JSON.stringify({vertices:points.length,samples:points.length*5,active,peak,motion}));
});
test('existing segment envelope excludes distant water and the original rim',()=>{
 const s=spec(),[ax,az,bx,bz]=s.endpoints;
 const dx=bx-ax,dz=bz-az,l=Math.hypot(dx,dz);
 for(let i=0;i<=20;i++)for(const sign of [-1,1])for(const offset of [0,1.85,2,3]){
  const x=ax+dx*i/20-sign*offset*dz/l,z=az+dz*i/20+sign*offset*dx/l;
  assert.ok(relief(.5+x/21,.5-z/16.4,1.7,s)<1e-12);
 }
 for(let i=0;i<48;i++){const a=i*2*Math.PI/48;assert.equal(relief(.5+.5*Math.cos(a),.5+.5*Math.sin(a),2,s),0);}
});
