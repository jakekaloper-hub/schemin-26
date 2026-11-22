/**
 * Provider-neutral text draft worker for local/connected Bullpen models.
 * It emits an unreviewed artifact only. Canon, character QA and release gates
 * remain independent; matching source bytes does NOT prove source truth.
 */
import { createHash } from "node:crypto";

const sha256 = text => createHash("sha256").update(text, "utf8").digest("hex");
const blocked = (code, reason) => ({ blocked: true, code, reason });

export function createModelDraftWorker({ role, provider, maxTokens = 384 } = {}) {
  if (typeof role !== "string" || !role.trim()) throw new TypeError("nonempty role required");
  if (!provider || typeof provider.generate !== "function") throw new TypeError("ModelProvider.generate required");
  if (!Number.isInteger(maxTokens) || maxTokens < 1 || maxTokens > 4096) throw new RangeError("invalid maxTokens");

  return async ({ input = {}, stage = {} } = {}) => {
    const source = input.source_packet;
    if (!source || typeof source.source_id !== "string" || !source.source_id.trim()
        || typeof source.text !== "string" || !source.text.trim()
        || typeof source.sha256 !== "string" || !/^[a-f0-9]{64}$/.test(source.sha256)
        || sha256(source.text) !== source.sha256) {
      return blocked("UNVERIFIED_SOURCE_PACKET", "Verified source text and exact SHA-256 required");
    }

    let response;
    try {
      response = await provider.generate({
        purpose: "schemin_preproduction_draft",
        system: "You draft editorial text using only supplied source evidence. Do not invent results, canon, identities, geography, or approval. If evidence is insufficient, say so. Your work is an unreviewed candidate, not a publication or render approval.",
        messages: [{ role: "user", content: "Source ID: " + source.source_id + "\nSource text:\n" + source.text + "\nTask: " + (stage.id || role) }],
        maxTokens,
      });
    } catch {
      return blocked("MODEL_DRAFT_UNAVAILABLE", "Model invocation failed; no draft artifact created");
    }

    const text = response?.text;
    if (typeof text !== "string" || !text.trim()) {
      return blocked("MODEL_DRAFT_UNAVAILABLE", "Model returned no usable text");
    }

    return {
      artifact: {
        kind: "MODEL_TEXT_DRAFT",
        state: "UNREVIEWED",
        role,
        stage_id: stage.id || null,
        source_id: source.source_id,
        source_sha256: source.sha256,
        text,
        response_sha256: sha256(text),
        model: typeof response.model === "string" ? response.model : "provider-defined",
        canon_approved: false,
        character_renderer_eligible: false,
        publication_eligible: false,
      },
    };
  };
}
