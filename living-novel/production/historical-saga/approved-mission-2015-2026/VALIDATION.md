# Validation evidence and its limits

Local execution on the task branch, 2026-10-24. These are actual command results, not a claim that every story or season passes literary acceptance. Exact artifact hashes are in independent review and reader receipts.

| Command | Observed result |
|---|---|
| `python living-novel/consultants/test_advisor_registry.py` | 12 tests passed |
| `python living-novel/consultants/author-council/test_author_router.py` | 10 tests passed |
| `python -m unittest discover -s living-novel/migrations -p 'test_*.py' -v` | 49 tests passed |
| `python -m unittest -v test_novel_os.py` from `living-novel/os/evaluations` | 34 tests passed |
| `python -m unittest discover -s living-novel/production/historical-saga/approved-mission-2015-2026/evidence -p 'test_coverage.py' -v` | 8 tests passed |
| Reader build and `python -m unittest -v test_reader.py` in `reader/` | 11 tests passed; exact command output in `reader/TECHNICAL_CHECK.json` |
| `review/check_candidate_scenes.py` | 24 actual scenes, zero structural/source-join errors, no missing registers; see durable reviewer result |
| `review/check_historical_candidate_scenes.py` | 11 historical scenes across four events; zero structural/source/dual-authority errors |
| `review/check_2015_jake_connected_account.py` | Three 2015 Jake scenes for one event; zero source/POV/scope/foreknowledge errors under the bounded user-attestation plus Flaim-continuity rule |
| `review/check_2015_jake_arc.py` | Six further 2015 Jake scenes link every remaining observed team-1 event; zero source/POV/scope/foreknowledge errors |
| `review/check_2016_jake_arc.py` | Ten 2016 Jake passages link every observed team-1 event; zero source/POV/scope/foreknowledge errors |
| `review/check_2017_jake_lane.py` | Eight 2017 Jake passages cover all sixteen Flaim-joined team-1 events; zero source/POV/scope errors |
| `assemble_candidate_links.py` | Fifty-six distinct source-event keys, 62 actual scene anchors and 99 scene-event links; no acceptance asserted |
| Repository-native checkpoint emit/resume | Receipt emitted and VALID_CHECKPOINT resolved; stage is audit/draft production, not canon |

Source checks resolve real observation pointers and hashes rather than trusting an acceptance label. They preserve equal-score rows whose declared winner is HOME without inventing a tiebreak cause; distinguish one documented bye from other unpaired rows; and keep multiweek aggregate repeats separate from distinct contests.

Reader validation preserves all 62 inventoried original blobs, escapes source HTML, verifies known temporal lane order, includes every declared literary file, checks actual anchors/content digests/local links, rejects an empty final reader, and prominently discloses historical incompletion. This is static technical evidence. Managed Chromium denied local file navigation; no screenshot, visual acceptance, accessibility certification or browser pass is claimed.

These checks do not authenticate historical owner identities, establish full schedule completeness, prove book-level literary quality, approve fictional world deltas, or turn a model review into authenticated Director/human acceptance. Remote CI status belongs to the exact pushed commit and must be reported separately from these local results.
