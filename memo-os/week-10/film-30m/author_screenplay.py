#!/usr/bin/env python3
"""Author scene-specific film dialogue and editorial VO against the frozen 34-folio storyboard.

These lines are candidate screenplay fiction, never quotes from real team owners.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import os

HERE=Path(__file__).resolve().parent
board_source=Path(os.environ.get("FILM_BOARD_JSON",str(HERE/"film_storyboard_v1.json")))
board=json.loads(board_source.read_text(encoding="utf-8"))
# (Edited narrator paragraph; action intent; candidate scripted dialogue)
SCENE = {
"P01": ("Two performances broke a ceiling that had stood all season: His Majesty's Blood at 208.76, and The LLC at 203.96.",
"Hold the champion in Jackson birthday light and the executive in his mountain command position. Two differently lit territories, no physical meeting.",[]),
"P02": ("Six separate confrontations, one Commonwealth, and four games still to come. The record says what happened. The roads tell us what it cost.",
"Travel a sealed folio, winding route markers, and recognizable props with one continuous oblique table move. Stop on the empty space waiting for Week Eleven.",[]),
"P03": ("The standings will be entered once. A fallen hoop stays fallen. A truck passes the same empty road every week. The people in this world have to live with both truths.",
"An anonymous official seals the weather-worn door. Keep civic labor ordinary, no commissioner portrait, no unverified speech.",[]),
"P04": ("All six games have final scores. These are completed results, not predictions. There are six teams at six wins and four losses.",
"Neutral official board in the records pavilion. The correct six games and figures are native typeset from the locked source, never generated as pixels.",[]),
"P05": ("The outlaw gets his laugh from the Highland gallery. Then he repeats the centaur's four-hoofed stance. A second laugh proves one too many.",
"A wide fixes wet rail, galleries, D0nkey K0ng and rear-left service gate. Chili imitates and bows; the centaur stiffens and brings the already-owned lasso off his shoulder.",
[("THE CHILI CHEESERS","Four hooves, and not one of them knows how to dance."),("D0NKEY K0NG","That was your second chance.")]),
"P06": ("The gate is still open. The rope reaches him first. The outlaw's own momentum turns capture into a skid through the groove he made himself.",
"One legible sequence: loop approaches torso, rope closes around upper arms/torso—not neck—boots skid, D0nkey braces on four hooves. No instant tying, no axed rope.",
[("THE CHILI CHEESERS","I was only leaving!"),("D0NKEY K0NG","Then stop running.")]),
"P07": ("The centaur finishes the knot by hand. The hat lies beyond reach. The gallery sees the man who wanted to be its main attraction.",
"Hold after physical work is complete. Audience faces remain anonymous; Chili's face is visible above mud and he looks toward the entrance. All four of DK's hooves remain planted.",
[("THE CHILI CHEESERS","They're still watching?"),("D0NKEY K0NG","You asked for an audience.")]),
"P08": ("Red tries one more sandbag beside the battered goal. The storm watches. Water doesn't need to break the wall; it knows an old rut.",
"Sandbag handling is slow and material. The runoff follows the established tire rut around the end of the line. El Niño is embodied at the far side of the same field, not a face in the clouds.",
[("RED LEOPARDS","Hold. Just hold." )]),
"P09": ("Later, far inland, Red reaches the Forgotten Court. One tree has already fallen across the road. A second comes down above the old right-wall hoop.",
"Travel is indicated by cut and carried mud, never proximity. Frame the familiar hoop intact for one breath, then one heavy branch strikes the right-wall backboard.",
[("RED LEOPARDS","Not this place.")]),
"P10": ("In 2022 the advantage vanished in a semifinal. The rim hangs wrong again today. But Red isn't out of this season; there is still another repair to decide whether to make.",
"Let his fingers touch the loose net beneath the hoop. El Niño laughs from across the same cold rain-swept court. Keep the 2022 record verbal, never fabricate a flashback reenactment.",
[("RED LEOPARDS","I could fix it." )]),
"P11": ("One front. Different consequences. Coast water, inland wind, wetland runoff later. At the mountain lake, the lamps are lit early.",
"Three regional exposures in editorial sequence, never a single continuous location. Use the established bridge to orient the audience. Localized wind ripples road fabric.",
[]),
"P12": ("There was a time when the waterfall was the loudest thing a family heard. Not tonight.",
"Jackhammer in the paving layer, compressor and hose below; a newborn cries offscreen, then three heads share one body at the balcony rail. Keep the upstairs room offscreen.",
[("PARTNER (O.S.)","Can you come here? Please."),("THREE DREADED SNAKE","What is that noise?")]),
"P13": ("The machine stops. For a moment the waterfall is all anyone hears. Seven Deadly Chins has listened—and chooses the music instead.",
"Stage a genuine silent interval. One hand releases jackhammer, then raises speaker volume while tool is down. TDS looks toward the protected doorway before sound recommences.",
[("THREE DREADED SNAKE","Enough! There's a child trying to sleep!"),("SEVEN DEADLY CHINS","I heard you.")]),
"P14": ("The circle of broken paving grows. The father gets louder. So does the music. The jackhammer begins the same damage all over again.",
"One big vertical payoff. Same patch, same operator, same balcony. Three furious heads on one torso, Chins with both hands returning to the tool. No arbitrary temple collapse.",
[("THREE DREADED SNAKE","You heard every word."),("SEVEN DEADLY CHINS","Every single one.")]),
"P15": ("Mud Dogs holds the swamp entrance like a border. The truck is carrying beer; its driver is just making another delivery.",
"Stay low in the hound POV. Driver checks the mirror, cargo straps remain tight, raised service strip and soft shoulder remain distinct. Bark communicates territorial claim.",
[]),
"P16": ("He doesn't stop. He doesn't race. The truck continues at precisely the speed of an ordinary appointment.",
"Mirror check, steady truck on firm raised road, barking hound on soft shoulder, loaded trailer receding without loss. No collision, no thrown keg and no violent confrontation.",
[("SLOB ON MY DOBB (MUTTER)","Road's clear.")]),
"P17": ("The tail lamp disappears. The road is quiet. The postcard is a taunt—not an elimination ticket. Mud Dogs still has a narrow route.",
"Hold on empty wetland path and flooded racing scars, Cancún card fluttering against sign. Do not stamp playoff elimination or show fabricated escape flight.",
[]),
"P18": ("There are numbers behind the stories. McCaffrey gave Slob 52.60. Three players combined for 113.86 for His Majesty's Blood, and three more combined for 103.66 for The LLC; Gibbs brought Dr. Duckhook 47.40. El Niño won with Pickens on the bench. The Monday comeback still left ObiWan 37.43 short.",
"Type every numerical receipt from the source. Avoid false player action footage; use document surfaces and accurate score overlays, not generated words.",
[]),
"P34": ("Sunday's fantasy totals are not proof that players are healthy, returning, or ruled out beyond the verified reports. The record carries the medical uncertainty into Week Eleven.",
"Editorial montage of authentic roster lines and medically qualified reporting: source text remains adjacent and fully reviewable. No reenactment of diagnosis or injury.",
[]),
"P19": ("At Jackson, the birthday boy receives the guest who nearly lost his title path to him last season. The room is warm; the windows are darkening.",
"Existing Jackson hall geography. Dr Duckhook turns sideways among guests; HMB keeps his approved armor, concealed eyes, cloak and belt, holding a wrapped object. No fabricated team speeches.",
[("DR. DUCKHOOK","You didn't come empty-handed."),("HIS MAJESTY'S BLOOD","I remembered the occasion.")]),
"P20": ("The ribbon comes away. The box opens. The 200 Burger is understood before anyone needs to explain the number.",
"Box lid first, host's glance second, nearby guests' reaction third. Preserve the untouched separate cake on the sideboard.",
[("DR. DUCKHOOK","That is a very large burger."),("HIS MAJESTY'S BLOOD","Two hundred reasons to celebrate.")]),
"P21": ("And then the other cake is no longer on the sideboard. The room does not know whether to cheer or wince.",
"Separate single cake-face contact. Frosting on Duckhook's orange bill and green vest; the huge burger remains untouched. Realistic cake weight, no injury.",
[("DR. DUCKHOOK (MUFFLED)","Happy birthday to me.")]),
"P22": ("Their earlier meeting came down to eight tenths of a point. This time ObiWan finds the first battery, turns its red fire with a green blade, and watches it fail.",
"Frame original mountain causeway, first battery and distant lamp; its destructive failure precedes the executive leaving the chair. The home arch stays lit.",
[("OBIWAN JACOBY","One down.")]),
"P23": ("The LLC leaves the chair. For an impossible moment the offer is almost reasonable: surrender the blade, and the lit arch will be spared. The defender looks back—and refuses.",
"Chair creak, steps descended, two figures stand shoulder-to-shoulder then LLC circles. Pause for the temptation and look toward the lit home arch. No blow or battery discharge yet.",
[("THE LLC","Lay down the blade. The arch stays lit."),("OBIWAN JACOBY","That light isn't yours to bargain with.")]),
"P24": ("The hand goes up. The surviving battery turns. The flash catches the blade and empties the field of shadow. The arch lamp stays lit. The final difference was 37.43.",
"The second battery fires after hand signal. The first is already disabled. Second lightning branch lights empty chair; no coronation, no erased home arch, no result reversal.",
[]),
"P25": ("Six NFL clubs are on bye. The refreshed fantasy rosters still leave seven specialist positions uncovered across six teams; reserve slots are not medical clearance.",
"Read exact unfilled specialist slots as source-matched minimal graphic highlights. No imaginary player portraits, acquisitions, injury confirmations or roster moves.",
[]),
"P26": ("Twenty-nine completed transactions belong to the Week Ten record. Pending requests are not completed moves. After the trade deadline the question is available depth.",
"Exact official transaction categories and timestamps remain a legible hand-entered editorial matrix, not a rendered hologram of fictional trades.",
[]),
"P27": ("Six teams are six and four. Yet equal records don't mean equal seeding. Slob on my Dobb leads the official standings and total points.",
"Deep civic standings ledger with native typeset twelve-name table, brief character emblems only from approved source. Hold enough to read without an enormous AI-generated number wall.",
[]),
"P28": ("Pizza has three six-win teams. Wings has two. Burgers has one. The same record now carries different weight in each division.",
"One slow pan from each known division marker to its factual member records. Map geography only from Atlas, division labels are competitive overlays rather than regional boundaries.",
[]),
"P29": ("The scoring-form index is a receipt, not a forecast: seventy percent season production and thirty percent Week Ten performance.",
"Accurate source-driven 70/30 diagram on an in-world ledger. Avoid fake odds and changing the formula after publication.",
[]),
"P30": ("Four games remain. All twelve still have a route, nobody has clinched, and a nine-win finish guarantees entry. An eight-win season alone may not.",
"Year clock over protected division schedule; do not illustrate determined playoff outcomes or eliminate Mud Dogs early.",
[]),
"P31": ("The next six are unfinished stories. A single crossover remains before the three divisional rounds. Only Mud Dogs is eliminated by losing Week Eleven.",
"Map tomorrow's fixtures as crossed paths without pretending next week's games have occurred. Keep their unresolved result markers blank.",
[]),
"P35": ("At the bridge, two six-and-four contenders occupy opposite approaches. Nothing crosses the stone yet, but both know what the next meeting means.",
"Open shot establishes unoccupied bridge span. DK stands on one approach and HMB opposite; eyelines lock to same pier. Do not show first blow or winner. No new belt or crown.",
[]),
"P33": ("The weather has not finished moving. Slob's cargo passed unhindered. Next week El Niño comes to his place; both teams still have work between Sundays.",
"Return to wetland camp, distant ordinary maintenance and tangible weather. No new encounter, no future victory, no climate discontinuity; finish on unresolved camp light.",
[])
}
assert len(SCENE)==34,len(SCENE)
expected={s["folio"].split("-")[-1] for s in board["scenes"]}
assert set(SCENE)==expected,sorted(expected-set(SCENE))

def wc(s):
    return len(re.findall(r"\b[\w’'-]+\b",s))

scenes=[]
lines=[
"# SCHEMIN ’26 / WEEK 10 — THE COMMONWEALTH CUT",
"## Thirty-minute shooting screenplay — candidate, performance and sound draft",
"",
"**Stage:** SCRIPT DRAFT / NOT LOCKED / NO NEW CANON OR REAL-OWNER QUOTATIONS",
"**Source:** frozen 34-scene film storyboard, existing full Memo OS copy and 66 source-directed shots. Screenplay authoring supplements are explicitly proposals.",
"**Length:** exact proposed 30:00 picture timeline (not a finished 30-minute spoken performance). Dialogue marked as fictional actor-audition material; voice profiles and approval remain open.",
"",
"---",""
]
for s in board["scenes"]:
    pid=s["folio"].split("-")[-1]
    narrator,action,dialogue=SCENE[pid]
    vo_time=wc(narrator)*60/145
    dx_time=sum(wc(text)*60/135 for _,text in dialogue)
    assert vo_time+dx_time<=s["duration_s"]-4,(pid,s["duration_s"],vo_time,dx_time)
    locked=s["publication_copy"].get("body","")
    lines.extend([
        f"### {s['id']} — {s['title'].upper()}",
        f"**Picture:** {s['start']}–{s['end']} ({s['duration_s']} seconds)  |  **Source:** {s['folio']}  |  **Region:** {s['setting'].get('venue_id') or s['setting'].get('set_id') or s['setting'].get('venue_type')}",
        f"**Cast:** {', '.join(s['characters']) or 'No principal speaking character'}  |  **Boarded coverage:** {len(s['shots'])} shots",
        "",
        f"*ACTION / DIRECTOR'S BEAT (PROPOSED)* — {action}",
        "",
        f"**COMMONWEALTH NARRATOR (V.O. — FILM ADAPTATION CANDIDATE):** {narrator}",
        ""
    ])
    if dialogue:
        lines.append("**FICTIONAL DIALOGUE DRAFT (NOT REAL-OWNER QUOTES; REQUIRES EDITORIAL LOCK)**")
        for char,text in dialogue:
            lines.append(f"- **{char}:** “{text}”")
        lines.append("")
    else:
        lines.extend(["**CHARACTER DIALOGUE:** None proposed. Source performance is visual, sound-led or documentary.",""])
    lines.append("**CAMERA, ACTION & SOUND — MATCH TO SOURCE BOARD**")
    for sh in s["shots"]:
        lines.append(f"- **{sh['id']} · {sh['start']}–{sh['end']}** | {sh['role']}. {sh['camera']}. {sh['blocking']} [Motion: {sh['movement']}; Foley: {sh['sound_cue']}]")
    lines.extend([
       "",
       f"**SET STATE:** {s['sound']['ambience']}. **ORIGINAL SCORE:** {s['sound']['original_music_brief']}.",
       f"**TIME/CONTINUITY:** {s['time_logic']}. {s['transition'] or 'Hold scene consequence.'}",
       f"**PROHIBITED ALTERATIONS:** {'; '.join(s['forbidden_mutations']) if s['forbidden_mutations'] else 'No unapproved source or location change.'}",
       f"**RUNTIME METER (CANDIDATE):** {round(vo_time,1)} sec adapted VO + {round(dx_time,1)} sec proposed dialogue; {round(s['duration_s']-vo_time-dx_time,1)} sec coverage / dramatic holds / graphics and music. These segments may overlap in final edit.",
       "",
       "<details><summary>Controlling original Memo OS prose (fact/source reference, not automatic ADR)</summary>",
       "",
       locked,
       "",
       "</details>",
       "",
       "---",
       ""
    ])
    scenes.append({
      "scene_id":s["id"],"source_folio":s["folio"],"start":s["start"],"end":s["end"],
      "duration_sec":s["duration_s"],"location":s["setting"],
      "narrator_film_candidate":narrator,"camera_action_direction":action,
      "dialogue_proposal":[{"speaker":ch,"text":tx,"status":"FICTIONAL_DRAFT_NOT_REAL_OWNER_QUOTE"} for ch,tx in dialogue],
      "source_unchanged_body":locked,
      "source_publication_copy":s["publication_copy"],
      "source_request":s["source_request"],"source_sha256":s["source_sha256"],
      "counts":{"vo_words":wc(narrator),"candidate_dialogue_words":sum(wc(t) for _,t in dialogue),"allocated_picture_seconds":s["duration_s"],
       "vo_time_at_145wpm":round(vo_time,2),"dialogue_time_at_135wpm":round(dx_time,2)},
      "image_appearance_status":"REQUIRES_PER_SHOT_CANON_QA","voice_status":"NOT_CAST","script_status":"CANDIDATE"
    })
payload={"schema":"schemin.week10.screenplay.v1","stage":"WORKING_FILM_SCRIPT_NOT_LOCKED","source_storyboard":"film_storyboard_v1.json",
"runtime_seconds":1800,"source_pages":34,"source_beat_count":66,"fictional_dialogue_policy":"These are proposed in-world fictional dramatizations, not statements by real league owners; review before use.",
"scene_scripts":scenes}
(HERE/"SCREENPLAY_CANDIDATE_V1.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(HERE/"SCREENPLAY_CANDIDATE_V1.md").write_text("\n".join(lines).rstrip()+"\n",encoding="utf-8")
print(json.dumps({"scenes":len(scenes),"speaker_lines":sum(len(x["dialogue_proposal"]) for x in scenes),
"voiceover_words":sum(x["counts"]["vo_words"] for x in scenes),
"candidate_dialogue_words":sum(x["counts"]["candidate_dialogue_words"] for x in scenes),
"screenplay_bytes":(HERE/"SCREENPLAY_CANDIDATE_V1.md").stat().st_size,
"original_source_words_preserved":sum(len(x["source_unchanged_body"].split()) for x in scenes)},indent=2))
