# Schemin '26 — Audio Capability Adapter V1

**Status:** CANDIDATE / PROVIDER NOT WIRED  
**Owner:** Architect + Setup Man  
**Independent gates:** Warden + Umpire

## Purpose

Define a provider-neutral, fail-closed seam for future Schemin audio production without making any third-party voice application part of Schemin or Bullpen Core.

Candidate uses include:
- Weekly Memo narration or audio recap;
- Living Novel narration / audiobook experiments;
- scene or dialogue reads;
- transcription of authorized league audio;
- dubbing or trailer-production experiments.

This contract does **not** assert that an audio provider is installed, configured, healthy, or production-approved.

## External research provenance

The immediate architecture donor is `debpalash/VoiceStudio`, inspected at commit `0834c8be28460fc4e0518bdb31eb57c494b253b2`.

Useful patterns observed:
- a local-first audio runtime exposed through MCP/API;
- explicit provider health checks;
- per-client/agent voice identity;
- file outputs that avoid pushing large audio payloads through model context;
- a bounded filesystem as a security boundary for file-shaped traffic;
- separate speech, transcription, dubbing, voice-design, and voice-cloning operations.

VoiceStudio is AGPL-3.0. No VoiceStudio implementation is copied into Schemin. This adapter is an independent provider-neutral interface informed by those architectural lessons.

Additional Bullpen-level research into `mattpocock/skills` and `github/awesome-copilot` reinforces the separation between reusable capability, orchestration, provider/tool adapters, and project-local workflows.

## Executable seam

Implementation: `bullpen-runtime/src/audio-capability-adapter.js`

Supported operation vocabulary:
- `generate_speech`
- `transcribe`
- `dub`
- `design_voice`
- `clone_voice`

A provider advertises only the operations it actually supports. The adapter blocks unsupported operations rather than silently substituting behavior.

## Fail-closed requirements

1. **No provider:** return `AUDIO_PROVIDER_NOT_WIRED`.
2. **Unsupported operation:** return `AUDIO_OPERATION_UNSUPPORTED`.
3. **Voice cloning:** require `consentVerified === true`; otherwise return `AUDIO_VOICE_CONSENT_REQUIRED`.
4. **File-shaped traffic:** require the provider to declare and enforce a bounded filesystem; otherwise return `AUDIO_FILE_BOUNDARY_REQUIRED`.
5. **Provider health:** when a health check exists, it must pass immediately before invocation; otherwise return `AUDIO_PROVIDER_UNHEALTHY`.
6. **No fake production:** provider responses still flow through the normal Bullpen runtime artifact/gate contract before a production workflow can claim success.

The current adapter does not independently resolve symlinks or enforce an OS-level sandbox. `boundedFilesystem:true` is therefore a provider contract, not proof by itself. A real provider integration must demonstrate that confinement with provider-specific tests before promotion.

## Voice identity and consent

Schemin character identity is not permission to clone a real person's voice.

Any real-person voice cloning or reference-audio use requires explicit authorization for that source material. Character voices may instead be synthetic/designed voices without impersonating a real participant.

Per-agent or per-character voice binding, if introduced later, must be stored as project-local presentation metadata. It must not mutate character canon, narrative truth, or Bullpen Director identity.

## Promotion path

A concrete provider remains NOT_WIRED until all of the following are evidenced:
- provider installation/configuration is explicitly authorized;
- health check and supported-operation discovery are executable;
- file-boundary behavior is tested;
- consent handling is tested where cloning/reference audio exists;
- produced audio becomes a real runtime artifact;
- an independent QA gate verifies the artifact;
- licensing and distribution obligations are reviewed for the actual provider/model;
- rollback/removal is documented.

Until then, this V1 contract is an integration seam and safety boundary, not a production audio system.
