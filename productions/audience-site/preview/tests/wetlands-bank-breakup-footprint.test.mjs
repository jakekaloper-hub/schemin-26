import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const start=source.indexOf('float bankBreakup=');
const end=source.indexOf('float bankMask=',start);
const block=source.slice(start,end);
const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const vec2=(x,y)=>({x,y});
const dot=(a,b)=>a.x*b.x+a.y*b.y;
const scale=(a,s)=>vec2(a.x*s,a.y*s);
// Execute the actual shader expressions with controlled UV derivatives.
// Only the vector arithmetic syntax is translated; this is not GPU evidence.
const scalar=block.replace(/\b(?:float|vec2)(?=\s+\w+\s*=)/g,'let')
 .replace('vUv-vec2(.5)','vec2(vUv.x-.5,vUv.y-.5)')
 .replace('13.*vec2(-bankDelta.y,bankDelta.x)/max(dot(bankDelta,bankDelta),.00001)',
  'scale(vec2(-bankDelta.y,bankDelta.x),13./max(dot(bankDelta,bankDelta),.00001))');
const evaluate=new Function('vUv','bankAngle','uTime','sin','max','abs','vec2','dot','scale','dFdx','dFdy','mix','smoothstep',scalar+'\nreturn bankBreakup;');
const sample=(x,y,t,h,k=h)=>evaluate(vec2(x+.5,y+.5),Math.atan2(y,x),t,Math.sin,Math.max,Math.abs,vec2,dot,scale,()=>vec2(h,0),()=>vec2(0,k),(a,b,w)=>a+(b-a)*w,smooth);
const original=(x,y,t)=>.45+.55*(.5+.5*Math.sin(Math.atan2(y,x)*13+t*.63));

test('bank angular breakup uses a seam-safe local footprint independently of the radial carrier',()=>{
 assert.ok(start>=0&&end>start);
 assert.ok(block.includes('bankBreakGradient=13.*vec2(-bankDelta.y,bankDelta.x)/max(dot(bankDelta,bankDelta),.00001)'));
 assert.ok(block.includes('abs(dot(bankBreakGradient,dFdx(vUv)))'));
 assert.ok(block.includes('abs(dot(bankBreakGradient,dFdy(vUv)))'));
 assert.ok(!block.includes('fwidth(bankAngle'));
 assert.ok(source.includes('bankCrest*bankOpticalGain*bankBreakup*bankMask*uBankContact'));
 assert.ok(!/uStorm|uWeather|uGlobalCalm/.test(block));
});

test('resolved bank breakup preserves ordinary animation around the existing circumference',()=>{
 let motion=0;
 for(let i=0;i<96;i++)for(const r of [.42,.45,.48])for(const t of [0,2,7]){
  const a=i*Math.PI/48,x=r*Math.cos(a),y=r*Math.sin(a),near=sample(x,y,t,.002);
  assert.ok(Math.abs(near-original(x,y,t))<1e-12);
  motion=Math.max(motion,Math.abs(near-sample(x,y,t+1,.002)));
 }
 assert.ok(motion>.1);
});

test('coarse bank breakup tends to its phase mean without a seam or overbrightening',()=>{
 let mean=0;
 for(let i=0;i<4096;i++)mean+=original(.45,0,i*2*Math.PI/(4096*.63));
 mean/=4096;
 assert.ok(Math.abs(mean-.725)<1e-12);
 for(let i=0;i<96;i++)for(const r of [.42,.45,.48])for(const t of [0,2,7]){
  const a=i*Math.PI/48,x=r*Math.cos(a),y=r*Math.sin(a);
  const near=sample(x,y,t,.002),mid=sample(x,y,t,.025),far=sample(x,y,t,.06);
  assert.ok(Math.abs(far-mean)<1e-12);
  assert.ok(mid>=Math.min(near,far)-1e-12&&mid<=Math.max(near,far)+1e-12);
  assert.ok(mid>=.45-1e-12&&mid<=1+1e-12);
 }
 for(const h of [.002,.025,.06])for(const t of [0,2,7]){
  assert.ok(Math.abs(sample(-.45,1e-7,t,h)-sample(-.45,-1e-7,t,h))<3e-6);
 }
 assert.ok(Number.isFinite(sample(0,0,0,.025)));
});
