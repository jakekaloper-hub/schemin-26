import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { createModelDraftWorker } from "../src/model-draft-worker.js";

const hash = text => createHash("sha256").update(text).digest("hex");
const source = { source_id: "verified-weekly-fact-lock", text: "Week 10: six verified matchup results.", sha256: hash("Week 10: six verified matchup results.") };
const ctx = { input: { source_packet: source }, stage: { id: "manuscript_slice" } };

test("produces a traceable unapproved text artifact using an injected model provider", async () => {
  let calls = 0;
  const worker = createModelDraftWorker({ role: "beatWriter", provider: { async generate(request) {
    calls++; assert.match(request.messages[0].content, /verified matchup results/);
    return { text: "A draft account of those results.", model: "local-example" };
  }} });
  const output = await worker(ctx);
  assert.equal(calls, 1);
  assert.equal(output.artifact.kind, "MODEL_TEXT_DRAFT");
  assert.equal(output.artifact.state, "UNREVIEWED");
  assert.equal(output.artifact.source_sha256, source.sha256);
  assert.equal(output.artifact.response_sha256, hash("A draft account of those results."));
  assert.equal(output.artifact.canon_approved, false);
  assert.equal(output.artifact.character_renderer_eligible, false);
});

test("rejects absent or mismatched source bytes without invoking the provider", async () => {
  let calls = 0;
  const worker = createModelDraftWorker({ role: "beatWriter", provider: { async generate() { calls++; return { text: "never" }; } } });
  for (const bad of [undefined, { ...source, sha256: "0".repeat(64) }, { ...source, text: "" }]) {
    const result = await worker({ ...ctx, input: { source_packet: bad } });
    assert.equal(result.blocked, true);
    assert.equal(result.code, "UNVERIFIED_SOURCE_PACKET");
  }
  assert.equal(calls, 0);
});

test("rejects empty or malformed model responses without creating an artifact", async () => {
  const worker = createModelDraftWorker({ role: "beatWriter", provider: { async generate() { return { text: "  " }; } } });
  const result = await worker(ctx);
  assert.equal(result.blocked, true);
  assert.equal(result.code, "MODEL_DRAFT_UNAVAILABLE");
});

test("rejects unsafe adapter setup and prevents source-free drafts", async () => {
  assert.throws(() => createModelDraftWorker({ role: "beatWriter", provider: {} }), /generate/);
  assert.throws(() => createModelDraftWorker({ role: "", provider: { generate() {} } }), /role/);
});
