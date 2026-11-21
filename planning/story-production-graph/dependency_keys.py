#!/usr/bin/env python3
"""Architect/Setup Man: typed dependency keys for selective invalidation."""

VALID_CLASSES={"BASE","RESULT","CHARACTER","LOCATION","COPY","AUDIO","PRESENTATION"}

def event_base(event_id): return f"{event_id}::BASE"
def event_result(event_id): return f"{event_id}::RESULT"
def character(character_id): return f"CHAR::{character_id}"
def location(location_id): return f"LOC::{location_id}"
def copy(scene_id): return f"COPY::{scene_id}"
def audio(scene_id): return f"AUDIO::{scene_id}"
def presentation(scene_id): return f"PRESENT::{scene_id}"

def classify(key):
    if "::RESULT" in key: return "RESULT"
    if key.startswith("CHAR::"): return "CHARACTER"
    if key.startswith("LOC::"): return "LOCATION"
    if key.startswith("COPY::"): return "COPY"
    if key.startswith("AUDIO::"): return "AUDIO"
    if key.startswith("PRESENT::"): return "PRESENTATION"
    return "BASE"
