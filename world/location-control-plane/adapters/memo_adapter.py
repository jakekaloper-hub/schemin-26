#!/usr/bin/env python3
from pathlib import Path
import sys
COMPILER = Path(__file__).resolve().parents[1] / "compiler"
sys.path.insert(0, str(COMPILER))
from location_control_plane import compile_world_packet, resolve_homeland

def compile_memo_location_packet(location_id, character_ids=None, event_class="REGULAR", sublocation_handle=None, home_character_id=None):
    packet=compile_world_packet(location_id,character_ids or [],"MEMO",event_class,sublocation_handle,home_character_id,False)
    if packet.get("status") in {"READY_FOR_SEMANTIC_QA","READY_FOR_RENDER"}:
        packet["memo_adapter"]={
            "venue_lock_required":True,
            "world_state_lock_required":True,
            "post_release_writeback":"Scout/Librarian/Architect classification required for any new evidence."
        }
    # Additive, read-only civilization context; never elevates semantic QA to publication.
    if packet.get("status") in {"READY_FOR_SEMANTIC_QA", "READY_FOR_RENDER"}:
        from pathlib import Path
        import sys
        root = Path(__file__).resolve().parents[3]
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from world.engine.civilization_consumers import resolve_scene_context
        context = resolve_scene_context(location_id, "memo")
        if not context.get("ok"):
            packet["status"] = "HUMAN_REVIEW_REQUIRED"
            packet.setdefault("review_blockers", []).append("CIVILIZATION_CONTEXT_UNRESOLVED")
        else:
            packet["civilization_context"] = context
            packet["civilization_context_status"] = "INTERPRETIVE_NON_PROMOTING"
    # Bind actual Commissioner-approved visual, physical and spatial identity
    # evidence through the existing Character Canon resolver. This is NOT a
    # permit to create, submit, or publish generated character artwork.
    if character_ids:
        from canon.characters.runtime.reference_authority import resolve_approved_lineup_presentation
        visual = resolve_approved_lineup_presentation(character_ids)
        if visual.get("state") != "COMMISSIONER_APPROVED_VISUAL_PRESENTATION_EVIDENCE":
            packet["status"] = "HUMAN_REVIEW_REQUIRED"
            packet.setdefault("review_blockers", []).append("CHARACTER_VISUAL_PRESENTATION_UNRESOLVED")
            packet["character_visual_authority"] = {
                "state": "GENERATION_BLOCKED",
                "reason": visual.get("reason", "UNRESOLVED"),
            }
        else:
            # Runtime spatial/morphology coherence, not merely downstream docs.
            subjects = visual["subjects"]
            bad = []
            for subject in subjects:
                homeland = resolve_homeland(subject["character_id"])
                if homeland.get("status") != "CURRENT_HOMELAND_RESOLVED":
                    bad.append(subject["character_id"])
                    continue
                home = homeland["homeland"]
                anchor = subject["spatial_anchor"]
                physical = subject["physical_constraints"]
                if (anchor.get("home_location_id") != home.get("primary_location_id")
                    or set(anchor.get("region_ids", [])) != set(home.get("physical_zone_ids", []))
                    or not physical.get("anatomy_constraints")
                    or not subject["presentation"].get("negative_rules")):
                    bad.append(subject["character_id"])
            if bad:
                packet["status"] = "HUMAN_REVIEW_REQUIRED"
                packet.setdefault("review_blockers", []).append("CHARACTER_PHYSICAL_SPATIAL_CANON_MISMATCH")
                packet["character_visual_authority"] = {
                    "state": "GENERATION_BLOCKED", "character_ids": bad
                }
                return packet
            packet["character_visual_authority"] = visual
            packet["character_visual_authority_status"] = "VERIFIED_APPEARANCE_ONLY"
            packet["character_rendering_eligible"] = False
            packet["visual_render_release_gate"] = "C1_T15_T16_AND_PROVIDER_SOURCE_BINDING_HOLD"
            packet["character_physical_constraints"] = {
                v["character_id"]: v["physical_constraints"] for v in visual["subjects"]
            }
            packet["character_spatial_anchors"] = {
                v["character_id"]: v["spatial_anchor"] for v in visual["subjects"]
            }
            # Preserve LCP's original location-specific relationships and
            # require that approved character's registered home ID is sound.
    return packet
