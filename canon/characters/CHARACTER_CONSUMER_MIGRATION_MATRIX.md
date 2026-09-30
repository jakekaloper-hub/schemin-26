# CHARACTER CONSUMER MIGRATION MATRIX
status: AUDIT_IN_PROGRESS

|Consumer|Current character source|CCCP integrated|Local appearance authority removed|Historical firewall|Test|Status|
|---|---|---|---|---|---|---|
|Weekly Memo OS|CCCP integration contract + legacy prose packets|PARTIAL|NO|PARTIAL|pending|HOLD|
|Waiver Wire|Memo OS / visual prompt path|PARTIAL|NO|PARTIAL|waiver incident simulation|HOLD|
|GOTW|Memo/visual production docs|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Matchup artwork|Memo/visual production docs|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Covers|Memo visual production|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Scoreboards|Memo production|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Pittsy's Book|Memo production|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Live Looks|local narrative/visual packets|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Chronicles|historical + local character prose|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Living Novel|Novel OS character/POV/world packets|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Universe OS|worldbuilding + character canon|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Owner spotlights|Memo/social production|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Social/promo|varied|AUDIT_REQUIRED|NO|NO|pending|HOLD|
|Bullpen visual skills|plugin/runtime dependent|AUDIT_REQUIRED|NO|NO|pending|HOLD|

## Required end state
Every consumer requests CHARACTER_ID + SCENE_REQUEST. Appearance is compiled only by CCCP into CHARACTER_RENDER_PACKET. Historical context is opt-in and cannot override identity.
