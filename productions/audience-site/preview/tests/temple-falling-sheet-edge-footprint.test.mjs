import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const start=source.indexOf('if(uFall>.5){',source.indexOf('fragmentShader:'));
const end=source.indexOf('}else if(uWetland>.5){',start);
const fall=source.slice(start,end);
const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const scalar=fall.slice(fall.indexOf('float lateralEdge='),fall.indexOf('gl_FragColor=vec4(fallTint,fallingAlpha)')).replace(/\bfloat\b/g,'let');
// Execute the real scalar opacity expression with a controlled derivative.
// This is analytical shader-contract evidence, not a GPU pixel test.
const evaluate=new Function('vUv','uTime','sin','smoothstep','mix','fwidth',scalar+'\nreturn fallingAlpha;');
const sample=(u,v,t,w)=>evaluate({x:u,y:v},t,Math.sin,smooth,(a,b,x)=>a+(b-a)*x,()=>w);
const original=(u,v,t)=>.88*(1-.50*(1-smooth(0,.16,u)*(1-smooth(.84,1,u)))
 *smooth(.02,.12,v)*(1-smooth(.88,.98,v))*(.55+.45*Math.sin(v*31-t*2.1+Math.sin(u*9)*.65)));

test('Temple side-opacity filter is branch-local and uses its own periodic phase',()=>{
 assert.ok(start>=0&&end>start);
 assert.ok(fall.includes('fwidth(edgeFlutterPhase)'));
 assert.ok(fall.includes('edgeFlutterPhase=vUv.y*31.-uTime*2.1+sin(vUv.x*9.)*.65'));
 assert.ok(!source.slice(end).includes('edgeFlutterPhase'));
 assert.ok(!/uStorm|uWeather|uRain|uGlobalCalm/.test(fall));
});

test('resolved opacity and ordinary water-clock motion remain exactly the existing response',()=>{
 let motion=0;
 for(let i=0;i<=40;i++)for(let j=0;j<=40;j++)for(const t of [0,1.9,8]){
  const u=i/40,v=j/40,x=sample(u,v,t,.1);
  assert.ok(Math.abs(x-original(u,v,t))<1e-12);
  motion=Math.max(motion,Math.abs(x-sample(u,v,t+.47,.1)));
 }
 assert.ok(motion>.08);
});

test('unresolved opacity converges to the temporal mean, with bounded transition and preserved ends',()=>{
 const u=0,v=.5;
 let mean=0;
 for(let i=0;i<4096;i++)mean+=original(u,v,i*2*Math.PI/(4096*2.1));
 mean/=4096;
 assert.ok(Math.abs(mean-.638)<1e-12);
 for(let i=0;i<128;i++){
  const t=i/11,near=sample(u,v,t,.1),mid=sample(u,v,t,.75),far=sample(u,v,t,2);
  assert.ok(Math.abs(far-mean)<1e-12);
  assert.ok(mid>=Math.min(near,far)-1e-12&&mid<=Math.max(near,far)+1e-12);
  for(const x of [0,.08,.5,.92,1])for(const y of [0,.02,.5,.98,1])for(const w of [.1,.75,2]){
   const opacity=sample(x,y,t,w);
   assert.ok(Number.isFinite(opacity)&&opacity>=.44-1e-12&&opacity<=.88+1e-12);
   if(y<=.02||y>=.98||x===.5)assert.equal(opacity,.88);
  }
 }
});
