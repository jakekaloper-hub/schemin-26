# Mud Dogs shoreline controlled physical-GPU comparison

Original source-only observer builds, baseline 4a83b39e and refined 587ff7a2.
See inspection.html for the side-by-side originals and comparison.json for exact metrics.
Synthetic Eastern noon, global calm, paused ordinary water at phase zero.
This is candidate engineering evidence, not approved art or live weather.

From the repository root, run the verifier:
```sh
node productions/audience-site/preview/evidence/gpu-mud-dogs-shoreline-comparison-587ff7a2-20261125/verify.mjs
```

To recreate the capture tool in a disposable checkout of 587ff7a2, copy
preview/tools/temple-static-capture.mjs to a new file in the same tools directory.
Apply capture-preset.patch to that copy (patch accepts an explicit target file).
The resulting SHA-256 must match comparison.json. Use the original tool's
arguments with preset mud, a new output directory and the expected exact source
SHA. Build each observer from its corresponding exact source revision using the
existing pinned dependency and source-only build instructions in preview/README.md.
Never overwrite the retained original captures. The historic capture tool is unchanged.
