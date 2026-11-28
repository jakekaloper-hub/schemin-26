import fs from 'node:fs';
import {inflateSync,deflateSync} from 'node:zlib';
import {createHash} from 'node:crypto';
const sig=Buffer.from([137,80,78,71,13,10,26,10]);
export function decodePng(path){
 const bytes=fs.readFileSync(path);
 if(!bytes.subarray(0,8).equals(sig))throw Error('NOT_PNG');
 let w,h,bits,type,interlace;
 const chunks=[];let end=false;
 for(let at=8;at+12<=bytes.length;){
  const len=bytes.readUInt32BE(at),name=bytes.toString('ascii',at+4,at+8);
  if(len>bytes.length-at-12)throw Error('PNG_CHUNK_TRUNCATED');
  const data=bytes.subarray(at+8,at+8+len);
  if(name==='IHDR'){w=data.readUInt32BE(0);h=data.readUInt32BE(4);bits=data[8];type=data[9];interlace=data[12];}
  if(name==='IDAT')chunks.push(data);
  at+=12+len;if(name==='IEND'){end=true;break;}
 }
 if(!end||!w||!h||w>4096||h>4096||bits!==8||![2,6].includes(type)||interlace!==0||!chunks.length)throw Error('UNSUPPORTED_PNG_FORMAT');
 const ch=type===2?3:4,stride=w*ch,raw=inflateSync(Buffer.concat(chunks));
 if(raw.length!==(stride+1)*h)throw Error('INVALID_PNG_SCANLINE_LENGTH');
 const pixels=Buffer.alloc(w*h*ch);
 for(let y=0;y<h;y++){
  const type=raw[y*(stride+1)],start=y*stride,off=y*(stride+1)+1;
  for(let x=0;x<stride;x++){
   const left=x>=ch?pixels[start+x-ch]:0,up=y?pixels[start-stride+x]:0,ul=y&&x>=ch?pixels[start-stride+x-ch]:0;
   let p=0;
   if(type===1)p=left;
   else if(type===2)p=up;
   else if(type===3)p=(left+up)>>1;
   else if(type===4){const a=left+up-ul,da=Math.abs(a-left),db=Math.abs(a-up),dc=Math.abs(a-ul);p=da<=db&&da<=dc?left:db<=dc?up:ul;}
   else if(type!==0)throw Error('UNSUPPORTED_PNG_FILTER');
   pixels[start+x]=(raw[off+x]+p)&255;
  }
 }
 return {width:w,height:h,channels:ch,pixels,sha256:createHash('sha256').update(bytes).digest('hex')};
}
export function roiDifference(a,b,rect,threshold=12){
 if(a.width!==b.width||a.height!==b.height||a.channels!==b.channels)throw Error('PNG_DIMENSION_MISMATCH');
 const [x,y,w,h]=rect;
 if(![x,y,w,h].every(Number.isInteger)||x<0||y<0||w<=0||h<=0||x+w>a.width||y+h>a.height||threshold<0||threshold>255)throw Error('INVALID_ROI');
 let changed=0,mean=0,peak=0;
 for(let row=y;row<y+h;row++)for(let col=x;col<x+w;col++){
  const i=(row*a.width+col)*a.channels;
  const delta=(Math.abs(a.pixels[i]-b.pixels[i])+Math.abs(a.pixels[i+1]-b.pixels[i+1])+Math.abs(a.pixels[i+2]-b.pixels[i+2]))/3;
  mean+=delta;peak=Math.max(peak,delta);if(delta>threshold)changed++;
 }
 return {rect,changed,total:w*h,fraction:changed/(w*h),meanAbsoluteDelta:mean/(w*h),peakDelta:peak};
}

/** Fixed screen-pixel regions were identified by direct inspection of three
 * genuine, independently hash-pinned Apple M3 Pro / Three-WebGL2 frames.
 * Water-focused regions are not water-only semantic segmentation. */
export const reviewRegions=Object.freeze({
 temple:{placeId:'LOC-TDS-WATERFALL-TEMPLE',water:[620,340,34,145],static:[705,350,100,70]},
 jackson:{placeId:'LOC-COUNTRY-CLUB-JACKSON',water:[665,118,65,130],static:[632,400,120,68]},
 'mud-dogs':{placeId:'LOC-MUD-DOGS-SWAMP',water:[690,560,180,55],static:[200,490,170,110]}
});
function crc32(data){
 let c=0xffffffff;
 for(const byte of data){c^=byte;for(let j=0;j<8;j++)c=(c>>>1)^((c&1)?0xedb88320:0);}
 return (c^0xffffffff)>>>0;
}
function pngChunk(name,data){
 const nameBytes=Buffer.from(name,'ascii'),head=Buffer.alloc(8);
 head.writeUInt32BE(data.length,0);nameBytes.copy(head,4);
 const crc=Buffer.alloc(4);crc.writeUInt32BE(crc32(Buffer.concat([nameBytes,data])),0);
 return Buffer.concat([head,data,crc]);
}
/** Deterministic no-credit/zero-dependency PNG derived strictly from actual
 * camera-held moving frames. Black = unchanged, amber = per-pixel RGB difference;
 * color is diagnostic markup, not a newly rendered environment or a water mask. */
