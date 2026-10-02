# Production Checkpoint Store

**Authority:** Production Checkpoint Standard V1  
**Status:** ACTIVE storage location

Checkpoint receipts are written beneath this directory by workflow.

Example:

```text
checkpoints/
  weekly-memo/
    W4-STORY-LOCK-001.json
  living-novel/
    CH04-MIN-PRE-PROSE-001.json
```

A checkpoint file is evidence of completed reusable work, not authority to invent or promote facts/canon.

Create one with:

```bash
python governance/resilience/checkpoint_cli.py emit \
  --checkpoint-id <id> \
  --project "<project>" \
  --workflow <workflow> \
  --stage <stage> \
  --owner <owner> \
  --source-authority <repo/path> \
  --input <repo/path> \
  --output <repo/path> \
  --evidence <run:...|commit:...|repo/path> \
  --invalidate "<condition>"
```

Resolve the latest still-valid checkpoint with:

```bash
python governance/resilience/checkpoint_cli.py resume --workflow <workflow>
```

The resolver verifies source authority, current input digests, output existence/digests, and evidence references before returning a checkpoint.
