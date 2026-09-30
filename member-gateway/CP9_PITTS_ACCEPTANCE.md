# CP9 — Pitts Member Acceptance

**Status:** IMPLEMENTATION / CONTROLLED ACCEPTANCE HARNESS

## Member job
Pitts asks his AI for **Pittsy's Book inputs**. He does not need to know Director names, SCK, Data Gateway internals or repository paths.

The member-facing surface:
1. authenticates the delegated client;
2. discovers only permitted semantic jobs;
3. invokes `pittys_book.inputs`;
4. returns validated shared league inputs with freshness, limitations and authority/QA state;
5. explains BLOCKED and STALE states in member language;
6. suppresses duplicate execution through the existing run ledger.

## Ownership boundary
Schemin owns shared league truth/context and governed outflow. Pittsy's Book owns handicapping, lines, odds, wagers, ledger and presentation. No Pittsy proprietary model is imported into Schemin by this checkpoint.

## Important limitation
This is the real **Pitts identity/capability path inside the repository acceptance harness**, not yet a connection to Pitts's separate ChatGPT account/client. External account connectivity requires a deployed authenticated transport and Pitts's explicit connection action. CP9 must not claim that external connection exists until it does.
