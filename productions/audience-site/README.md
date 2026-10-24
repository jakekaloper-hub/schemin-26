# Commonwealth audience website

Read-only presentation consumer of Schemin canon, atlas and archived publications. This directory owns website presentation only; it cannot approve manuscripts, release memos or mutate world geography.

## Reproduce

Requirements: Python 3.12+, Node 22+, Poppler (`pdftoppm`), Git and materialized repository LFS assets. No npm dependencies or model/API calls.

```bash
python3 productions/audience-site/tests/test_public_catalog.py
npm --prefix productions/audience-site test
python3 productions/audience-site/build_public_catalog.py
```

The generated `dist/` is ignored by Git. It contains HTML/CSS/JavaScript, a derived `data.json`, the exact approved portrait crops and 75 web-resolution memo page images by default, or 110 with the recovered released sources. Original PDFs remain in their owning archive; the website provides pinned original links. No source bytes are overwritten.

To reproduce the full five-issue deployment, materialize the two canonical originals from their existing Library records into an external directory and run:

```bash
python3 productions/audience-site/build_public_catalog.py --released-source-dir /absolute/path/to/released-originals
CATALOG_RELEASED_SOURCE_DIR=/absolute/path/to/released-originals python3 productions/audience-site/tests/test_public_catalog.py
```

Required exact filenames: `Week 2 memo.pdf` (68,380,271 bytes, 14 pages) and `Pro_Schemin_Week_3_Memo_Final.pdf` (103,917,769 bytes, 21 pages). Fresh SHA-256 ingestion receipts are fixed in the builder. They remain in existing durable source storage; no reconstructed original is committed. Without this explicit source directory the reproducible base build has Weeks 4–6 and no latest-released claim. The supplied deployment contains all five issues and resolves Week 3 through the existing resolver.

## Publication boundaries

Week 4 and Week 6 are Commissioner-supplied source editions. Week 5 is an artwork-review edition. The October 22 intake verifies their source bytes but does not promote their release status. This app does not claim that Week 6 is the latest accepted release.

The four novel installments are preserved historical archive editions. The commissioned twelve-owner rewrite is not promoted by this site. No fabricated POV selection or completed historical volumes are offered.

The atlas consumes the canonical non-metric topology. Editorial candidate records are not included in public output. Character portraits are existing Commissioner-approved crops, hash-verified during the build; no generated character route is activated.

## Hosting and updates

Hosting project: `appgprj_6ada6ac1df0881918e9a8cfe1fa0c3e2`.

Public deployment uses a separate generated presentation mirror with `.openai/hosting.json` declaring `dist`. Canonical implementation remains in this repository. Rebuild after accepted content or source-edition updates, run checks, synchronize the exact output, commit/push the hosting mirror and save/deploy that exact version. Inspect deployment terminal status before claiming the audience site is live.

For source updates, verify input eligibility and hash receipts first. Do not change release controls merely to make an item appear. Reading progress is device-local and source-version-specific; clearing browser storage resets it. Browser storage failure must not prevent reading.

## Recovery

The hosting provider retains saved versions. Redeploy a previously verified saved version to restore the public site, then smoke-check home, atlas, memo and reader links. Keep the release’s source commit, generated catalog source revision and saved version/deployment IDs in the execution report. A rollback procedure is documented here; a real rollback must not be claimed until it is rehearsed.

## Review

Use `planning/audience-site/EXECUTION_LEDGER.md` for current execution evidence and limitations. Engineering tests do not constitute founder approval of the atmosphere or design.


## Offline memo text review candidates

The verified Weeks4–6 source PDFs are image-only. The optional local review tool uses Poppler and Tesseract, without model/API calls, to create selected physical-page images, OCR candidate text and a keyboard-readable side-by-side review page:

```bash
python3 productions/audience-site/build_memo_text_candidates.py --week 6 --page 1 --page 2 --output /tmp/week6-text-review
```

The intake manifest is read from the current Git commit. Source PDF size, SHA-256 and physical page count must match it. Every candidate records source revision/hash, physical page number and image/text hashes. Output must be empty and outside public `src/` and `dist/`. This is an **UNREVIEWED_OCR_CANDIDATE**, never publication eligible. The public catalog does not import these packets. OCR failures leave no candidate receipt; partial artifacts are not accepted output.

