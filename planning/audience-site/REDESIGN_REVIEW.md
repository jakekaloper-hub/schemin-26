# Audience experience redesign checkpoint

Implemented homepage, atlas, Twelve, profiles, memo archive/issues, library/reader. Expanded 23 canonical destinations and seven physical-region pages. Location terrain, climate, travel, landmarks and routes are sourced from existing World Engine and derived location cards; no new canon is asserted. Week 6 visual reference informs gilt rules, wine banners, dark surfaces and serif hierarchy.

Independent review found catalog-error UI crash, stale memo image failure recovery, and constrained atlas panning. All three repaired. Browser verified released Week 3 pagination and reload, profile/manuscript links, reader 50% resume and text-size persistence; desktop homepage and 390px iframe homepage inspected. Destination desktop DOM verified. Expanded destination mobile visual acceptance, complete navigation regression and final deployment remain pending.

Verification: Node suite 10/10; Python discovery 21 passed, one optional recovered-release integration skipped in default run (22 total). Existing user portable-renderer test file unchanged; implementation now supports its PyMuPDF fallback. Production build recovered all five issues/110 pages and four exact archival manuscripts.

Original artwork commissions: 0/49 complete. Existing approved images are temporary presentation assets; original artwork and founder visual acceptance remain open. Do not call the entire founder artwork mission complete.

Build: Python3, Poppler or PyMuPDF, npm test, python -m unittest discover -s productions/audience-site/tests -p 'test_*.py'; python productions/audience-site/build_public_catalog.py --released-source-dir <exact recovered PDFs directory>. SCHEMIN_SOURCE_REVISION may pin the verified remote source commit. Recovered source PDFs must match hardcoded ingestion hashes; without them source editions remain distinguished and no release is invented.
