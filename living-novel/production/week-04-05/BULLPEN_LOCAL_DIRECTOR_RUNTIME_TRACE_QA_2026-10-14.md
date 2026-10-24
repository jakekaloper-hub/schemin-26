# Bullpen Local Director Runtime — Actual Invocation and Evidence QA
**Mission:** Bullpen #117 / Schemin #166, 2026-10-14  
**State:** **ACTUAL LOCAL MODEL-BACKED DIRECTOR INVOCATIONS EXECUTED — QUALITY GATE FAIL/CLOSER CORRECTION; NOT AUTHENTICATED INDEPENDENT APPROVAL.**

## Invocation provenance (not simulation)

Through the user-authorized Desktop Commander connection to the online macOS device, the local checkout at `~/Developer/ai/bullpen-runtime` was located and inspected. The checkout was on an **existing dirty, unrelated mission branch**; nothing in its working tree was edited, reset, committed, or merged.

Ollama was observed reachable on loopback `127.0.0.1:11434` with installed model families including `qwen2.5-coder:7b` and `qwen3:8b`.

Using the actual local `runtime/consultEngine.js` / `createConsultEngine().consultDirector()` and `core/directors/portableProfiles` (via the official local code path), five registered Directors were invoked with specific Novel mission inputs. The `adapters/models/authenticatedChat.js` module carried OpenAI-compatible requests to the **loopback Ollama endpoint** using its adapter-required placeholder key. This is **NOT strong identity authentication to an independent Bullpen server**. `EventEmitter` and `traceSink.record` captured emitted `director_consult` tracing. This proves actual code-driven model calls and generated responses, **not human, independent, or fully authenticated organizational authority**.

| Director slug | Actual model | Runtime trace latency | Source-credibility outcome |
|---|---|---:|---|
| `the_librarian` | `qwen2.5-coder:7b` | 22,482 ms | **QA HOLD:** treated two correctly different final team scores as a “discrepancy” |
| `the_beat_writer` | `qwen2.5-coder:7b` | 13,174 ms | **QA REJECT:** proposed artificial `novel/book` directory merely to clear Netlify; neglected manuscript-migration priority |
| `the_architect` | `qwen2.5-coder:7b` | 19,211 ms | **QA REJECT:** fabricated characters to expand the partial Chapter IV SHA and repeated empty-directory Netlify bypass |
| `the_umpire` | `qwen2.5-coder:7b` | 7,856 ms | **QA REJECT:** same cosmetic Netlify recommendation; same model/runtime cannot provide independent literary signoff |
| `the_closer` | `qwen3:8b` | 22,750 ms | **DIRECTIONAL PASS / NOT APPROVAL:** explicitly rejects fake Netlify repair; prioritizes 17 unwritten source scenes, independent literary QA, character and exact-blob Founder gates; escalates other desks' QA failures |

The first four consultations ran sequentially in one local Node process, with a separate bounded Closer counterweight run under a different installed local model. Both processes completed successfully and produced their own runtime trace events.

### Explicit rejected assertions
1. `157.33` (ObiWan) and `139.67` (DK) are two verified team totals. Their inequality is the legitimate result, **not** conflicting provider source evidence. Week 4 Flaim finality receipts in PR #128 govern.
2. The Chapter IV original manuscript's complete Git blob SHA is **`851ab270b577a9b5e4d28eab7b75178b9fc7e84f`**, confirmed from PR #128 via GitHub. A Director model's invented full SHA must not be indexed.
3. `novel/book` does not exist as an approved published book. Creating a placeholder solely to pass Netlify would be a false green, disconnected from working twelve-path reader publication. Deployment configuration is its own scoped engineering gate.
4. Local code invocation and an Ollama model response do not equal authenticated Bullpen director identity, an independent Umpire, a human author council, an exercised world mutation, a merge, or exact Founder canon consent.

## What actually survives Director challenge
- **G2 Character:** PR #171 now has current Wilson owner-specific four-legged Arsenal Gorilla Centaur doctrine reflected in live World Engine records AND the whole-book source precedence matrix; all six applicable GitHub CI workflows passed on its current candidate commit. Leave draft until qualified review.
- **G5 Chapter IV:** PR #128 uses actual Week 4 finality and starter receipts. The accepted-candidate soft manuscript blob remains untouched; independent assessment / exact Founder approval still HOLD.
- **G3 POV migration:** PR #130 already contains Prologue V4R2, 19/19 source-section candidate mapping for Chapters I–II, **two original draft scenes**, and an approved-ontology-decision packet for El Niño **as a proposal** (no exception license). Seventeen sections remain unwritten and the hard manuscripts still contain Edrin/Oren narrator scenes.
- **G4 Atlas:** the canonical graph expands route via-stops; 12/12 Week 4–5 travel pairs have graph paths, with weather/travel duration a separate check.
- **G8 reader and publication:** inkjs remains experimental; don't cosmetically satisfy an unrelated Netlify deploy using empty book assets.

## Independent QA and release state

**Validated:** Actual invocation of registered profile prompts through Bullpen ConsultEngine and loopback Ollama, five responses and five trace events; no local checkout mutation. The Closer's last response was a correction / priority recommendation, not a Director-authenticated canon act.

**Rejected:** four first-pass Director outputs as source-confident decision evidence. Umpire response cannot independently approve its own provider or the Author Room. Actual autonomy/coding and migration checks still require source-bound engineering PRs and external Founder consent where applicable.

**Result:** `LOCAL_RUNTIME_EXECUTION_VERIFIED` and `DIRECTOR_ANSWER_RELIABILITY_GATE_HOLD`; **no false-green; no canon, world or publication approval**.

## Next authorized tranche

The Closer should route the next round through existing PR #130's 17 remaining Chapter I–II source sections (each with bounded principal POV, decision, cost and knowledge receipts); schedule a genuinely separate qualified Umpire review of revised manuscripts and character/Atlas/POV constraints, then request exact Founder byte approval when drafts have passed. In parallel, keep PR #171 on its character-source QA track and PR #128 on its pre-canon literary/correctness track. Netlify can be repaired only against a real approved publish root.

**Record boundary:** no full raw model transcripts are committed; this report is a reviewed, bounded provenance/quality summary. The user owns the local runtime and can revoke Desktop Commander access independently.
