import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const start=source.indexOf('}else if(uWetland>.5){');
const end=source.indexOf('}else if(uRiver>.5){',start);
const wetland=source.slice(start,end);
const ribbon=wetland.slice(wetland.indexOf('if(uChannel>.5){'),wetland.indexOf('vec3 channelSheen='));
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
// Execute the actual scalar GLSL expressions as JS with a controlled derivative.
// This is an analytical shader contract, not a GPU shader or pixel test.
const scalar=ribbon.slice(ribbon.indexOf('float gap'),ribbon.lastIndexOf('}'))
 .replace(/\bfloat\b/g,'let');
const evaluate=new Function('along','across','uTime','fineLine','p','sin','smoothstep','length','mix','fwidth',
 'let channelRibbons=0;\n'+scalar+'\nreturn channelRibbons;');
const sample=(a,b,t,carrier,radius,footprint)=>evaluate(a,b,t,carrier,[radius,0],
 Math.sin,smooth,v=>Math.hypot(...v),(x,y,z)=>x+(y-x)*z,()=>footprint);
const nearMask=(a,b,t)=>smooth(.34,.80,.5+.5*Math.sin(a*23-t*.53+Math.sin(b*11)*.72));

test('channel gap phase independently filters the existing optical ribbon',()=>{
 assert.ok(start>=0&&end>start);
 assert.ok(ribbon.includes('fwidth(gapCoordinate)'));
 assert.ok(ribbon.includes('fwidth(channelRibbonCoordinate)'));
 assert.ok(ribbon.includes('fineLine*.45424*interior'));
 assert.ok(!/uStorm|uWeather|uGlobalCalm/.test(wetland));
 assert.ok(!source.slice(end).includes('gapCoordinate'));
});

test('resolved gaps retain original motion and bank taper without reviving a filtered carrier',()=>{
 let change=0;
 for(let i=0;i<64;i++)for(const radius of [0,.83,1]){
  const a=i/32-1,b=.22,t=2,carrier=.73,bank=1-smooth(.70,.98,radius);
  const x=sample(a,b,t,carrier,radius,.1);
  assert.ok(Math.abs(x-carrier*nearMask(a,b,t)*bank)<1e-12);
  change=Math.max(change,Math.abs(x-sample(a,b,t+2,carrier,radius,.1)));
  for(const footprint of [.1,.75,2])assert.equal(sample(a,b,t,0,radius,footprint),0);
 }
 assert.ok(change>.2);
});

test('undersampled longitudinal breakup converges to the phase mean with bounded intermediate gain',()=>{
 let total=0;
 for(let i=0;i<4096;i++)total+=nearMask(i*2*Math.PI/(4096*23),0,0);
 const mean=total/4096;
 assert.ok(Math.abs(mean-.45424)<.00001);
 for(let i=0;i<128;i++){
  const a=i/64-1,b=.13,t=1.4;
  const near=sample(a,b,t,1,0,.1),mid=sample(a,b,t,1,0,.75),far=sample(a,b,t,1,0,2);
  assert.ok(Math.abs(far-mean)<.00001);
  assert.ok(mid>=Math.min(near,far)-1e-12&&mid<=Math.max(near,far)+1e-12);
  assert.equal(sample(a,b,t,1,1,2),0);
 }
});
