import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const start=source.indexOf('}else if(uWetland>.5){');
const end=source.indexOf('}else if(uRiver>.5){',start);
const region=source.slice(start,end);
// Evaluate actual source advection sign and bound flow vectors on CPU;
// this tests directional coherence, not GLSL execution or rendered pixels.
const signMatch=region.match(/wetlandUv = vUv ([+-]) uFlow \* uTime;/);
const flowMatch=source.match(/kind==='channel'\?new THREE\.Vector2\(([^)]+)\):kind==='swamp'\?new THREE\.Vector2\(([^)]+)\)/);
const flows=flowMatch?flowMatch.slice(1).map(v=>v.split(',').map(Number)):[];
function sample(u,v,t,flow){
 assert.ok(signMatch,'recognized source advection');
 const sign=signMatch[1]==='+'?1:-1;
 const x=u+sign*flow[0]*t,y=v+sign*flow[1]*t;
 const meander=Math.sin(y*10+Math.sin(x*6)*.5)*.024;
 return [(x+meander)*44+y*11+Math.sin(x*9)*.8,
 .5+.5*Math.sin((x-y)*10+Math.sin(y*6)*.6)];
}
test('current sheen and sediment translate with both inherited illustrative flow vectors',()=>{
 assert.equal(flows.length,2);
 for(const flow of flows)for(let i=1;i<=9;i++)for(let j=1;j<=9;j++)for(const t of [.5,2,4]){
  const u=i/10,v=j/10,initial=sample(u,v,0,flow);
  const moved=sample(u+flow[0]*t,v+flow[1]*t,t,flow);
  for(let k=0;k<2;k++)assert.ok(Math.abs(initial[k]-moved[k])<1e-10,'transport follows source heading');
 }
});
test('startup pattern and nonzero animation remain, with no weather input',()=>{
 for(const flow of flows){
  const [a,b]=sample(.43,.62,0,flow);
  const meander=Math.sin(.62*10+Math.sin(.43*6)*.5)*.024;
  assert.ok(Math.abs(a-((.43+meander)*44+.62*11+Math.sin(.43*9)*.8))<1e-12);
  assert.ok(Math.abs(b-(.5+.5*Math.sin((.43-.62)*10+Math.sin(.62*6)*.6)))<1e-12);
  assert.ok(Math.abs(sample(.43,.62,2,flow)[0]-a)>.1);
 }
 assert.ok(!/uStorm|uWeather|uGlobalCalm/.test(region));
});
test('base physical displacement and channel ribbons retain forward heading and local eddy stays anchored',()=>{
 assert.ok(source.includes('dot(uv-vec2(.5),heading)*30.-uTime*1.16'));
 assert.ok(source.includes('normalize(uFlow+vec2(.0001,.0001))'));
 assert.ok(region.includes('alongAxis=normalize(uFlow)'));
 assert.ok(region.includes('along*7.-uTime*.90'));
 assert.ok(region.includes('length((vUv-vec2(.52,.44))*vec2(1.,1.4))*30.-uTime*.15'));
 assert.ok(region.includes('fwidth(currentCoordinate)'));
});
