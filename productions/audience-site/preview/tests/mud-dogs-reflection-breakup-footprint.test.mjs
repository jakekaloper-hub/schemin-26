import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const begin=source.indexOf('}else if(uWetland>.5){');
const end=source.indexOf('}else if(uRiver>.5){',begin);
const wetland=source.slice(begin,end);
const smooth=x=>{const t=Math.max(0,Math.min(1,(x-.35)/.8));return t*t*(3-2*t);};
const mix=(a,b,t)=>a+(b-a)*t;

test('canopy product is filtered at sum and difference footprints, retaining its root envelope',()=>{
 assert.ok(begin>=0&&end>begin);
 for(const term of [
  'float canopyPhaseX=delta.x*3.8-uTime*.27;',
  'float canopyPhaseY=delta.y*4.4+uTime*.21;',
  'max(fwidth(canopyPhaseX+canopyPhaseY),fwidth(canopyPhaseX-canopyPhaseY))',
  'wateryBreakup=mix(wateryBreakup,.5,smoothstep(.35,1.15,canopyFootprint));',
  'canopyShade=max(canopyShade,canopyFade*(.66+.34*wateryBreakup));'
 ])assert.ok(wetland.includes(term),term);
 assert.ok(wetland.indexOf('wateryBreakup=mix')<wetland.indexOf('canopyShade=max'));
});
test('trunk mirror retains the existing envelope and independently filters its moving breakup',()=>{
 for(const term of [
  'float mirrorPhase=delta.y*10.+uTime*.51+delta.x*4.;',
  'mirrorBreakup=mix(mirrorBreakup,.55,smoothstep(.35,1.15,fwidth(mirrorPhase)));',
  'trunkReflection=max(trunkReflection,mirrorStreak*mirrorBreakup);',
  'trunkMirrorMix=clamp(trunkReflection*.20*trunkView*bankFade,0.,.20)'
 ])assert.ok(wetland.includes(term),term);
 assert.ok(wetland.indexOf('mirrorBreakup=mix')<wetland.indexOf('trunkReflection=max'));
 assert.ok(!source.slice(end).includes('mirrorPhase'));
 assert.ok(!/uStorm|uRain|uWeather|uGlobalCalm/.test(wetland));
});
test('analytic footprint model retains resolved motion, coarse means and original bounds',()=>{
 for(const step of [.001,.04,.2]){
  const canopySpan=step*(3.8+4.4),mirrorSpan=step*(4+10);
  let sumC=0,sumM=0,count=0,maxC=0,maxM=0;
  for(let x=0;x<64;x++)for(let y=0;y<64;y++){
   const a=x*Math.PI/32,b=y*Math.PI/32;
   const c=t=>mix(.5+.5*Math.sin(a-t*.27)*Math.sin(b+t*.21),.5,smooth(canopySpan));
   const m=t=>mix(.55+.45*Math.sin(a+b+t*.51),.55,smooth(mirrorSpan));
   const cv=c(0),mv=m(0);
   assert.ok(cv>=0&&cv<=1&&mv>=.1-1e-12&&mv<=1);
   sumC+=cv;sumM+=mv;count++;
   maxC=Math.max(maxC,Math.abs(c(0)-c(2)));
   maxM=Math.max(maxM,Math.abs(m(0)-m(2)));
   if(step===.2){assert.equal(cv,.5);assert.equal(mv,.55);}
  }
  assert.ok(Math.abs(sumC/count-.5)<1e-12);
  assert.ok(Math.abs(sumM/count-.55)<1e-12);
  if(step===.001){assert.equal(smooth(canopySpan),0);assert.equal(smooth(mirrorSpan),0);assert.ok(maxC>.1&&maxM>.1);}
 }
});
