export const AUDIO_CODES=Object.freeze({
  NOT_WIRED:"AUDIO_PROVIDER_NOT_WIRED",
  UNSUPPORTED:"AUDIO_OPERATION_UNSUPPORTED",
  CONSENT_REQUIRED:"AUDIO_VOICE_CONSENT_REQUIRED",
  FILE_BOUNDARY_REQUIRED:"AUDIO_FILE_BOUNDARY_REQUIRED",
  UNHEALTHY:"AUDIO_PROVIDER_UNHEALTHY"
});

export const AUDIO_OPERATIONS=Object.freeze([
  "generate_speech",
  "transcribe",
  "dub",
  "design_voice",
  "clone_voice"
]);

const fileShapedFields=["audioPath","referenceAudioPath","outputPath"];

function blocked(code,reason){return {blocked:true,code,reason};}

export function createAudioCapabilityAdapter(provider){
  if(!provider){
    return async()=>blocked(AUDIO_CODES.NOT_WIRED,"No Schemin audio provider is configured.");
  }
  if(typeof provider.invoke!=="function") throw new TypeError("audio provider requires invoke(request)");
  const operations=new Set(Array.isArray(provider.operations)?provider.operations:[]);
  const unknown=[...operations].filter(op=>!AUDIO_OPERATIONS.includes(op));
  if(unknown.length) throw new Error("audio provider declares unsupported operation: "+unknown[0]);

  return async request=>{
    const operation=request?.operation;
    if(!operations.has(operation)){
      return blocked(AUDIO_CODES.UNSUPPORTED,"Audio provider does not support operation: "+String(operation));
    }
    if(operation==="clone_voice"&&request?.consentVerified!==true){
      return blocked(AUDIO_CODES.CONSENT_REQUIRED,"Voice cloning requires explicit verified consent.");
    }
    const hasFileShape=fileShapedFields.some(field=>typeof request?.[field]==="string"&&request[field].length>0)
      || request?.outputMode==="files" || request?.outputMode==="both";
    if(hasFileShape&&provider.boundedFilesystem!==true){
      return blocked(AUDIO_CODES.FILE_BOUNDARY_REQUIRED,"File-shaped audio traffic requires a provider-enforced bounded filesystem.");
    }
    if(typeof provider.healthCheck==="function"){
      const health=await provider.healthCheck();
      if(health?.ok!==true){
        return blocked(AUDIO_CODES.UNHEALTHY,health?.reason||"Audio provider health check failed.");
      }
    }
    return provider.invoke({...request,providerId:provider.id||"external-audio-provider"});
  };
}
