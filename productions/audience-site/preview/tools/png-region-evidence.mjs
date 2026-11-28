/** Dependency-free lossless RGB PNG reader for source-pinned GPU evidence.
 * This deliberately does not derive scene identity from rendered colors.
 * Bounding-box results are screen-region observations, not water-mesh isolation.
 */
import assert from 'node:assert/strict';
import {inflateSync} from 'node:zlib';

const PNG_SIGNATURE=Buffer.from([137,80,78,71,13,10,26,10]);
const MAX_PIXELS=4096*4096;

export function decodeRgbPng(bytes){
 assert.ok(Buffer.isBuffer(bytes)&&bytes.subarray(0,8).equals(PNG_SIGNATURE),'INVALID_PNG_SIGNATURE');
 let offset=8,header=null,parts=[],ended=false;
 while(offset<bytes.length){
  assert.ok(offset+12<=bytes.length,'TRUNCATED_PNG_CHUNK');
  const size=bytes.readUInt32BE(offset),type=bytes.toString('ascii',offset+4,offset+8);
  assert.ok(size<=bytes.length-offset-12,'TRUNCATED_PNG_DATA');
  const chunk=bytes.subarray(offset+8,offset+8+size);
  if(type==='IHDR'){
   assert.ok(header===null&&size===13,'INVALID_PNG_HEADER');
   const width=chunk.readUInt32BE(0),height=chunk.readUInt32BE(4),bitDepth=chunk[8],colorType=chunk[9];
   assert.ok(width>0&&height>0&&width*height<=MAX_PIXELS,'PNG_SIZE_UNSUPPORTED');
   assert.ok(bitDepth===8&&(colorType===2||colorType===6)&&chunk[10]===0&&chunk[11]===0&&chunk[12]===0,'PNG_FORMAT_UNSUPPORTED');
   header={width,height,channels:colorType===2?3:4};
  }else if(type==='IDAT'){
   assert.ok(header!==null,'PNG_MISSING_HEADER');parts.push(chunk);
  }else if(type==='IEND'){
   assert.equal(size,0,'INVALID_PNG_END');ended=true;assert.equal(offset+12,bytes.length,'PNG_TRAILING_DATA');break;
  }else if((type.charCodeAt(0)&32)===0){
   throw Error('PNG_CRITICAL_CHUNK_UNSUPPORTED: '+type);
  }
  offset+=size+12;
 }
 assert.ok(header&&parts.length>0&&ended,'PNG_INCOMPLETE');
 const {width,height,channels}=header,stride=width*channels;
 const raw=inflateSync(Buffer.concat(parts),{maxOutputLength:height*(stride+1)});
 assert.equal(raw.length,height*(stride+1),'PNG_SCANLINE_SIZE_MISMATCH');
 const pixels=Buffer.alloc(height*stride);
 for(let y=0;y<height;y++){
  const src=y*(stride+1),dst=y*stride,filter=raw[src];
  assert.ok(filter>=0&&filter<=4,'PNG_FILTER_UNSUPPORTED');
  for(let x=0;x<stride;x++){
   const v=raw[src+1+x],left=x>=channels?pixels[dst+x-channels]:0,up=y>0?pixels[dst-stride+x]:0,
     topLeft=y>0&&x>=channels?pixels[dst-stride+x-channels]:0;
   let prediction=0;
   if(filter===1)prediction=left;
   else if(filter===2)prediction=up;
   else if(filter===3)prediction=Math.floor((left+up)/2);
   else if(filter===4){
    const p=left+up-topLeft,dl=Math.abs(p-left),du=Math.abs(p-up),dt=Math.abs(p-topLeft);
    prediction=dl<=du&&dl<=dt?left:du<=dt?up:topLeft;
   }
   pixels[dst+x]=(v+prediction)&255;
  }
 }
 return {...header,pixels};
}

/** Rectangle uses half-open [x0,x1) × [y0,y1) pixel bounds.
 * A changed pixel needs at least one RGB channel to differ by minDelta.
 */
export function changedPixels(before,after,rectangle,{minDelta=2}={}){
 assert.ok(before&&after&&before.width===after.width&&before.height===after.height&&before.channels===after.channels,'PNG_FRAME_DIMENSION_MISMATCH');
 assert.ok(Array.isArray(rectangle)&&rectangle.length===4&&rectangle.every(Number.isInteger),'INVALID_PIXEL_REGION');
 const [x0,y0,x1,y1]=rectangle;
 assert.ok(x0>=0&&y0>=0&&x1>x0&&y1>y0&&x1<=before.width&&y1<=before.height,'PIXEL_REGION_OUT_OF_BOUNDS');
 assert.ok(Number.isInteger(minDelta)&&minDelta>=1&&minDelta<=255,'INVALID_PIXEL_THRESHOLD');
 let changed=0;const channels=before.channels;
 for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){
  const index=(y*before.width+x)*channels;
  if([0,1,2].some(c=>Math.abs(before.pixels[index+c]-after.pixels[index+c])>=minDelta))changed++;
 }
 return {changed,total:(x1-x0)*(y1-y0)};
}