export function encodeRegionDifference(a,b,rect){
 roiDifference(a,b,rect);
 const [x,y,w,h]=rect,raw=Buffer.alloc((w*4+1)*h);
 for(let row=0;row<h;row++)for(let col=0;col<w;col++){
  const index=((y+row)*a.width+(x+col))*a.channels,off=row*(w*4+1)+1+col*4;
  const delta=(Math.abs(a.pixels[index]-b.pixels[index])+Math.abs(a.pixels[index+1]-b.pixels[index+1])+Math.abs(a.pixels[index+2]-b.pixels[index+2]))/3;
  const strength=Math.max(0,Math.min(255,Math.round((delta-3)*5)));
  raw[off]=strength?Math.min(255,64+strength):9;
  raw[off+1]=strength?Math.min(230,Math.round(strength*.72)):19;
  raw[off+2]=strength?Math.round(strength*.16):22;
  raw[off+3]=255;
 }
 const ihdr=Buffer.alloc(13);ihdr.writeUInt32BE(w,0);ihdr.writeUInt32BE(h,4);ihdr[8]=8;ihdr[9]=6;
 return Buffer.concat([sig,pngChunk('IHDR',ihdr),pngChunk('IDAT',deflateSync(raw,{level:9})),pngChunk('IEND',Buffer.alloc(0))]);
}
export function produceWaterEvidence(captureDir,outputDir){
 if(fs.existsSync(outputDir))throw Error('EVIDENCE_FOLDER_ALREADY_EXISTS');
 const original=JSON.parse(fs.readFileSync(captureDir+'/manifest.json','utf8'));
 if(original.sourceRevision!=='0736e071e4fcd3c70deea60e565293ccfde2230b'||
 original.status!=='CANDIDATE_NOT_APPROVED'||original.publicationAuthorized!==false||
 original.renderer!=='three-webgl2'||original.weatherStatus!=='GLOBAL_CALM'||
 original.ordinaryWaterAdvanced!==true||original.pausedSceneHashesEqual!==true||
 original.captures.length!==12)throw Error('UNVERIFIED_PHYSICAL_CAPTURE_MANIFEST');
 const records=[];
 for(const [slug,region] of Object.entries(reviewRegions)){
  const files=['01-moving','02-moving','03-paused-a','04-paused-b'].map(s=>slug+'-'+s+'.png');
  const captures=files.map(f=>original.captures.find(c=>c.file===f&&c.placeId===region.placeId));
  if(captures.some(c=>!c||c.width!==1440||c.height!==813))throw Error('INVALID_CAPTURE_MAPPING');
  const frames=files.map((f,i)=>{const frame=decodePng(captureDir+'/'+f);if(frame.sha256!==captures[i].sha256)throw Error('CAPTURE_HASH_MISMATCH');return frame;});
  const moving=roiDifference(frames[0],frames[1],region.water);
  const staticControl=roiDifference(frames[0],frames[1],region.static);
  const paused=roiDifference(frames[2],frames[3],region.water);
  if(!(moving.changed>0&&staticControl.changed===0&&paused.changed===0&&
  captures[1].waterTime>captures[0].waterTime&&captures[2].waterTime===captures[3].waterTime))throw Error('WATER_REGION_MOTION_EVIDENCE_INCOMPLETE');
  const diff=encodeRegionDifference(frames[0],frames[1],region.water);
  records.push({slug,placeId:region.placeId,waterRegion:region.water,stableControlRegion:region.static,
   moving,staticControl,paused,
   originalFiles:files.map((file,i)=>({file,sha256:captures[i].sha256})),
   derivedFile:slug+'-water-region-rgb-difference.png',
   derivedSha256:createHash('sha256').update(diff).digest('hex'),derivedBytes:diff.length,derivedDimensions:[region.water[2],region.water[3]],
   bytes:diff});
 }
 fs.mkdirSync(outputDir,{recursive:false});
 for(const record of records)fs.writeFileSync(outputDir+'/'+record.derivedFile,record.bytes);
 const manifest={
  status:'CANDIDATE_NOT_APPROVED',publicationAuthorized:false,
  purpose:'PHYSICAL_GPU_FIXED_CAMERA_WATER_FOCUSED_REGION_RGB_DIFFERENCES_NOT_WATER_ONLY_SEGMENTATION',
  sourceRevision:original.sourceRevision,captureManifest:'../gpu-wetlands-exact-0736e071-20261123/manifest.json',
  renderer:original.renderer,gpu:original.gpu,syntheticScenario:original.syntheticScenario,
  weatherStatus:original.weatherStatus,ordinaryWaterAdvanced:original.ordinaryWaterAdvanced,
  notes:'Fixed-camera physical-GPU moving frames show color changes in preselected water-focused regions while nearby control terrain/masonry samples remain pixel-identical; explicit pause is pixel-identical. Motion is bounded evidence of the displayed water-area optics, not exclusive water-pixel attribution, independent art approval, or real weather.',
  sites:records.map(({bytes,...r})=>r)
 };
 fs.writeFileSync(outputDir+'/manifest.json',JSON.stringify(manifest,null,2)+'\n');
 return manifest;
}
if(process.argv[1]?.endsWith('/water-pixel-evidence.mjs')&&process.argv.length===4){
 const manifest=produceWaterEvidence(process.argv[2],process.argv[3]);
 console.log(JSON.stringify({status:'WATER_REGION_DIAGNOSTIC_COMPLETE',sites:manifest.sites.map(s=>({slug:s.slug,movingChanged:s.moving.changed,staticChanged:s.staticControl.changed,pausedChanged:s.paused.changed,derivedSha256:s.derivedSha256}))}));
}
