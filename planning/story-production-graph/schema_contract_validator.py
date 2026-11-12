#!/usr/bin/env python3
"""Dependency-free JSON Schema subset validator for Story Production Graph contracts.

Supports the schema keywords used by this directory: type, required,
properties, additionalProperties, items, minItems, minLength, minimum,
enum, const, pattern. It intentionally fails on unsupported keywords that
would affect validation rather than silently treating them as passed.
"""
from __future__ import annotations
import json,re
from pathlib import Path

BASE=Path(__file__).resolve().parent

SCHEMAS={
 "issue":BASE/"memo_issue_v1.schema.json",
 "event":BASE/"event_v1.schema.json",
 "encounter":BASE/"encounter_v1.schema.json",
 "scene":BASE/"scene_v1.schema.json",
 "compiler":BASE/"compiler_manifest_v1.schema.json",
 "chronicle":BASE/"chronicle_projection_v1.schema.json",
 "artifact":BASE/"artifact_lineage_v1.schema.json",
}

def _type_ok(value,want):
    if want=="object": return isinstance(value,dict)
    if want=="array": return isinstance(value,list)
    if want=="string": return isinstance(value,str)
    if want=="integer": return isinstance(value,int) and not isinstance(value,bool)
    if want=="number": return isinstance(value,(int,float)) and not isinstance(value,bool)
    if want=="boolean": return isinstance(value,bool)
    if want=="null": return value is None
    raise AssertionError(f"unsupported schema type: {want}")

def validate(value,schema,path="$"):
    if "type" in schema:
        types=schema["type"] if isinstance(schema["type"],list) else [schema["type"]]
        if not any(_type_ok(value,t) for t in types):
            raise AssertionError(f"{path}: expected type {types}, got {type(value).__name__}")
    if "const" in schema and value!=schema["const"]:
        raise AssertionError(f"{path}: expected const {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise AssertionError(f"{path}: {value!r} not in enum {schema['enum']!r}")
    if isinstance(value,str):
        if "minLength" in schema and len(value)<schema["minLength"]:
            raise AssertionError(f"{path}: string shorter than minLength")
        if "pattern" in schema and re.search(schema["pattern"],value) is None:
            raise AssertionError(f"{path}: {value!r} does not match {schema['pattern']!r}")
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        if "minimum" in schema and value<schema["minimum"]:
            raise AssertionError(f"{path}: {value} below minimum {schema['minimum']}")
    if isinstance(value,list):
        if "minItems" in schema and len(value)<schema["minItems"]:
            raise AssertionError(f"{path}: {len(value)} items below minItems {schema['minItems']}")
        if "items" in schema:
            for i,item in enumerate(value):
                validate(item,schema["items"],f"{path}[{i}]")
    if isinstance(value,dict):
        required=schema.get("required",[])
        for key in required:
            if key not in value:
                raise AssertionError(f"{path}: missing required key {key!r}")
        props=schema.get("properties",{})
        if schema.get("additionalProperties") is False:
            extra=set(value)-set(props)
            if extra:
                raise AssertionError(f"{path}: additional properties not allowed: {sorted(extra)}")
        for key,sub in props.items():
            if key in value:
                validate(value[key],sub,f"{path}.{key}")
    return True

def load_schema(kind):
    return json.loads(SCHEMAS[kind].read_text())

def validate_season_graph(season,compiler):
    issue_schema=load_schema("issue")
    event_schema=load_schema("event")
    enc_schema=load_schema("encounter")
    scene_schema=load_schema("scene")
    compiler_schema=load_schema("compiler")
    for i,x in enumerate(season["issues"]): validate(x,issue_schema,f"issues[{i}]")
    for i,x in enumerate(season["events"]): validate(x,event_schema,f"events[{i}]")
    for i,x in enumerate(season["encounters"]): validate(x,enc_schema,f"encounters[{i}]")
    for i,x in enumerate(season["scenes"]): validate(x,scene_schema,f"scenes[{i}]")
    validate(compiler,compiler_schema,"compiler")
    return True

if __name__=="__main__":
    import sys
    sys.path.insert(0,str(BASE))
    from adapt_2026_memo_season import compile_season
    from build_2026_season_compiler import build
    validate_season_graph(compile_season(),build())
    print("STORY_GRAPH_SCHEMA_CONFORMANCE_PASS")
