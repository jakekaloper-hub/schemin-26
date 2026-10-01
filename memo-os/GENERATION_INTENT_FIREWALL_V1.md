# Weekly Memo OS — Generation Intent Firewall V1

**Status:** V5.6 RC dependency  
**Parent:** V5.5 Integrated Preproduction Hardening  
**Purpose:** prevent a valid production brief from being transformed into the wrong artifact class at generation time.

## Immutable generation contract

Every generative-media operation receives a compact immutable packet derived from the locked Page Production Contract.

```yaml
generation_intent_id:
run_id:
issue_id:
page_id:
scene_id:
artifact_type:
expected_medium:
story_beat:
world_location_id:
character_packet_ids:
reference_asset_ids:
reference_asset_hashes:
composition:
camera:
foreground:
midground:
background:
lighting:
text_policy:
expected_dimensions:
prohibited_outputs:
next_gate: GENERATION_INTENT_QA
```

## Default prohibited outputs for publication illustration

Unless the Page Production Contract explicitly requests one, reject:
- workflow diagram;
- operating-system diagram;
- dashboard;
- control panel;
- generic UI;
- generic infographic;
- complete magazine page;
- uncontrolled factual typography;
- generic character reconstruction;
- unrelated scene;
- placeholder art.

The generation operation may not infer artifact class from the broader chat or project context. The packet controls the call.

## Generation Intent QA

Before Character QA, independently ask: **Is this actually the requested publication artifact?**

PASS requires:
- requested artifact class;
- requested scene identity;
- required characters broadly present;
- requested World/Encounter setting broadly present;
- composition materially aligned;
- prohibited output class absent.

FAIL returns directly to generation. Do not spend downstream Character/World/Mobile QA on the wrong artifact class.

## Regression requirements

- GENINT-001 illustration request returning dashboard → FAIL
- GENINT-002 illustration request returning workflow diagram → FAIL
- GENINT-003 art-only request returning complete magazine page → FAIL
- GENINT-004 correct medium, wrong scene → FAIL
- GENINT-005 missing required character → FAIL
- GENINT-006 correct artifact class/scene → PASS
