import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {BullpenRuntime,STATUS} from "../src/runtime.js";
import {FileArtifactStore,FileJobStore} from "../src/persistent-store.js";
import {requireProductionAdapter} from "../src/adapters.js";

test("retryable gate causes bounded revision then passes",async()=>{
 let n=0;const workers={maker:async()=>({artifact:{n:++n}}),review:async({attempt})=>attempt===1?{pass:false,retryable:true,reason:"revise"}:{pass:true}};
 const r=await new BullpenRuntime({workers,maxAttempts:2}).run({jobId:"retry",pipeline:{id:"p",stages:[{id:"x",worker:"maker",gate:"review"}]}});
 assert.equal(r.status,STATUS.PASSED);assert.equal(r.stages[0].attempts,2);assert.equal(r.artifacts.length,2);
});
test("retry exhaustion fails",async()=>{
 const workers={maker:async()=>({artifact:{}}),review:async()=>({pass:false,retryable:true,reason:"still bad"})};
 const r=await new BullpenRuntime({workers,maxAttempts:2}).run({jobId:"exhaust",pipeline:{id:"p",stages:[{id:"x",worker:"maker",gate:"review"}]}});
 assert.equal(r.status,STATUS.FAILED);assert.equal(r.stages[0].attempts,2);
});
test("creator cannot self certify",async()=>{
 const workers={same:async()=>({artifact:{}})};
 const r=await new BullpenRuntime({workers}).run({jobId:"self",pipeline:{id:"p",stages:[{id:"x",worker:"same",gate:"same"}]}});
 assert.equal(r.status,STATUS.BLOCKED);
});
test("missing independent gate blocks",async()=>{
 const workers={maker:async()=>({artifact:{}})};
 const r=await new BullpenRuntime({workers}).run({jobId:"nogate",pipeline:{id:"p",stages:[{id:"x",worker:"maker",gate:"review"}]}});
 assert.equal(r.status,STATUS.BLOCKED);assert.match(r.failure.reason,/missing gate/);
});
test("missing artifact blocks",async()=>{
 const workers={maker:async()=>({}),review:async()=>({pass:true})};
 const r=await new BullpenRuntime({workers}).run({jobId:"noartifact",pipeline:{id:"p",stages:[{id:"x",worker:"maker",gate:"review"}]}});
 assert.equal(r.status,STATUS.BLOCKED);
});
test("persisted job resumes without replaying passed stage and preserves provenance",async()=>{
 const root=await fs.mkdtemp(path.join(os.tmpdir(),"bullpen-"));let first=0;const store=new FileJobStore(root),artifacts=new FileArtifactStore(root);
 const p={id:"p",stages:[{id:"a",worker:"a",gate:"ga"},{id:"b",worker:"b",gate:"gb"}]};
 let workers={a:async()=>({artifact:{n:++first}}),ga:async()=>({pass:true})};
 let r=await new BullpenRuntime({workers,jobStore:store,artifactStore:artifacts}).run({jobId:"resume",pipeline:p});assert.equal(r.status,STATUS.BLOCKED);
 workers={...workers,b:async()=>({artifact:{ok:true}}),gb:async()=>({pass:true})};
 r=await new BullpenRuntime({workers,jobStore:store,artifactStore:artifacts}).run({jobId:"resume",pipeline:p,resume:true});
 assert.equal(r.status,STATUS.PASSED);assert.equal(first,1);assert.match(r.artifacts[0].sha256,/^[a-f0-9]{64}$/);assert.ok(r.invocations[0].artifactId);
});
test("unavailable production adapter fails closed",async()=>{
 const worker=requireProductionAdapter("image-generation");
 const workers={worker,gate:async()=>({pass:true})};
 const r=await new BullpenRuntime({workers}).run({jobId:"adapter",pipeline:{id:"p",stages:[{id:"x",worker:"worker",gate:"gate"}]}});
 assert.equal(r.status,STATUS.FAILED);assert.match(r.failure.reason,/BLOCKED_EXTERNAL_ADAPTER/);
});
