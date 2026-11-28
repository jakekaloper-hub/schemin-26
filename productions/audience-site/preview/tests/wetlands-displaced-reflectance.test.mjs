import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const start=source.indexOf('}else if(uWetland>.5){'),end=source.indexOf('}else if(uRiver>.5){',start);
const region=source.slice(start,end);
const clamp=x=>Math.min(1,Math.max(0,x));
const dot=(a,b)=>a.reduce((sum,v,i)=>sum+v*b[i],0);
const unit=v=>{const m=Math.hypot(...v);return m>.00001?v.map(x=>x/m):[0,1,0];};
// Select the actual source incidence operand, not a hardcoded desired model.
function incidence(face,eye){
 const match=region.match(/float viewIncidence=clamp\(abs\((viewToEye\.y|dot\(wetlandNormal,viewToEye\))\),0\.,1\.\);/);
 assert.ok(match,'recognized source incidence expression');
 const n=unit(face),e=unit(eye);
 return clamp(Math.abs(match[1]==='viewToEye.y'?e[1]:dot(n,e)));
}
const grazing=i=>.035+.21*(1-i)**2;
const trunkView=i=>{const x=clamp((1-i-.22)/(.80-.22));return x*x*(3-2*x);};

test('existing displaced normal is evaluated once before both optical consumers',()=>{
 assert.ok(start>=0&&end>start);
 assert.equal(region.split('vec3 wetlandFace=cross(dFdx(vWorld),dFdy(vWorld));').length,2);
 assert.ok(region.indexOf('vec3 wetlandNormal=')<region.indexOf('float viewIncidence='));
 assert.ok(region.indexOf('float viewIncidence=')<region.indexOf('float reliefSlope='));
 assert.ok(region.includes('wetlandFaceSize>.00001?wetlandFace/wetlandFaceSize:vec3(0.,1.,0.)'));
 assert.ok(region.includes('float viewIncidence=clamp(abs(dot(wetlandNormal,viewToEye)),0.,1.);'));
 assert.ok(region.includes('trunkView=smoothstep(.22,.80,1.-viewIncidence)'));
 assert.ok(region.includes('grazingGain=.035+.21*pow(1.-viewIncidence,2.)'));
 assert.ok(!/uStorm|uWeather|uGlobalCalm/.test(region));
});
test('opposite resolved surface slopes respond differently at one fixed camera',()=>{
 const eye=[.8,.6,0],toward=[.14,.99,0],away=[-.14,.99,0];
 const a=incidence(toward,eye),b=incidence(away,eye);
 assert.ok(a>b+.15);
 assert.ok(grazing(b)>grazing(a)+.02);
 assert.ok(trunkView(b)>trunkView(a)+.2);
});
test('flat and degenerate surfaces preserve old incidence, winding is irrelevant, and gains remain bounded',()=>{
 for(let i=0;i<=40;i++)for(let j=0;j<=40;j++){
  const eye=[Math.cos(i*.14)*Math.cos(j*.04),Math.sin(j*.04),Math.sin(i*.14)*Math.cos(j*.04)];
  const face=[Math.sin(i*.17)*.25,1,Math.cos(j*.13)*.25];
  const a=incidence(face,eye),b=incidence(face.map(x=>-x),eye);
  assert.ok(Math.abs(a-b)<1e-12);
  assert.ok(Math.abs(incidence([0,1,0],eye)-Math.abs(unit(eye)[1]))<1e-12);
  assert.equal(incidence([0,0,0],eye),incidence([0,1,0],eye));
  assert.ok(Number.isFinite(a)&&a>=0&&a<=1);
  assert.ok(grazing(a)>=.035&&grazing(a)<=.245+1e-12);
  assert.ok(trunkView(a)>=0&&trunkView(a)<=1);
 }
});
