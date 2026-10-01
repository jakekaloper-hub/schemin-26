# FIX LOG — Character Reference Portability Mission

1. **Defect:** only 2/12 reference manifests existed.
   **Fix:** normalized all 12 owner manifests with exact source expectations and explicit HOLD state.

2. **Defect:** repository had no executable source-byte integrity audit tied to all 12 approved expectations.
   **Fix:** added `source_byte_integrity.py` and machine registry.

3. **Defect:** mount truth could be represented by booleans without an explicit mounted-byte hash/repository/Git receipt.
   **Fix:** mount contract now requires approved == mounted hash plus durable path/blob/size evidence.

4. **Defect:** renderer capabilities could be asserted without a capability evidence receipt.
   **Fix:** negotiation now requires `evidence_state=PROVEN` + capability receipt.

5. **Defect:** renderer success did not prove which references/bindings actually participated.
   **Fix:** output now requires exact request/route/mount/reference/binding execution receipt.

6. **Defect:** active runtime tests were not covered by a dedicated path-triggered CI workflow.
   **Fix:** added Character Generation Boundary CI.

7. **Defect:** shared Render Adapter candidate did not require the stronger Character-authority receipts.
   **Fix:** candidate profile/validator/tests now require source-integrity, mount and capability receipts.

No fix claims G1 closed.
