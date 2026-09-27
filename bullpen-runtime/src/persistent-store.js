import fs from "node:fs/promises";
import path from "node:path";
import { createHash } from "node:crypto";

const safe=s=>String(s).replace(/[^a-zA-Z0-9._-]/g,"_");
export class FileArtifactStore {
  constructor(root=".bullpen"){this.root=root}
  async put(jobId,stageId,artifact){
    const body=JSON.stringify(artifact,null,2);
    const sha256=createHash("sha256").update(body).digest("hex");
    const dir=path.join(this.root,"artifacts",safe(jobId));
    await fs.mkdir(dir,{recursive:true});
    const id=`${safe(stageId)}-${sha256.slice(0,12)}`;
    const file=path.join(dir,`${id}.json`);
    await fs.writeFile(file,body,{flag:"wx"}).catch(async e=>{
      if(e.code!=="EEXIST") throw e;
    });
    return {id,jobId,stageId,sha256,path:file,createdAt:new Date().toISOString()};
  }
}

export class FileJobStore {
  constructor(root=".bullpen"){this.root=root}
  file(jobId){return path.join(this.root,"jobs",`${safe(jobId)}.json`)}
  async save(state){
    const file=this.file(state.jobId); await fs.mkdir(path.dirname(file),{recursive:true});
    const tmp=`${file}.tmp`; await fs.writeFile(tmp,JSON.stringify(state,null,2)); await fs.rename(tmp,file);
    return file;
  }
  async load(jobId){return JSON.parse(await fs.readFile(this.file(jobId),"utf8"))}
}
