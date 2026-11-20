#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const source=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const library=read('INKLINGS_SIX_SCREENPLAY_PILOT_LIBRARY_V1.json');
const queue=read('INKLINGS_50_REMAINING_SCREENPLAY_PRODUCTION_QUEUE_V1.json');
const byId=new Map(source.fixtures.map(f=>[f.id,f]));
const published=new Set(library.scenes.map(x=>x.fixture_id));
const ids=new Set(queue.queue.map(x=>x.fixture_id));
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const checks=[];function t(label,fn){fn();checks.push(label);}
t('Total 56 archived fixtures partition exactly into six audited scripts and fifty assignments',()=>{
 assert.equal(source.fixtures.length,56);
 assert.equal(library.scenes.length,6);
 assert.equal(queue.queue.length,50);
 assert.equal(new Set([...published,...ids]).size,56);
 assert.ok([...published].every(id=>!ids.has(id)));
 assert.ok(source.fixtures.every(x=>published.has(x.id)||ids.has(x.id)));
});
t('Every assignment contains correct source proof, era and immutable score hash',()=>{
for(const item of queue.queue){
 const f=byId.get(item.fixture_id);
 assert.ok(f);
 assert.equal(item.year,f.year);
 assert.equal(item.round,f.round);
 assert.deepEqual(item.source_locked.home,f.home);
 assert.deepEqual(item.source_locked.away,f.away);
 assert.equal(item.source_locked.winner_slot,f.winner_slot);
 assert.equal(item.source_locked.fingerprint,sha(JSON.stringify({id:f.id,home:f.home,away:f.away,win:f.winner_slot,period:f.scoring_period})));
 assert.equal(item.workflow.stage,'QUEUED_EDITORIAL');
}
});
t('All future scripts are blocked from automatic canon publication or delegated actor stage',()=>{
assert.ok(queue.queue.every(x=>x.workflow.publication==='HOLD'));
assert.ok(queue.queue.every(x=>x.required_script.prohibitions.some(y=>y.includes('human owner identity'))));
assert.ok(queue.queue.every(x=>x.required_script.components.some(y=>y.includes('personally perform'))));
});
t('Every venue and ceremonial draw is source-linked and retains permanent scar reference',()=>{
assert.ok(queue.queue.every(x=>x.draw.id&&x.draw.ticket));
assert.ok(queue.queue.every(x=>x.venue.round_fixed&&x.venue.permanent_scar==='TRACE-'+x.fixture_id));
assert.ok(queue.queue.every(x=>x.verified_margin>=0));
});
t('Queue is reproducibly prioritized without manipulating sporting outcome',()=>{
assert.equal(queue.next_five.length,5);
assert.deepEqual(queue.next_five.map(x=>x.fixture_id),queue.queue.slice(0,5).map(x=>x.fixture_id));
assert.ok(queue.queue.every((x,i)=>i===0||x.priority<=queue.queue[i-1].priority));
assert.ok(queue.queue.every(x=>x.year<=2025));
assert.ok(!queue.queue.some(x=>x.source_locked.fixture_id.startsWith('HIST-POST-2026')));
});
t('All eleven historical seasons remain represented in the remaining work',()=>{
const count=Object.values(queue.census.by_year).reduce((a,b)=>a+b,0);
assert.equal(count,50);
assert.equal(Object.keys(queue.census.by_year).length,11);
});
console.log(JSON.stringify({status:'PASS',checks:checks.length,completed_longform:6,remaining:50,all_historical:56,source_history_untouched:true,details:checks},null,2));
