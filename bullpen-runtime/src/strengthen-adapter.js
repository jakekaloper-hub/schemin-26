export const CORE_STRENGTHEN_LIFECYCLE=Object.freeze([
  "research","plan","execute","test","audit","learn"
]);

function assertCanonicalLifecycle(lifecycle){
  if(!Array.isArray(lifecycle)) throw new Error("canonical strengthen route requires lifecycle");
  if(lifecycle.length!==CORE_STRENGTHEN_LIFECYCLE.length) throw new Error("canonical strengthen lifecycle mismatch");
  for(let i=0;i<CORE_STRENGTHEN_LIFECYCLE.length;i++){
    if(lifecycle[i]!==CORE_STRENGTHEN_LIFECYCLE[i]) throw new Error("canonical strengthen lifecycle mismatch");
  }
}

function normalizeProjectGates(projectGates={}){
  const normalized={};
  for(const [phase,gates] of Object.entries(projectGates)){
    if(!CORE_STRENGTHEN_LIFECYCLE.includes(phase)) throw new Error("project gate targets unknown strengthen phase: "+phase);
    const list=Array.isArray(gates)?gates:[gates];
    if(!list.length||list.some(g=>typeof g!=="string"||!g.trim())) throw new Error("project gates must be non-empty strings");
    normalized[phase]=Object.freeze([...list]);
  }
  return Object.freeze(normalized);
}

export function consumeStrengthenRoute(canonicalRoute,{projectGates={}}={}){
  if(!canonicalRoute||canonicalRoute.command!=="strengthen") throw new Error("expected canonical strengthen route");
  assertCanonicalLifecycle(canonicalRoute.lifecycle);
  return Object.freeze({
    project:"schemin-26",
    command:"strengthen",
    coreLifecycle:Object.freeze([...CORE_STRENGTHEN_LIFECYCLE]),
    projectGates:normalizeProjectGates(projectGates),
    directors:Object.freeze(Array.isArray(canonicalRoute.directors)?[...canonicalRoute.directors]:[]),
    source:"jakekaloper-hub/bullpen"
  });
}
