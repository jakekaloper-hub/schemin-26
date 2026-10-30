# 2016 causal Chapter XVIII — source, assembly, execution and writer QA receipt

**2026-10-30 | NONCANON DRAFT | INDEPENDENT EDITORIAL HOLD | NO MERGE / PUBLICATION**

## Actual delivery

- Continuation of existing open draft PR #243 on `novel/historical-epic-2015-2026`; predecessor: 2016 causal Chapter XVII checkpoint. No replacement Novel OS and no canonical manuscript edit.
- **Literature:** `THE_RIVER_KEPT_NO_PLACE_CHAPTER_18_NONCANON.md` — 5,141 whitespace-separated words **including editorial handoff**, five movements; verified Git blob `899ac5eba4e4bb212652ed31baae08c0636631b8`.
- **Reader:** `READING_COPY_CAUSAL_CHAPTERS_01_18_NONCANON.md` — 91,731 whitespace-separated words including book metadata and editorial handoffs; verified Git blob `78560d0a2775a66340570d8382bbb90ae5992a22`. Eighteen source-component rows, eighteen opens/closes, source exact.
- **Regression artifact:** `living-novel/historical-chronicle/qa/test_2016_causal_chapter_eighteen_reader.py` — twelve new unittest methods staged to the draft branch, verifying source-exact embedded text, Git blob fingerprints, prior reader invariance, protected canon, archive, narrative/source holds, and word/structure thresholds. **Do not assert the new twelve methods have executed until there is a runner receipt.**
- **Genuine scene turn:** In the second offered upriver workday, a proposed night-watch employment offer competes with return to the shelter. A hill community holds a private naming rite without treating the stranger Jake as audience or authority. After day-two load-out, he is paid a bounded wage, disembarks downriver and takes an inland road; there is **no homecoming**, no proof that Mara received his message, and no settled shelter debt.

## Actual source and runtime reconciliation

- Schemin current main intake commit `ec941811d6334d70015ec97b2ac68a2d8a26eec6`; Bullpen main `86889a59efb0e7dcdc37eef639981944dc77ed67`.
- Source authority: `living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md`, blob `67fcd669dc7b43393f2d15e93545301961dd81e4`. Twelve-owner exclusive POV and causal chapter architecture govern; superseded archive POV text has no active authority.
- Bullpen controls read: `BULLPEN.md`, `docs/COMMAND_SYSTEM_V2.md`, `runtime/lifecycleEngine.js`, and `knowledge/EXECUTION_CONTROL_REGISTRY_V1.json`. Project current task registry still reports `NOVEL-NEXT-002 NOT_STARTED`; do not silently rewrite that task status based on this separate draft saga.
- Read current issues #210 #211 #214 #215 #219. PR #188 is merged; #243 open DRAFT; #252 and #261 remain open DRAFT / HOLD; newer PR #264 is a distinct Chapter I causal candidate and is not auto-merged or superseded.
- Retained 2016 archived transcription `G01_2016_FULL_WEEKLY_MATCHUPS.json` Git blob `6dbec1fe2537139f3a97c6a78250e2bae082a518`; user/human-to-2016-scoring-slot attribution remains **NOT PROVIDER AUTHENTICATED**. Chapter XVIII asserts no league scores or outcomes.

## Source-exact mechanical evidence — PASS (connector assertions)

- **18/18** reader manifest source filenames, recorded Git blob hashes, text segments and whitespace word counts matched the exact committed chapter files when re-fetched from draft PR #243.
- **17/17** predecessor manifests remain identical; each prior manuscript source blob is identical to the preceding reader's source. Prior seventeen-chapter reader remained at Git blob `7ba3cf83ff59d187929a71861c1d053abbb05140`.
- Four 2026 hard-canon files: Prologue `5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0`; Chapter I `26a17f05eb0565e7648c29add03ee9580ec933c3`; Chapter II `30fcf23a3eb8872fa0fb4dff029fe30044141121`; Chapter III `49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc`. Authenticated GitHub source blob checks found **main == draft branch** for all four. 2016 archive blob also unchanged.
- Distinguish **tool-level readback/source assertions** from an independently executed Python regression run or author acceptance.

## Actual executable regression evidence — previous suite PASS; new suite pending

- At exact checked-out draft commit **`57cd809acc51a0f23b37a8b6204fafc11dd303fc`**, an authorized, isolated sparse worktree was materialized at `/tmp/commonwealth-novel-2016-20261030` on the connected Mac. The command `python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal_chapter*reader.py' -v` completed: **170 tests, 0 failures, OK**.
- This **executed and verified** the earlier Chapter XV (13) and Chapter XVII (11) suites, previously marked unrun, alongside existing earlier chapter regressions. This result is tied to `57cd809a` and is **not** a claim that new Chapter XVIII tests executed or that CI enrolled them.
- Attempt to fast-forward the isolated Mac checkout and execute the new Chapter XVIII tests via Remote Desktop Commander **timed out**. No success or failure may be inferred from the timed-out command; investigate ongoing process output before retrying. The new test source was committed at `12c79f7bb75b68d1aadae8a091bf63ac47387792`.
- CI should be read back against the exact final PR head; older successful checks do not prove the new Python suite ran.

## Writer's literary challenge — NOT independent acceptance

- **Conflict distinctness:** The proper novel turn is choosing to return after an attractive new employment offer. If the story merely repeats the earlier lesson that Jake cannot direct others, the chapter should be cut or rewritten. The offer must remain a live possibility, not a straw man.
- **Ritual / invented culture:** The bell-and-stone naming rite is an original proposed local practice; a reader could mistake it for established Commonwealth law. It requires independent Atlas/Civilization review and a challenge to cultural appropriation or sentimentality. No dead-person identity is claimed as historical.
- **Material plausibility:** Returning heavy packing, kiln shields, downriver transit and seasonal wage need a route and economic pass. No formal employment relationship with an actual person is asserted. Proposed water conditions and distances may be impossible under the period Atlas.
- **Character autonomy:** Eren's future, Vessa's personal loss and Deren's memory remain independent of Jake and unresolved. Avoid turning those supporting characters into a convenient moral chorus.
- **Temporal risk:** Jake travels downriver then *starts* an inland walk. He has not arrived at the shelter; no messenger acknowledgment, relationship settlement, renewed commission, bridge repair, mill restoration or championship outcome is in evidence.
- **Privacy / POV boundary:** All suggested interiority concerns the proposed fictional owner character, not real Jake's 2016 private thoughts. Eren, Aren, Vessa, Pell, Deren receive only observed behavior and dialogue.

## Unresolved production gates

Independent Authors Council, period Character Canon, Atlas, Librarian and Umpire approvals **NOT OBSERVED**. Founder-only hard canon, merge if restricted, publication and external consequence gates **NOT GRANTED**. Draft is NONCANON and shall not publish or alter protected Prologue / Chapters I–III.
