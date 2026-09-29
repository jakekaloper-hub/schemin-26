# CCP v2 Consumer Adapter Contract — R11
Consumers: Weekly Memo OS, Chronicles, Living Novel, Live Looks, Xcode/app.

Public interface only:
1. resolve(query)
2. compile_contract(query, layers, scene)
3. QA policy evaluation
4. publication_receipt()

Forbidden:
- reading legacy Master Canon as runtime identity source;
- copying character dictionaries into consumers;
- deriving anatomy from team names;
- treating weekly POV/story state as identity;
- generating character-bearing art when contract.render_ready=false.

Migration: existing CCCP integration contracts remain compatibility shims until R12 shadow run passes. New consumer code should target v2 compiled contract/receipt rather than raw files.
