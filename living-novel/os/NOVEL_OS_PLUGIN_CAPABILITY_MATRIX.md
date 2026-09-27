# NOVEL OS PLUGIN CAPABILITY MATRIX
**Status:** PHASE-2 AUDIT — 2026-09-27

| Capability | Provider | Purpose | Input | Output | Canon authority | Write authority | Failure mode | Fallback | Installation | Recommendation |
|---|---|---|---|---|---|---|---|---|---|---|
| repository control | GitHub | durable OS/code/docs | repo state | commits/files/CI | none itself | repo writes | API/auth/index failure | last-known-good repo + local artifact | connected/available | ADOPT core |
| visual generation | Higgsfield | image/video prototypes and production | briefs + refs | media | zero | media workspace | model/reference drift | native image generation / alternate adapter | installed | ADOPT adapter |
| visual generation | OpenArt | alternative models/reference workflows | briefs + refs | image/video | zero | media workspace | provider/model drift | Higgsfield/native | not installed | OPTIONAL |
| cinematic/video | Runway | motion prototypes, edits, multi-shot | visual packets | video/image/audio | zero | media workspace | credits/provider | Higgsfield | not installed | OPTIONAL later |
| creative finishing | Adobe | retouch/layout/PDF/asset workflows | approved assets | finished assets/docs | zero | Adobe workspace | account/tool availability | local artifact tools | not installed | OPTIONAL publishing |
| knowledge/project workspace | Notion | human-facing planning/knowledge | registries/tasks | pages/db | zero | workspace | duplication/drift | GitHub canonical records | not installed | REJECT as core; optional mirror |
| project tracking | Linear | engineering issues/releases | OS backlog | issues/projects | zero | workspace | drift from repo | GitHub issues/docs | not installed | OPTIONAL |
| project tracking/docs | ClickUp/Coda | workflow dashboards | project state | tasks/docs/tables | zero | workspace | duplicate truth | GitHub | not installed | REJECT core |
| Drive/docs | Google Drive | source/reference retrieval and sharing | user files | docs/files | evidence only | Drive when authorized | sync/version ambiguity | GitHub/source registry | available | ADAPT as source ingress |

## Authority rule
Plugins provide capabilities, not truth. Plugin output enters Novel OS as SOURCE, GENERATED_ASSET, or WORKFLOW_EVIDENCE and is promoted only through Novel OS gates.

## Installation ruling
No new SaaS/plugin is required to proceed. Existing GitHub + Higgsfield/native capabilities cover the immediate OS and Prologue workload. Optional providers should be connected only when a concrete production requirement justifies the dependency.
