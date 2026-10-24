---
name: schemin-pdf-bytes
description: Retrieve and verify actual original Schemin '26 PDF bytes from Git LFS archives using canonical release manifests.
---
# Schemin PDF Byte Recovery

Use whenever an exact archived weekly memo PDF is needed for Memo OS, visual QA, publication evidence or ChatGPT document review.

1. Resolve the requested week through the canonical publication manifest. Current Week 4–6 manifest: `governance/publication-manifest/WEEKS_04_06_COMMISSIONER_SOURCE_INTAKE_2026_10_22.json`. Do not guess paths for other weeks.
2. On an authorized repository checkout, materialize missing Git LFS files with `git lfs pull`. Verify actual bytes, not a pointer or a Markdown description.
3. Execute `python3 skills/schemin-pdf-bytes/scripts/verify_pdf_bytes.py --repo-root . --manifest governance/publication-manifest/WEEKS_04_06_COMMISSIONER_SOURCE_INTAKE_2026_10_22.json --week 6 --receipt /tmp/schemin-week-6-pdf-receipt.json`.
4. Only `VERIFIED_REAL_BYTES` means PDF magic bytes, exact byte count and expected SHA-256 were observed. `POINTER_ONLY` and `FAIL` are not acceptance.
5. Follow the separate PDF render/visual QA and Memo OS publication procedures. Never equate correct bytes with approved character likeness, artwork or publication.
6. Reuse the verified file and receipt when the canonical hashes remain unchanged; avoid requesting repeat uploads.

This is a repository-local skill. It does not automatically install itself as a first-party ChatGPT platform skill, grant new permissions or schedule background execution.