export const BLOCKED_EXTERNAL_DEPENDENCY="BLOCKED_EXTERNAL_DEPENDENCY";
export function requireProductionAdapter(name,adapter){
 if(adapter) return adapter;
 return async()=>({blocked:true,code:BLOCKED_EXTERNAL_DEPENDENCY,reason:"Production adapter unavailable: "+name});
}
export function productionWorker(name,adapter){
 const invoke=requireProductionAdapter(name,adapter);
 return async ctx=>{
  const result=await invoke(ctx);
  if(result?.blocked) return result;
  if(!result?.artifact) return {blocked:true,code:BLOCKED_EXTERNAL_DEPENDENCY,reason:name+" returned no production artifact"};
  return result;
 };
}
