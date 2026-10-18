'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const cp=require('node:child_process');
const path=require('node:path');
const source=process.env.BULLPEN_MEMORY_STORE_PATH;
if(!source || !fs.existsSync(source)){console.error('BLOCKED: BULLPEN_MEMORY_STORE_PATH must point to authorized Bullpen knowledge/memoryStore.js');process.exit(2)}
const {createMemoryStore,assertMemoryEntry}=require(source);
const root=path.resolve(__dirname,'../../..');
const generated=cp.execFileSync('python3',['-c',`
import importlib.util,json
from pathlib import Path
root=Path.cwd()
def imp(n,p):
 s=importlib.util.spec_from_file_location(n,root/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=imp('h','living-novel/os/adapters/hydrated_author_memory.py')
b=imp('b','living-novel/os/adapters/bullpen_memory_contract.py')
p=h.hydrate(character_id='CHAR-JAKE-KALOPER',scene_year=2026,scene_week=3)
print(json.dumps(b.export_memories(p,observed_at='2026-10-18T13:00:00Z')))
`],{cwd:root,encoding:'utf8'});
const entries=JSON.parse(generated);
assert(entries.length>0);
const store=createMemoryStore();
for(const e of entries){assertMemoryEntry(e);store.add(e);assert.equal(store.get(e.id).value.classification,'WORLD_EVENT_NOT_PERSONAL_MEMORY')}
const original=entries[0];
assert.equal(store.resolveKey(original.key,{scope:'schemin-26',now:'2026-10-18T13:00:00Z'}).state,'resolved');
assert.equal(store.resolveKey(original.key,{scope:'different-project',now:'2026-10-18T13:00:00Z'}).state,'missing');
const conflicting={...original,id:original.id+'-conflict',confidence:0.5};
store.add(conflicting);
assert.equal(store.resolveKey(original.key,{scope:'schemin-26',now:'2026-10-18T13:00:00Z'}).state,'conflict');
store.add({...original,id:original.id+'-corrected',supersedes:[original.id,conflicting.id],confidence:0.8});
assert.equal(store.resolveKey(original.key,{scope:'schemin-26',now:'2026-10-18T13:00:00Z'}).state,'resolved');
assert.equal(store.get(original.id).status,'superseded');
const stale=createMemoryStore([{...original,id:'short-lived',key:'test-stale',freshness_days:1,observed_at:'2026-01-01T00:00:00Z'}]);
assert.equal(stale.resolveKey('test-stale',{scope:'schemin-26',now:'2026-10-18T13:00:00Z'}).state,'stale');
console.log(JSON.stringify({contract:'PASS',entries:entries.length,checks:['validation','add/readback','project-scope','conflict','supersession','freshness'],persistent_service_connected:false}));
