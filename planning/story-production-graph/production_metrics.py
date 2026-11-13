#!/usr/bin/env python3
"""Analyst lane: measurable Story Production Graph quality metrics."""
from __future__ import annotations

def coverage(events, encounters, scenes):
    event_ids={e["event_id"] for e in events}
    encounter_events={e["event_id"] for e in encounters}
    scene_events={s["event_id"] for s in scenes}
    return {
      "events":len(events),
      "encounters":len(encounters),
      "scenes":len(scenes),
      "event_to_encounter_coverage":round(len(event_ids & encounter_events)/len(event_ids),4) if event_ids else 1.0,
      "event_to_scene_coverage":round(len(event_ids & scene_events)/len(event_ids),4) if event_ids else 1.0,
    }

def reuse_metrics(scenes):
    anchors=sum(len(s["location"].get("persistent_anchors",[])) for s in scenes)
    unique_locations={s["location"]["location_id"] for s in scenes}
    unique_events={s["event_id"] for s in scenes}
    return {
      "scene_count":len(scenes),
      "unique_locations":len(unique_locations),
      "unique_events":len(unique_events),
      "persistent_anchor_references":anchors,
      "average_anchor_reuse_per_scene":round(anchors/len(scenes),2) if scenes else 0,
    }

def risk_metrics(events, scenes):
    return {
      "provisional_events":sum(e["authority"]["evidence_status"]!="VERIFIED" for e in events),
      "accepted_events":sum(e["authority"]["canon_status"]=="ACCEPTED" for e in events),
      "world_writeback_enabled":sum(bool(e["state"].get("world_writeback_allowed")) for e in events),
      "accepted_scenes":sum(s["qa"]["publication_state"]=="ACCEPTED" for s in scenes),
    }

def report(events,encounters,scenes):
    return {
      "coverage":coverage(events,encounters,scenes),
      "reuse":reuse_metrics(scenes),
      "risk":risk_metrics(events,scenes),
    }
