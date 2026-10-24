import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {createRequire} from "node:module";
import {execFileSync} from "node:child_process";
import {BullpenRuntime,STATUS} from "../../../bullpen-runtime/src/runtime.js";
import {FileArtifactStore,FileJobStore} from "../../../bullpen-runtime/src/persistent-store.js";
const require=createRequire(import.meta.url);
const storePath=process.env.BULLPEN_MEMORY_STORE_PATH;
if(!storePath) throw new Error("BULLPEN_MEMORY_STORE_PATH required; no simulated memoryStore");
const {createMemoryStore,assertMemoryEntry}=require(storePath);
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"../../..");
const py=`import importlib.util,json
from pathlib import Path
root=Path.cwd()
def load(n,p):
 spec=importlib.util.spec_from_file_location(n,root/p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
h=load("h","living-novel/os/adapters/hydrated_author_memory.py")
e=load("e","living-novel/os/adapters/bullpen_memory_contract.py")
print(json.dumps(e.export_memories(h.hydrate(character_id="CHAR-JAKE-KALOPER",scene_year=2026,scene_week=3),observed_at="2026-10-18T13:00:00Z")))
`;
const entries=JSON.parse(execFileSync("python3",["-c",py],{cwd:root,encoding:"utf8"}));
assert(entries.length>0);
const temp=await fs.mkdtemp(path.join(os.tmpdir(),"schemin-memory-gate-"));
try {
 const jobs=new FileJobStore(temp), artifacts=new FileArtifactStore(temp);
 const pipeline={id:"novel-memory-gate",stages:[{id:"export-memory",worker:"exporter",gate:"validator"},{id:"verify-readback",worker:"reader",gate:"auditor"}]};
 let exports=0;
 const workers={
  exporter:async()=>({artifact:{entries:entries.map(e=>{assertMemoryEntry(e);return e}),count:++exports}}),
  validator:async()=>({pass:true}),
 };
 const first=await new BullpenRuntime({workers,jobStore:jobs,artifactStore:artifacts}).run({jobId:"novel-memory",pipeline});
 assert.equal(first.status,STATUS.BLOCKED);
 assert.equal(first.stages[0].status,STATUS.PASSED);
 const observed=await fs.readFile(first.artifacts[0].path,"utf8");
 const record=JSON.parse(observed);
 const reader=async()=>{
  const memory=createMemoryStore(record.entries);
  for(const entry of entries){assert.deepEqual(memory.get(entry.id).value,entry.value);assert.equal(memory.resolveKey(entry.key,{scope:"schemin-26",now:"2026-10-18T13:00:00Z"}).state,"resolved")}
  return {artifact:{verified:entries.length,sourceArtifact:first.artifacts[0].sha256}};
 };
 const resumed=await new BullpenRuntime({workers:{...workers,reader,auditor:async()=>({pass:true})},jobStore:jobs,artifactStore:artifacts}).run({jobId:"novel-memory",pipeline,resume:true});
 assert.equal(resumed.status,STATUS.PASSED);
 assert.equal(exports,1);
 const restarted=new FileJobStore(temp);
 const saved=await restarted.load("novel-memory");
 assert.equal(saved.status,STATUS.PASSED);
 assert.equal(saved.artifacts.length,2);
 assert.equal(JSON.parse(await fs.readFile(saved.artifacts[1].path,"utf8")).verified,entries.length);
 console.log(JSON.stringify({result:"PASS",entries:entries.length,artifact_sha256:saved.artifacts[0].sha256,restart_recovery:true,resume_without_replay:true,actual_bullpen_contract:true,temporary_store_only:true,authenticated_director_runtime:false}));
} finally {await fs.rm(temp,{recursive:true,force:true})}
