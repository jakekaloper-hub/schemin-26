import test from "node:test";
import assert from "node:assert/strict";
import {createAudioCapabilityAdapter,AUDIO_CODES} from "../src/audio-capability-adapter.js";

test("blocks when no audio provider is wired",async()=>{
  const invoke=createAudioCapabilityAdapter(null);
  const result=await invoke({operation:"generate_speech",text:"hello"});
  assert.equal(result.blocked,true);
  assert.equal(result.code,AUDIO_CODES.NOT_WIRED);
});

test("blocks operations the provider does not declare",async()=>{
  const invoke=createAudioCapabilityAdapter({
    id:"test",
    operations:["generate_speech"],
    invoke:async()=>({artifact:{kind:"audio"}})
  });
  const result=await invoke({operation:"transcribe"});
  assert.equal(result.code,AUDIO_CODES.UNSUPPORTED);
});

test("requires verified consent before voice cloning",async()=>{
  const invoke=createAudioCapabilityAdapter({
    id:"test",
    operations:["clone_voice"],
    boundedFilesystem:true,
    invoke:async()=>({artifact:{kind:"voice-profile"}})
  });
  const result=await invoke({operation:"clone_voice",referenceAudioPath:"ref.wav"});
  assert.equal(result.code,AUDIO_CODES.CONSENT_REQUIRED);
});

test("requires provider-enforced filesystem bounds for file-shaped traffic",async()=>{
  const invoke=createAudioCapabilityAdapter({
    id:"test",
    operations:["transcribe"],
    invoke:async()=>({artifact:{kind:"transcript"}})
  });
  const result=await invoke({operation:"transcribe",audioPath:"clip.wav"});
  assert.equal(result.code,AUDIO_CODES.FILE_BOUNDARY_REQUIRED);
});

test("blocks an unhealthy provider",async()=>{
  const invoke=createAudioCapabilityAdapter({
    id:"test",
    operations:["generate_speech"],
    healthCheck:async()=>({ok:false,reason:"backend offline"}),
    invoke:async()=>({artifact:{kind:"audio"}})
  });
  const result=await invoke({operation:"generate_speech",text:"hello"});
  assert.equal(result.code,AUDIO_CODES.UNHEALTHY);
  assert.match(result.reason,/offline/);
});

test("passes a safe supported request through to the provider",async()=>{
  const invoke=createAudioCapabilityAdapter({
    id:"local-audio",
    operations:["generate_speech"],
    healthCheck:async()=>({ok:true}),
    invoke:async request=>({artifact:{kind:"audio",provider:request.providerId}})
  });
  const result=await invoke({operation:"generate_speech",text:"Schemin"});
  assert.deepEqual(result,{artifact:{kind:"audio",provider:"local-audio"}});
});
