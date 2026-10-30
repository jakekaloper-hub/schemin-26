# Chapter XXII — The Cover and the Cargo
## Source-bounded literary and technical QA — NONCANON / SELF-REVIEW ONLY
**Recorded:** 2026-10-30. **Owner:** draft Author Room/Novel OS. **Status:** submitted for independent review, not accepted.

### Actual delivered work
- Substantive five-movement fictional chapter at \`living-novel/historical-chronicle/seasons/2016/causal-novel/THE_COVER_AND_THE_CARGO_CHAPTER_22_NONCANON.md\`, **6,641 whitespace-delimited words including editorial notes**.
- Source-exact 22-chapter reader \`READING_COPY_CAUSAL_CHAPTERS_01_22_NONCANON.md\`, **116,650 whitespace-delimited words including headers, manifest and editorial notes**. First 21 components carried unchanged; preceding reader blob: \`322138c36de8bf80cf01b41b7870203bc70fd205\`. New chapter Git blob: \`7b2ce956d5aa2836d6f2d30a3520d8c521e870c7\`.
- Fourteen new Python regression tests in \`living-novel/historical-chronicle/qa/test_2016_causal_chapter_twenty_two_reader.py\`. Already enrolled via existing CI discovery pattern \`test_2016_causal_chapter*reader.py\`; results must be read at exact resulting branch head.

### Minimum pre-prose gate — retrospectively checked against written text
1. **Job:** turn the stolen-book mystery into a physical supply and evidence problem with a costly, incomplete discovery.
2. **Dramatic question:** can Jake and Esi recover truthful evidence before the missing records cause material harm without falsely accusing a witness or discharging unproved debts?
3. **POV:** fictional Jake (one of the twelve principals) exclusively in close limited viewpoint. Esi, Tern, Len and others act independently, never narrate.
4. **Location:** existing fictional shelter and market → introduced provisional west store; weighing of physical cargo requires these sites. None is Atlas-certified.
5. **Opening pressure:** Esi's theft notice must be posted but Jake cannot pay the board fee; the old supply account is incomplete.
6. **Turn:** a physically observed empty cover and cut binding displace rumor; an actual load nearly leaves undelivered, and Esi renegotiates a witnessed partial receipt.
7. **Consequence:** flour enters kitchen, the recovered probable cover is independently held one more day, missing leaves are still gone, new ledger will be transparently reconstructable, and the stolen-book notice remains unposted through Jake's error.
8. **Advanced loop:** book loss now has material/economic consequences; Jake's limits are tested by an unfinished assigned task; Mara's absence and Esi's authority persist.
9. **Off page:** archival competitive outcomes, all unproven 2016 owner identifications, hard-canon 2026 events and other Chronicle obligations are not depicted.
10. **Exit pressure:** the loose pages have circulated with an unidentified carrier; private obligations might be sold or used against people before provenance can be restored.

### Direct source constraints and checked integrity
- Controlling matrix: \`living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md\` (main Git blob \`67fcd669dc7b43393f2d15e93545301961dd81e4\`).
- Chapter rule: \`living-novel/os/NOVEL_CAUSAL_CHAPTER_ARCHITECTURE_V1.md\`, no week-to-chapter conversion.
- Retained 2016 archive: \`living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json\` (Git blob \`6dbec1fe2537139f3a97c6a78250e2bae082a518\`), unchanged on main and draft branch. Historical 2016 Jake-owner binding **NOT PROVIDER-AUTHENTICATED**. Fiction includes **no historical score or results**.
- Main-versus-branch fresh blob comparisons: protected Prologue \`5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0\`; Chapters I \`26a17f05eb0565e7648c29add03ee9580ec933c3\`, II \`30fcf23a3eb8872fa0fb4dff029fe30044141121\`, III \`49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc\`. All four **identical** on both refs as directly fetched 2026-10-30.
- An initial pre-CI static correction changed a new regression assertion from uppercase \`POV\` to lowercase \`pov\` after noticing \`chapter.lower()\`; this is a test-author edit, **not an observed CI failure**.
- **Observed CI result and repair:** Novel OS CI [run #41108686341](https://github.com/jakekaloper-hub/schemin-26/actions/runs/41108686341) executed 242 tests and failed **2 test-only string assertions**, because the test demanded a literal sentence about the unposted notice and used incorrect capitalization for the supplier invoice. The underlying manuscript and reader remain unchanged. Two assertions were repaired in test-only commit `67b460d8990e18695207ce52f541001d8c9bff4a`; the repaired suite requires separate exact-head CI confirmation. This is not a green claim.
- In-memory reader assembly preflight: 22 manifest rows ordered 1–22; 22 BEGIN and END source markers, previously assembled chapter material preserved. This is **not** a substitute for GitHub CI or an independent review.

### Literary self-challenge — unresolved, not independent clearance
1. **Structural repetition (HIGH):** Chapter XXI also focuses on fraudulent papers, Esi's careful distinctions and witness language. Chapter XXII adds a recovered physical cover, an actual nearly interrupted supply delivery, and a new binding, but the written narrator returns to precision-of-testimony more often than ideal. Independent developmental editor should determine whether to condense repetition and foreground competing emotional stakes.
2. **Jake's agency (MEDIUM):** his choice to pay Tern and follow the cover's lead causes the failure to post the notice; this is concrete, but risks repeating the same lesson from earlier chapters. A future chapter should force a choice not reducible to correct procedure.
3. **Economic plausibility (HIGH):** one-day paid storage, public-board fees, warehouse pledge-for-meal terms, measured load, writable witness duplicates and binding technology are plausible fiction, **not period-correct Atlas-approved law**. A source authority review must decide whether they fit the Commonwealth.
4. **Secondary character autonomy (MEDIUM):** Esi negotiates, Tern sets labor terms, the porter corrects his own account, and Len makes a distinct observation. Their interior states remain outside Jake's knowledge. Check that the women do not function merely as Jake's teachers.
5. **Mystery causality (MEDIUM):** the porter remembers loose pages only after a second round of questions. The distinction between cover, contents and cloth is deliberate but may feel arranged to sustain suspense. The measure-keeper's cupboard provides limited custody of cover; there is still **no certified thief**.
6. **Human-owner identity / protected text (RELEASE BLOCK):** this is not an authenticated 2016 owner POV or a supplement to the protected 2026 chapters; no such claim is made.

### Mandatory HOLD
No real Authors Council, Character Canon/Atlas, independent Umpire, Founder canon approval, merge or publication acceptance is recorded by this self-review. PR #243 remains draft. Check exact-head CI independently; re-run local regression suite only if connected Mac execution is actually available. Do not interpret this document as a green acceptance.
