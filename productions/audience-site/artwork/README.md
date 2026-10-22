# Commissioned website artwork

Status: no generated assets. Two built-in generation attempts failed before returning image bytes. See `planning/audience-site/artwork-redesign/GENERATION_FAILURE_RECEIPT.md`.

The 49-page commissioning inventory lives in `planning/audience-site/artwork-redesign/COMMISSIONING_INVENTORY.json`; 37 subject-free prompts are prepared in `NON_CHARACTER_PROMPT_SET.json`. The 12 character commissions additionally remain under the existing character-generation hold.

After successful generation and visual review, place original image files here and add `manifest.json`:

```json
{
  "schemaVersion": 1,
  "assets": {
    "home": {
      "file": "home.webp",
      "alt": "An empty mountain ridge overlook in dawn mist.",
      "status": "REVIEWED_PRESENTATION",
      "subjectClass": "environment",
      "sha256": "REPLACE_WITH_FRESH_OUTPUT_BYTE_HASH",
      "focal": "65% 50%"
    }
  }
}
```

The example is documentation only, not an accepted asset receipt. Record exact prompt, source constraints, output dimensions, fresh byte hash, mobile focal decision, and visual review evidence alongside each commission before using reviewed status. Preserve original outputs. No script automatically awards visual acceptance.

The builder permits only the 37 environment/editorial slots. CHAR-* slots and character subject classes are rejected; a status string cannot bypass character generation eligibility. Unreviewed outputs are excluded, stale published artwork is removed, and invalid file paths or hashes stop the build.

Original memo pages and archival manuscript text are independent of this artwork and must remain intact. Existing imagery may remain as compatibility fallback until a commission is ready; it does not count as custom-art coverage. Do not deploy this groundwork as the completed redesign.
