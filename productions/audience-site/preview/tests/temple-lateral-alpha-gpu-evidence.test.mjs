import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';

const dir=new URL('../evidence/gpu-temple-lateral-alpha-20261123/',import.meta.url);
const manifest=JSON.parse(readFileSync(new URL('manifest.json',dir),'utf8'));
const sourceRevision='e57be199638fd3e432fff4493281aae0595d1c12';
const files=[
 ['01-unlabeled-world.png',null],
 ['02-country-club-jackson.png','LOC-COUNTRY-CLUB-JACKSON'],
 ['03-waterfall-temple.png','LOC-TDS-WATERFALL-TEMPLE'],
 ['04-mud-dogs-swamp.png','LOC-MUD-DOGS-SWAMP']
];

test('Original Temple lateral-edge candidate GPU evidence is SHA-checked, source-bound and non-public',()=>{
 assert.equal(manifest.status,'CANDIDATE_NOT_APPROVED');
 assert.equal(manifest.publicationAuthorized,false);
 assert.equal(manifest.renderer,'three-webgl2');
 assert.match(manifest.gpu,/ANGLE .*Apple M3 Pro/);
 assert.equal(manifest.sourceRevision,sourceRevision);
 assert.equal(manifest.sourcesUnchanged,true);
 assert.deepEqual(manifest.captures.map(c=>[c.file,c.placeId]),files);
 for(const entry of manifest.captures){
  const bytes=readFileSync(new URL(entry.file,dir));
  assert.equal(bytes.length,entry.bytes,entry.file);
  assert.equal(createHash('sha256').update(bytes).digest('hex'),entry.sha256,entry.file);
  assert.equal(bytes.toString('ascii',1,4),'PNG');
  assert.equal(bytes.readUInt32BE(16),entry.width);
  assert.equal(bytes.readUInt32BE(20),entry.height);
  assert.deepEqual([entry.width,entry.height],[1440,813]);
  assert.ok(entry.frames>=2,'must be browser-rendered frame');
 }
});
