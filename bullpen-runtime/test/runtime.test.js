import test from "node:test";
import assert from "node:assert/strict";
import {BullpenRuntime,STATUS} from "../src/runtime.js";

const pipeline={id:"test",stages:[
 {id:"source",worker:"source",gate:"sourceGate"},
 {id:"render",worker:"render",gate:"renderGate"}
]};

test("passes only when every worker emits artifact and every gate passes",async()=>{
 const workers={
  source:async()=>({artifact:{kind:"source",sha:"abc"}}),
  sourceGate:async()=>({pass:true}),
  render:async()=>({artifact:{kind:"image",path:"spread.png"}}),
  renderGate:async()=>({pass:true})
 };
 const result=await new BullpenRuntime({workers}).run({jobId:"job-1",pipeline});
 assert.equal(result.status,STATUS.PASSED);
 assert.equal(result.artifacts.length,2);
 assert.equal(result.stages.every(s=>s.status===STATUS.PASSED),true);
});

test("fails closed when a QA gate rejects an artifact",async()=>{
 const workers={
  source:async()=>({artifact:{kind:"source"}}),
  sourceGate:async()=>({pass:true}),
  render:async()=>({artifact:{kind:"image"}}),
  renderGate:async()=>({pass:false,reason:"character mismatch"})
 };
 const result=await new BullpenRuntime({workers}).run({jobId:"job-2",pipeline});
 assert.equal(result.status,STATUS.FAILED);
 assert.equal(result.failure.stage,"render");
});

test("blocks instead of simulating an unavailable specialist",async()=>{
 const result=await new BullpenRuntime({workers:{}}).run({jobId:"job-3",pipeline});
 assert.equal(result.status,STATUS.BLOCKED);
 assert.match(result.failure.reason,/missing worker/);
});
