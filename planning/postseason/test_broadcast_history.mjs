#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const broadcast=JSON.parse(fs.readFileSync(path.join(dir,'CHAMPIONSHIP_ISLAND_BROADCAST_HERITAGE_2015_2026.proposal.json'),'utf8'));
const tests=[];
function test(label,fn){fn();tests.push(label);}
test('All eleven historical editions have distinct coverage states',()=>{
 assert.equal(broadcast.years.length,11);
 assert.deepEqual(broadcast.years.map(x=>x.year),Array.from({length:11},(_,i)=>2015+i));
 assert.equal(new Set(broadcast.years.map(x=>x.era_status)).size,11);
});
test('Old seasons do not pretend contemporary screens were always present',()=>{
 assert.match(broadcast.years[0].coverage_heritage_proposal,/No historical digital footage asserted/);
 assert.match(broadcast.years[1].coverage_heritage_proposal,/not asserted/);
 assert.match(broadcast.years.find(x=>x.year===2018).coverage_heritage_proposal,/modern retrospectives/);
});
test('Professional present-era multi-camera coverage is explicit',()=>{
 assert.match(broadcast.years.find(x=>x.year===2025).coverage_heritage_proposal,/Multi-camera/);
 assert.ok(broadcast.technical_doctrine.physical_components.includes('central certified-results studio'));
 assert.ok(broadcast.technical_doctrine.physical_components.includes('site-wide public large screens'));
});
test('Every round has the correct number of separately staffed event feeds',()=>{
 assert.equal(broadcast.venue_unit_packages.QF.feeds,3);
 assert.equal(broadcast.venue_unit_packages.SF.feeds,2);
 assert.equal(broadcast.venue_unit_packages.FINAL.feeds,1);
 assert.ok(broadcast.venue_unit_packages.FINAL.camera_tasks.some(x=>x.includes('memorial')));
});
test('Mainland distribution remains unresolved, not magically instant',()=>{
 assert.equal(broadcast.technical_doctrine.distribution_to_mainland.state,'HOLD_WORLD_TECH');
 assert.ok(broadcast.technical_doctrine.distribution_to_mainland.not_authorized.includes('satellites'));
});
test('Memorial and official results protections remain separate',()=>{
 assert.ok(broadcast.technical_doctrine.governance.some(x=>x.includes('Official ESPN result')));
 assert.ok(broadcast.technical_doctrine.governance.some(x=>x.includes('Michael Farrell')));
});
test('The 2026 edition has no future outcome or predetermined finalists',()=>{
 assert.equal(broadcast.current_2026.season,2026);
 assert.equal(broadcast.current_2026.outcomes,null);
 assert.equal(broadcast.current_2026.finalists,null);
 assert.equal(broadcast.current_2026.champion,null);
 assert.match(broadcast.current_2026.release_gate,/WORLD_TECH/);
});
test('No false globally promoted technology claim',()=>{
 assert.equal(broadcast.status,'FOUNDER_F08_AUTHORIZED_CREATIVE_DIRECTION_TECH_CANON_HELD');
 assert.ok(broadcast.technical_doctrine.governance.some(x=>x.includes('No global modernity override')));
});
console.log(JSON.stringify({status:'PASS',tests:tests.length,season_coverage:11,modern2026_winners:0,checks:tests},null,2));
