# Schemin '26 Capability Map V1
status: PHASE_1_REVIEWED

## Capability domains
| ID | Capability | Primary inputs | Output/control | Failure class |
|---|---|---|---|---|
| TRUTH-01 | live league acquisition/freshness | Flaim/ESPN/gateway | validated league state | P0/P1 |
| TRUTH-02 | historical league reconstruction | verified records | historical ledger | P1 |
| ID-01 | owner/team/alias resolution | canon registry | canonical identity | P1 |
| CHAR-01 | character body/identity canon | character control plane | render identity package | P0/P1 |
| CHAR-02 | reference provenance/mount proof | approved binaries/manifests | renderer-addressable refs | P0/P1 |
| WORLD-01 | geography/venue resolution | World Engine | location/route/world state | P1 |
| WORLD-02 | inhabitant ontology | World Engine | body/world constraints | P1 |
| POV-01 | temporal POV/knowledge | novel state | bounded POV packet | P1 |
| NARR-01 | story architecture | facts/canon/world/POV | narrative treatment | P2 |
| EDIT-01 | Memo editorial | weekly evidence | page/story plan | P1/P2 |
| NOVEL-01 | long-form literary production | history/world/POV | manuscript | P1/P2 |
| VIS-01 | scene visual interpretation | narrative+world+canon | visual brief | P1 |
| VIS-02 | composition/cinematography | visual brief | composition contract | P1/P2 |
| VIS-03 | page/layout hierarchy | copy+art | publication layout | P2 |
| AI-01 | model/provider routing | render contract | generation route | P1 |
| AI-02 | prompt/render compilation | canon/world/story | generation request | P0/P1 |
| AI-03 | generation execution | authenticated refs/request | candidate asset | P1 |
| QA-01 | character identity QA | candidate+refs | pass/reject/review | P0/P1 |
| QA-02 | evidence QA | artifact+truth | factual certification | P1 |
| QA-03 | world/continuity QA | artifact+world/POV | continuity certification | P1 |
| QA-04 | editorial/visual quality QA | artifact+brief | quality certification | P2 |
| PROD-01 | dependency/workflow orchestration | assignment graph | production state | P1 |
| PROD-02 | release assembly | certified artifacts | PDF/release candidate | P1 |
| GOV-01 | independent release control | QA receipts | release ruling | P0/P1 |
| KNOW-01 | provenance/supersession/archive | repo evidence | canonical index | P1 |
| FIRE-01 | Mercer firewall | project boundaries | isolation proof | P0 |
| SPEC-01 | Pittsy's Book/special products | truth+editorial rules | specialized module | P1/P2 |
| LEARN-01 | retrospective/regression learning | incidents/releases | tests/patches | P2 |

## Dependency spine
TRUTH -> ID/CHAR/WORLD/POV -> NARR/EDIT/NOVEL -> VIS -> AI -> QA -> PROD -> GOV -> KNOW/LEARN.

## Phase 1 audit
Double-check: capability set compared against PROJECT_CONTROL_REGISTRY five-plane architecture, Memo OS, World Engine V1.1, Living Novel and Character Control Plane plans.
Bugs:
- ORG-0101 P1: visual work previously collapsed generation mechanics, art direction and identity authority.
- ORG-0102 P2: specialized product capabilities were not explicit in initial plan.
- ORG-0103 P1: reference mounting is a separate capability and must not be hidden inside prompting.
Fix: VIS, AI and CHAR reference capabilities separated; specialized and firewall capabilities added.
Tests: every released subsystem maps to >=1 capability; every production path terminates in independent GOV-01.
Polish: capability names are project functions, not executive titles.
Sign-off: Librarian APPROVED inventory structure; Groundskeeper APPROVED production coverage; Scout APPROVED truth plane; Beat Writer APPROVED narrative coverage; Pitching Coach APPROVED AI separation; Umpire APPROVED governance coverage.
