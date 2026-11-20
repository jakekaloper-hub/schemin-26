# Chapter L V2 — Author-side source, continuity and QA receipt

**Date:** 2026-11-04  
**Status:** NONCANON / INDEPENDENT EDITORIAL HOLD  
**Owner:** developmental author-side production; **not** an independent Authors Council or Umpire acceptance  
**Owning draft:** Schemin PR #243, `novel/historical-epic-2015-2026`  
**Verified production commit:** `d9d0cdb354431b6762a415c1fc9695f785688df4`

## Literary change actually written

- *The Night Below the Room — The Third Story*, revised Chapter L, **8,347 words including metadata/author notes**.
- **2,376 words of new fictional scene prose**, `THE_NIGHT_BELOW_THE_ROOM_THE_THIRD_STORY_CH50_V2_SCENE_NONCANON.md`, Git blob `5e5eccb5234e4aae1e276579dac1dbf8487dd227`.
- Original Chapter L source `THE_NIGHT_BELOW_THE_ROOM_CHAPTER_50_NONCANON.md` remains Git blob `920d3fda6c9f366d9c56e45745b8db117c8e3fa8`.
- Revised integrated Chapter L Git blob `94e81f9b84a6300a40d108935d26e25f2f5acfac`.
- The six original movements are preserved, in order and with unchanged original bodies; new movement VI precedes original movement VI, renumbered VII.

In the added scene, three travelers who stayed at Ina's workshop debate what it means to remain for one night without giving anyone authority over the others. Tovin tells a deliberately comic invented fable. Neris, Dovan, and Tovin disagree over the road, a jointly owned damaged cart rail, and their rights to give their own accounts. Jake observes rather than commanding them. The scene adds personal history and humor amid the staircase crisis without asserting real-world owner psychology or league outcomes.

## Adversarial author-side continuity repair

A first draft inadvertently brought Meric back to inspect the damaged stair on the afternoon of the collapse, contradicting original movement V's explicit **first-light next-day** return. That draft was corrected in both the standalone scene and integrated chapter **before** the final verified production commit. In the final scene Meric remains absent and Ina makes preparations for the lower sorting-room arrangement; original movement VII still delivers the one-night shelter.

The story-in-story is expressly proposed secondary-world invention. An accidental historical source claim must not be inferred from the goose, uncle, injured leg, dye trade, place or weather. The scene intentionally does not determine the safety of the upper frame or Neris's injury, restore the cart, recover Hessa, or establish Garran's authority.

## Continuity holds carried forward

- **Six split three-and-three:** Hessa plus two companions inland; Neris, Dovan and Tovin at Ina's private workshop. Hessa's sister and the missing eight remain unlocated. River lure sponsor unidentified.
- **Physical:** Failed staircase and uncertain upper structure; Meric will examine from a safe position no earlier than first light; one of the jointly owned cart's side rails broken in emergency, wheels/axle retained. Original twenty-one-night undertaking not retroactively erased; lower sorting room offered for one night only, no permanent refuge or public lodging created.
- **Economy:** Ina's wet dye work suspended, dry orders displaced. Jake retains four coins from knowingly false secondary-world eyewitness payment; Pell's lost hauling wage and refusal to absolve Jake remain unresolved. No new payment, contract, public authority or business recovery is invented.
- **World/POV:** Sole limited interior is proposed fictional Jake, among the twelve authorized principal owners. 2016 owner-to-scoring-slot authentication remains incomplete. Neris/Dovan/Tovin and other supporting people are external character actions only. Protected 2026 Prologue/Chapters I–III unchanged.

## Verified technical evidence at exact production commit

- **22/22 newly introduced Chapter L V2 regression tests passed**, including six-movement source-exact preservation, protected canon Git blobs, 2016 archival blob, POV/evidence safeguards and reader mutation-negative tests.
- **47-part nonpublishing reader assembled source-exact** by `build_2016_causal_47_part_third_story_reader.py`: Chapters I–L, **363,606 source-component words including metadata**; preceding 46 component bodies preserved.
- `Novel OS CI` push workflow #41849747916 — **success**, `https://github.com/jakekaloper-hub/schemin-26/actions/runs/41849747916`.
- `Cross-Domain Authority CI` PR workflow #41849767065 — **success**.
- `Bullpen Runtime CI` push workflow #41849747501 — **success**.
- `Repository Merge Gate` PR workflow #41849767022 — **success**.
- Temporary GitHub Actions artifact: `commonwealth-2016-47part-third-story-developmental-reader-noncanon`, id `13332268024`, 737,036 bytes, expires 2026-11-11 14:40:10 UTC. The rebuild script remains committed for later regeneration.

## Independent review required — NOT received

1. Authors Council: Does the goose fable and explicit debate offer narrative relief or over-repeat the novel's evidence/testimony theme?
2. Character Canon: Are the three travelers' new biographies and humor too late or too conveniently individualized? They remain proposed rather than period-approved.
3. Historical Librarian + Atlas: Confirm that all dates, craft arrangements, lodging and geography remain clearly invented; do not interpret them as 2016 owner identities or authenticated events.
4. Narrative architect: **Fifty consecutive Jake-centered chapters** create a major ensemble distribution defect. Do not solve by inventing any historical owner identity or unauthorized interior viewpoint.
5. Independent Umpire: Examine source provenance and the first-light repair before any approval. Passing CI is not independent literary acceptance.

**Final disposition:** DRAFT only. **NO MERGE / NO CANON PROMOTION / NO PUBLICATION.** Founder-only release gates are not waived.
