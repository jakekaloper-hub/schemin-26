# Bullpen Runtime V1

This package converts Bullpen from role-played review language into an executable, fail-closed production contract.

## Non-negotiable rule

A Bullpen role has **not acted** unless a worker invocation produces a recorded artifact. A stage has **not passed** unless its configured gate returns `pass: true`. Missing workers block the job; they are never simulated.

## Canonical Bullpen route adapter

`src/counterweight-adapter.js` consumes route output from canonical `jakekaloper-hub/bullpen`.

It intentionally does **not** copy the 18-Director counterweight registry. It:
- preserves canonical primary ownership;
- carries activated counterweights into the participant set;
- allows Schemin project-local roles to be appended without becoming Directors;
- fails closed if the canonical counterweight contract is missing or changes primary ownership;
- records the standalone Bullpen revision that passed the integration gate.

## Chronicle spread DAG

`source_packet → manuscript_slice → spread_spec → art_job → composition → final_qa`

Each stage stores an artifact. Gates are separate worker contracts so the creator cannot self-certify completion.

## Current state

V1 implements the orchestration kernel, artifact contract, Chronicle pipeline declaration, canonical Bullpen counterweight-route adapter, and executable tests. External adapters (GitHub persistence, model/agent invocation, image generation and visual inspection) intentionally remain separate. Until an adapter exists, the runtime must report BLOCKED rather than pretend the work happened.

## Run locally

`npm test`

## Next implementation tranche

1. GitHubArtifactStore: append-only job manifests + artifact SHA/provenance.
2. Worker adapter interface for real model/agent calls.
3. Image job adapter and visual QA adapter.
4. Retry/revision routing with bounded attempts.
5. CLI/API entrypoint and resumable state.
6. Prologue Spread 01 canary run before batch production.
