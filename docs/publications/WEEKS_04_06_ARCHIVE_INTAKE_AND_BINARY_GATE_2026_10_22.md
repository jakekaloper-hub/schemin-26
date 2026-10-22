# Schemin '26 — Week 4–6 Commissioner source intake

**Status: SOURCE RECONCILED / RAW PDF BYTES NOT YET ARCHIVED.**

On October 22, 2026 the Commissioner supplied three PDFs directly in ChatGPT. An intake JSON alongside this document stores verified local SHA-256, byte length, exact supplied basename, page count, and sampled visual landmark evidence.

## Important publication distinction

- Week 4 is named **Official Memo**, 33 pages, but the older repository publication manifest still marks Week 4 BLOCKED. This discrepancy requires explicit release-evidence reconciliation, not a silent flip.
- Week 5 is **Artwork Review 19 Pages**, and is Commissioner-supplied. The file title alone does not prove it is the immutable league-shared final. Preserve the exact filename until publication equivalence is confirmed.
- Week 6 is a 23-page Week 6 Memo; its end page is the *Final Word* with a Commonwealth relief Atlas. Do not assume folio text numbering equals PDF page count.

## Archival gap

**Do not claim these PDF bytes are in GitHub.** This GitHub connection supports creating text files, but no current trusted mechanism transferred the local PDFs to GitHub. The 121,338,910-byte Week 4 PDF is over GitHub's normal 100 MiB? limit (GitHub hard limit 100 MB), so even an ordinary Git binary commit is unsuitable. Prefer Git LFS with authorized transport and repository quota verification, or a GitHub Release asset upload. Preserve original byte-for-byte files. Avoid using reduced-size derivatives as replacements.

Suggested storage layout, once an authorized binary archive path exists:

- `archive/publications/2026/week-04/Pro_Schemin_26_Week_4_Official_Memo.pdf`
- `archive/publications/2026/week-05/Schemin26_Week5_Artwork_Review_19_Pages.pdf`
- `archive/publications/2026/week-06/Schemin_26_Week_6_Memo.pdf`

After ingest: download each archived original, recompute SHA-256, assert exact match to intake manifest; only then change `archive_status` to `VERIFIED_STORED`, set immutable storage URL/blob, and consider a separately governed release-manifest update.

## Atlas archaeology

Published artwork is source evidence for *depicted scenes* and narrative events; its map placement is not automatically metric world geography. Preserve page-level citations and reconcile with `world/canon/PUBLISHED_LOCATION_REGISTER_V1.md`, `world/atlas/ATLAS_CONTROL_PLANE_V2.md`, and PR #226. No LOC creation or geography promotion is part of this archival intake.
