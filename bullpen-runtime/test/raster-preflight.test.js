import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, symlinkSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createHash } from "node:crypto";
import { deflateSync } from "node:zlib";
import { inspectPngFile } from "../src/raster-preflight.js";

const sha = bytes => createHash("sha256").update(bytes).digest("hex");
const crc = bytes => {
 let c = 0xffffffff;
 for (const byte of bytes) {
  c ^= byte;
  for (let b=0; b<8; b++) c = (c >>> 1) ^ (c & 1 ? 0xedb88320 : 0);
 }
 return (c ^ 0xffffffff) >>> 0;
};
const chunk = (name, data) => {
 const type = Buffer.from(name, "ascii"), body = Buffer.concat([type,data]);
 const out = Buffer.alloc(12+data.length);
 out.writeUInt32BE(data.length,0); body.copy(out,4);out.writeUInt32BE(crc(body),8+data.length);
 return out;
};
const png = (width,height) => {
 const ihdr=Buffer.alloc(13);
 ihdr.writeUInt32BE(width,0); ihdr.writeUInt32BE(height,4);
 ihdr[8]=8;ihdr[9]=2; // RGB8 non-interlaced
 const pixelRows=Buffer.alloc(height*(1+width*3)); // Filter=0 and zero pixels
 return Buffer.concat([
  Buffer.from([137,80,78,71,13,10,26,10]),
  chunk("IHDR",ihdr), chunk("IDAT",deflateSync(pixelRows)),chunk("IEND",Buffer.alloc(0))
 ]);
};
const dir=mkdtempSync(join(tmpdir(),"schemin-raster-test-"));
const good=png(1080,1920), filename="P10.png";
writeFileSync(join(dir,filename),good);

test("accepts exact verified 1080x1920 PNG as technical preflight only",()=>{
 const r=inspectPngFile({root:dir,relativePath:filename,expectedSha256:sha(good)});
 assert.equal(r.state,"RASTER_PREFLIGHT_PASSED");
 assert.deepEqual([r.width,r.height],[1080,1920]);
 assert.equal(r.sha256,sha(good));
 assert.equal(r.character_qa_approved,false);
 assert.equal(r.publication_eligible,false);
});
test("fails closed on wrong memo geometry",()=>{
 const r=inspectPngFile({root:dir,relativePath:filename,expectedSha256:sha(good),width:941,height:1672});
 assert.equal(r.state,"RASTER_PREFLIGHT_BLOCKED");
 assert.equal(r.code,"GEOMETRY_MISMATCH");
});
test("fails closed on a changed file hash or corrupted PNG chunk",()=>{
 const altered=Buffer.from(good); altered[altered.length-10]^=1;
 writeFileSync(join(dir,"altered.png"),altered);
 const hash=inspectPngFile({root:dir,relativePath:filename,expectedSha256:"f".repeat(64)});
 assert.equal(hash.code,"SOURCE_HASH_MISMATCH");
 const corrupt=inspectPngFile({root:dir,relativePath:"altered.png",expectedSha256:sha(altered)});
 assert.equal(corrupt.code,"INVALID_PNG");
});
test("rejects missing, traversal and symlink files",()=>{
 const missing=inspectPngFile({root:dir,relativePath:"absent.png",expectedSha256:sha(good)});
 assert.equal(missing.state,"RASTER_PREFLIGHT_BLOCKED");
 assert.equal(inspectPngFile({root:dir,relativePath:"../secret.png",expectedSha256:sha(good)}).code,"UNSAFE_ASSET_PATH");
 symlinkSync(join(dir,filename),join(dir,"link.png"));
 assert.equal(inspectPngFile({root:dir,relativePath:"link.png",expectedSha256:sha(good)}).code,"UNSAFE_ASSET_PATH");
});
test("cannot treat a spoofed IHDR-only PNG as a real raster",()=>{
 const ihdr=Buffer.alloc(13);ihdr.writeUInt32BE(1080,0);ihdr.writeUInt32BE(1920,4);ihdr[8]=8;ihdr[9]=2;
 const fake=Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk("IHDR",ihdr),chunk("IEND",Buffer.alloc(0))]);
 writeFileSync(join(dir,"fake.png"),fake);
 assert.equal(inspectPngFile({root:dir,relativePath:"fake.png",expectedSha256:sha(fake)}).code,"INVALID_PNG");
});
