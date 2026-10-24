import {readFileSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';
import assert from 'node:assert/strict';
const dir=dirname(fileURLToPath(import.meta.url)), repo=resolve(dir,'../../..');
const read=p=>readFileSync(resolve(repo,p),'utf8');
const registryPath='canon/characters/CHARACTER_REGISTRY.yaml';
const factPath='memo-os/week-3/WEEK_3_FACT_LOCK_V1.md';
const snapshotPath='memo-os/week-3/WEEK_3_FINAL_EVIDENCE_SNAPSHOT_06.md';
const characters=[...read(registryPath).matchAll(/^  - \{id: (CHAR-[A-Z-]+), owner: [^,]+, team: (?:"([^"]+)"|'([^']+)'|([^,}]+)),/gm)]
 .map(m=>({id:m[1],team:(m[2]??m[3]??m[4]).trim()}));
assert.equal(characters.length,12,'expected twelve canon principals');
assert.equal(new Set(characters.map(x=>x.id)).size,12,'duplicate canonical IDs');
const fact=read(factPath),snapshot=read(snapshotPath);
assert.match(fact,/Status: LOCKED for Week 3 Memo production/);
const factMatch=fact.match(/^- ObiWan Jacoby ([0-9]+\.[0-9]{2}) def Three Dreaded Snake ([0-9]+\.[0-9]{2})\.$/m);
assert.ok(factMatch,'missing locked matchup fact');
const [,obiwan,snake]=factMatch;
assert.ok(snapshot.includes('Three Dreaded Snake '+snake+' - ObiWan Jacoby '+obiwan+'; winner ObiWan Jacoby.'),'Flaim/ESPN final snapshot disagrees');
const data={
 schema:1,id:'W3-2026-OBIWAN-TDS',season:2026,week:3,
 status:'FACT_LOCKED_READER_SAMPLE',winner:'CHAR-JAKE-KALOPER',
 score:{'CHAR-JAKE-KALOPER':Number(obiwan),'CHAR-PHILLIP-PITTS':Number(snake)},
 provenance:{factLock:factPath,providerSnapshot:snapshotPath},
 caveat:'Historical matchup only; linked Ink prose is NONCANON.'
};
const scenes={
 schema:1,classification:'NONCANON_EXPERIMENT',eventId:data.id,
 routes:[
 {pov:'CHAR-JAKE-KALOPER',knot:'obiwan',status:'ILLUSTRATIVE_NOT_APPROVED',source:'living-novel/experiments/inkjs-pov-reader/story.ink',knowledgeCutoff:'2026-W03-POSTFINAL',worldLocation:'UNVERIFIED_SCENE_PROPOSAL'},
 {pov:'CHAR-PHILLIP-PITTS',knot:'snake',status:'ILLUSTRATIVE_NOT_APPROVED',source:'living-novel/experiments/inkjs-pov-reader/story.ink',knowledgeCutoff:'2026-W03-POSTFINAL',worldLocation:'UNVERIFIED_SCENE_PROPOSAL'}
 ]};
assert.ok(read(scenes.routes[0].source).includes('=== obiwan ==='));
assert.ok(read(scenes.routes[1].source).includes('=== snake ==='));
const story=read(scenes.routes[0].source);
assert.ok(story.includes(obiwan)&&story.includes(snake),'Ink narrative score drift');
const files={'characters.json':characters,'event.generated.json':data,'scenes.generated.json':scenes};
let drift=0;
for(const [name,obj] of Object.entries(files)){
 const path=resolve(dir,name),out=JSON.stringify(obj,null,2)+'\n';
 if(process.argv.includes('--check')){if(readFileSync(path,'utf8')!==out){console.error(name+' is stale');drift++;}}
 else writeFileSync(path,out);
}
if(drift)process.exitCode=1;
