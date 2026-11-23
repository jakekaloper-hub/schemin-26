import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {assertShadowFramebufferReady,nextWaterPhase} from '../renderer.mjs';
const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
function fixture({complete=true,bound=true}={}){
 const calls=[],framebuffer={label:'shadow-target'};
 const gl={
  FRAMEBUFFER:1,FRAMEBUFFER_BINDING:2,FRAMEBUFFER_COMPLETE:3,
  getParameter:(name)=>{calls.push(['binding',name]);return bound?framebuffer:null;},
  checkFramebufferStatus:(target)=>{calls.push(['status',target]);return complete?3:4;},
  bindFramebuffer:(target,value)=>calls.push(['bind',target,value])
 };
 return {gl,calls,framebuffer};
}
test('existing shadow framebuffer is checked without changing its binding',()=>{
 const {gl,calls,framebuffer}=fixture();
 assert.equal(assertShadowFramebufferReady(gl,framebuffer),undefined);
 assert.deepEqual(calls,[['binding',gl.FRAMEBUFFER_BINDING],['status',gl.FRAMEBUFFER]]);
});
test('incomplete target fails closed and unbinds before any scene draw',()=>{
 const {gl,calls,framebuffer}=fixture({complete:false});
 assert.throws(()=>assertShadowFramebufferReady(gl,framebuffer),/SHADOW_FRAMEBUFFER_INCOMPLETE/);
 assert.deepEqual(calls.at(-1),['bind',gl.FRAMEBUFFER,null]);
});
test('misbound target fails closed instead of inspecting the default framebuffer',()=>{
 const {gl,calls,framebuffer}=fixture({bound:false});
 assert.throws(()=>assertShadowFramebufferReady(gl,framebuffer),/SHADOW_FRAMEBUFFER_NOT_BOUND/);
 assert.deepEqual(calls,[['binding',gl.FRAMEBUFFER_BINDING],['bind',gl.FRAMEBUFFER,null]]);
});
test('invalid shadow input has no effects',()=>{
 const {gl,calls,framebuffer}=fixture();
 assert.throws(()=>assertShadowFramebufferReady(gl,null),/INVALID_SHADOW_TARGET/);
 assert.throws(()=>assertShadowFramebufferReady(null,framebuffer),/INVALID_SHADOW_TARGET/);
 assert.throws(()=>assertShadowFramebufferReady({getParameter:()=>1},framebuffer),/INVALID_SHADOW_TARGET/);
 assert.deepEqual(calls,[]);
});
test('real native renderer checks attachment before depth draw and restores default framebuffer',()=>{
 const a=source.indexOf('gl.bindFramebuffer(gl.FRAMEBUFFER,fb);'),
  b=source.indexOf('gl.framebufferTexture2D(gl.FRAMEBUFFER,gl.COLOR_ATTACHMENT0'),
  c=source.indexOf('gl.framebufferRenderbuffer(gl.FRAMEBUFFER,gl.DEPTH_ATTACHMENT'),
  d=source.indexOf('assertShadowFramebufferReady(gl,fb);'),
  e=source.indexOf('gl.useProgram(S);'),
  f=source.indexOf('gl.bindFramebuffer(gl.FRAMEBUFFER,null);',e),
  g=source.indexOf('gl.useProgram(P);',f);
 assert.ok(a>=0&&b>a&&c>b&&d>c&&e>d&&f>e&&g>f);
 assert.match(source,/gl\.drawArrays\(gl\.TRIANGLES,0,terrain\.count\);gl\.bindFramebuffer\(gl\.FRAMEBUFFER,null\);/);
});
test('ordinary shader water continues during weather calm but freezes on explicit pause',()=>{
 assert.equal(nextWaterPhase(5,12,false),12);
 assert.equal(nextWaterPhase(5,12,true),5);
 assert.match(source,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uTime,waterTime\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uWater,1\);bind\(P,ocean\);/);
});
