# Commissioner Bot — Privacy & Consent Gate

**Status:** Mandatory before production ingestion.

The bot is a visible league participant/assistant, not a covert collector.

- Inform every participant that accessible messages may be processed and retained for league purposes.
- Define retention duration, authorized readers, deletion, and export before collection.
- Direct-message content is private to that owner by default.
- Private content cannot be quoted, summarized, inferred into group answers, or used to advantage another owner without explicit authorization.
- Credentials, authentication tokens, payment information, and unrelated sensitive personal information must not become league memory.
- Minimize attachment storage and define separate attachment retention.
- Encrypt persistent stores and keep transport credentials outside source control.
- Audit administrative access and cross-partition reads.

## Commissioner neutrality
The shared Commissioner may use verified league data and shared league memory. It must not use Jake's Mercer/private-GM intelligence, or another owner's private strategy, to produce ostensibly neutral league responses.
