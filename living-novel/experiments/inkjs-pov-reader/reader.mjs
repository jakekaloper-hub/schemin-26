import {availablePOVs,createReader,readToChoice,bookmark,restore} from './engine.mjs';
import source from './story.ink?raw';
const container=document.querySelector('#characters'),storyEl=document.querySelector('#story'),choicesEl=document.querySelector('#choices'),status=document.querySelector('#status'),save=document.querySelector('#save');let story,pov;
function render(){const section=readToChoice(story);storyEl.textContent+=section.text;choicesEl.replaceChildren();for(const c of section.choices){const button=document.createElement('button');button.textContent=c.text;button.onclick=()=>{story.ChooseChoiceIndex(c.index);render()};choicesEl.append(button)}save.disabled=false;}
function start(id){pov=id;story=createReader(source,pov);storyEl.textContent='';status.textContent='Reading: '+availablePOVs.find(c=>c.id===id).team;render();}
for(const c of availablePOVs){const b=document.createElement('button');b.textContent=c.team+(c.implemented?'':' — not available');b.disabled=!c.implemented;b.onclick=()=>start(c.id);container.append(b);}
save.onclick=()=>{try{localStorage.setItem('schemin-pov-prototype-v1',bookmark(story,pov));status.textContent='Bookmark saved locally';}catch(e){status.textContent='Save failed: '+e.message;}};
document.querySelector('#resume').onclick=()=>{try{const data=localStorage.getItem('schemin-pov-prototype-v1');if(!data)throw new Error('No bookmark');({story,pov}=restore(source,data));storyEl.textContent='';status.textContent='Resumed: '+availablePOVs.find(c=>c.id===pov).team;render();}catch(e){status.textContent='Resume failed: '+e.message;}};
