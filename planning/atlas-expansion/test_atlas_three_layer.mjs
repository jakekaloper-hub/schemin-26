import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,"../..");
const load=p=>JSON.parse(fs.readFileSync(path.join(root,p),"utf8"));
const draft=load("planning/atlas-expansion/ATLAS_THREE_LAYER_DOSSIERS_V1.json");
const proposals=load("planning/atlas-expansion/ATLAS_EXPANSION_44_CANDIDATES_V1.json");
const world=load("world/data/locations.json");
const existing=load("world/data/atlas_location_candidates.json");
const owners=load("world/data/owner_domains.json");
const topology=load("planning/postseason/ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json");
const venues=load("planning/postseason/ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json");
const encounters=load("planning/postseason/HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json");
const supersession=load("planning/postseason/ATLAS_LAST_FIELD_SUPERSESSION_PACKET_V1.json");
const recordsByNs=Object.groupBy(draft.records,d=>d.namespace);
const getSet=(a)=>new Set(a);
const exactIds=(actual,expected,label)=>assert.deepEqual([...actual].sort(),[...expected].sort(),label);
test("147 unique identifiers with exact namespace/source ID coverage",()=>{
 assert.equal(draft.records.length,147);
 assert.equal(getSet(draft.records.map(d=>d.id)).size,147);
 exactIds((recordsByNs.ACTIVE_LOC||[]).map(d=>d.id),world.locations.map(l=>l.id),"active");
 exactIds((recordsByNs.EDITORIAL_CAND||[]).map(d=>d.id),existing.candidates.map(l=>l.id),"existing editorials");
 exactIds((recordsByNs.POSTSEASON_TOPOLOGY_NODE||[]).map(d=>d.id),topology.nodes.map(l=>l.id),"island network");
 exactIds((recordsByNs.POSTSEASON_ISLAND_SITE_CAND||[]).map(d=>d.id),venues.sites.map(l=>l.id),"island arenas");
 exactIds((recordsByNs.NEW_EXPANSION_CAND||[]).map(d=>d.id),proposals.proposals.map(l=>l.id),"new proposals");
});
test("all 147 have 3 substantial different review layers",()=>{
 for(const d of draft.records){
  const l=Object.values(d.depth_layers).map(x=>x.source_aware_depth);
  assert.equal(l.length,3,d.id);
  assert(l.every(x=>typeof x==="string"&&x.length>=175),d.id+" thin layer");
  assert.equal(new Set(l).size,3,d.id+" duplicate layer");
  assert(d.provenance.length>0,d.id+" lacks provenance");
 }
});
test("preserve existing source statuses and rejected candidates",()=>{
 for(const d of recordsByNs.ACTIVE_LOC){
  assert.equal(d.source_record_status,world.locations.find(x=>x.id===d.id).canon_status);
 }
 for(const d of recordsByNs.EDITORIAL_CAND){
  const source=existing.candidates.find(x=>x.id===d.id);
  assert.equal(d.source_record_status,source.lifecycle_status);
  if(source.lifecycle_status==="REJECTED_FOR_DRIFT")assert.match(d.depth_layers["3_HISTORICAL_STRATIGRAPHY_AND_POSTSEASON"].source_aware_depth,/REJECTED/);
 }
 assert.equal(world.locations.length,23);
});
test("44 new sites: 3 per domain, 8 cross-domain, four island service candidates",()=>{
 assert.equal(proposals.proposals.length,44);
 const p=proposals.proposals;
 const validIds=new Set([...world.locations.map(x=>x.id),...topology.nodes.map(x=>"POST-NODE:"+x.id)]);
 for(const x of p){
  assert(x.id.startsWith("CAND-XP-"));
  assert(validIds.has(x.anchor),x.id+" invalid anchor");
  assert.equal(x.canon_status,"NEW_PROPOSAL_UNAPPROVED");
  assert.equal(x.period_placement,"UNDATED_PROPOSED_FICTION");
 }
 for(const o of owners.domains){
  assert.equal(p.filter(x=>x.team_slot_2026===o.team_id).length,3,o.character_id);
 }
 assert.equal(p.filter(x=>x.team_slot_2026===null).length,8);
 assert.equal(p.filter(x=>x.anchor.startsWith("POST-NODE:")).length,4);
});
test("historical 67 team-slot qualifications from actual 11 year brackets",()=>{
 assert.equal(encounters.annual.length,11);
 const yearly=encounters.annual;
 const count=yearly.reduce((n,y)=>n+y.entrants.length,0);
 assert.equal(count,67);
 for(const r of recordsByNs.NEW_EXPANSION_CAND.filter(x=>x.slot_history)){
  const actual=yearly.filter(y=>y.entrants.includes(r.slot_history.slot)).map(y=>y.year);
  assert.deepEqual(r.slot_history.playoff_years,actual,r.id);
  assert.equal(r.slot_history.identity_limit.includes("DOES NOT PROVE"),true);
 }
});
test("historical 56 fixtures source locked; proposed Island venue attribution is separate",()=>{
 assert.equal(encounters.fixtures.length,56);
 const allAssigned=[];
 for(const d of recordsByNs.POSTSEASON_ISLAND_SITE_CAND){
  const refs=d.historic_sports_facts_with_fictional_island_assignment;
  const original=venues.sites.find(x=>x.id===d.id);
  assert.equal(refs.length,original.fixtures_count);
  exactIds(refs.map(x=>x.id),original.historic_fixture_ids,d.id);
  for(const f of refs){
   const truth=encounters.fixtures.find(x=>x.id===f.id);
   assert.equal(f.winner_slot,truth.winner_slot);
   assert.equal(f.home.points,truth.home.points);
   assert.equal(f.away.points,truth.away.points);
   assert.equal(f.venue_status,"PROPOSED_ORIGINAL_FICTION");
   allAssigned.push(f.id);
  }
 }
 exactIds(allAssigned,encounters.fixtures.map(f=>f.id),"all fixtures assigned exactly once");
});
test("Last Field conflict explicitly unresolved and geography not silently mutated",()=>{
 assert.equal(supersession.current.zone_ids[0],"REG-CENTRAL-BASIN");
 assert.equal(supersession.proposed.zone_ids[0],"REG-INNER-SEA-LITTORAL");
 assert.equal(supersession.proposed.new_active_location_id,null);
 assert.equal(supersession.no_mutation.location_writeback,false);
 assert.equal(draft.status,"EDITORIAL_REVIEW_OUTPUT__NOT_ACTIVE_CANON");
});
test("topology mismatch reported accurately without rewriting upstream",()=>{
 assert.equal(draft.audit.topology_edge_count_actual,topology.edges.length);
 assert.equal(draft.audit.topology_edge_count_declared,topology.checks.edge_count);
 assert.equal(draft.audit.topology_edge_count_disagreement,topology.edges.length!==topology.checks.edge_count);
 if(draft.audit.topology_edge_count_disagreement)console.warn("REVIEW HOLD: topology edges declared",topology.checks.edge_count,"but actual",topology.edges.length);
});
