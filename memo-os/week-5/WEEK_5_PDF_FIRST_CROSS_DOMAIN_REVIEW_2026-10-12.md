# Week 5 — PDF-First Cross-Domain Production Review
**Status:** DOCUMENTARY CROSS-DOMAIN REVIEW / PROPOSED EXECUTION CONTROLS; **NOT** authenticated Director, Author Council, consultant, or Umpire signatures.
**North Star:** Deliver one complete, cinematic, legible, portable **Week 5 league-shareable PDF**, not an HTML substitute. Use existing Memo OS, Master Production Packet, 32-page provisional manifest, page packets and approved Commissioner amendments; do not create a new OS.
**Source basis inspected:** `MASTER_PRODUCTION_PACKET.md`, `PUBLICATION_PAGE_MANIFEST.json`, `PRODUCTION_READINESS_REPORT.md`, `WEEK_5_PERSONALIZATION_EDITORIAL_AND_SHOT_EXECUTION_2026-10-12.md`, `memo-os/PUBLICATION_FIDELITY_CONTRACT_V1.md`, `memo-os/week-4/publication-readiness/WEEK_04_PUBLICATION_DESIGN_QA.md`, `WEEK_04_PUBLICATION_RECEIPT.md`. The Week 4 receipt is explicitly a TEMPLATE / RELEASE BLOCKED, not proof of an accepted Week 4 PDF.

## Domain review matrix — recommendations for actual owners to accept or revise
| Review seat | Assessment / required action | Acceptance evidence |
|---|---|---|
| Closer / production sponsor | A source packet is not the league deliverable. Freeze one PDF release candidate, not an HTML viewer. Keep 32 pages provisional pending layout proof. | PDF artifact + signed publication receipt |
| Groundskeeper / production | Single deterministic manifest → assembled PDF → per-page visual proof → issue QA. Reject orphan pages, inconsistent orientation, missing fonts, and placeholder copy. | build log, page manifest parity, export receipt |
| Beat Writer / Author Council | Preserve the six four-page narrative waves, but edit for one dramatic job per page; overtures remain prose-forward, spoilers and winner POV gated. Distinguish dialogue invented for fiction from owner quotes. | approved 32-page manuscript and POV lock |
| Librarian / character canon | Verify exact owner-specific bytes/hash/renderer mount for each depicted character, including Arsenal Centaur, one-body three-head serpent, Belt Keeper and no belt on ObiWan. | character-ID → source SHA-256 → mounted bytes → output subject audit |
| Atlas / world geography | Keep the six venue IDs, temporary chess arena, Western street and jousting lists; swamp remains partly damaged only. | geography and time-specific continuity receipt |
| Visual Direction / Art | Week 2/3 publication fidelity is the quality floor; no repetitive generic hero-image + report-card templates. Use varied full-page cinematic compositions and deterministic typography. | page-level technical + publication fidelity PASS |
| Scout / league truth | Six ESPN Week 5 results remain UNDECIDED at last authenticated read; never lock conditional winners or playoff percentages without proof. | certified Fact Lock + corrections window |
| Pitty's Book / math | Settle only verified lines and receipts; separate wagers, editorial power rankings and modeled playoff probabilities. Omit unverified probability values. | reconciled ledger and math QA |
| Architect / export engineering | Use a PDF-first page assembly pipeline, optimize image assets before embedding, subset fonts, validate no raster corruption; HTML is not the league delivery channel. | reproducible build, measured file size, export QA |
| Warden / sharing | Avoid hidden private source assets, credentials or internal GitHub data in PDF metadata or attachments. | metadata and disclosure audit |
| Umpire / independent QA | Block release if any page fails canonical identity, readable typography, publication fidelity, final data or PDF integrity. No implied signoff. | independent recorded veto/pass |
| Consultants — John Ezzell, Jeff Lunsford and third consultant (identity not verified here) | Requested lenses: editorial product experience, production cost/reliability, operational distribution. These are **review prompts**, not evidence of their participation or agreement. | actual review notes or authenticated ACK |

