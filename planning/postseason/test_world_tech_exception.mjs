#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const worldLaw=fs.readFileSync(path.resolve(root,'../../world/atlas/phase-1/MODERNITY_LAYER_CANDIDATE_REGISTRY_V1.md'),'utf8');
const proposal=fs.readFileSync(path.join(root,'ISLAND_WORLD_TECH_EXCEPTION_RATIFICATION_V1.md'),'utf8');
const broadcast=JSON.parse(fs.readFileSync(path.join(root,'CHAMPIONSHIP_ISLAND_BROADCAST_HERITAGE_2015_2026.proposal.json'),'utf8'));
const atlas=JSON.parse(fs.readFileSync(path.join(root,'ATLAS_NEUTRAL_CAUSEWAY_SITING_HYPOTHESIS_V1.proposal.json'),'utf8'));
const checks=[];function t(label,cb){cb();checks.push(label)}
t('Active Atlas modernity policy still rejects unrestricted modern electronic equipment',()=>{
 assert.match(worldLaw,/pre-modern Schemin technology ceiling/i);
 assert.match(worldLaw,/electronic arcade/);
 assert.match(worldLaw,/modern NASCAR/);
 assert.match(worldLaw,/modern firearms paintball/);
});
t('Founder modern broadcast is expressly isolated from the mainland premodern law',()=>{
 assert.match(proposal,/Localized, League-neutral event-technology enclave/);
 assert.match(proposal,/does not.*?imply satellite television/is);
 assert.match(proposal,/WORLD OS RATIFICATION NOT YET GRANTED/);
});
t('Early historical island media episodes do not assert electronic camera archive as fact',()=>{
 for(const x of broadcast.years.filter(x=>x.year<=2016))assert.match(x.coverage_heritage_proposal,/No historical digital footage asserted|not asserted/);
 assert.match(proposal,/2015–2016.*?heralds/is);
});
t('Modern fixtures in recent seasons explicitly require World Tech ratification',()=>{
 assert.match(proposal,/2025.*WORLD\/TECH EXCEPTION REQUIRED/);
 assert.match(proposal,/2026.*WORLD\/TECH EXCEPTION REQUIRED/);
 assert.match(broadcast.status,/WORLD_TECH_CANON_HELD/);
});
t('The island remains owner-neutral and physically unpromoted while technology is unresolved',()=>{
 assert.equal(atlas.hypothesis.public_mainland_gate.owner_character_id,null);
 assert.equal(atlas.canon_promotion,false);
 assert.deepEqual(atlas.world_writes,[]);
});
t('No manufactured World technology or historical 2026 winner is emitted by this exception',()=>{
 assert.match(proposal,/NO global premodern law changed/);
 assert.match(proposal,/no actual electricity created/i);
 assert.equal(broadcast.current_2026.champion,null);
});
console.log(JSON.stringify({status:'PASS',checks:checks.length,release:'WORLD_TECH_PENDING',world_mutations:0,details:checks},null,2));
