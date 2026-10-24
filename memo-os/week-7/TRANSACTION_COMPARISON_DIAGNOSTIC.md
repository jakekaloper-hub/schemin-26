# Complete-row transaction comparison

`compare_transaction_snapshots.py BEFORE.json AFTER.json OUTPUT.json` compares two complete normalized snapshots with matching league, season, provider source and window metadata. It preserves full before/after changed rows and binds both exact input byte streams by SHA-256. Exit zero means the row comparison completed; it never means provider authenticity, accepted freshness, stewardship approval or Fact Lock.

Both inputs must contain `week7_transactions.transactions`, unique transaction IDs, timestamp/status fields, correct count/window row totals, `truncated=false` and zero dropped timestamps. A count-only baseline cannot substitute for full rows. Reordering rows is not a transaction change. Same-count replacements and status changes are reported explicitly.

The checked-in October23 evidence contains33 rows; the retained October22 baseline contains a29-count summary, not those29 rows. Therefore the actual baseline comparison remains HOLD. Tests self-compare the stored capture and use explicitly synthetic mutations to verify the comparator; they do not reconstruct the missing historical snapshot. No source artifact or release state is modified by this command.

This addresses the existing intake row-diff requirement only. It does not implement or certify the separate COLLAB/SCK runtime control program. Source-native raw bytes, full prior snapshot, semantic/freshness review and the release acknowledgement remain required under the intake's existing no-merge gate.
