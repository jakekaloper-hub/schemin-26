# Fantasy League Artworks Integration

Upstream repository: `jakekaloper-hub/fantasy-league-artworks`

## Boundary

Fantasy League Artworks (FLA) is the reusable product/platform and creative-engineering repository.
Schemin '26 is the league-specific operating repository.

## Allowed dependency direction

Schemin '26 may:
- consult FLA Bullpen operating patterns;
- reuse compatible FLA architecture and creative workflows;
- request upstream platform improvements;
- reference FLA documentation and implementation.

Schemin '26 must not:
- treat FLA league-agnostic defaults as league facts;
- silently mutate FLA when only a Schemin-specific change is needed;
- copy stale league state from FLA into current production;
- bypass Schemin canon or Data Gateway contracts.

## Cross-repo change rule

If a Schemin need reveals a reusable platform defect or capability gap:
1. document the Schemin requirement here;
2. open/implement the reusable change in FLA;
3. record the FLA commit/PR reference in Schemin;
4. keep league-specific configuration in Schemin.
