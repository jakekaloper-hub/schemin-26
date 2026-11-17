import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

// Shader regressions inspect the actual scene source. Existing Three.js tests
// separately verify the complete Temple mesh, source bindings, and water clock.
const source=readFileSync(new URL('../regional-assets.mjs',import.meta.url),'utf8');
const vertex=source.split('vertexShader:`')[1]?.split('`,')[0];
const fragment=source.split('fragmentShader:`')[1]?.split('`});')[0];

const normalized=(x,y,z)=>{
 const n=Math.hypot(x,y,z);
 return n>1e-5?[x/n,y/n,z/n]:[0,0,1];
};
const response=(normal,eye,base)=>{
 const n=normalized(...normal),v=normalized(...eye);
 const cosine=Math.min(1,Math.max(0,Math.abs(n.reduce((s,x,i)=>s+x*v[i],0))));
 const grazing=(1-cosine)**3;
 const foldFacet=Math.min(1,Math.max(0,Math.abs(n[2])));
 return base.map((x,i)=>Math.min(1,Math.max(0,x*(.945+.055*foldFacet)+[.08,.10,.08][i]*(grazing*.32))));
};

test('Temple retains its single fixed-edge, physically animated falling sheet',()=>{
 assert.ok(vertex&&fragment,'shader source must be present');
 assert.match(vertex,/if\(uFall>\.5\)/);
 assert.match(vertex,/sideHold=sin\(uv\.x\*3\.14159265\)/);
 assert.match(vertex,/endHold=sin\(uv\.y\*3\.14159265\)/);
 assert.match(vertex,/p\.z\+=\.10\*sideHold\*endHold\*folds/);
 assert.match(source,/new THREE\.PlaneGeometry\(width,drop,8,12\)/);
 assert.match(source,/waterfall\(g,-5\.8,7\.2,1\.8,2\.15,6\.9\)/);
 assert.doesNotMatch(vertex,/\buStorm\b|\buWeather\b/i);
});

test('candidate fold shading is isolated to waterfall branch and computed from displaced world geometry',()=>{
 const fall=fragment.indexOf('if(uFall>.5){');
 const wetland=fragment.indexOf('}else if(uWetland>.5){');
 assert.ok(fall>=0&&wetland>fall);
 const scoped=fragment.slice(fall,wetland);
 assert.match(scoped,/faceCross=cross\(dFdx\(vWorld\),dFdy\(vWorld\)\)/);
 assert.match(scoped,/faceSize>\.00001\?faceCross\/faceSize:vec3\(0\.,0\.,1\.\)/);
 assert.match(scoped,/eyeRay=normalize\(cameraPosition-vWorld\)/);
 assert.match(scoped,/grazing=pow\(1\.-clamp\(abs\(dot\(sheetNormal,eyeRay\)\),0\.,1\.\),3\.\)/);
 assert.match(scoped,/foldFacet=clamp\(abs\(sheetNormal\.z\),0\.,1\.\)/);
 assert.match(scoped,/fallBase=mix\(uColor,vec3\(\.84,\.96,\.89\),\.27\+stripe\*\.14\+foam\*\.17\)/);
 assert.match(scoped,/fallTint=clamp\(fallBase\*\(\.945\+\.055\*foldFacet\)\+vec3\(\.08,\.10,\.08\)\*\(grazing\*\.32\),0\.,1\.\)/);
 assert.match(scoped,/gl_FragColor=vec4\(fallTint,\.88\)/);
 assert.doesNotMatch(fragment.slice(wetland),/faceCross|sheetNormal|fallTint/,'other existing water material branches untouched');
 assert.doesNotMatch(scoped,/\buStorm\b|\buWeather\b|\buRain\b/);
});

test('bounded fold and grazing response is nontrivial, finite, and alpha/boundary neutral',()=>{
 const base=[.52,.70,.61], normalFlat=[0,0,1],normalFold=[.4,.2,.85];
 const flat=response(normalFlat,[0,0,1],base);
 const folded=response(normalFold,[0,0,1],base);
 const grazing=response(normalFold,[1,0,0],base);
 assert.ok(flat.some((c,i)=>Math.abs(c-folded[i])>1e-4));
 assert.ok(grazing.some((c,i)=>Math.abs(c-folded[i])>1e-4));
 for(const n of [[0,0,0],normalFlat,normalFold,[100,-100,1]])
  for(const eye of [[0,0,1],[1,0,0],[-.3,.2,.6]]){
   const c=response(n,eye,base);
   assert.ok(c.every(x=>Number.isFinite(x)&&x>=0&&x<=1));
  }
 assert.match(fragment,/gl_FragColor=vec4\(fallTint,\.88\)/,'same inherited opacity');
 assert.doesNotMatch(source,/worldMutationAllowed\s*:\s*true/);
 assert.match(source,/CANDIDATE_NOT_APPROVED/);
});
