import test from "node:test";
import assert from "node:assert/strict";
import {consumeStrengthenRoute,CORE_STRENGTHEN_LIFECYCLE} from "../src/strengthen-adapter.js";

test("accepts the canonical Bullpen strengthen lifecycle",()=>{
  const adapted=consumeStrengthenRoute({
    command:"strengthen",
    lifecycle:["research","plan","execute","test","audit","learn"],
    directors:["the_closer","the_architect","the_umpire"]
  },{
    projectGates:{
      research:["league evidence provenance"],
      audit:["Schemin canon and publication regression"]
    }
  });
  assert.deepEqual(adapted.coreLifecycle,CORE_STRENGTHEN_LIFECYCLE);
  assert.equal(adapted.project,"schemin-26");
  assert.deepEqual(adapted.projectGates.audit,["Schemin canon and publication regression"]);
  assert.equal(Object.isFrozen(adapted.coreLifecycle),true);
  assert.equal(Object.isFrozen(adapted.projectGates),true);
  assert.equal(Object.isFrozen(adapted.projectGates.audit),true);
});

test("rejects a reordered or incomplete lifecycle",()=>{
  assert.throws(()=>consumeStrengthenRoute({
    command:"strengthen",
    lifecycle:["research","execute","plan","test","audit","learn"]
  }),/lifecycle mismatch/);
  assert.throws(()=>consumeStrengthenRoute({
    command:"strengthen",
    lifecycle:["research","plan","execute","test","audit"]
  }),/lifecycle mismatch/);
});

test("project gates can strengthen phases but cannot create new core phases",()=>{
  assert.throws(()=>consumeStrengthenRoute({
    command:"strengthen",
    lifecycle:["research","plan","execute","test","audit","learn"]
  },{projectGates:{publish:["release"]}}),/unknown strengthen phase/);
});
