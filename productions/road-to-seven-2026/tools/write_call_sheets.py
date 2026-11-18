#!/usr/bin/env python3
"""Create source-derived cinematography call sheets for seven Road to Seven folios."""
from pathlib import Path
import json,sys
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
manifest=json.loads((BASE/"STAGING_MANIFEST.json").read_text())
bench=json.loads((ROOT/"memo-os/cinematography/PRODUCTION_SPECIALIST_REFERENCE_BENCH_V1.json").read_text())
scenes=[json.loads((ROOT/item["staging_path"]).read_text()) for item in manifest["staging"]]
lines=[
"# THE ROAD TO SEVEN — The Twelve: Studio Call Sheets","",
"**Status:** Film-staging preproduction; source-backed, no PNG generated. The actual project Visual Direction Lead, Atlas, Character Librarian and Editorial Designer retain authority. Umpire acts only on genuine artifacts.","",
"The named crew profiles below are PUBLISHED-METHOD REFERENCE LENSES, not participating human professionals, and do not endorse or approve this work.","",
"## Full twelve-member production-specialty desk","",
"| Practitioner method lens | Accountable practical task | Direct pages |",
"|---|---|---|"]
for r in bench["profiles"]:
    role=next(x for x in scenes[0]["staging_crew"] if x["reference_profile"]==r["name"])
    pages=[x["page_id"] for x in scenes if next(y for y in x["staging_crew"] if y["reference_profile"]==r["name"])["direct_page_assignment"]]
    lines.append(f'| {r["name"]} ({r["domain"]}) | {role["concrete_assignment"]} | {", ".join(pages)} |')
lines+=["","## El Niño: Seven-page weather continuity spine","",
"**World source:** World Engine V1.1 and world/data/weather_regions.json. The loaded persistent world-state record is only as of end_of_week_3_2026; there is no validated Week 10 global storm event in that record. These are deliberate artistic weather stage directions, NOT a canon promotion.",
"",
"- Direct manifestation: El Niño appears embodied at Storm Bowl on RT7-P02. His blue-water/orange-heat human elemental design remains visible.",
"- Eastern storm sources: His Majesty's Blood's keep, Red's jungle ruins and LLC's maritime boardroom can show local coastal weather potential; a visually evocative rain/wind event is NOT automatically proven as El Niño.",
"- Propagation: Slob and D0nkey K0ng in Upper Valleys, ObiWan mountain, and Chins in Central Basin can carry distant cloud/pressure hints, without asserting flooding or road closure.",
"- Separate southern watershed: Duckhook's golf course, Snake's temple and Mud Dogs' swamp can have humidity, river spray and hydrological water independent of Niño.",
"- Western rain shadow: Chili's stable stays dry and dusty; there is no automatic rain event crossing into his homeland.",
"- The cover uses atmospheric pressure as a metaphor across existing biomes, not a literal continuous view or new permanent portal system.","",
"## Full-seven static film call sheets",""]
for s in scenes:
    lines.extend([
      f'### {s["page_id"]} — {s["page_title"]}',"",
      "**Camera and lens:** "+s["camera"],"",
      "**Editorial seam:** "+s["graphic_transition"],"",
      "**Implied sound/action cue:** "+s["sound_implied_only"],"",
      "**Directly selected specialist lenses:** "+
        ", ".join(x["reference_profile"]+" ("+x["domain"]+")" for x in s["staging_crew"] if x["direct_page_assignment"])+".",""])
    if s["page_id"]=="RT7-P01":
        c=s["cover_staging"]
        lines.extend(["**Cover set:** "+c["set"],"**Weather:** "+c["weather_cue"],"**Staging:** "+c["pose"],""])
    else:
        for x in s["characters"]:
            z=x["approved_costume_visual"]
            lines.extend([
             f'**{x["side"].upper()} — #{x["seed"]} {x["team"]} — {x["location_id"]}**',"",
             "- **Set:** "+x["physical_set"]+". Atlas anchors: "+", ".join(x["anchor_landmarks"])+".",
             "- **Blocking and character POV:** "+x["pose_action"]+".",
             "- **Dress/wardrobe:** "+x["shoot_costume_dressing"]+". Approved morph: "+z["subject_morphology"]+". Palette: "+", ".join(z["palette"])+".",
             "- **Weather:** "+x["weather_exposure"]+". Attribution: "+x["el_nino_attribution"]+". "+x["el_nino_note"],
             "- **Lighting:** KEY "+x["motived_lighting"]["key"]+"; FILL "+x["motived_lighting"]["fill"]+"; RIM "+x["motived_lighting"]["rim"]+"; AIR "+x["motived_lighting"]["air"]+".",
             "- **Avoid:** "+"; ".join(z["negative_rules"])+".",""])
    lines.extend(["**Shot acceptance:** Viewer should recognize both locations and character morphologies before reading any caption. Light must be motivated; equal subject prominence and two clear text zones. This call sheet does not prove a rendered image.",""])
lines += ["## Editorial assembly / production safeguards","",
"1. Cover: symbolic twelve roads/seven places, sunrise; no champion revealed.",
"2. Summit: warm rough foothills versus blue/orange humanoid storm presence at eastern Storm Bowl.",
"3. Pursuit: all four DK lower legs and giant axe silhouette versus shadowed hood/eye red glow at storm keep.",
"4. Threshold: preserved golf-club historical stains versus Chins in Central Basin commons, no new destruction.",
"5. Seventh Gate: Red's humid Eastern Forest ruins versus Chili's dusty brown-hat Western stable and Dark Horse.",
"6. Long Road: LLC's historically scarred harbor boardroom versus ObiWan's ridge with green blade and retriever.",
"7. Against the Impossible: three heads sharing one armored reptilian body and one four-legged swamp-hound with chains; independently hydrological wetland mist.",
"",
"Exact lettering, records, and vendor probabilities must come from deterministic render inputs, never be retyped by a generative image model. The captured FFHub cohort for on-image publication is November 18. Visual QA of images remains NOT RUN.",
"",
"**Critical source conflict:** The October 18 character presentation approves a four-legged Arsenal gorilla-centaur for DK, while his historical primary file remains a different bipedal visual and has not been formally superseded. Use the October 18 presentation only as scene styling; do not claim final artist/reference-binding clearance without resolving that registered conflict.",
"",
"## Pending honest release checks","",
"Film render and source subject attachment; identity by pixel-level inspection; subject/body/costume/landmark continuity; light contrast at native and 390px scales; exact percentages/records after overlay; Umpire source + raster review; Founder release. All unperformed."
]
text="\n".join(lines)+"\n"
dest=BASE/"STUDIO_CALL_SHEETS.md"
if "--dry-run" in sys.argv:
    assert dest.exists() and dest.read_text()==text,"Missing or stale film call sheets"
else:dest.write_text(text)
print(json.dumps({"pages":len(scenes),"specialists":len(bench["profiles"]),"chars":len(text)}))
