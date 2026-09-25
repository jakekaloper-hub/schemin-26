# Commissioner Bot — Architecture v0.1

## Memory partitions
- **shared_league** — authorized group-chat context.
- **owner_private** — direct-message context isolated by owner.
- **verified_league** — ESPN/Data Gateway, rules, transactions and validated facts.
- **derived_storyline** — AI-extracted narrative events with provenance/confidence.

`owner_private` is never available to another owner or to a group response.

## Commissioner modes
- **GROUP_COMMISSIONER** — neutral assistant using shared + verified data.
- **OWNER_ASSISTANT** — private assistant using that owner's private context plus shared + verified data.
- **ADMIN** — explicitly authorized maintenance/commissioner operations.

## Canonical MessageEvent
```json
{
  "event_id": "uuid",
  "transport": "imessage",
  "conversation_id": "opaque",
  "message_id": "opaque",
  "sender_identity_id": "opaque",
  "league_owner_id": null,
  "sent_at": "ISO-8601",
  "visibility": "shared_league",
  "body": "message text",
  "attachments": [],
  "reply_to": null,
  "consent_state": "authorized",
  "ingested_at": "ISO-8601"
}
```

## Required production gates
1. Apple/iMessage transport feasibility demonstrated on controlled devices.
2. Participant consent workflow defined.
3. Retention/deletion/export policy defined.
4. Encryption at rest and secret management selected.
5. Private/shared isolation tests passing.
6. Prompt-injection and malicious-message tests passing.
7. Data Gateway remains authoritative over conversational claims.
8. Bot identity and processing are visibly disclosed.
