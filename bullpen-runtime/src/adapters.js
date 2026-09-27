export function requireProductionAdapter(name,adapter){if(!adapter)return async()=>{throw new Error(`BLOCKED_EXTERNAL_ADAPTER: ${name}`)};return adapter}
