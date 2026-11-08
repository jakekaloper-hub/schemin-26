# Schemin Unreal Bridge — prototype v0.1
Local-only fail-closed preview manifest validator. No actual Unreal data import yet.
Tests use explicitly synthetic IDs and SHA values; they are not canonical world records.
A future World Engine-owned exporter must verify source records before issuing evidence receipts.
Never promote PREVIEW to canon or write Unreal edits back to the authoritative repo.
Run: python3 -m unittest discover -s ScheminBridge/tests -v