## Proposed PDF delivery specification — targets, not measured results
- **Primary artifact:** one standalone PDF with all 32 pages in the approved order; no internet, HTML, JavaScript or app viewer required. A browser preview can be optional, never a substitute.
- **Target maximum:** **25 MB**, with **15 MB preferred** for messaging/mobile sharing. These are production budgets, **not a claim about any existing PDF or guaranteed attachment limits**. If over 25 MB, optimize images/fonts and re-export before requesting a larger budget; do not silently cut approved story pages.
- **Page geometry:** choose and freeze a single portrait page size after proof. Maintain full-bleed visual ambition with text-safe zones. Do not assume the 1024×1536 concept raster is an accepted print size or sufficient DPI.
- **Image pipeline:** derive per-page print-size assets from approved master renders; convert opaque photographic/painted composites to quality-tested JPEG (initial trial quality 78–85, not fixed final), preserve transparent overlays only where needed; remove duplicate full-resolution image copies; avoid embedding source-resolution masters unmodified.
- **Typography:** deterministic vector text with embedded/subset fonts, readable 390px phone-width preview, full canonical team names, verified line wrapping, safe margins and no text rasterization unless justified by independent QA.
- **Assembly:** one page = one manifest record = one page packet = one final PDF page. Use reusable assets without degrading page-specific art. Export once from approved, immutable inputs; verify final file signature, page count, page dimensions, font presence, per-page rendering, image fidelity and metadata.
- **Distribution:** validate actual share route and platform limits (league chat/email) before calling the PDF shareable. Optional lighter second PDF may be derived only from the same approved page set, with no missing editorial content. Do not distribute HTML in place of PDF.

## Mandatory measurable PDF acceptance gate
1. **PDF_EXISTS:** actual generated PDF on disk with SHA-256, bytes and build provenance.
2. **PAGE_PARITY:** page count matches the locked manifest (32 provisional), order and titles checked.
3. **SIZE:** actual bytes <=25,000,000 target (preferred <=15,000,000); if not, FAIL and optimize; targets can be changed only by Commissioner approval after real distribution tests.
4. **TEXT:** extractable full canonical names, scores and editorial copy; no missing glyphs, text clipping or font substitution.
5. **PHONE:** raster preview of every page at 390px width; headings, scores, body copy and jokes remain legible. Record failure pages.
6. **ART:** independent page-level technical acceptance AND publication fidelity, preserving cinematic depth and identity.
7. **INTEGRITY:** re-open/render all pages, check page geometry, blank/corrupt pages, metadata and no hidden credentials.
8. **FACTS:** final ESPN results, corrections, Pitty's Book settlement and any playoff odds independently verified.
9. **CANON:** actual exact character mount and subject binding receipts, Atlas temporal continuity, no prohibited film-copy elements.
10. **INDEPENDENT:** authenticated Umpire approval with evidence. No synthetic PASS.

## Findings and priority actions
**F1 — HIGH:** Current Master Production Packet has no measured PDF size target or explicit PDF-only publication acceptance. **Remedy:** incorporate this additive contract in the existing master and readiness; do not create another OS.
**F2 — HIGH:** 32-page manifest is provisional; full copy, image assets and physical shell QA are not finished. **Remedy:** freeze only after manuscript/page-budget and one real PDF export proof.
**F3 — HIGH:** Week 4 publication receipt is a blocked template. Do not use it as evidence that an HTML-first process passed.
**F4 — HIGH:** 20 personalized pages have source-level drafts and reconciliation, not author-approved manuscripts. Final outcomes and six winner POVs still gated.
**F5 — HIGH:** No current Week 5 PDF file, file-size measurement, page-by-page rendered preview, character mount receipt or independent Umpire acceptance has been produced by this review.
**F6 — MEDIUM:** The older readiness report contains superseded 'dedup incomplete' text; the later dated reconciliation section controls. Reconcile those contradictions in place.
**F7 — MEDIUM:** For premium illustrated pages, aggressive compression can destroy fine text and textures. Do not optimize solely to hit the byte target: if a page loses fidelity, fix the pipeline, not the story.

## Actual cross-domain review gate
Send this packet to the authenticated Closer, Groundskeeper, Beat Writer/Author Council, Librarian, Scout, Visual Lead, Architect, Atlas, Warden, consultants and independent Umpire through the operational Bullpen runtime if available. Require role ID, authenticated response provenance, actionable amendments, conflicts, final vote, and Umpire receipt. **No live consultation or independent acceptance is claimed in this document.**
