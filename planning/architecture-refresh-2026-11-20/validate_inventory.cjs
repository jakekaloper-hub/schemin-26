// Snapshot-only check: does not certify production logic, canon, or independent QA.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const dir = __dirname;
const inv = JSON.parse(fs.readFileSync(path.join(dir,'AUDIT_INVENTORY_V1.json'),'utf8'));
const route = JSON.parse(fs.readFileSync(path.join(dir,'REVIEW_QUEUE_V1.json'),'utf8'));
const distinct = items => new Set(items).size === items.length;
assert.equal(inv.source.truncated, false);
assert.equal(inv.source.tracked_files, inv.files.length);
assert.equal(inv.source.tracked_directories, inv.folders.length);
assert.equal(inv.source.tracked_paths, inv.files.length + inv.folders.length);
assert.equal(inv.domains.length, 20);
assert.equal(route.domain_workstreams.length, 20);
assert.equal(route.directors.length, 18);
assert.equal(route.consultant_lenses.length, 3);
assert.ok(distinct(inv.files));
assert.ok(distinct(inv.folders.map(x=>x.path)));
assert.ok(distinct(inv.domains.map(x=>x.path)));
assert.ok(distinct(route.domain_workstreams.map(x=>x.path)));
assert.ok(distinct(route.directors.map(x=>x.id)));
assert.deepEqual(
 new Set(route.domain_workstreams.map(x=>x.path)),
 new Set(inv.domains.map(x=>x.path))
);
assert.ok(inv.domains.every(d=>d.entrypoint === null || d.entrypoint_present === true));
assert.ok(inv.folders.every(d=>d.review_status === 'DISCOVERED_NOT_TESTED'));
assert.ok(route.domain_workstreams.every(d=>d.stage === 'QUEUED' && d.complete === false));
assert.ok(route.directors.every(d=>d.participation === 'ASSIGNED_NOT_RUN'));
console.log('PASS derived snapshot accounting; no active/accepted status claims.');
