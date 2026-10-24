# Unreal Environment Production Standard v0.1

**Authority:** World Engine / Atlas, with character and publication counterweights.  
**Status:** PROPOSED on draft PR #238; local preview implementation exists, not approved world art.

## Purpose
Translate the existing Schemin Commonwealth into a consistent collection of Unreal scenes without creating a parallel Atlas. Every visualized place must preserve its immutable location identifier, canonical classification, physical zone, owner identity, landmark labels, source commit and provenance.

## Production layers
1. **Source contract:** `world/data/locations.json` and later approved Location Control Plane and Atlas records; exact Git commit and bytes are recorded.
2. **Environment specification:** one record per source location with unchanged landmark labels, explicit UNRESOLVED metric scale, unresolved terrain, art approval status and publication gate.
3. **Geometry preview:** Unreal generates clearly identified *unsized proxies*, camera blocking and level indexing. A saved `.umap` confirms asset creation but does not mean physically accurate or playable.
4. **Authored visual design:** World Engine + Visual Direction reconcile landform, dimensions, settlement hierarchy, materials, lighting and history from governing canon. New invention is a proposal until explicitly approved.
5. **Runtime/render verification:** measured Play-in-Editor movement, collision, packaging, Sequencer tracks and rendered proof, with machine-specific memory/performance evidence.
6. **Promotion:** independent Umpire review; no Unreal output writes back to World Engine automatically.

## Anti-drift checks
- `location_id` must remain stable across exports and Unreal levels.
- Preserve `PERMANENT_CANON`, `PROVISIONAL_CANON` and `INTERPRETIVE_CANON` distinctions.
- Never infer metric distances from abstract coordinate arrays.
- Landmark proxies retain their *source labels* and are not presented as finished terrain or structures.
- No character embodiment/model output without approved reference-byte and subject-binding gates.
- No new paid asset service without budget approval.
- No claim of real-time ESPN event sync without freshness receipts.

## Local implementation evidence (not a canonical release)
On the connected Mac, `ScheminBridge/build_environment_specs.py` generates `environment_specs.json` for 23 pinned Atlas locations. Sixteen local Python test methods pass, including the environment-spec fidelity checks. Unreal contains generated schematic maps, not finished Commonwealth assets.

## Next acceptance
The engineering team must implement build-from-spec rather than fixed handcrafted map templates, validate source-record identity against a fresh pinned export, load one environment in PIE, and demonstrate actual rendered preview capture before this standard can be promoted.