Reviewers must compare every line, name, score, caption and reading order with the original pixels, record corrections against the source/page hashes, and independently accept a future companion before public integration. Candidate OCR is not a fact lock, accessible edition certification, creative rewrite or permission to change the original PDF. An offline reviewer can open `review.html`, follow physical-page links and focus/select the candidate text. No reviewed-transcript approval mechanism is claimed by this tool.

### Reviewed text companions (optional, none accepted yet)

`memo-text/ACCEPTED_COMPANIONS.json` is an explicit, repository-reviewed publication allowlist subordinate to the original edition and existing source/release authority. It ships empty. The builder never searches OCR folders or treats a candidate's flags as permission to publish. No reviewed transcription or accessibility certification is claimed by this implementation.

A future entry names `packet`, `packetSha256`, `reviewReceipt`, and `reviewReceiptSha256` (repository-relative paths and exact SHA-256 digests). The packet must have status `REVIEWED_TEXT_COMPANION`, the catalog's `memoId`, exact `sourcePdfSha256` and `sourcePageCount`, and unique in-range physical pages. Each page supplies `physicalPage`, reviewed `title`, literal `text`, its UTF-8 `textSha256`, and a reviewed `visualDescription`. Partial coverage is permitted and displayed honestly; unavailable pages retain an explicit notice and their original images.

The separately reviewed receipt must bind that exact packet and PDF hash, declare `decision: ACCEPTED_FOR_TEXT_COMPANION`, `scope: TEXT_COMPANION_ONLY`, distinct nonempty `preparedBy`/`reviewer` identifiers, the sorted `acceptedPhysicalPages`, and `checks` with `textAccuracy`, `readingOrder`, and `visualDescription` each `PASS`. These are recorded review declarations, **not authentication of a reviewer**. Adding the allowlist entry requires the existing independent review and publication authority; do not generate a receipt merely to satisfy these structural checks. Changing either accepted artifact invalidates its digest. Review each line/name/number/order/visual description against the original before acceptance; original source bytes, release state and canon are never changed by this consumer.

Accepted text is rendered as text nodes, with a revision-pinned review-record link and per-page contents labels. Unreviewed OCR, pending/self-declared nonindependent receipts, wrong source hashes, duplicate/out-of-range pages, changed text, and repository path escapes fail the build. The test fixtures demonstrate the eligible path without creating a real acceptance entry. Archival chapter contents derive only from headings in the unchanged accepted manuscript; section links preserve the chapter route and support keyboard focus and reload.

### Character profiles, map callouts and composition integration

Profiles project exact literary sections from the twelve existing character dossiers and directed STANCE text from the closed STEP 5 relationship graph. They are explicitly fictional characterization at the opening of2026, not real-owner psychology or a current-week relationship update. Historical CAUSE fields, old identity locks and the stale narrative POV register are not imported; current approved portrait/appearance data remains authoritative. No owner mapping is guessed from historical slots.

The schematic atlas retains every canonical abstract dot position. Named screen-space callouts connect to those dots with leader lines; their responsive cell layout provides non-overlapping60px-high buttons without inventing geographical positions. Seven region names remain visible above the map. On narrow screens the canvas grows vertically to accommodate names. This is accessible schematic navigation, not the coordinated positional painting or its23-anchor visual acceptance.

A separate character-composition consumer now supports eligible profile imagery without relaxing the environment-art gate. See `artwork/CHARACTER_COMPOSITION_CONSUMER.md` for exact source, reference, runtime and independent review bindings. Its shipped allowlist is empty; no actual character composition is promoted. Pillow is required for real image-byte verification and is installed explicitly in the audience workflow. Optional reviewed compositions remain separate from the primary approved character portrait. Removed accepted entries remove only previously managed generated output after integrity checks; unrelated or changed output fails closed.

### Visible-text companion review scope

Accepted companions preserve the readable wording, names, scores, captions, printed errors and physical-page reading order of the source PDF. Intrinsically clipped or unreadable decorative marks are disclosed in each page visual description; hidden words are never reconstructed. Acceptance for this batch records actual separate AI source-pixel review with explicitly simulated Bullpen framing, not authenticated human signoff, complete decoding of invisible marks, canon promotion or whole-product visual acceptance. Substantive text or numeric ambiguity that cannot be faithfully represented remains outside the accepted subset. Each receipt records the exact physical pages and packet/source hashes.
