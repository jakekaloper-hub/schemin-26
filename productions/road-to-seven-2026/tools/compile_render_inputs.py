#!/usr/bin/env python3
"""Compile seven source-locked Road to Seven art jobs; never renders images.

Outputs: folios/RT7-P01..P07/RENDER_INPUT.json
A missing/ambiguous source, unknown character, probability drift or prose identity
raises, rather than producing a noncanonical PNG instruction.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
REVIEW = HERE / "reviews" / "INKLINGS_TWELVE_POV_EDITORIAL_COPY.md"
LIVE = HERE / "evidence" / "FFHUB_LIVE_W11_2026-11-18_SUMMARY.json"
FORK = HERE / "evidence" / "FFHUB_FUTURE_FORKS_2026-11-18.json"
CHAR = REPO / "canon" / "characters" / "APPROVED_LINEUP_2026_10_18.json"

CHOSEN_FUTURE = {
    "Slob on my Dobb": (13, "Dr. Duckhook"),
    "El Niño": (12, "Seven Deadly Chins"),
    "D0nkey K0ng": (12, "ObiWan Jacoby"),
    "His Majesty's Blood": (13, "El Niño"),
    "Dr. Duckhook": (12, "Red Leopards"),
    "Seven Deadly Chins": (12, "El Niño"),
    "Red Leopards": (13, "The Chili Cheesers"),
    "The Chili Cheesers": (13, "Red Leopards"),
    "The LLC": (14, "El Niño"),
    "ObiWan Jacoby": (12, "D0nkey K0ng"),
    "Three Dreaded Snake": (13, "D0nkey K0ng"),
    "Mud Dogs": (12, "Three Dreaded Snake"),
}
CANVAS = {"width":1080, "height":1920, "format":"PNG", "aspect":"9:16"}
LAYOUT = {
    "heading":{"top":42,"bottom":175,"left":50,"right":1030},
    "cinema":{"top":185,"bottom":1280,"left":42,"right":1038},
    "copy_left":{"top":1290,"bottom":1872,"left":52,"right":523},
    "copy_right":{"top":1290,"bottom":1872,"left":557,"right":1028},
    "margin_px":48, "mobile_test_width_px":390,
    "minimum_mobile_body_font_px":11,
    "design_note":"full-resolution typography, contrast tested at 390 px; exact overlays separate from scene raster"
}

def percent(value, places=1):
    quantum = Decimal("1").scaleb(-places)
    return f"{Decimal(str(value)).quantize(quantum,rounding=ROUND_HALF_UP):.{places}f}%"

def hash_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read():
    return (REVIEW.read_text(encoding="utf-8"),
            json.loads(LIVE.read_text(encoding="utf-8")),
            json.loads(FORK.read_text(encoding="utf-8")),
            json.loads(CHAR.read_text(encoding="utf-8")))

def narrative_entries(text):
    matches = list(re.finditer(
        r'^\*\*(Left|Right) / #(\d+) (.*?) — (.*?)\*\*\s*$',
        text, re.MULTILINE))
    assert len(matches)==12, f"Expected 12 unique Inklings POV headings; found {len(matches)}"
    result={}
    for i,m in enumerate(matches):
        rest=text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)]
        paragraph=rest.strip().split("\n\n",1)[0].strip()
        assert 35<=len(paragraph.split())<=100,(m.group(2),len(paragraph.split()))
        seed=int(m.group(2))
        assert seed not in result,seed
        result[seed]={"side":m.group(1).lower(),"team":m.group(3),
                      "headline":m.group(4),"paragraph":paragraph}
    return result

def build(dry_run=False):
    manuscript, live, futures, lineup = read()
    figures={t["team"]:t for t in live["teams"]}
    canon={c["character_id"]:c for c in lineup["individuals"]}
    pov=narrative_entries(manuscript)
    assert len(figures)==12 and len(pov)==12
    assert len(futures["cases"])==10 and futures["run_count"]==20
    outputs=[]
    scene_refs=[]
    for n in range(1,8):
        folder=HERE/"folios"/f"RT7-P{n:02d}"
        scene_path=folder/"scene.json"
        scene=json.loads(scene_path.read_text(encoding="utf-8"))
        assert scene["id"]==f"RT7-P{n:02d}" and scene["artifact"]["width"]==1080 and scene["artifact"]["height"]==1920
        assert scene["lighting_contract"]["method"]=="BAKED_IN_MOTIVATED_LIGHTING_BEFORE_RENDERING"
        art={
          "schema":"schemin.road_to_seven.render_job.v1",
          "state":"ART_DIRECTION_READY_NOT_RENDERED",
          "page_id":scene["id"],"page_title":scene["title"],
          "canvas":CANVAS, "layout":LAYOUT,
          "fixed_time_cutoff":"W10 final, as of 2026-11-17",
          "vendor_capture":"FFHub November 18, 2026, 10,000 simulations",
          "numbers_source":str(LIVE.relative_to(REPO)),
          "writing_source":str(REVIEW.relative_to(REPO)),
          "lighting_and_camera":{"camera":scene.get("camera",scene.get("cover",{}).get("camera")),
                                 "lighting":scene["lighting_contract"],
                                 "specialist_lenses":scene["visual_studio"]["specialist_lenses"],
                                 "directions_source":scene["visual_studio"]["source_document"]},
          "image_generation_policy":{"background":"canon-safe cinematic scenes and motivated lighting",
                 "forbidden_in_generated_raster":"No generated team names, record numbers, source percentages or readable copy",
                 "exact_overlay":"Separate deterministic typography pass after rendering",
                 "must_preserve_identity":"each canonical character crop SHA and Atlas structural plate"},
          "overlays":[],
          "review":{"visual_render":"NOT_RUN","identity_pixel_qa":"NOT_RUN",
                    "text_readability_390px":"NOT_RUN","independent_umpire":"NOT_SIGNED"}
        }
        panels=scene.get("character_panels",[])
        if n==1:
            assert not panels
            art["overlays"]=[{"kind":"cover","title":"THE ROAD TO SEVEN",
                "subtitle":"Twelve Contenders. Seven Berths. One Commonwealth.",
                "facts":"12 CONTENDERS · 7 BERTHS · 4 WEEKS",
                "note":"All twelve mathematically alive and none clinched after Week 10"}]
        else:
            assert len(panels)==2
            for p in panels:
                seed=p["official_week10_seed"]
                assert (seed == (n-2)*2+(1 if p["side"]=="left" else 2)),p
                rec=pov[seed]; assert rec["team"]==p["team"] and rec["side"]==p["side"]
                t=figures[p["team"]]
                for local,source in (("ffhub_baseline_pct","baseline_pct"),("ffhub_w11_win_pct","win_pct"),("ffhub_w11_loss_pct","loss_pct")):
                    assert abs(p[local]-t[source])<0.0001,(seed,local)
                char=canon[p["character_id"]]
                assert char["crop"]==p["approved_crop_path"] and char["home_location_id"]==p["atlas_location_id"]
                image=REPO/p["approved_crop_path"]
                card=REPO/p["atlas_card_path"]; plate=REPO/p["atlas_structural_plate_path"]
                assert image.is_file() and hash_file(image)==p["approved_crop_sha256"]
                assert card.is_file() and plate.is_file()
                assert p["character_id"] in json.loads(card.read_text())["owner_character_ids"]
                wk,op=CHOSEN_FUTURE[p["team"]]
                fork=[x for x in p["selected_future_forks"] if x["week"]==wk and x["against"]==op]
                assert len(fork)==1,(p["team"],wk,op)
                f=fork[0]
                base_decimals=2 if p["team"]=="Mud Dogs" else 1
                if p["team"]=="Mud Dogs":
                    mathnote="Must win all four. Outside help required. Week 11 loss = mathematical elimination."
                else:
                    mathnote="Still alive after a Week 11 loss; no berth clinched at Week 10."
                art["overlays"].append({
                    "kind":"character_pov","side":p["side"],"team":p["team"],"seed":seed,
                    "record":p["week10_record"],
                    "narrative_headline":rec["headline"],"narrative_body":rec["paragraph"],
                    "playoff_probability":percent(t["baseline_pct"],base_decimals),
                    "if_w11_win":percent(t["win_pct"],base_decimals),
                    "if_w11_loss":percent(t["loss_pct"],base_decimals),
                    "future_fork":{"week":wk,"opponent":op,
                                   "if_win":percent(f["if_win_pct"],2),
                                   "if_loss":percent(f["if_loss_pct"],2),
                                   "public_caption":f"W{wk} VS {op.upper()}"},
                    "math_scope_note":mathnote,
                    "character_asset":{"id":p["character_id"],"path":p["approved_crop_path"],
                                       "sha256":p["approved_crop_sha256"]},
                    "atlas_asset":{"id":p["atlas_location_id"],"card":p["atlas_card_path"],
                                   "plate":p["atlas_structural_plate_path"]},
                    "lighting":scene["lighting_contract"][p["side"]]
                })
        output=folder/"RENDER_INPUT.json"
        if dry_run:
            assert output.is_file(), f"missing locked render input {output}"
            assert json.loads(output.read_text(encoding="utf-8")) == art, f"stale or corrupted render input {output}"
        else:
            output.write_text(json.dumps(art,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        outputs.append({"page":scene["id"],"path":str(output.relative_to(REPO)),
                        "characters":len(panels),"copy_fragments":len(art["overlays"])})
        scene_refs.append(hash_file(scene_path))
    index={"compiler_version":"road7-v1","pages":outputs,
           "scene_shas":scene_refs,"manuscript_sha256":hash_file(REVIEW),
           "vendor_summary_sha256":hash_file(LIVE),"future_summary_sha256":hash_file(FORK),
           "warning":"A complete render manifest is NOT proof that final pixels exist or passed art QA"}
    if dry_run:
        manifest = HERE / "RENDER_MANIFEST.json"
        assert manifest.is_file(), "missing frozen render manifest"
        assert json.loads(manifest.read_text(encoding="utf-8")) == index, "source changes require render input regeneration"
    else:
        (HERE/"RENDER_MANIFEST.json").write_text(json.dumps(index,indent=2)+"\n")
    return index

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--dry-run",action="store_true")
    args=p.parse_args();print(json.dumps(build(dry_run=args.dry_run),indent=2))
