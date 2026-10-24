# Memo release-candidate bundles — existing Memo OS staging lane

This folder contains *future* Weekly Memo release candidates, not a new publication authority. It extends the existing Page Production Contract, Publication Fidelity Contract, Release Evidence and publication registry.

## Deterministic bundle path
`memo-os/release-candidates/2026-week-06/issue-manifest.json` and sibling PDF, page master PNGs, immutable FLAIM provider snapshot, and independent image review evidence.

Every claimed `RELEASED` weekly memo for season 2026 Week 6 onward in `governance/publication-manifest/PUBLICATION_MANIFEST_V1.json` requires the corresponding bundle. The `Memo Issue Guardrail Regression` GitHub Action now inspects each bundled manifest when this directory or the publication registry changes. Unrelated historical Week 5 distribution is unaffected.

## Minimum real-candidate evidence
- `issue-manifest.json`: expected page count, PDF relative path, exact SHA256, all unique page slots, master-image paths and SHA256s, declared scores/roles/canon review statuses, release state.
- `provider_receipt_path` and `provider_receipt_sha256`: a separate immutable FLAIM/ESPN retrieval receipt with `league_id`, `week`, `source=FLAIM_ESPN`, `status=FINAL`, and exactly six matchup keys, home/away owners, and final scores. Obtaining the data must occur via the authenticated FLAIM connector; *file labels and hashes alone do not prove provider authentication*. Store retrieval identifier, extraction timestamp and raw-provider provenance in the companion intake register.
- Each page's `review_receipts`: scopes `visual`, `atlas`, `mobile` and (when owner appears) `character`. Require an image file showing actual reviewed artifact, evidence SHA256, page-master SHA256, PDF SHA256, reviewer's ID, decision/time; character reviews additionally bind canonical IDs and the source asset SHA256; Atlas review binds venue ID.
- `umpire_receipt`: distinct review identity, decision, timestamp, and final PDF hash. Umpire must examine the actual pages, not merely insert a PASS string. Recorded claims remain auditable *assertions*, not cryptographic identification or proof of independence absent an authenticated runtime/reviewer audit trail.

## Gate
```bash
python3 -m pip install pymupdf pillow
python3 memo-os/tests/validate_artifacts.py memo-os/release-candidates/2026-week-06/issue-manifest.json
```

**Hard boundary:** Machine validation verifies byte hashes, decodable screenshots, field associations and complete attestations. It does not recognize character likeness, read small raster text, know that a venue is canonical, independently query FLAIM, or cryptographically authenticate a claimed reviewer. Those must be evidenced by Scout, Librarian, World/Atlas Lead, Visual Lead and Umpire using authenticated tools and actual visual inspection. Fake `PASS` receipts are governance violations. No automatic merge/release based on a successful synthetic test.

**No empty fictional placeholders:** Do not add a dummy release candidate that can pass CI. Every candidate is an actual staged publication with immutable source bytes.
