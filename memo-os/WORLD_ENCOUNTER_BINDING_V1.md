# Weekly Memo OS — World / Encounter Binding V1

**Status:** V5.6 RC dependency  
**Authority:** World Engine V1.1

## Purpose
Bind each visual story to persistent Schemin geography instead of treating pages as isolated illustrations.

## Required fields

```yaml
encounter_id:
page_id:
home_team:
away_team:
venue_id:
venue_type: HOME | NEUTRAL | SPECIAL
division_context:
terrain:
climate:
world_state_in:
persistent_landmarks:
route_from_away_origin:
travel_validated:
new_or_provisional_location:
prior_appearances:
world_state_out:
canonization_notes:
```

## Venue law
- ordinary regular-season/divisional encounters default to verified home-team established environment;
- GOTW/playoff/championship encounters default to approved neutral Schemin locations unless specifically resolved otherwise;
- away participants require an approved route/path when World Engine requires it;
- generated scenery is not automatically canon.

## QA
Block when:
- location contradicts World Engine;
- terrain/scale is incompatible;
- a persistent landmark resets without explanation;
- travel is impossible under the route model;
- new scenery is silently promoted to canon.
