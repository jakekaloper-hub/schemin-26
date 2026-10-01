# Weekly Memo OS — Reference Mount Receipt V1

**Status:** V5.6 RC dependency  
**Purpose:** prove canonical pixel references were actually supplied to character-bearing generation.

A prompt that describes a character is not equivalent to a mounted reference.
A reference stored somewhere in the project is not equivalent to a mounted reference.

## Receipt

```yaml
generation_intent_id:
page_id:
expected_reference_ids:
expected_reference_hashes:
mounted_reference_ids:
mounted_reference_hashes:
mount_status: PASS | BLOCKED
verified_at:
```

PASS requires expected IDs/hashes to match the mounted set required by the Page Production Contract and Character Packet Gate.

If a required reference is absent or mismatched, generation must not start.

The final raster remains subject to Character QA even when mount_status=PASS.
