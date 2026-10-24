# Raster text diagnostic

`python memo-os/tools/compare_editorial_raster_text.py page.png page.receipt.json diagnostic.json`

Requires Pillow, local Tesseract OCR with English language data (`tesseract-ocr`, `tesseract-ocr-eng` on Ubuntu). CI installs these and runs an actual pixel extraction positive/mismatch regression; the real OCR test explicitly skips when the executable is unavailable locally. Test fixtures also require DejaVu Sans.

The PNG must match the compositor receipt hash. Each declared region is cropped from immutable decoded PNG bytes, observed using Tesseract, and compared to the receipt's rendered line commands. Only one terminal OCR linefeed is removed; whitespace, case, punctuation and Unicode remain exact. Exit0 means every declared region matched; exit1 means a comparison mismatch. Missing tools/failed extraction raise an error, never a successful observation.

The output binds PNG and render-receipt hashes, crop hashes, OCR version/configuration, observed text and comparison differences. This is a diagnostic against render commands, not an approved manuscript, complete page coverage, OCR accuracy certification, PDF render-back comparison, independent visual judgment, mobile review or publication approval. Blank/omitted regions and false upstream copy remain outside this check. No editorial normalization policy is invented and no acceptance state is promoted.

## Final PDF pipeline

`python memo-os/tests/validate_artifacts.py candidate/manifest.json` retains the existing issue, artifact, release-evidence and Creative DNA checks and emits `pdf_copy_diagnostics` alongside their errors. The existing artifact gate now compares the actual full-page render-back against each PNG master, rejecting overlays, rotation and changed geometry even when embedded image bytes match.

For ISSUE_PACKAGE pages with `editorial_receipt_path` and `editorial_spec_path`, final-PDF diagnostics bind PDF/master/receipt/spec bytes, render the final page, observe the declared text regions with the same OCR method, and fail the command on changed text or failed observation. Selectable PDF text is recorded separately; an image-only PDF's empty text layer does not stand in for OCR. Pages lacking editorial receipts are explicitly `NOT_RUN_NO_EDITORIAL_RECEIPT`, and `all_pages_observed` is false. This preserves existing non-editorial package contracts, without claiming complete text coverage or introducing a new approval policy.

Source-spec hash matching establishes provenance consistency only; it does not establish approved-copy or normalization authority. A PASS of existing structural gates with NOT_RUN pages is not full text acceptance.

Synthetic test receipts and PASS labels exist only in test temporary directories. A successful diagnostic remains distinct from approved manuscript comparison, authenticated reviewer identity, mobile visual acceptance and release authority. A RELEASED fixture without the existing provider/reviewer evidence remains rejected by the same pipeline.
