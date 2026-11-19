#!/usr/bin/env node
/** Founder Interview II eleven final scenes, superseding old challenge-form fiction.
 * Historical champions, venues and matchups are checked against the official spine.
 */
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const h=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const d=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const im=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const story={
2015:{title:'The Bridge That First Bore a Champion',angle:'Founding engineering trial and the first record in stone',prose:[
'In the first recorded season the enormous final stadium had no large screens, no chain of annual inscriptions, and no glittering procession of prior champions. The Last Field already possessed two permanent gates, and both finalists entered beneath stone still pale where it had been repaired. Between them the public ceremonial draw called Bridge Over Void. A safe and temporary engineering span, raised above a protected demonstration trench, became the evening’s instrument of judgment.',
'Austin’s Hyena’s began assembling the first crossing with immediate confidence, physically setting the opening supports. Discount Belichick worked opposite him, choosing a slower arrangement whose stresses could be checked in public. The second stage was not a speech but a structural counter: both contestants tested their own work, heard the fault in it, and had to personally correct what had been placed incorrectly. At the last passage the judges inspected a final span beneath a gallery where the crowd could see each adjustment without pretending the trial generated real-world fantasy points.',
'The certified championship result was Discount Belichick 211.50 to Austin’s Hyena’s 187.00. The defeated finalist left the field; the first recoverable champion remained where every later champion would stand. A marked fixture from the bridge trial was preserved, and a date was added to a previously empty record. Neither the naming year of the Michael Farrell Trophy nor a private biography was invented in that founding silence.'
]},
2016:{title:'The Sound of the Staffs',angle:'Second year, familiar stone and a two-person contest of balance',prose:[
'Visitors already knew how to follow the causeway to the Last Field. Returning spectators could identify the same two gates, the same field orientation and the first championship mark; the island had begun acquiring memory without requiring an empire of new stadiums. The draw selected Twin Staff Balance. The apparatus was simple: a guarded stone ring, equal permitted equipment and a sequence of lawful controlled engagements.',
'Austin’s Hyena’s and The Gunslingers personally stepped into the ring. Their first exchanges tested distance. In the middle passage each changed grip and stance as the other countered, making the fight look less like an exhibition and more like an argument conducted through motion. A late reversal forced both to reset before a final protected exchange. The spectators closest to the ring heard the effort and the referee more clearly than any commentator.',
'Austin’s Hyena’s won the official record, 217.70 to 206.88. An abrasion remained on the arena’s removable contact surface. It was inspected, repaired for safety and retained as a dated trace. The championship location was unchanged, yet the second season already felt different from the first because the people watching understood the cost of reaching it.'
]},
2017:{title:'The Spiral of Six',angle:'A wider tournament reaches a precision-based championship',prose:[
'Six contenders had entered the expanded tournament. By championship week, the new first-round arenas and the older semifinal stands had already reduced them to two. The Fournecators and The Gunslingers reached the original Last Field, where the ceremony selected Slingstone Spiral: a protected, three-position projectile trial with a guarded backstop rather than a fight to the death.',
'Each contestant personally took the first firing position. The target pattern shifted at the second station, forcing the two to read the distance, choose a different release and answer the public evidence of an opponent’s better technique. The spiral ended at a final isolated scoring mark. The ground had not become a new arena: only its removable range equipment changed. A damaged target plate would be dated, removed and kept as material history.',
'The Fournecators won the verified final 144.20 to 80.42. The victory was comfortable on the official scoreboard even after the screenplay gave both opponents active decisions. A sixth-team era was entering the island’s archive, but the same championship stone and the same two gates held the ending.'
]},
2018:{title:'A Tenth Before the Final Whistle',angle:'A close survivor and a floodline sporting challenge',prose:[
'Kardiac Kids had almost failed to reach this point. Its opening-round survival by 114.37 to 114.27 had become the most repeated argument on Losers’ Beach. Now Christopher Columbus entered across the field from that survivor. The ceremony revealed Floodline Soccer, a controlled sporting challenge on temporary, drained turf with marked water-resistant lanes—a form the oldest stone oval could hold without sacrificing its permanent floor.',
'The two competitors personally controlled the ball in each of three phases. First came a conventional sequence of contested possession; then the course narrowed, placing more burden on the owner’s footwork and timing; finally the last scored attempt required each to act without a substitute or team mate finishing the move. The public could see one contender recover a poor position only to be answered by another change of direction. A scuff on a protected field inlay survived as the site’s dated trace.',
'Kardiac Kids was certified champion at 160.69 to 153.26. The sport changed from earlier championships but the final gate did not. The beach would remember the opening round’s tenth of a point, while the stone record remembered the only result that awarded the title.'
]},
2019:{title:'Three Crossings for a New League Name',angle:'Tactical bridge trial at a renamed championship',prose:[
'The event signs now carried the Pro Schemin’ Football League name. The Last Field underneath them was unmistakably the same ground. Make Amarica Great Again and Please, Please, Please, please came to its gates, each having survived a larger tournament. The ceremonial draw selected Three Bridges: a tactical crossing trial assembled as a set of protected spans on the historic oval.',
'The opponents were required to take their markers personally. Each bridge gave a different possible approach, and neither man could use a professional retinue to claim the crucial middle. A feint at the first crossing drew one competitor toward a blocked ramp. In the second passage the rival adapted, shifting across a removable span while the arena’s spectators followed the physical geometry. The third required a final choice of crossing under a neutral judge. The damaged training-span fitting was preserved; the original field remained intact.',
'The verified final belonged to Please, Please, Please, please, 158.30 to 113.46. Fresh banners did not confer victory, and the new name did not reset the institution’s past. It merely announced another entry in a championship procession that was already five seasons old.'
]},
2020:{title:'Three Quarters of a Point',angle:'A nearly tied championship of endurance and balance',prose:[
'The last championship was not the largest the island had seen, but it may have been the quietest at certification. The Grinch and Where Mahomies at? stood beneath the original Last Field gates as the draw selected Balance of Twelve, a three-part endurance-and-control trial using verified support stations over a maintained stone surface. With the crowd watching, both contestants personally began the first hold.',
'The second station altered the balance demands. One contender steadied his effort while the other made a correction; neither could hand the weight to a helper. The third demanded a final controlled transfer as fatigue made every adjustment conspicuous. The officials measured the demonstration and kept the victory standard lowered until the true sporting ledger was signed. Some spectators on the beach had already decided what the ending meant, but their assumptions held no authority over the record.',
'Where Mahomies at? prevailed 189.19 against 188.44. A margin of 0.75 was announced only after verification. A marked lifting edge remained in the historical repair ledger. The field stayed operational; the silence before the declaration became the unforgettable part of the year.'
]},
2021:{title:'The First Seven and the Stone Kart',angle:'Modern sporting expansion with a fixed historic arena',prose:[
'Seven teams had entered the expanded postseason, three quarterfinals had required their own permanent venues, and the broadcast centre now followed the island as one event. The Last Field’s original gates remained below newer galleries. Dewars White Label and The Third Coming arrived for a final drawn as Stone Kart Derby: an enclosed, low-speed controlled track installed above the oval without rewriting the original foundations.',
'Both contestants took the steering role personally. The opening circuit revealed contrasting lines; the middle passage made them correct those lines when the course changed around a removable barrier; the last legal crossing narrowed their options until technique mattered more than spectacle. The teams, mechanics and judges could prepare or inspect equipment, but could not steer or complete a challenge stage in either contender’s place. A retired barrier would join the island’s collection of scarred fixtures.',
'Dewars White Label won the certified championship 178.06 to 96.58. The new tournament format had required better technology and more staff, not a new final location. The modern additions were visible around the same old gates that had watched the founding years.'
]},
2022:{title:'The Bullseye After the Upset',angle:'The 13–1 favorite is absent; a 7–7 survivor competes',prose:[
'Much of the audience had spent championship week talking about the absent Red Leopards, whose 13–1 regular season had ended in a semifinal loss to El Niño. At the Last Field, El Niño faced Where Mahomies at? under a different pressure: the final’s official record would not remember where a contender had been seeded. The ceremony selected Moving Bullseye, a controlled marksmanship test with protected moving targets.',
'Both finalists took the first range positions themselves. In the second passage a target moved behind protective shields, requiring each to change sighting technique and adjust to the opponent’s publicly witnessed attempts. In the last, the final target ran its prepared course while the spectators kept clear of the firing line. A punctured target plate was recovered as an enduring physical mark, not left as an active danger. The old stadium remained structurally untouched.',
'El Niño, a 7–7 regular-season qualifier, was certified champion 111.56 to 78.30. The result required no mystical weather intervention and no new scoring formula. The final simply proved the post-season’s basic principle: making it to the island gives a chance; surviving it gives a name in stone.'
]},
2023:{title:'Sixth Seed, Highest Stone',angle:'Unexpected route culminates in a personally fought wrestling trial',prose:[
'Eggs Benedict had entered the postseason as a sixth seed. Arm Chair GM came from the other side of the bracket. Their confrontation took place at the Last Field, not at a floating venue chosen for their personas. The draw selected Crown Wrestling Ladder, a series of protected grappling stations staged above the original level ground, with safety crews and impartial scoring around every ring.',
'At the opening station each contender personally attempted a lawful hold. The second required adjusting leverage as an opponent changed posture and position. The final passage was closer to the central dais, within sight of the oldest stones. Neither contender could appoint a wrestling proxy or leave the work to a professional supporting cast. Equipment was damaged and repaired; the original arena did not become another ruin.',
'Eggs Benedict won the source-certified final 192.88 to 140.76. The audience did not need the sixth seed to become a literal king to understand the achievement. The permanent final ground accepted another name, while the beach held eleven competitors who had wanted that place instead.'
]},
2024:{title:'A Champion at the Trebuchet Line',angle:'Three-round survival and precision engineering on a historic final',prose:[
'ObiWan Jacoby entered the championship after personally surviving two earlier playoff fixtures. The King had arrived from the bye path and a semifinal. On the Last Field, the two original gates opened toward removable engineering apparatus: Trebuchet Target, a precision siege-engine demonstration with unloaded or safely controlled projectiles aimed at an empty protected wall.',
'The first stage required each finalist to build and inspect his own scaled device. In the middle passage, both responded to changes in angle and counterweight while the spectators watched their attempts travel toward the guarded target. In the third they set the final mechanism personally. No hired crew could take the decisive shot, and the old field remained safe behind replaceable target panels. The damage to one expendable structural fixture was recorded for preservation.',
'ObiWan won the official championship 187.52 to 161.68. The 2024 inscription joined the earlier names on the same walk, and its winner crossed the historic field as the current titleholder. The arena’s foundations, orientation and old gates were unchanged, ready to confront him again in another season.'
]},
2025:{title:'The Gates Remember',angle:'Returning former champion meets the near-eliminated challenger',prose:[
'ObiWan Jacoby entered the Last Field as the previous year’s champion. The Immortal had reached this gate after surviving Dr. Duckhook in a semifinal decided by 0.40. Modern viewing screens surrounded the old stone arena, but its entrances and the angle of the final ceremonial path remained fixed. The draw called Quarry Ambush, a nonlethal tactical course of removable rock-faced barriers and controlled effects installed above the field.',
'Both finalists acted personally through the simulated rubble, an elevated protected crossing, and a final contested standard. ObiWan changed route to preserve a tired shoulder. The Immortal answered with a slower, controlled approach despite fatigue from earlier rounds. A staged burst of smoke darkened an expendable fitting away from the crowd and the protected memorial axis; its trace was preserved after safe removal rather than left as a danger.',
'The Immortal was certified champion 161.07 to 109.56. ObiWan’s 2024 stone remained on the Champions’ Walk, but his 2025 attempt was over. The Belt passed, the Michael Farrell Trophy received dignified remembrance, and a soot-marked component from the final joined the island’s material record. The eleventh completed season closed beneath the same gates that had stood for the first.'
]}
};
const chosen=d.ceremonies.filter(x=>x.round==='FINAL'),finals=h.fixtures.filter(x=>x.round==='FINAL');
const scenes=chosen.map((v,i)=>{
 const f=finals.find(x=>x.id===v.fixture_id),t=im.traces.find(x=>x.fixture_id===v.fixture_id),n=story[v.year];
 assert.ok(f&&t&&n);
 assert.ok(n.prose.length===3);
 const winner=f.home.team_slot===f.winner_slot?f.home:f.away;
 return {year:v.year,title:n.title,angle:n.angle,prose:n.prose,ceremonial_draw:{obstacle_id:v.selected_obstacle_id,name:v.obstacle_name,ticket:v.draw_ticket_sha256},
 verified:{home:f.home,away:f.away,winner_slot:f.winner_slot,winner_name:winner.name,fixture_id:f.id},
 venue_id:'CAND-POST-LAST-FIELD',permanent_trace_id:t.trace_id,original_historical_text_status:'V1_SUPERSEDED_ONLY_FOR_PROPOSED_CHALLENGE_FORM',
 screenplay_expansion:v.year===2025?'INKLINGS_2025_LAST_FIELD_SCREENPLAY_PILOT_V1.md':null,
 source_status:'ESPN_RESULT_FIXED; ARTISTIC_TRIAL_NEW_FICTION',release:'PREPRODUCTION'};
});
assert.equal(scenes.length,11);
const result={schema:'schemin.inklings.last_field_championship_scenes.interview_ii.v2',
 status:'FOUNDER_II_CHALLENGE_CORRECTED_LITERARY_PREPRODUCTION_NOT_CANON',
 supersedes_for_challenge_form:'INKLINGS_ELEVEN_CHAMPIONSHIP_FINALE_SCRIPTS_V1.proposal.json',
 sources:['HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json','HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json'],
 count:11,scenes};
const target=path.join(root,'INKLINGS_ELEVEN_CHAMPIONSHIP_FINALES_INTERVIEW_II_V2.proposal.json'),serialized=JSON.stringify(result,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(target,'utf8'),serialized);
else fs.writeFileSync(target,serialized);
console.log(JSON.stringify({status:'PASS',finales:11,no_2026:true,forms:scenes.map(x=>x.ceremonial_draw.name)}));
