# Native image-generation incident — Bullpen investigation

Date: 2026-10-22, America/New_York.
Status: REPRODUCED_EXTERNAL_TOOL_FAILURE / NOT RESOLVED.

## Executed investigation

The existing Bullpen command compiler compiled:
- /bullpen incident Diagnose native image-generation runtime HTTP400 unknown reasoning parameter; trace schema boundary, preserve zero incremental spend, no false recovery claims.
- /bullpen debug Isolate native provider payload from website implementation; minimal supported request and independent acceptance.

Incident route: Setup Man, Groundskeeper, Umpire, Bookkeeper, Scout. Debug route: Setup Man, Architect.
These are real command-compilation receipts; they do not establish that persistent authenticated Directors ran a hosted remediation service.

## Minimal reproduction

The built-in image tool was called with only its required prompt argument:
```json
{"prompt":"Original Schemin website entrance illustration: an empty stone overlook above forested mountain ridges at dawn, a closed ledger on the terrace, mist, hand-painted oil and gouache, pine-green shadows and ivory light. Wide composition with quiet space on the left for website text. No people, animals, text, logos, or watermark."}
```

It returned:
```text
HTTP 400 Bad Request
Unknown parameter: 'reasoning'.
type: invalid_request_error
param: null
code: unknown_parameter
```

No optional background, reference, model, or reasoning argument was supplied. No image bytes or request ID were returned.

## Findings and limits

- Failure reproduced independently of the website build and optional image-tool arguments.
- The exposed image-tool schema offers prompt, reference inputs, and transparency; it offers no setting to remove a hidden reasoning field or select/reset the internal provider.
- Plugin management exposes plugin discovery/permissions/removal, not repair of this built-in tool.
- Official Images API reference does not list reasoning as an image-generation body parameter:
  https://developers.openai.com/api/reference/resources/images/methods/generate
- Inference: an internal request adaptation or provider compatibility fault is plausible. The exact injection point, endpoint, deployed model, and responsible service cannot be established from available diagnostics.
- No engine, website, or Bullpen repository edit has been shown to repair this request. No speculative patch was made.
- No alternate paid API was invoked, account settings changed, or support report sent.

## Required recovery evidence

The platform integration owner must inspect the constructed request and remove unsupported parameters or route it to a compatible endpoint, then a native image call must return a real image. A minimal successful image and the actual homepage commission must both be visually checked before resuming the full batch.

No repair, recovered capability, generated artwork, visual acceptance, or deployment is claimed. All49 commissions remain unfinished. A separate ChatGPT image session is a possible workaround, not a verified fix of this session.
