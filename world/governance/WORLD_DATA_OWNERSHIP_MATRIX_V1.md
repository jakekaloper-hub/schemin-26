# WORLD DATA OWNERSHIP MATRIX V1

| Entity / surface | Authoritative store | Derived / view stores | Allowed consumers | Allowed mutator | Rebuild targets |
|---|---|---|---|---|---|
| Physical region | `world/data/physical_zones.json` | Atlas, Location Cards | Atlas, Memo, Novel, Art | governed World mutation | all spatial views |
| Active location | `world/data/locations.json` | Location Cards, travel graph, Interactive Atlas | all world consumers | governed location promotion/update | LCP, references, Atlas, Memo, Novel |
| Route | `world/data/routes.json` | travel graph, packets, Atlas | Atlas, Memo, Novel, Art | governed route mutation | travel graph, venue resolver, all consumers |
| Division overlay | `world/data/divisions.json` | Atlas / packets | all consumers | governed division update | packets and views |
| Owner-domain relation | `world/data/owner_domains.json` | Homeland Cards | Atlas, Memo, Novel, Art | governed world update | homeland packets/views |
| Current world state | `world/data/current_world_state.json` | cards, Atlas, hydration | Memo, Novel, Art | World Evolution apply path | LCP, refs, Atlas, hydration |
| World-state history | `world/data/world_state_events.json` | memory views, packets | Universe, Atlas, Memo, Novel | World Evolution apply path | memory/state consumers |
| Candidate geography | `world/data/atlas_location_candidates.json` | editorial catalog | Bullpen/editorial review | candidate governance only | candidate views |
| Location Card | none; DERIVED | `world/location-control-plane/locations/**/CARD.json` | production consumers | compiler only | regenerated artifact |
| Homeland Card | none; DERIVED | `world/location-control-plane/homelands/**/CARD.json` | production consumers | compiler only | regenerated artifact |
| Travel graph | none; DERIVED CACHE | `living-novel/os/geography/world_travel_graph_v1.json` | Novel, route QA | World/Atlas compiler only | regenerated from routes/locations |
| Structural environment plate | none; DERIVED | `world/environment-references/plates/**` | previs/art | deterministic renderer | regenerated |
| Interactive Atlas | none; VIEW | `world/atlas/interactive/SCHEMIN_ATLAS_INTERACTIVE.html` | humans | builder only | regenerated |
| Canonical World Plate | none; VIEW | production artifact | humans | Art pipeline | never writes upstream |

## Rule
No row may acquire a second independent ACTIVE authority without an explicit architecture migration and acceptance gate.
