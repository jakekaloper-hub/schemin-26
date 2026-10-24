# Atlas route audit correction — 2026-10-14

**Controlling source:** `world/data/routes.json` and `living-novel/os/geography/world_travel_graph_v1.json` on main. The hydrated travel graph contains **23 locations and 24 traversable edges**, derived from **18 route records** with intermediate `via_location_ids` and `via_location_id` stops.

**Correction of the earlier G4 simulation:** A naive endpoint-only graph claimed two Week 4–5 routes to `LOC-SLOB-FOOTHILL-CAMP` were disconnected and six location-route assertions invalid. This was **incorrect**. The existing `ROUTE-HEARTHROAD` contains the camp as an intermediate stop, and other alleged defects similarly use via stops. The canonical World Engine validator already expands these through `route_chain()` / `build_location_graph()`.

Using the hydrated graph, **12/12** Week 4–5 away teams have a structural path to their verified host's home anchor. **0/6** route-access assertions remain invalid when intermediate stops are accounted for. The LLC to Mud Dogs path uses four expanded graph edges. Proposed HMB–TDS neutral grounds remain reachable by both teams.

**Disposition:** G4 structural reachability PASS; route time, weather closures, permits and any world-state transaction are separate checks. **Do not add roads or mutate Atlas geography to 'fix' a nonexistent topology defect.** Earlier simulation documents reporting 5/6 fixture reachability are superseded *for graph-connectivity claims* by this correction. Historical simulation artifacts remain as provenance, not controlling route evidence.

**Mission:** Bullpen #117 / Schemin #166 / PR #167. This correction is source-grounded readback performed during actual mission execution, not an authenticated Director or independent Umpire signoff.
