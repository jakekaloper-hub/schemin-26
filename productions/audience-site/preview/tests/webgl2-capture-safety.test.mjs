import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtempSync,writeFileSync,rmSync,readFileSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';

const script=new URL('../tools/webgl2-journey-smoke.mjs',import.meta.url).pathname;
test('GPU capture path refuses to overwrite existing visual evidence before starting Chrome',()=>{
 const dir=mkdtempSync(join(tmpdir(),'cw-capture-guard-'));
 const guard=join(dir,'do-not-replace.txt');
 try{
  writeFileSync(guard,'ORIGINAL EVIDENCE');
  const p=spawnSync(process.execPath,[script,script,'--capture-dir',dir],{encoding:'utf8',timeout:6000});
  assert.notEqual(p.status,0);
  assert.match(p.stderr,/CAPTURE_DIRECTORY_EXISTS/);
  assert.equal(readFileSync(guard,'utf8'),'ORIGINAL EVIDENCE');
 }finally{rmSync(dir,{recursive:true,force:true});}
});
test('GPU capture rejects malformed opt-in arguments without starting Chrome',()=>{
 const p=spawnSync(process.execPath,[script,script,'--capture-dir'],{encoding:'utf8',timeout:6000});
 assert.notEqual(p.status,0);
 assert.match(p.stderr,/Optional capture argument/);
});
