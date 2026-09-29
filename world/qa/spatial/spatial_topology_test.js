const fs = require("fs");
const path = require("path");

const f = JSON.parse(fs.readFileSync(path.join(__dirname, "spatial_topology_fixture.json"), "utf8"));
const zones = new Set(f.zones);
const edges = new Set();
for (const [a,b] of f.adjacency) {
  if (!zones.has(a) || !zones.has(b)) throw new Error("Adjacency references unknown zone");
  edges.add([a,b].sort().join("|"));
}
for (const r of f.routes) {
  if (!zones.has(r.from) || !zones.has(r.to)) throw new Error(`Route ${r.id} unknown endpoint`);
  if (r.band === "REGIONAL" && !edges.has([r.from,r.to].sort().join("|"))) {
    throw new Error(`Route ${r.id} claims REGIONAL but zones are not adjacent`);
  }
}
if (f.owners.length !== 12) throw new Error("Expected 12 owner domains");
for (const o of f.owners) if (!zones.has(o.zone)) throw new Error(`Owner ${o.id} unknown zone`);

let badCaught = 0;
for (const x of f.bad_fixtures) {
  let invalid = false;
  if (!zones.has(x.from) || !zones.has(x.to)) invalid = true;
  else if (x.kind === "route_nonadjacent_claimed_regional" && !edges.has([x.from,x.to].sort().join("|"))) invalid = true;
  if (invalid) badCaught++;
}
if (badCaught !== f.bad_fixtures.length) throw new Error("Known-bad fixtures not all detected");

console.log("WORLD_SPATIAL_TOPOLOGY: PASS");
console.log(`zones=${f.zones.length} adjacency=${f.adjacency.length} routes=${f.routes.length} owners=${f.owners.length} bad_detected=${badCaught}`);
