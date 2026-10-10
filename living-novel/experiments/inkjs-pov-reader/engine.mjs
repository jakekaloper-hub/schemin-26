import * as inkjs from 'inkjs/full';
import characters from './characters.json' with { type: 'json' };
const { Compiler } = inkjs;
export const event = Object.freeze({id:'W3-2026-OBIWAN-TDS',season:2026,week:3,status:'NONCANON illustrative scene; historic score fixture',score:Object.freeze({'CHAR-JAKE-KALOPER':136.73,'CHAR-PHILLIP-PITTS':114.50})});
const paths=Object.freeze({'CHAR-JAKE-KALOPER':'obiwan','CHAR-PHILLIP-PITTS':'snake'});
export const availablePOVs=Object.freeze(characters.map(c=>Object.freeze({...c,implemented:!!paths[c.id]})));
export function createReader(source,pov){if(!paths[pov])throw new Error('POV not implemented');const s=new Compiler(source).Compile();if(!s)throw new Error('ink compile failed');s.ChoosePathString(paths[pov]);return s;}
export function readToChoice(story){let text='';while(story.canContinue)text+=story.Continue();return {text,choices:story.currentChoices.map((c,index)=>({index,text:c.text}))};}
export function bookmark(story,pov){if(!paths[pov])throw new Error('Unknown POV');return JSON.stringify({schema:1,eventId:event.id,pov,storyState:story.state.ToJson()});}
export function restore(source,serialized){const b=JSON.parse(serialized);if(b.schema!==1||b.eventId!==event.id||!paths[b.pov])throw new Error('Invalid bookmark identity');const story=createReader(source,b.pov);story.state.LoadJson(b.storyState);return {story,pov:b.pov};}
