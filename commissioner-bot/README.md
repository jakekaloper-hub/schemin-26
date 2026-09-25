# Schemin' Commissioner Bot

**Status:** Architecture / prototype track  
**Technical authority:** The Setup Man  
**Knowledge steward:** The Librarian  
**Data authority:** The Scout  
**AI behavior:** The Pitching Coach  
**Security/privacy:** The Warden + Commissioner General

## Mission
Build a league-owned conversational assistant that can eventually participate as a visible member of the Pro Schemin' group conversation and support league members in 1:1 conversations. The transport layer is replaceable: iMessage is a desired interface, not a hard dependency of the intelligence system.

## Core contract
1. Group conversation is shared league context.
2. Direct messages are private to the sender by default.
3. Verified ESPN/league-system facts are separate from conversational claims.
4. Extracted memories retain source, speaker, timestamp, visibility, confidence, and provenance.
5. Jokes, trash talk, predictions, and rumors never become verified facts automatically.
6. No collection begins without participant consent and a retention policy.
7. Private strategy never leaks into Commissioner responses or shared memory.

## Architecture
```text
iMessage / future transports
        |
 Transport Adapter
        |
 Message Event Store
        |
 Identity + Permission Resolver
        |
 Conversation Intelligence
   |          |          |
Shared     Private    Extracted
Memory     Memory      Events
   \          |          /
       League Knowledge
             |
   Verified Data Gateway
             |
 Commissioner Reasoning
             |
 Response / Query Layer
```

## Phases
**0 — Feasibility:** prove the Apple/iMessage endpoint without coupling the backend to undocumented assumptions.

**1 — Listen / normalize / remember:** authorized ingestion, owner/team identity, immutable raw events, structured league events, retrieval.

**2 — Commissioner assistant:** mention/reply-driven rules, history, ESPN-backed questions, receipts, and summaries.

**3 — Private owner assistant:** 1:1 owner context with strict private-memory isolation and explicit share-to-group actions.

**4 — Controlled participation:** optional proactive league summaries/reminders with rate limits and governance.

## Non-goals
- Circumvent iMessage encryption.
- Secretly collect participant conversations.
- Let Jake's private Mercer intelligence influence neutral Commissioner behavior.
- Make the core intelligence model dependent on iMessage.
