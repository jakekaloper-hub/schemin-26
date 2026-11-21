#!/usr/bin/env python3
"""Build seven Road-to-Seven staging contracts from canonical character + Atlas records.
Production proposals are NON-CANON and DO NOT render images or change the World Engine.
"""
import json,hashlib,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[3]
BASE=ROOT/"productions/road-to-seven-2026"
SCENES=BASE/"folios"
WORLD=ROOT/"world"
CANON=ROOT/"canon"
CREW=ROOT/"memo-os/cinematography/PRODUCTION_SPECIALIST_REFERENCE_BENCH_V1.json"
THEME="El Niño's atmospheric motif follows Atlas climate causality; not every storm is El Niño"
roles={
 "Doug Chiang":{"pages":[1,3,6],"task":"Production-design scale hierarchy, anchor architecture, shape language for symbolic cover, Highland keep and boardroom/mountain split"},
 "Dylan Cole":{"pages":[1,2,5,7],"task":"Atlas-aware geography/biome design; separate Eastern coast, Upper Valleys, Western dry range and Southern Wetlands"},
 "Joe Letteri":{"pages":[2,3,5,7],"task":"Character-specific morphology and weather-light interaction; verify Niño human elemental, DK centaur, spotted Red and three heads"},
 "Ngila Dickson":{"pages":[2,3,4,5,6],"task":"Costume continuity from approved Oct 18 image delta; fabric wetness and period materials without redesign"},
 "Andy Serkis":{"pages":[2,4,5,7],"task":"Express physical emotional intentions through gaze/weight/gesture; distinct POVs, no declared game outcome"},
 "Rob Alonzo":{"pages":[3,4,5,6,7],"task":"Grounded contact points and action axes; swords/axes/clubs/tack must respect anatomy and set safety"},
 "James Baxter":{"pages":[2,4,5,7],"task":"Readable silhouette and separate emotion at phone scale; confirm no species morphing"},
 "Frank Masi":{"pages":[1,2,3,4,5,6,7],"task":"Lens height, frame depth and decisive still moment on every folio; no repetitive generic hero-pose"},
 "John Knoll":{"pages":[1,2,3,4,5,6,7],"task":"Two-location composite seam, lighting/plate passes, exact source-bound render inputs, deterministic typography pipeline"},
 "Jill Bogdanowicz":{"pages":[1,2,3,4,5,6,7],"task":"Color and exposure management; atmosphere/light continuity WITHOUT imposing identical storms in each region"},
 "Thelma Schoonmaker":{"pages":[1,2,3,4,5,6,7],"task":"Seven-page editorial sequence and visual rhythm; action direction and story-pacing escalates to final survival stakes"},
 "Randy Thom":{"pages":[1,2,3,4,5,6,7],"task":"Sound-implied visual cues: water roar, cloth flutter, axe impact risk, gravel scrape, horse tack, marsh sucking; no audio generation"}
}
cards={
2:{"camera":"36mm full-height diagonal editorial diptych, medium-low Slob and wide 3/4 Niño; each face readable; separate distant horizons","left":{"pose":"Slob grips an oversized SLOB keg as a weight at the rough training ground, one boot planted in the dirt; studies a marked six-week route on training slate","set":"Tailgate yard + rough training ground; original timber/metal gear, no new tower","costume":"Work overalls, backward cap, bare shoulders, beard and huge keg; do not substitute generic knight armor","weather":"EAST_PROPAGATION_POSSIBLE","weather_cue":"Possible distant coast-sourced high cloud behind northern foothills; light breeze moves canvas, NO proven storm arrival or road damage"},
"right":{"pose":"El Niño stands embodied at weather-exposed Storm Bowl service counter; one arm braces against sea spray, the other gathers controlled water/light; no lightning strike on opposing characters","set":"Weather-exposed venue and service counter remain visible against rocky coast","costume":"Long dark hair and beard, bare muscular torso, blue water flank, orange thermal flank and chest emblem, not a faceless cloud","weather":"EMBODIED_AT_STORM_BOWL","weather_cue":"Direct visible embodied weather system contained to his own source venue; cloud pressure and spray respond locally, not across all biomes"},"cut":"Cloud-gap diptych joined only by graphic pressure isobar; distinct Upper Valleys and Eastern Storm Coast","sound":"keg metal scrape against training dirt / shoreline spray and thunder muted over Storm Bowl"},
3:{"camera":"28mm low near-training-court horse-body wide on left; 50mm upward keep threshold close-medium on right; do not crop DK hind legs","left":{"pose":"D0nkey K0ng plants all four equine limbs on Highland training court, cannon heraldry and axe held low, stepping toward road approach","set":"Actual highland stronghold, existing training court and road approach, no invented victory dais","costume":"ONE fused gorilla-centaur, broad black-fur upper body and four equine legs, red/gold Arsenal war cloth and big axe; no horse rider","weather":"EAST_PROPAGATION_POSSIBLE","weather_cue":"Thin distant passing clouds and ridge-edge wind; no northern blizzard, no event-specific coastal flood"},
"right":{"pose":"HMB guards the established dark keep threshold, ornate sword tip down, chest medallion visible; Belt remains rightful artifact, no raising it in victory","set":"Existing dark keep/championship hall entrance; weather-sheltered stone threshold","costume":"Hood obscures face except two red eye glows, segmented black iron, crimson-black cloak, gold chest ornament and downward ornate sword","weather":"EAST_STORM_SOURCE_LOCAL","weather_cue":"Wind whips cloak on storm-exposed Eastern Coast, dim moisture/spray on parapet; storm is physically possible, not automatically El Niño"},"cut":"Two architectural thresholds in separate zones with matched stone visual direction, no fantasy bridge across long geography","sound":"four hoof impacts and axe strap / wet cloak and distant coastal gale"},
4:{"camera":"55mm ground-level fairway geometry left; 40mm off-axis roadside shot right to make physical comedy readable","left":{"pose":"Duckhook sights down a golf driver over an unswung ball; green vest and white duck bill unobscured, quietly recalculating approach","set":"Country Club clubhouse, green and water hazards; retain historical Week3 chili contamination as unresolved, never pristine-reset by default","costume":"White-feathered duck head orange bill, green golf cap, green vest, club driver, not a human golfer or generic bucket-hat duck","weather":"INDEPENDENT_SOUTHERN_HYDROLOGY","weather_cue":"Humid morning, dew and independently sourced wetland water-hazard haze; NOT asserted to be caused by Niño"},
"right":{"pose":"Seven Deadly Chins steps out of the road commons BBQ yard gripping metal tool but NOT swinging into buildings; grimacing toward coming Mud matchup","set":"Roadside hall, BBQ yard and caravan court with grounded trucks/canvas; no new destruction","costume":"Very heavyset human with multiple folded chins, red trucker cap, dark glasses, dirty tank/overalls and blunt metal tool","weather":"CENTRAL_BASIN_PROPAGATION_POSSIBLE","weather_cue":"Weak distant banked cloud over Central Basin, hard afternoon sun/dust in local road; no arbitrary flood"},"cut":"Green curvature and asphalt roadside edge align graphically, not physically adjacent","sound":"golf-ball stillness and light clubhouse wind / distant rattling truck and scraping metal"},
5:{"camera":"40mm crouched predatory view through old ruin stones left; 50mm stable doorway profile with horse depth right","left":{"pose":"Red Leopards crouches on a known jungle ruin approach, spear pointed DOWN as a guarded line, eyes scanning routes; not physically fighting Chili yet","set":"Established jungle ruins and predator banners; preserve old stone and terrace without inventing new destruction/repair","costume":"Red coat with black spots, actual feline muzzle, leather/metal shoulder armor and spear, no human face or plain gold cat","weather":"EAST_STORM_SOURCE_LOCAL","weather_cue":"Localized wet leaf sheen, wind shifting predator banners and heavy cloud at Eastern Forest/Storm Coast; plausible regional weather, attribution to Niño unproven"},
"right":{"pose":"Chili puts one hand on the Dark Horse's tack outside stable, other on gate latch, turning toward a dusty road where Red will wait in W13","set":"Real Chili stable, Dark Horse enclosure and pit smoke; never magical neighboring Red ruins","costume":"Human outlaw, BROWN cowboy hat, rust/red-orange shawl, western leather, Dark Horse as SEPARATE companion; not a generic sheriff","weather":"WESTERN_DRY_RAIN_SHADOW","weather_cue":"Golden dry light, slow pit smoke and windborne dust. A faint distant far-east cloud is only an atmospheric hint; no rain or Niño flood here"},"cut":"A graphic diagonal seventh-place threshold separates humid dark green rainforest from hot dry stable amber, not a physical border","sound":"spear leather creak, dripping leaves / horse tack jingles and stable boards"},
6:{"camera":"50mm seated desk/ledger interior left, 35mm mountain lookout low perspective right, balanced similar subject size","left":{"pose":"The LLC sits in executive chair marking a ledger, cigar held away from paper, expensive suit sleeves and red tie recognizable; not crowned","set":"Executive chamber, trade ledgers, harbor market overlook; remember Week2 damage/repair unknown, never pristine reset","costume":"Well-groomed human executive, dark tailored suit, RED tie, dark sunglasses, gold accents, cigar/briefcase and chair","weather":"EAST_STORM_SOURCE_LOCAL","weather_cue":"Harbor storm-glow through window, possible moisture on glass; no new roof blowout or flooding, old Week3 storm memory belongs Storm City history"},
"right":{"pose":"ObiWan stands on high-ridge war-room overlook with green energy blade angled low pointing toward next road, golden retriever alongside near stone steps","set":"Trade Jedi Mountain Base high ridge and war-room overlook, no new ceremonial Belt pedestal","costume":"Blond human strategist in earth-tone robes, green energy sword, GOLDEN RETRIEVER companion; Belt expressly forbidden","weather":"EAST_PROPAGATION_POSSIBLE","weather_cue":"Windswept mountain clouds and distant eastern storm bank beyond intervening ridges only if visibility supports it; not guaranteed see Storm Bowl"},"cut":"Editorial graphic transition from harbor-window rain reflection to mountain air; different horizons, no direct line of sight","sound":"quiet ledger pages, harbor shutter / mountain cloth and footstep with dog pads"},
7:{"camera":"48mm wet stone eye-level on three-headed Snake left, low 32mm grounded swamp quadruped full-body shot on right","left":{"pose":"One armored humanoid torso and exactly THREE living snake heads look in distinct directions while body moves DOWN one established temple step; post-haircut heads","set":"Podium Shadow Waterfall Temple waterfall/temple stone/dense vegetation; no new shrine, family event or building collapse","costume":"Three serpent heads on one reptilian armored HUMANOID torso, bronze scales/moss/dark leather, weapons below; do not restore pre-haircut long dreads","weather":"INDEPENDENT_SOUTHERN_HYDROLOGY","weather_cue":"Warm wetland humidity, waterfall spray and watershed-fed water level; evidence does NOT identify these as an El Niño event"},
"right":{"pose":"Mud Dogs takes one heavy FOUR-LEGGED step from mud channel onto raised ground, chains dragging, all four paws and snarling low hound silhouette visible","set":"Established Mud Dogs swamp mud channels and raised ground, not a tropical shoreline or generic arena","costume":"Quadrupedal feral swamp-hound, matted moss/mud coat, collar/chain and fangs; NO humanoid anatomy or clean household dog","weather":"INDEPENDENT_SOUTHERN_HYDROLOGY","weather_cue":"Muddy shallow channel reflections and near-ground humid mist from Southern Wetlands; no unsourced flood/road washout attributed to Niño"},"cut":"Two southern wetlands scene plates connected visually by haze, never by a canonically continuous waterway","sound":"three breath rhythms and waterfall / sloshing mud, taut chain and one labored step"}
}
cover={
 "camera":"24mm extreme high editorial montage, seven luminous symbolic openings at far depth, twelve independent owner-domain silhouettes, no spatially contiguous master valley",
 "pose":"No literal all-character group portrait; route silhouettes and individual signature environments carry the twelve POVs",
 "set":"Atlas biomes remain distinct in graphic montage: Eastern storm coast, Inner Sea harbor, Upper Valley ridges, Western stable, Central Basin commons, Southern wetlands",
 "costume":"No misleading generic character silhouettes or invented canonical representatives; if any principal is depicted use the 12 approved crops",
 "weather":"SYMBOLIC_ATLAS_COMPOSITE",
 "weather_cue":"Pressure-system arc appears over correct eastern coast and fades along licensed downstream sequence; west stays dry and southern flood/humidity remains separate watershed system",
 "cut":"Routes are symbolic editorial montage; gate locations are NOT physical canon",
 "sound":"suggest wind and waves at eastern edge, dry saddle/tack west, swamp water south; silent PNG"
}
weather_lookup={
"EMBODIED_AT_STORM_BOWL":("EMBODIED_APPROVED","El Niño visible as the singular elemental; local atmosphere explicitly sourced to him within the scene, no permanent new weather event"),
"EAST_STORM_SOURCE_LOCAL":("CLIMATE_ELIGIBLE_ATTRIBUTION_UNPROVEN","Local eastern/Inner Sea storm pattern eligible; not enough evidence to call its current storm El Niño"),
"EAST_PROPAGATION_POSSIBLE":("DOWNSTREAM_PROPAGATION_NOT_CONFIRMED","Allow sky-pressure motif but not a specific storm event, flooding or travel closure without recorded propagation"),
"CENTRAL_BASIN_PROPAGATION_POSSIBLE":("DOWNSTREAM_PROPAGATION_NOT_CONFIRMED","Central Basin can be downstream but sky motif does not prove direct Niño weather; avoid arbitrary flood"),
"INDEPENDENT_SOUTHERN_HYDROLOGY":("SEPARATE_WATERSHED","Southern Wetlands humidity, river water and swamp mist are local/hydrological until a separate evidence event exists"),
"WESTERN_DRY_RAIN_SHADOW":("WESTERN_RAIN_SHADOW","Preserve Western Tablelands dust/heat tendency; no coast-wide rain forced into Chili Stable"),
"SYMBOLIC_ATLAS_COMPOSITE":("SYMBOLIC_NO_NEW_CANON","Global dramatic weather curve visualizes the crossroads, not an actual continent-spanning weather incident")
}
def hash_bytes(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def compile(dry=False):
    assert CREW.is_file(),"No authoritative specialist bench found"
    profiles=json.loads(CREW.read_text())["profiles"];names=[x["name"] for x in profiles]
    assert len(profiles)==12 and set(names)==set(roles),set(names)^set(roles)
    zones=json.loads((WORLD/"data/weather_regions.json").read_text())
    assert len(zones["weather_regions"])==4
    state=json.loads((WORLD/"data/current_world_state.json").read_text())
    assert state["as_of"].startswith("end_of_week_3"),"Re-evaluate freshness guard; source changed"
    outputs=[]
    for i in range(1,8):
        d=SCENES/f"RT7-P0{i}"
        src=json.loads((d/"scene.json").read_text())
        base=cover if i==1 else cards[i]
        frame={
          "schema":"schemin.road7.staging.v1","page_id":src["id"],"page_title":src["title"],
          "authority":"EDITORIAL_PROPOSAL_NO_WORLD_STATE_MUTATION",
          "world_engine_source":"world/SCHEMIN_WORLD_ENGINE_V1_1_RELEASE_RECEIPT.md",
          "atlas_weather_source":"world/data/weather_regions.json",
          "world_state_source":"world/data/current_world_state.json",
          "world_state_record_as_of":state["as_of"],
          "temporal_warning":"Latest loaded persistent world-state source is Week 3; no direct Week 10 El Niño global storm event was established. This is proposed cinematic staging, not a source-verified new physical event.",
          "cast_cutoff":"Final through Week 10 2026; W11-W14 unplayed",
          "physical_weather_is_not_playoff_probability":True,
          "global_motif":THEME,
          "camera":base["camera"],"graphic_transition":base["cut"],
          "sound_implied_only":base["sound"],
          "lighting_source":src["lighting_contract"],
          "staging_crew":[{
            "reference_profile":x["name"],"domain":x["domain"],
            "project_role_sponsor":x["sponsor"],"mode":"PUBLISHED_METHOD_LENS_NO_HUMAN_PARTICIPATION",
            "concrete_assignment":roles[x["name"]]["task"],
            "direct_page_assignment":i in roles[x["name"]]["pages"]
          } for x in profiles],
          "actual_authority":["Schemin Visual Direction","Atlas/World Engine","Character Librarian","Editorial Designer","Independent Umpire after raster"],
          "characters":[],
          "output_policy":{"render_generated_text":False,"overlay_from_locked_render_input":True,
                           "dimensions":[1080,1920],"no_raster_yet":True}
        }
        if i==1:
            frame["cover_staging"]={k:base[k] for k in ("pose","set","costume","weather","weather_cue")}
            frame["cover_staging"]["weather_attribution"]=weather_lookup[base["weather"]][0]
        else:
            for actor in src["character_panels"]:
                side=actor["side"]
                placement=base[side]
                card=json.loads((ROOT/actor["atlas_card_path"]).read_text())
                delta=json.loads((ROOT/actor["appearance_delta_path"]).read_text())
                canonical=delta["approved_visual_assertions"]
                assert actor["character_id"] in card["owner_character_ids"]
                assert delta["character_id"]==actor["character_id"]
                assert card["location_id"]==actor["atlas_location_id"]
                position={"side":side,"team":actor["team"],"seed":actor["official_week10_seed"],
                   "character_id":actor["character_id"],"location_id":actor["atlas_location_id"],
                   "physical_zone":card["physical_zone"]["id"],"terrain":card["physical_zone"]["terrain"],
                   "physical_set":placement["set"],"anchor_landmarks":card["persistent_landmarks"],
                   "pose_action":placement["pose"],"performance_intent":"Personal response to mathematically possible playoff path; no future result implied",
                   "approved_costume_visual":canonical,"shoot_costume_dressing":placement["costume"],
                   "costume_not_new_canon":True,
                   "reference_image":actor["approved_crop_path"],"reference_sha256":actor["approved_crop_sha256"],
                   "weather_relationships":card["weather_relationships"],"weather_role":placement["weather"],
                   "weather_exposure":placement["weather_cue"],"el_nino_attribution":weather_lookup[placement["weather"]][0],
                   "el_nino_note":weather_lookup[placement["weather"]][1],
                   "entering_world_state":card["current_world_state"],
                   "motived_lighting":src["lighting_contract"][side],
                   "blocking_restrictions":canonical["negative_rules"]+
                       ["Neither team is eliminated or clinched after Week 10","No new permanent terrain/location mutation","Do not imply split-screen worlds physically touch"]}
                frame["characters"].append(position)
        assert len(frame["characters"])==(0 if i==1 else 2)
        dest=d/"STAGING.json"
        if dry:
            assert dest.is_file(),f"Missing {dest}"
            assert json.loads(dest.read_text())==frame,f"Stale {dest}"
        else:
            dest.write_text(json.dumps(frame,indent=2,ensure_ascii=False)+"\n")
        outputs.append({"page":frame["page_id"],"staging_path":str(dest.relative_to(ROOT)),
                        "location_count":len(frame["characters"]),
                        "weather_roles":[x["weather_role"] for x in frame["characters"]],
                        "sha256":hash_bytes(dest) if not dry else hashlib.sha256((json.dumps(frame,indent=2,ensure_ascii=False)+"\n").encode()).hexdigest()})
    doc={"schema":"schemin.road7.staging_manifest.v1","specialists":len(roles),"staged_pages":len(outputs),
         "current_world_state_cutoff":state["as_of"],"world_engine_authority":"v1.1",
         "staging":outputs,"no_new_weather_event_asserted":True,
         "no_personal_credits_or_endorsements":True,"no_pngs_generated":True}
    manifest=BASE/"STAGING_MANIFEST.json"
    if dry:
        assert manifest.is_file(),"Missing staging manifest"
        assert json.loads(manifest.read_text())==doc,"Staging manifest drift"
    else:manifest.write_text(json.dumps(doc,indent=2)+"\n")
    return doc
if __name__=="__main__":
    print(json.dumps(compile("--dry-run" in sys.argv),indent=2))
