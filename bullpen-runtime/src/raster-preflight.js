/**
 * Technical PNG preflight. Validates exact bytes, dimensions and PNG structure,
 * NOT likeness, source authority, artwork quality, or publication eligibility.
 * Uses Node builtins so the zero-incremental-spend production path is portable.
 */
import { createHash } from "node:crypto";
import { lstatSync, readFileSync, realpathSync } from "node:fs";
import { isAbsolute, relative, resolve, sep } from "node:path";
import { inflateSync } from "node:zlib";

const SIGNATURE = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
const SHA_PATTERN = /^[a-f0-9]{64}$/;
const blocked = (code, reason) => ({
  state: "RASTER_PREFLIGHT_BLOCKED", code, reason,
  character_qa_approved: false, publication_eligible: false,
});

function crc32(bytes) {
  let crc = 0xffffffff;
  for (const byte of bytes) {
    crc ^= byte;
    for (let i = 0; i < 8; i++) {
      crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0);
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function validatePng(bytes, width, height) {
  if (bytes.length < 57 || !bytes.subarray(0, 8).equals(SIGNATURE)) throw Error("PNG_SIGNATURE");
  let offset = 8, ihdr = null, ended = false, idat = [];
  while (offset < bytes.length) {
    if (offset + 12 > bytes.length) throw Error("TRUNCATED_CHUNK");
    const length = bytes.readUInt32BE(offset);
    const type = bytes.toString("ascii", offset + 4, offset + 8);
    const end = offset + 12 + length;
    if (end > bytes.length) throw Error("TRUNCATED_CHUNK");
    const payload = bytes.subarray(offset + 8, offset + 8 + length);
    const chunkBody = bytes.subarray(offset + 4, offset + 8 + length);
    if (crc32(chunkBody) !== bytes.readUInt32BE(offset + 8 + length)) throw Error("CRC_MISMATCH");
    if (!ihdr && type !== "IHDR") throw Error("IHDR_NOT_FIRST");
    if (type === "IHDR") {
      if (ihdr || length !== 13) throw Error("INVALID_IHDR");
      const w = payload.readUInt32BE(0), h = payload.readUInt32BE(4);
      if (!w || !h || w !== width || h !== height) throw Error("GEOMETRY_MISMATCH");
      const depth = payload[8], color = payload[9];
      if (depth !== 8 || ![0, 2, 4, 6].includes(color) || payload[10] !== 0 || payload[11] !== 0 || payload[12] !== 0)
        throw Error("UNSUPPORTED_PNG_ENCODING");
      ihdr = {width:w, height:h, channels:({0:1, 2:3, 4:2, 6:4})[color]};
    } else if (type === "IDAT") {
      if (ended) throw Error("IDAT_AFTER_END");
      idat.push(payload);
    } else if (type === "IEND") {
      if (length !== 0 || !idat.length || end !== bytes.length) throw Error("INVALID_IEND");
      ended = true;
    } else if (type !== "PLTE" && /^[A-Z]/.test(type)) {
      throw Error("UNSUPPORTED_CRITICAL_CHUNK");
    }
    offset = end;
  }
  if (!ended || !ihdr || !idat.length) throw Error("MISSING_IMAGE_DATA");
  const rowBytes = 1 + ihdr.width * ihdr.channels;
  const required = rowBytes * ihdr.height;
  if (!Number.isSafeInteger(required) || required > 256*1024*1024) throw Error("RASTER_TOO_LARGE");
  const decoded = inflateSync(Buffer.concat(idat), {maxOutputLength:required+1});
  if (decoded.length !== required) throw Error("RASTER_TRUNCATED");
  for (let row = 0; row < ihdr.height; row++) {
    if (decoded[row * rowBytes] > 4) throw Error("INVALID_SCANLINE_FILTER");
  }
  return ihdr;
}

export function inspectPngFile({root, relativePath, expectedSha256, width=1080, height=1920, maxBytes=64*1024*1024}={}) {
  if (typeof expectedSha256 !== "string" || !SHA_PATTERN.test(expectedSha256)) return blocked("UNTRUSTED_EXPECTED_HASH","Exact expected SHA-256 is required");
  if (!Number.isInteger(width) || !Number.isInteger(height) || width<=0 || height<=0) return blocked("INVALID_GEOMETRY","Positive integer dimensions are required");
  if (typeof root !== "string" || typeof relativePath !== "string" || !root.trim() || !relativePath.trim()
      || isAbsolute(relativePath) || relativePath.split(/[\\/]/).some(p=>!p || p==="." || p==="..")) {
    return blocked("UNSAFE_ASSET_PATH","Relative asset path required within an explicit root");
  }
  try {
    const trustedRoot=realpathSync(root);
    const path=resolve(trustedRoot,relativePath);
    const rel=relative(trustedRoot,path);
    if (!rel || rel.startsWith(".."+sep) || rel==="..") return blocked("UNSAFE_ASSET_PATH","Asset escapes trusted root");
    // No file or intermediate directory may be a symlink.
    let cursor=trustedRoot;
    for (const part of relativePath.split(/[\\/]/)) {
      cursor=resolve(cursor,part);
      if (lstatSync(cursor).isSymbolicLink()) return blocked("UNSAFE_ASSET_PATH","Symlink asset paths are not accepted");
    }
    const stat=lstatSync(path);
    if (!stat.isFile() || stat.size>maxBytes) return blocked("UNSAFE_ASSET_FILE","Expected bounded PNG file");
    const bytes=readFileSync(path), actual=createHash("sha256").update(bytes).digest("hex");
    if (actual !== expectedSha256) return blocked("SOURCE_HASH_MISMATCH","PNG differs from expected bytes");
    try {
      validatePng(bytes,width,height);
    } catch (err) {
      if (err.message==="GEOMETRY_MISMATCH") return blocked("GEOMETRY_MISMATCH","Dimensions differ from locked page geometry");
      return blocked("INVALID_PNG","PNG integrity or decoding failed");
    }
    return {
      state:"RASTER_PREFLIGHT_PASSED",sha256:actual,
      width,height,byte_size:bytes.length,technical_integrity_verified:true,
      character_qa_approved:false,editorial_qa_approved:false,publication_eligible:false,
    };
  } catch {
    return blocked("ASSET_UNAVAILABLE","Asset could not be safely inspected");
  }
}
