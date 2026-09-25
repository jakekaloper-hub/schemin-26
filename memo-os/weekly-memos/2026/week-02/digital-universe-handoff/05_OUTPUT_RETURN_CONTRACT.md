# Output and return contract

Return a folder:
```
RETURN/
  MACHINE_REPORT.md
  QC_REPORT.md
  RETURN_NOTES.md
  render_manifest.json
  workflows/
  clips/
    A01.*
    A02.*
    A03.*
    A04.*
    A05.*
  assembled/
    special-delivery.*
  post/
```

Each manifest entry must contain: shot id, source asset filename/checksum, engine, model/checkpoint, workflow/version, seed, dimensions, fps, frame count/duration, generation settings, output filename/checksum, QC decision and notes.

Do not label anything PUBLISHED or OFFICIAL. Use `INTERNAL_CANDIDATE`.

If you cannot render, return the same structure with MACHINE_REPORT, RETURN_NOTES, workflow/config work completed, and exact blocker evidence.