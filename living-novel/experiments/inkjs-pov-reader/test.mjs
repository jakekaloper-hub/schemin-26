import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {availablePOVs,createReader,readToChoice,bookmark,restore,event} from './engine.mjs';
const source=readFileSync(new URL('./story.ink',import.meta.url),'utf8');
test('twelve unique canonical IDs and two available routes',()=>{assert.equal(availablePOVs.length,12);assert.equal(new Set(availablePOVs.map(c=>c.id)).size,12);assert.equal(availablePOVs.filter(c=>c.implemented).length,2);});
test('historical score consistency across both POVs',()=>{for(const id of ['CHAR-JAKE-KALOPER','CHAR-PHILLIP-PITTS']){const story=createReader(source,id);const o=readToChoice(story);assert.match(o.text,/136\.73/);assert.match(o.text,/114\.50/);assert.equal(o.choices.length,2);story.ChooseChoiceIndex(0);assert.match(readToChoice(story).text,/bridge remained/i);}assert.ok(Object.isFrozen(event.score));});
test('bookmark restoration retains choices',()=>{const pov='CHAR-PHILLIP-PITTS';const story=createReader(source,pov);readToChoice(story);const restored=restore(source,bookmark(story,pov));assert.equal(restored.pov,pov);assert.equal(restored.story.currentChoices.length,2);restored.story.ChooseChoiceIndex(1);assert.match(readToChoice(restored.story).text,/A score could decide/);});
test('unapproved POV fails closed',()=>assert.throws(()=>createReader(source,'CHAR-KEVIN-ZEEK'),/not implemented/));
test('bookmark identity and spoiler boundary reject forged or unsupported POVs',()=>{
 const story=createReader(source,'CHAR-JAKE-KALOPER');readToChoice(story);
 const valid=JSON.parse(bookmark(story,'CHAR-JAKE-KALOPER','Visible passage'));
 for(const payload of [
  {...valid,pov:'CHAR-KEVIN-ZEEK'},
  {...valid,pov:'__proto__'},
  {...valid,eventId:'W4-FUTURE'},
  {...valid,schema:2},
  {...valid,transcript:null},
  {...valid,transcript:'future'.repeat(20000)},
  {...valid,storyState:{unexpected:'object'}},
  {...valid,storyState:''}
 ])assert.throws(()=>restore(source,JSON.stringify(payload)),/Invalid bookmark/);
 assert.throws(()=>restore(source,'not json'),/Invalid bookmark JSON/);
 assert.throws(()=>restore(source,JSON.stringify(valid)+' '.repeat(1100000)),/Invalid bookmark size/);
 assert.throws(()=>bookmark(story,'CHAR-JAKE-KALOPER','x'.repeat(100001)),/Invalid bookmark transcript/);
});

test('reader identities match canonical character registry on repository checkout',()=>{
 const registry=readFileSync(new URL('../../../canon/characters/CHARACTER_REGISTRY.yaml',import.meta.url),'utf8');
 const canonical=[...registry.matchAll(/^  - \{id: (CHAR-[A-Z-]+), owner: [^,]+, team: (?:"([^"]+)"|'([^']+)'|([^,}]+)),/gm)].map(m=>({id:m[1],team:(m[2]??m[3]??m[4]).trim()}));
 assert.equal(canonical.length,12,'canonical registry must resolve twelve entries');
 assert.deepEqual(availablePOVs.map(({id,team})=>({id,team})),canonical,'reader roster drifted from canonical registry');
});

test('locked Week 3 reader event includes verified provenance and safe route classifications',()=>{
 assert.equal(event.status,'FACT_LOCKED_READER_SAMPLE');
 assert.equal(event.winner,'CHAR-JAKE-KALOPER');
 assert.equal(event.provenance.factLock,'memo-os/week-3/WEEK_3_FACT_LOCK_V1.md');
 assert.equal(event.provenance.providerSnapshot,'memo-os/week-3/WEEK_3_FINAL_EVIDENCE_SNAPSHOT_06.md');
 const manifest=JSON.parse(readFileSync(new URL('./scenes.generated.json',import.meta.url),'utf8'));
 assert.equal(manifest.classification,'NONCANON_EXPERIMENT');
 assert.equal(manifest.eventId,event.id);
 assert.equal(manifest.routes.length,2);
 assert.deepEqual(manifest.routes.map(r=>r.pov).sort(),['CHAR-JAKE-KALOPER','CHAR-PHILLIP-PITTS'].sort());
 for(const route of manifest.routes){
  assert.equal(route.status,'ILLUSTRATIVE_NOT_APPROVED');
  assert.equal(route.knowledgeCutoff,'2026-W03-POSTFINAL');
  assert.equal(route.worldLocation,'UNVERIFIED_SCENE_PROPOSAL');
 }
});
