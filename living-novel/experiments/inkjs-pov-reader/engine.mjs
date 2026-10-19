import * as inkjs from 'inkjs/full';
import characters from './characters.json' with { type: 'json' };
const { Compiler } = inkjs;
const MAX_BOOKMARK_BYTES = 1024 * 1024;
const MAX_TRANSCRIPT_CHARS = 100_000;
export const event = Object.freeze({id:'W3-2026-OBIWAN-TDS',season:2026,week:3,status:'NONCANON illustrative scene; historic score fixture',score:Object.freeze({'CHAR-JAKE-KALOPER':136.73,'CHAR-PHILLIP-PITTS':114.50})});
const paths=Object.freeze({'CHAR-JAKE-KALOPER':'obiwan','CHAR-PHILLIP-PITTS':'snake'});
export const availablePOVs=Object.freeze(characters.map(c=>Object.freeze({...c,implemented:Object.hasOwn(paths,c.id)})));
export function createReader(source,pov){
  if(typeof pov!=='string'||!Object.hasOwn(paths,pov))throw new Error('POV not implemented');
  const story=new Compiler(source).Compile();
  if(!story)throw new Error('ink compile failed');
  story.ChoosePathString(paths[pov]);
  return story;
}
export function readToChoice(story){let text='';while(story.canContinue)text+=story.Continue();return {text,choices:story.currentChoices.map((c,index)=>({index,text:c.text}))};}
export function bookmark(story,pov,transcript=''){
  if(typeof pov!=='string'||!Object.hasOwn(paths,pov))throw new Error('Unknown POV');
  if(typeof transcript!=='string'||transcript.length>MAX_TRANSCRIPT_CHARS)throw new Error('Invalid bookmark transcript');
  const serialized=JSON.stringify({schema:1,eventId:event.id,pov,transcript,storyState:story.state.ToJson()});
  if(BufferByteLength(serialized)>MAX_BOOKMARK_BYTES)throw new Error('Bookmark exceeds size limit');
  return serialized;
}
function BufferByteLength(value){return new TextEncoder().encode(value).byteLength;}
export function restore(source,serialized){
  if(typeof serialized!=='string'||BufferByteLength(serialized)>MAX_BOOKMARK_BYTES)throw new Error('Invalid bookmark size');
  let saved;
  try{saved=JSON.parse(serialized);}catch{throw new Error('Invalid bookmark JSON');}
  if(!saved||typeof saved!=='object'||Array.isArray(saved)||saved.schema!==1||saved.eventId!==event.id||
     typeof saved.pov!=='string'||!Object.hasOwn(paths,saved.pov))throw new Error('Invalid bookmark identity');
  if(typeof saved.transcript!=='string'||saved.transcript.length>MAX_TRANSCRIPT_CHARS)throw new Error('Invalid bookmark transcript');
  if(typeof saved.storyState!=='string'||saved.storyState.length===0)throw new Error('Invalid bookmark state');
  const story=createReader(source,saved.pov);
  try{story.state.LoadJson(saved.storyState);}catch{throw new Error('Invalid bookmark state');}
  return {story,pov:saved.pov,transcript:saved.transcript};
}
