import { randomUUID } from "node:crypto";

export const STATUS = Object.freeze({
  PENDING:"pending", RUNNING:"running", PASSED:"passed", FAILED:"failed", BLOCKED:"blocked"
});

export class BullpenRuntime {
  constructor({workers={}, artifactStore}={}) {
    this.workers=workers;
    this.artifactStore=artifactStore ?? new MemoryArtifactStore();
  }

  async run({jobId=randomUUID(), pipeline, input={}}) {
    if (!pipeline?.stages?.length) throw new Error("pipeline requires stages");
    const state={jobId,pipeline:pipeline.id,status:STATUS.RUNNING,input,stages:[],artifacts:[]};
    for (const stage of pipeline.stages) {
      const rec={id:stage.id,worker:stage.worker,status:STATUS.RUNNING,attempts:0};
      state.stages.push(rec);
      const worker=this.workers[stage.worker];
      if (!worker) return this.#block(state,rec,`missing worker: ${stage.worker}`);
      try {
        rec.attempts++;
        const result=await worker({jobId,input,state,stage});
        if (!result?.artifact) return this.#block(state,rec,`worker ${stage.worker} produced no artifact`);
        const stored=await this.artifactStore.put(jobId,stage.id,result.artifact);
        state.artifacts.push(stored);
        if (stage.gate) {
          const gate=this.workers[stage.gate];
          if (!gate) return this.#block(state,rec,`missing gate: ${stage.gate}`);
          const verdict=await gate({jobId,input,state,stage,artifact:stored});
          rec.gate={worker:stage.gate,...verdict};
          if (verdict?.pass !== true) {
            rec.status=STATUS.FAILED;
            state.status=STATUS.FAILED;
            state.failure={stage:stage.id,reason:verdict?.reason ?? "gate failed"};
            return state;
          }
        }
        rec.status=STATUS.PASSED;
        rec.artifactId=stored.id;
      } catch (error) {
        rec.status=STATUS.FAILED;
        state.status=STATUS.FAILED;
        state.failure={stage:stage.id,reason:error.message};
        return state;
      }
    }
    state.status=STATUS.PASSED;
    return state;
  }

  #block(state,rec,reason){
    rec.status=STATUS.BLOCKED;
    state.status=STATUS.BLOCKED;
    state.failure={stage:rec.id,reason};
    return state;
  }
}

export class MemoryArtifactStore {
  constructor(){this.items=[]}
  async put(jobId,stageId,artifact){
    const item={id:`${jobId}:${stageId}:${this.items.length+1}`,jobId,stageId,artifact,createdAt:new Date().toISOString()};
    this.items.push(item); return item;
  }
}
