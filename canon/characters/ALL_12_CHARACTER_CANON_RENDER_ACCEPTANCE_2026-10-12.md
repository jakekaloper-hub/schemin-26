# Schemin '26 — All Twelve Character Canon / Render Acceptance Gate
**Commissioner directive 2026-10-12.** Applies to Memo, Living Novel, covers, portraits, social art, cinematic scenes, and any image generation. **Binding editorial and QA policy on working branch; not proof of actual renderer enforcement.**

## Authority and precedence
Owner-specific active approved visual source bytes and the latest explicit Commissioner correction > owner active package > active visual authority registry > master reference plate (historical where stale) > prose canon > prior art. Team rename does not redesign owner. **Do not render** if any required exact source/hash, asset mount, subject binding, temporal state, or independent QA evidence is missing. No generic prompt-only stand-in. The rejected human Dr. Duckhook illustration is not canon.

## Twelve-owner hard locks and reject tests
| Owner / team | Required identity and signature | Immediate rejection |
|---|---|---|
| Jake Kaloper / ObiWan Jacoby | Youthful blond Trade Jedi; earth-tone robes/field jacket; green energy sword; golden retriever | Championship belt, generic knight, masked soldier |
| Kevin Zeek / Red Leopards | Giant red leopard/jaguar predator, black rosettes, amber eyes, tribal armor, claws | Human hunter, species/color drift |
| Jordan Hollingshead / Slob on my Dobb | Horned shaggy berserker, battered football armor, metal bat, pit-bull; **Frat Star** | Clean slim human, stale “Fart Star” alias |
| David Babb / The LLC. | Human corporate raider in dark tailored suit, sunglasses, cigar, executive/briefcase props | Animal mascot, generic fantasy warrior |
| Wilson Look / D0nkey K0ng | **One Arsenal Gorilla Centaur**, gorilla upper identity integrated with four equine legs, Arsenal-red/bronze gear, axe | Bipedal gorilla, rider and horse, two separate animals |
| Phillip Pitts / Three Dreaded Snake | **Exactly three serpent heads on one reptilian humanoid body**, green-gold scales, #3 gear; post-haircut state for Week 5 | Three separate snakes, one head, restored dreadlocks without temporal authority |
| Brandon Pryor / Chili Cheesers | Bearded Chili Outlaw, black cowboy hat, chili-red duster, pepper bandolier, chili pot, **The Dark Horse** | Chili King, bear/bloodhound, generic cowboy |
| Manning Welty / El Niño | Elemental storm-water/cloud/lightning humanoid, glowing blue eyes, storm staff | Sheriff/lawman, child, ordinary human, generic wizard |
| Austin Byars / His Majesty's Blood | Corpse-pale long-haired medieval immortal, rune armor, sword, championship belt | New king/vampire/blood monster; missing or transferred belt |
| Bobby Mitchell / Mud Dogs | Massive mud-covered canine/wolf beast, blue-orange elements, heavy chain, frightening teeth | Human fleeing swamp, clean pet dog |
| Zach Wilson / Dr. Duckhook | **Anthropomorphic white-gray duck**, yellow-orange bill, pale eyes, floral-camouflage bucket hat/golfwear, cigar, **right arm fused anatomically to golf driver**, swamp golf | Human country-club golfer, human wearing duck print, ordinary duck, detached club |
| Ben Whipple / Seven Deadly Chins | Heavyset bearded human bruiser, dirty white tank, CHIN UP SHUT UP cap, hammer, bottle, raccoon | Literal multi-chinned monster, polished athletic redesign |

The table is a **semantic summary**, not a substitute for each owner-specific current approved visual asset. Resolve each owner package and time-specific authority before rendering. Avoid treating descriptions above as complete evidence of exact colors/face/wardrobe where the source image has greater detail.

## Executable acceptance specification (to wire into existing renderer, not a new OS)
1. Resolve `owner_id` to `CHAR-*`, current team, approved visual-reference ID, temporal version and canonical source.
2. Retrieve exact image bytes from authorized storage; record SHA-256, Git blob/object reference, source authority and immutable content address. Reject missing/mismatched bytes.
3. Mount that exact asset into the actual generation runtime; log mounted-byte hash and subject-to-owner binding for **every** character in the scene. No reference recycling between characters.
4. Require explicit identity-positive and hard-negative prompt constraints compiled from package and latest correction. Scene/pose may change; species, silhouette, anatomy, companion and iconic props may not.
5. Validate each rendered character against their own source at native resolution and mobile/thumbnail scale. Independently reject wrong species, fused-arm failure, body count, number of heads/legs, wrong belt, wrong temporal hair, alias drift and cross-owner contamination.
6. In multi-character frames, run pairwise contamination checks and count all expected subjects. Do not accept a single reference PNG duplicated for multiple owners.
7. Attach machine-readable per-render receipt: character ID, active reference ID, source SHA, mounted SHA, prompt/negative-lock version, rendered artifact hash, reviewer verdict, timestamp and release decision. Independent Umpire reviews evidence, not a model's self-reported PASS.
8. Fail closed: `SOURCE_BYTES_REQUIRED`, `PROVIDER_CAPABILITY_BLOCKED`, `CHARACTER_IDENTITY_MISMATCH`, `TEMPORAL_STATE_CONFLICT`, or `UMPIRE_HOLD`. Never mark READY_FOR_RENDER from prose alone.

## Immediate regression cases
- **Dr. Duckhook:** reject the previously generated bearded human in green blazer even if labeled “Dr. Duckhook”; pass only duck body + fused right driver arm with source-verified details.
- **D0nkey K0ng:** reject bipedal gorilla, human rider on horse, two animals, wrong leg count.
- **Three Dreaded Snake:** reject separate snakes, fewer/more than three heads, incorrect post-haircut continuity.
- **ObiWan Jacoby:** reject championship belt.
- **His Majesty's Blood:** reject a generic wizard or character with belt absent.
- **Mud Dogs:** reject a human substitute, especially in Week 5 bulldozer flight scene.
- **Chili Cheesers / El Niño:** reject sheriff redesign; preserve The Dark Horse.
- **All twelve:** reject owner identity mismatch, mixed owner reference assets, unsupported reference source and unreadable identity at page size.

## Actual status
**POLICY/PACKAGE UPDATE ONLY.** Dr. Duckhook screenshot supplied in chat, but exact screenshot bytes are not yet stored as canonical GitHub image asset or verified in renderer. No twelve-owner clean-context source-byte proof, renderer-mount proof, automated runtime test or independent authenticated Bullpen Umpire acceptance is claimed. Production generation stays **HOLD** until the operational gates pass.
