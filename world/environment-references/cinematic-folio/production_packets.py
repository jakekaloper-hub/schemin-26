#!/usr/bin/env python3
"""Compile deterministic production-preparation packets from authoritative Folio inputs.

These are metadata/QA contracts only. They do not contain generative prompts, ask
any image provider to render, or claim publication / cinematic reference approval.
"""
import json
import re
from pathlib import Path


def compile_packets(world, root: Path):
    root = root.resolve()
    zones = {r["id"]: r for r in world["regions"]}
    sites = []
    for loc in world["locations"]:
        card_path = loc["source_location_card"]
        identifier = loc["id"]
        if not re.fullmatch(r"LOC-[A-Z0-9]+(?:-[A-Z0-9]+)*", identifier):
            raise ValueError("Unsafe or malformed location ID")
        expected_card = f"world/location-control-plane/locations/{identifier}/CARD.json"
        if card_path != expected_card:
            raise ValueError("Noncanonical Location Card path: " + identifier)
        source = (root / card_path).resolve()
        if not source.is_relative_to(root) or not source.is_file():
            raise ValueError("Missing or escaped source card: " + identifier)
        card = json.loads(source.read_text(encoding="utf-8"))
        if card["location_id"] != loc["id"]:
            raise ValueError("Card identity mismatch: " + loc["id"])
        zone = zones[loc["physical_zone_id"]]
        scenic = loc["cinematic_asset"]
        if scenic["approved_reference_uri"] is not None or scenic["render_preparation_status"] != "SOURCE_INDEX_ONLY":
            raise ValueError("Unreviewed reference promoted: " + loc["id"])
        sites.append({
            "packet_id": "FOLIO::" + loc["id"] + "::ESTABLISHING",
            "location_id": loc["id"],
            "name": loc["name"],
            "authority": "MAIN_WORLD_ENGINE",
            "status": "SOURCE_INDEX_ONLY",
            "render_permitted": False,
            "approved_cinematic_uri": None,
            "proposed_output_path": scenic["candidate_path_not_a_file"],
            "current_state_as_of": world["world_state_as_of"],
            "source_location_card": card_path,
            "source_card_sha256": loc["source_card_sha256"],
            "structural_reference_uri": loc["structural_reference"]["source_path"],
            "structural_reference_sha256": loc["structural_reference"]["sha256"],
            "region_id": loc["physical_zone_id"],
            "division_overlays": loc["membership_overlays"],
            "home_character_id": loc["home_character_id"],
            "home_team": loc["home_team"],
            "landmarks": loc["persistent_landmarks"],
            "access_route_ids": loc["access_route_ids"],
            "related_route_ids": loc["full_route_ids"],
            "physical_terrain": zone["environment"]["terrain"],
            "climate": zone["environment"]["climate"],
            "movement": zone["environment"]["movement"],
            "weather_relationships": card["weather_relationships"],
            "prohibited_inventions": card["prohibited_inventions"],
            "current_world_state": loc["current_world_state"],
            "historical_event_ids": [e["id"] for e in loc["historical_events"]],
            "next_gate": "EVIDENCE_HYDRATION_AND_VISUAL_ART_DIRECTION",
            "required_quality_controls": [
                "CANON_LOCATION_ID_AND_REGION_LOCK",
                "PHYSICAL_ROUTE_AND_HYDROLOGY_CHECK",
                "TEMPORAL_STATE_AND_HISTORICAL_SOURCE_CHECK",
                "APPROVED_REFERENCE_BYTE_BINDING",
                "INDEPENDENT_PIXEL_AND_RIGHTS_REVIEW_BEFORE_PROMOTION",
            ],
        })
    regions = []
    for region in world["regions"]:
        regions.append({
            "packet_id": "FOLIO::" + region["id"] + "::ESTABLISHING",
            "region_id": region["id"],
            "name": region["name"],
            "authority": "MAIN_WORLD_ENGINE",
            "status": "SOURCE_INDEX_ONLY",
            "render_permitted": False,
            "source_region_path": "world/data/physical_zones.json",
            "physical_terrain": region["environment"]["terrain"],
            "climate": region["environment"]["climate"],
            "movement": region["environment"]["movement"],
            "adjacent_region_ids": region["adjacent_region_ids"],
            "location_ids": region["location_ids"],
            "geography_warning": "Abstract regional bounds; no surveyed shoreline, distance, or sovereign boundary.",
            "next_gate": "GEOGRAPHIC_CONTEXT_AND_PHOTOGRAPHIC_STYLE_BRIEF",
        })
    historical = []
    for event in world["events"]:
        historical.append({
            "source_event_id": event["id"],
            "source_location_id": event["location_id"],
            "source_week": event["week"],
            "classification": event["classification"],
            "evidence_path": "world/data/world_state_events.json",
            "continuity_out": event["continuity_out"],
            "asset_uri": None,
            "render_permitted": False,
            "review_status": "SOURCE_EVIDENCE_ONLY",
        })
    island=world["cross_pr"]["island"]
    return {
        "schema": "schemin.cinematic_folio.production_packets.v1",
        "status": "CODE_ONLY_SOURCE_INDEX_NO_IMAGE_GENERATION",
        "source_world_state_cutoff": world["world_state_as_of"],
        "provenance": world["source_sha256"],
        "location_packet_count": len(sites),
        "region_packet_count": len(regions),
        "locations": sites,
        "regions": regions,
        "historical_event_candidates": historical,
        "island": {
            "authority": "UNMERGED_PR_322_PROPOSAL",
            "source_commit": world["cross_pr"]["source_pins"]["postseason_topology"]["commit"],
            "main_world_mutated": island["main_world_mutated"],
            "node_ids": [x["id"] for x in island["nodes"]],
            "venue_ids": [x["id"] for x in island["venues"]],
            "unresolved": island["unresolved"],
            "render_permitted": False,
            "next_gate": "POSTSEASON_ATLAS_SUPERSESSION_AND_SURVEY_REVIEW",
        },
        "governance": {
            "output_is_image": False,
            "generative_prompts_included": False,
            "state_is_review_only": True,
            "cinematic_approval_count": 0,
            "candidate_paths_are_NOT_existing_assets": True,
        },
    }
