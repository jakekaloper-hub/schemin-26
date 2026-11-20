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
