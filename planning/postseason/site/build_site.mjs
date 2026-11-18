#!/usr/bin/env node
/**
 * Build a single offline, self-contained Championship Island exhibit.
 * Consumes unpromoted Founder V2 preproduction data only.
 * This does NOT deploy a site or mutate active Atlas world geography.
 *
 * node planning/postseason/site/build_site.mjs [--check]
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const project=path.resolve(dir,'..');
function read(name){return JSON.parse(fs.readFileSync(path.join(project,name),'utf8'));}
const cards=read('INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json');
const sites=read('ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json');
const topology=read('ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json');
const contract=read('POSTSEASON_2026_ISLAND_EVENT_CONTRACT.proposal.json');
const finales=read('INKLINGS_ELEVEN_CHAMPIONSHIP_FINALE_SCRIPTS_V1.proposal.json');
assert.equal(finales.scenes.length,11,'Eleven authored championship scripts required');
assert.ok(finales.scenes.every(x=>{const f=cards.cards.find(c=>c.season===x.year&&c.round==='FINAL');return f && f.verified.winner_slot===x.verified.winner_slot && f.verified.home.points===x.verified.home.points && f.verified.away.points===x.verified.away.points;}),'Finale prose/source mismatch');
assert.equal(cards.cards.length,56,'Must have every historical title-path fixture');
assert.equal(cards.annual.length,11,'Must have eleven complete historical seasons');
assert.equal(cards.cards.reduce((n,c)=>n+c.beat_sequence.length,0),168);
assert.equal(topology.nodes.length,23);
assert.equal(topology.edges.length,45);
assert.equal(sites.sites.length,9);
assert.equal(contract.schedule.qualification_count,7);
assert.equal(contract.schedule.first_round_bye_seed,1);
assert.equal(contract.schedule.reseed,false);
assert.ok(cards.cards.every(c=>c.creative_status==='NONCANON_WORKSHOP_OUTPUT'));
assert.ok(topology.nodes.every(n=>n.coordinates===null));
const years=cards.annual.map(a=>a.season);
assert.deepEqual(years,Array.from({length:11},(_,i)=>2015+i));
const data={schema:'schemin.championship-island-static-exhibit.v1',
  editorial_state:'NONCANON_PRODUCTION_PREVIEW_NOT_ATLAS',
  source_pins:{fact:'ESPN_FLAIM_LEAGUE_1457621_HISTORY',place:'FOUNDER_V2_PROPOSED',release:'BLOCKED_INDEPENDENT_UMPIRE_AND_ATLAS'},
  cardsAnnual:cards.annual,cards:cards.cards,sites,topology,finales:finales.scenes};
const template=fs.readFileSync(path.join(dir,'index.template.html'),'utf8');
assert.equal(template.split('__ISLAND_DATA__').length,2,'Expected exactly one data slot');
const json=JSON.stringify(data).replace(/</g,'\\u003c').replace(/>/g,'\\u003e').replace(/&/g,'\\u0026').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029');
const html=template.replace('__ISLAND_DATA__',json);
assert.ok(html.includes('2026 is not decided.'));
assert.ok(!html.includes('__ISLAND_DATA__'));
assert.ok(!html.match(/<script[^>]*src=/));
assert.ok(!html.includes('http://fonts.googleapis.com'));
const dest=path.join(dir,'CHAMPIONSHIP_ISLAND_PREVIEW.html');
const current=fs.existsSync(dest)?fs.readFileSync(dest,'utf8'):null;
if(process.argv.includes('--check')){
  assert.equal(current,html,'Preview drift; rerun site builder to regenerate');
}else{
  fs.writeFileSync(dest,html,'utf8');
}
console.log(JSON.stringify({status:'PASS',mode:process.argv.includes('--check')?'CHECK':'BUILD',path:path.relative(project,dest),bytes:Buffer.byteLength(html),seasons:years.length,encounters:cards.cards.length,release_status:data.editorial_state,sha256:crypto.createHash('sha256').update(html).digest('hex')}));
