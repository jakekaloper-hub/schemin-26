# Commonwealth Visual Library — Review Candidate

This is an **internal review-only** static library, not a public deployment. Start an HTTP server from the **repository root** (for example: `python3 -m http.server 8000`) and visit `/docs/visual/`. Do not open the HTML by `file://` because the manifest fetch requires HTTP.

The registry currently contains 12 character crop records extracted directly from `canon/characters/APPROVED_LINEUP_2026_10_18.json`. Relative image/source paths point into the existing repository. Expected SHA values have **not** been independently rehashed. Commissioner approval covers that exact lineup presentation, not renderer binding, canonical primary asset promotion or independent QA. Source status remains HOLD.

Do not deploy this library publicly without a privacy and approval audit. Other Memo, Atlas and Novel collections are **not yet indexed**. Missing image previews are surfaced, not substituted. No canon or source assets have been changed.

QA prerequisites before promotion: validate existence and SHA-256 of all actual bytes; run browser responsive/accessibility tests; reconcile approval scopes and privacy; run canonical suite; obtain independent Umpire acceptance.

## Commonwealth Command Center (CVI-001)

Run `python3 docs/visual/build_command_center.py` from the repository root whenever its canonical input sources change. This regenerates `docs/visual/index.html` and `docs/visual/command-center.json` from 24 source references in six environments. The prior character gallery is preserved at `docs/visual/characters.html`.

This is a source-index implementation, **not 24 fully operational dashboards**. A source being present is not proof of active/runtime or released status. The current source presentation may include repository-internal information and must not be deployed publicly without an access review. Independent design, browser, accessibility, and security acceptance remain open. The generator has no external API dependencies and makes no source modifications.

Local Mac HTTPS can be served from an isolated checkout using the existing developer-only Python TLS server on loopback. The local certificate and private key must remain outside the public Git repository. No public deployment is implied by localhost availability.
