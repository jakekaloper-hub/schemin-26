#!/usr/bin/env node
/**
 * Built-in tooling only. Validates the generated offline exhibit is source-backed,
 * interactive JS parses and no remote or premature release is embedded.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const html=fs.readFileSync(path.join(dir,'CHAMPIONSHIP_ISLAND_PREVIEW.html'),'utf8');
const template=fs.readFileSync(path.join(dir,'index.template.html'),'utf8');
const source=JSON.parse(fs.readFileSync(path.resolve(dir,'..','INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json'),'utf8'));
const dataPart=html.match(/<script id="island-data" type="application\/json">([\s\S]*?)<\/script>/);
assert.ok(dataPart,'Offline exhibit missing data binding');
const model=JSON.parse(dataPart[1]);
const tests=[];
const test=(n,f)=>{f();tests.push(n);};

test('Exhibit reads all eleven years and no future winner',()=>{
 assert.equal(model.obstacles.families.length,12);
 assert.equal(model.obstacles.obstacles.length,120);
 assert.equal(Object.keys(model.physicsProfiles).length,6);
 assert.equal(model.material.years.length,11);
 assert.equal(model.bindings.proposals.length,56);
 assert.equal(model.material.perimeter_ruins.length,9);
 assert.equal(model.ceremonial.ceremonies.length,56);
 assert.equal(model.spatial.scene_packets.length,56);
 assert.equal(model.spatial.diagram_units,'CURRENT_ATLAS_PREVIEW_DISPLAY_PIXELS');
 assert.equal(model.impacts.traces.length,56);
 assert.equal(model.soloScenes.cards.length,56);
 assert.equal(model.bodyEffects.games.length,56);

 assert.equal(model.broadcast.years.length,11);
 assert.match(model.broadcast.years[0].coverage_heritage_proposal,/No historical digital footage asserted/);
 assert.equal(model.schema,'schemin.championship-island-static-exhibit.v1');
 assert.equal(model.editorial_state,'NONCANON_PRODUCTION_PREVIEW_NOT_ATLAS');
 assert.deepEqual(model.cardsAnnual.map(x=>x.season),Array.from({length:11},(_,i)=>2015+i));
 assert.ok(!model.cardsAnnual.some(x=>x.season===2026));
 assert.equal(model.cards.length,56);
});
test('Matchup facts and three-stage storyboards preserve identical provenance',()=>{
 const byId=new Map(source.cards.map(x=>[x.card_id,x]));
 for(const card of model.cards) {
   const known=byId.get(card.card_id);assert.ok(known);
   assert.deepEqual(card.verified,known.verified);
   assert.deepEqual(card.beat_sequence,known.beat_sequence);
   assert.equal(card.creative_status,'NONCANON_WORKSHOP_OUTPUT');
   assert.equal(card.beat_sequence.length,3);
 }
});
test('Only one permanent championship venue across the archive',()=>{
 const finals=model.cards.filter(c=>c.round==='FINAL');
 assert.equal(finals.length,11);
 assert.ok(finals.every(c=>c.venue.name==='Last Field'));
});
test('Modern seven-entrant round count and beach arithmetic remain unspoiled',()=>{
 const old=model.cardsAnnual.filter(x=>x.season>=2021);
 assert.equal(old.length,5);
 assert.ok(old.every(x=>x.contender_berths===7 && x.bye_slots.length===1));
 assert.ok(old.every(x=>x.beginning_beach_population===5 && x.post_final_nonchampion_population===11));
});
test('Schematic map contains 23 source nodes and 45 planned links',()=>{
 assert.equal(model.topology.nodes.length,23);
 assert.equal(model.topology.edges.length,45);
 assert.ok(model.topology.nodes.every(n=>n.coordinates===null));
 assert.ok(model.topology.edges.every(e=>e.status==='PLANNING_ONLY'));
});
test('Ceremonial draw, personal-stage scripts and permanent traces render as original fiction',()=>{
 assert.ok(html.includes('CEREMONIAL DRAW'));
 assert.ok(html.includes('PERMANENT ISLAND TRACE'));
 assert.ok(html.includes('PERSONAL PHYSICAL CONSEQUENCES'));
 assert.ok(model.soloScenes.cards.every(c=>c.acts.every(a=>a.solo_contender_A.personally_competes&&a.solo_contender_B.personally_competes)));
 assert.equal(model.impacts.annual_states.at(-1).cumulative_traces_at_close,56);
});
test('Searchable challenges and historic scar registry are present',()=>{
 assert.ok(html.includes('id="family-picker"'));
 assert.ok(html.includes('id="challenge-search"'));
 assert.ok(html.includes("id='trial-venue'"));
 assert.ok(html.includes("id='trial-year'"));
 assert.ok(html.includes('id="ruins-list"'));
 assert.ok(html.includes('renderChallenges()'));
 assert.ok(html.includes('renderRuins()'));
 assert.ok(html.includes('ALTERNATE INKLINGS OBSTACLE'));
});
test('Physical staging controls are fully sourced and require both actor lanes',()=>{
 assert.ok(html.includes('renderStagingPreview'));
 assert.ok(html.includes('Play all stages'));
 assert.ok(html.includes('aria-pressed'));
 assert.ok(model.spatial.scene_packets.every(p=>p.stage_axes.length===3));
 assert.ok(model.spatial.scene_packets.every(p=>p.stage_axes.every(x=>x.personally_performed)));
 assert.ok(model.spatial.scene_packets.every(p=>p.route_access.includes('contender')&&p.route_access.includes('broadcast')));
});
test('Client code parses without external JS imports',()=>{
 const all=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)];
 assert.equal(all.length,2);
 const client=all.at(-1)[1];
 assert.doesNotThrow(()=>new Function(client));
 assert.ok(client.includes('createElementNS'));
 assert.ok(client.includes("addEventListener('click'"));
 assert.ok(!/<script[^>]*src=/i.test(html));
 assert.ok(!/<iframe/i.test(html));
 assert.ok(!/\bfetch\s*\(/.test(client));
});
test('Interactive controls are keyboard-accessible and responsive',()=>{
 for(const id of ['#atlas','#history','#grounds','#beach','#memorial','#future'])assert.ok(html.includes(id.slice(1)));
 assert.ok(html.includes('aria-label="Choose historical season"'));
 assert.ok(html.includes("addEventListener('keydown'"));
 assert.ok(html.includes('@media(max-width:700px)'));
 assert.ok(html.includes('prefers-reduced-motion'));
});
test('Memorial, island canon and historical owner cautions stay visible',()=>{
 assert.ok(html.includes('Michael Farrell'));
 assert.ok(html.includes('The source archive does not establish the precise date'));
 assert.ok(html.includes('not a measured Atlas coordinate'));
 assert.ok(html.includes('Fictional Championship Island concept'));
 assert.ok(html.includes('PR #322'));
});
test('Build output is exactly template plus escaped source payload',()=>{
 const slotCount=template.split('__ISLAND_DATA__').length-1;
 assert.equal(slotCount,1);
 const json=JSON.stringify(model).replace(/</g,'\\u003c').replace(/>/g,'\\u003e').replace(/&/g,'\\u0026').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029');
 assert.equal(html,template.replace('__ISLAND_DATA__',json));
});
console.log(JSON.stringify({status:'PASS',tests:tests.length,checks:tests},null,2));
