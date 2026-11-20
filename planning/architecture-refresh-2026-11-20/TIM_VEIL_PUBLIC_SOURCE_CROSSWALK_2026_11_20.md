# Tim Veil method-lens source crosswalk — verified repository roots

**Observation date:** 2026-11-20. **Mode:** public-source technical pattern study only. Not a personal consultation, endorsement or reproduction permission for individual files. This supplement supports the 18-Director / 216-question docket.

| Source | Verified public evidence | Proposed narrow use | Boundary |
| --- | --- | --- | --- |
| [timveil/bloviate](https://github.com/timveil/bloviate) | Current default branch `main`. README describes deterministic test fixtures from database schema, with foreign-key awareness, seeded reproducibility and no copy of production rows. Root `LICENSE`: Apache-2.0. | Adapt the *method* of seeded synthetic fixtures to world-state/ESPN alias/schema negative tests. | Java/JDBC is not a reason to import a Java stack; never use fictitious fixture data as league truth. |
| [timveil/benchbase](https://github.com/timveil/benchbase) | Current default branch `main`. README expressly credits upstream CMU-DB/OLTPBenchmark framework and uses JDBC workloads; root license Apache-2.0 (copyright OLTPBenchmark Project). | Adapt fixed workload/repeatable before-after benchmarking for Bullpen and World Evolution. | Source is a fork; Tim cannot be credited as sole original author. Do not import SQL load generator into our JS/Python runtime. |
| [timveil/leaves-of-blocks](https://github.com/timveil/leaves-of-blocks) | Current default branch `main`. README shows Swift/iOS CI, privacy-first product practices; root MIT license. | Examine mobile smoke tests, privacy defaults and product-quality release habits. | Different app/platform; UX patterns require evidence that they suit Schemin's browser viewer. |
| [timveil/gcloud-menu-bar](https://github.com/timveil/gcloud-menu-bar) | Public current default branch `main`. Existing Bullpen source ledger found no root LICENSE at checked location. | Study credential-state UX as an abstract design problem. | **NO CODE COPY** until file-level license and security review. |

## Questions to technical method lens
- How would the **fixture methodology** make current World Evolution approval/chronology regressions harder to miss?
- How should a **frozen workload** establish a performance baseline before a claimed improvement?
- Which integration seam is best addressed by **small interfaces**, not a new OS or a global ID server?
- What explicit tests disprove candidate implementations under the one-world and zero-incremental-spend laws?

## Provenance and limits
The Bullpen's authoritative detailed source work remains `docs/advisors/TIM_VEIL_ADVISORY_LENS_V1.md`, `research/advisors/tim-veil-github-inventory-2026-10-09.json`, and `research/advisors/TIM_VEIL_18_DIRECTOR_OPPORTUNITY_REVIEW_V1.md`. Repository descriptions and root licenses are **not** a transitive license/security audit of dependencies or every source file. Any generated advice is synthetic and must face the owning Director, Librarian, Warden, and independent Umpire.
