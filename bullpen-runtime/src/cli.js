#!/usr/bin/env node
import {BullpenRuntime} from "./runtime.js"; import {FileArtifactStore,FileJobStore} from "./persistent-store.js"; import {CHRONICLE_SPREAD_PIPELINE} from "./pipelines.js";
const [cmd="run",jobId=`job-${Date.now()}`]=process.argv.slice(2);const runtime=new BullpenRuntime({workers:{},artifactStore:new FileArtifactStore(),jobStore:new FileJobStore()});const result=await runtime.run({jobId,pipeline:CHRONICLE_SPREAD_PIPELINE,resume:cmd==="resume"});console.log(JSON.stringify(result,null,2));process.exit(result.status==="passed"?0:2);
