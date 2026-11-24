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

test('Temporal GPU evidence refuses to overwrite an existing destination before Chrome',()=>{
 const dir=mkdtempSync(join(tmpdir(),'cw-temporal-guard-'));
 const guard=join(dir,'original.txt');
 try{
  writeFileSync(guard,'PRESERVE');
  const p=spawnSync(process.execPath,[script,script,'--temporal-dir',dir],{encoding:'utf8',timeout:6000});
  assert.notEqual(p.status,0);
  assert.match(p.stderr,/TEMPORAL_DIRECTORY_EXISTS/);
  assert.equal(readFileSync(guard,'utf8'),'PRESERVE');
 }finally{rmSync(dir,{recursive:true,force:true});}
});
test('Temporal evidence and standard captures are mutually exclusive',()=>{
 const p=spawnSync(process.execPath,[script,script,'--temporal-dir','/tmp/a','--capture-dir','/tmp/b'],{encoding:'utf8',timeout:6000});
 assert.notEqual(p.status,0);
 assert.match(p.stderr,/Optional capture argument/);
});

test('History sweep refuses an existing destination and is mutually exclusive with image modes',()=>{
 const dir=mkdtempSync(join(tmpdir(),'cw-history-guard-'));
 const guard=join(dir,'original.txt');
 try{
  writeFileSync(guard,'PRESERVE');
  const p=spawnSync(process.execPath,[script,script,'--history-sweep-dir',dir],{encoding:'utf8',timeout:6000});
  assert.notEqual(p.status,0);
  assert.match(p.stderr,/HISTORY_DIRECTORY_EXISTS/);
  assert.equal(readFileSync(guard,'utf8'),'PRESERVE');
  const mixed=spawnSync(process.execPath,[script,script,'--history-sweep-dir','/tmp/a','--capture-dir','/tmp/b'],{encoding:'utf8',timeout:6000});
  assert.notEqual(mixed.status,0);
  assert.match(mixed.stderr,/Optional capture argument/);
 }finally{rmSync(dir,{recursive:true,force:true});}
});

test('DPR image evidence refuses overwrite and incompatible capture options',()=>{
 const dir=mkdtempSync(join(tmpdir(),'cw-dpr-guard-'));
 const guard=join(dir,'original.txt');
 try{
  writeFileSync(guard,'PRESERVE');
  const p=spawnSync(process.execPath,[script,script,'--dpr-evidence-dir',dir],{encoding:'utf8',timeout:6000});
  assert.notEqual(p.status,0);
  assert.match(p.stderr,/DPR_DIRECTORY_EXISTS/);
  assert.equal(readFileSync(guard,'utf8'),'PRESERVE');
  for(const args of [['--dpr-evidence-dir'],['--dpr-evidence-dir','--dpr-check'],['--dpr-evidence-dir','/tmp/a','--capture-dir','/tmp/b'],['--dpr-evidence-dir','/tmp/a','--dpr-check']]){
   const mixed=spawnSync(process.execPath,[script,script,...args],{encoding:'utf8',timeout:6000});
   assert.notEqual(mixed.status,0);
   assert.match(mixed.stderr,/Optional capture argument/);
  }
 }finally{rmSync(dir,{recursive:true,force:true});}
});
