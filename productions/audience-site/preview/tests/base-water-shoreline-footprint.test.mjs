import test from 'node:test';
import assert from 'node:assert/strict';
import {createBaseWaterMaterial} from '../three-world.mjs';

// Inspect the actual shader passed to the adapter's injected Three interface.
// No GLSL execution or pixel-quality claim is made by these contract tests.
const THREE={
 UniformsUtils:{merge:()=>({})},UniformsLib:{fog:{}},
 ShaderMaterial:class {constructor(options){Object.assign(this,options);}},
 DoubleSide:2
};
const material=createBaseWaterMaterial(THREE);
const f=material.fragmentShader,v=material.vertexShader;
const fade=width=>{
 const t=Math.max(0,Math.min(1,(width-.5)/1.5));
 return 1-t*t*(3-2*t);
};
const crest=(a,b)=>Math.max(Math.sin(a)*Math.sin(b),0)**6;

test('shore breakup is band-limited using its own shorter wavelength',()=>{
 assert.match(f,/float shorePhaseA=vP\.x\*3\.1\+uTime\*\.8;/);
 assert.match(f,/float shorePhaseB=vP\.z\*2\.8-uTime\*\.71;/);
 assert.match(f,/float shorePixelSpan=max\(fwidth\(shorePhaseA\),fwidth\(shorePhaseB\)\);/);
 assert.match(f,/float shoreDetailFade=1\.-smoothstep\(\.5,2\.,shorePixelSpan\);/);
 assert.match(f,/float breaking=pow\(max\(sin\(shorePhaseA\)\*sin\(shorePhaseB\),0\.\),6\.\)\*shoreDetailFade;/);
});

test('at resolved footprint the original shore crest remains; coarse shoreline detail fades independently',()=>{
 const a=Math.PI/2,b=Math.PI/2;
 const offshoreWidth=1.7*.5,shoreWidth=3.1*.5;
 assert.equal(crest(a,b)*fade(.1),crest(a,b));
 assert.ok(crest(a,b)*fade(shoreWidth)<crest(a,b)*fade(offshoreWidth));
 assert.equal(fade(3.1),0);
 assert.ok(fade(1.7)>0);
 // Corresponds to the shader's separate derivative gains, not a pixel measurement.
 assert.match(f,/\*shoreDetailFade;/);
 assert.match(f,/pow\(max\(w,0\.\),9\.\)\*fineDetailFade/);
});

test('shore mask, underlying physical wave and ordinary time remain unchanged',()=>{
 assert.match(f,/shallows\*breaking\*\.25/);
 assert.match(f,/texture2D\(uShoreMask,clamp\(shoreUV,0\.,1\.\)\)/);
 assert.match(v,/p\.z\+=sin\(phaseX\)\*\.07\+sin\(phaseY\)\*\.05/);
 assert.doesNotMatch(v,/fwidth\(/);
 assert.doesNotMatch(v+f,/\buWeather\b|\buGlobalCalm\b/);
 assert.equal((v+f).match(/\buStorm\b/g).length,1);
 assert.notEqual(crest(1,1),crest(1+.8,1-.71));
});
