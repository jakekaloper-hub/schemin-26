# FLA Task Orientor → Execution Control reconciliation, 2026-10-17

**Mode:** existing Bullpen `/bullpen next`; FLA-pattern Task Orientation V1; **no new OS**.  
**Authoritative controls:** `PROJECT_CONTROL_REGISTRY.md`, `governance/task-orientation/TASK_CONTEXT_MATRIX_V1.json`, `governance/execution-control/TASK_REGISTRY_V1.json`, Bullpen Unified Execution Control V1.  
**Evidence:** connected FLAIM/ESPN actual Weeks 4–6 reads, GitHub `main` primary asset-directory readbacks, Library metadata and failed original-byte materialization calls. Full tool receipts exist in invoking session; written synopsis here is not a machine-signed receipt.

## Reconciled tasks — proposed in same review branch

| Task ID | Previous status | New status | Reason |
|---|---|---|---|
| `CHAR-PORT-002` | READY | IN_PROGRESS | Live 12-path GitHub inspection and Library recovery attempted; exactly two primary Git binaries on main, ten paths absent. Source/hash and mount acceptance not complete. |
| `MEMO-W4-002` | WAITING_EXTERNAL / P0 | IN_PROGRESS / P1 | Week 4 is historical after Week 5 distribution; urgent character recovery retains P0. External wait for games is no longer valid: ESPN now reports six decided outcomes. Post-Week-4 records, injuries, roster / transaction relevance and owning Fact Lock require validation; no COMPLETE / PASS. |
| `MEMO-W6-001` | Not registered | IN_PROGRESS | No duplicate Week 6 task in migrated registry. Live six fixture intake prepared in existing `memo-os/week-6/`. Final outcomes still UNDECIDED; production art blocked by character chain. |

All status transitions follow the Bullpen V1 state machine (`READY → IN_PROGRESS`; `WAITING_EXTERNAL → IN_PROGRESS`). **None enters COMPLETE.**

## Week 4 provider-closeout proof (not a Fact Lock by itself)

| Home | Away | Home final | Away final | Provider winner |
|---|---|---:|---:|---|
| D0nkey K0ng | ObiWan Jacoby | 139.67 | 157.33 | AWAY |
| Mud Dogs | Three Dreaded Snake | 126.98 | 149.84 | AWAY |
| Red Leopards | Dr. Duckhook | 164.08 | 128.36 | HOME |
| Slob on my Dobb | The Chili Cheesers | 190.72 | 139.96 | HOME |
| The LLC | His Majesty's Blood | 138.87 | 177.32 | AWAY |
| El Niño | Seven Deadly Chins | 170.62 | 106.20 | HOME |

Flaim `get_matchups(week=4)` returned these results on October 17. **Do not use this table to claim post-Week-4 standings were archived or that Week 4 Memo release gates passed.** The Publication Manifest currently marks Week 4 BLOCKED; it must not be auto-promoted.

## Week 5 vs Week 6 chronology

- Week 5's *distributed 19-page historical issue* is documented in `memo-os/week-5/WEEK_5_DISTRIBUTED_EDITION_POST_PUBLICATION_AUDIT_2026-10-14.md`. The connected ESPN Week 5 six results and scores agree with that audit's internal parity. This is **not** retroactive independent visual QA or immutable release certification.
- Week 6 is current league activity; all six ESPN fixtures are `UNDECIDED` at capture. New evidence lives at `memo-os/week-6/WEEK_6_FLAIM_SETUP_INTAKE_2026-10-17.md`.
- The existing Publication Manifest still has Week 3 as technical `CURRENT_BENCHMARK`. User-confirmed Week 5 distribution versus technical publication identity requires owning release-evidence reconciliation; no historical overwrite or implicit benchmark promotion.

## P0 risk controls

- No new character uploads requested; all twelve approved original reference identities are already recorded.
- No claim that Git blob SHA-1 equals approved SHA-256. Two primary binary paths are verifiably present, not rendered.
- No claim of authenticated 18-Director meeting, independent Umpire sign-off, local validator pass or CI pass.
- No Week 6 winner, championship, venue promotion or generated visual canon invented.
- Week 4 task and novel dependency remain open until actual evidenced criteria are satisfied.

## Next operator sequence

1. Character source recovery: seek already recorded exact source bytes through an **authorized raw-byte-capable route**, independently rehash, ingest 10 missing bytes, verify all 12 on fresh read, then pursue mount/subject-binding C1.
2. Week 6 editor: resolve six encounter venues and itineraries through actual Atlas IDs; write conditional story packets and develop non-character design specifications while C1 is held.
3. Scout: finish Week 4 archived fact scope only as required for genuine historical closure; reconcile its downstream dependency without replaying unnecessary publication work.
4. Umpire: run actual CI/regression checks on this PR, audit reference and temporal authority, accept/reject without fabricated sign-off. Promotion/merge only upon applicable real checks.

**Verdict:** Evidence intake and task-state reconciliation implemented as review candidate; **NOT independently tested or promoted**.

## First CI feedback and bounded regression repair

Initial PR #195 GitHub Actions readback: four workflows PASS (Cross-Domain Authority, Bullpen Runtime, Character Lock, Weekly Memo Authority), but Repository Merge Gate FAIL because three existing execution-control tests asserted *obsolete* registry statuses or next-task priority. The existing task-state vocabulary itself validated. Netlify `scheminnovel/deploy-preview` also reported FAIL; this known publish-path problem is tracked separately in Schemin #174/#191.

Corrective branch action: recategorize Week 4 historical fact closure from P0 to P1 (no acceptance bypass); preserve current character P0 in progress; update two stale task-fixture assertions; add Week 6 in-progress/not-released negative check in existing execution-control suite. A passing **new CI receipt** is required, not presumed.
