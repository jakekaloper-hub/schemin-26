"""Authored shot plans for the existing issue; preserves publication copy and canon."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[4];P=R/'memo-os/week-10/preproduction';E=Path(__file__).parent
issue=json.loads((P/'issue-previs.json').read_text());pages={p['page_id']:p for p in issue['pages']};order=issue['recommended_reading_order']
C={'chili':'CHAR-BRANDON-PRYOR','dk':'CHAR-WILSON-LOOK','red':'CHAR-KEVIN-ZEEK','nino':'CHAR-MANNING-WELTY','tds':'CHAR-PHILLIP-PITTS','chins':'CHAR-BEN-WHIPPLE','mud':'CHAR-BOBBY-MITCHELL','slob':'CHAR-JORDAN-HOLLINGSHEAD','duck':'CHAR-ZACH-WILSON','hmb':'CHAR-AUSTIN-BYARS','obi':'CHAR-JAKE-KALOPER','llc':'CHAR-DAVID-BABB'}
def shot(role,pov,camera,action,information,time='same moment'):
 return {'role':role,'pov_owner_ids':[C[k] for k in pov.split(',') if k],'camera':camera,'action':action,'new_information':information,'time_relation':time}
D={}
def add(n,structure,time,question,shots,layout,turn,grammar=None):
 pid=f'W10-P{n:02}';p=pages[pid]
 for i,s in enumerate(shots,1):s['id']=f'{pid}-V{i:02}'
 body=p['draft_copy']['body'];ranges=[]
 # Two ordered reading zones at most. Never abbreviate or repeat the supplied body.
 if len(shots)>1 and len(body)>200:
  boundaries=[m.end() for m in re.finditer(r'[.!?]\s+',body) if not body[max(0,m.start()-3):m.start()+1].endswith(('Dr.','St.','Jr.'))]
  split=min(boundaries,key=lambda x:abs(x-len(body)*.5)) if boundaries else len(body)
  ranges=[{'start':0,'end':split,'anchor':'opening perspective or clear adjacent atmosphere'},{'start':split,'end':len(body),'anchor':'main action or consequence reading zone'}]
 else:ranges=[{'start':0,'end':len(body),'anchor':'one continuous readable atmospheric field beside the main visual information'}]
 refs=[]
 for w,num in grammar or []:
  f=R/f'memo-os/week-10/production-evidence/recovery-20261116/precedent-w{w:02}-p{num:02}.jpg'
  refs.append({'week':w,'physical_page':num,'repo_path':str(f.relative_to(R)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'application':'SHOT GRAMMAR ONLY: viewpoint relation, time progression and hierarchy. Do not import this source character, costume, location, score, border or paragraph placement.'})
 D[pid]={'page_id':pid,'structure':structure,'time_logic':time,'visual_question':question,'shots':shots,'layout_direction':layout,'dominant_view':next((s['id'] for s in shots if s['role']=='dominant'),shots[0]['id']),'copy_flow':{'source':'issue-previs.json#'+pid+'/draft_copy','body_ranges':ranges,'all_other_copy_fields':'Retain every existing heading, deck, callout, result, football-context line and table row once. Coalesce identical heading/deck only as already permitted.','flow_rule':'The body ranges are exact contiguous slices in source order, not extra captions per shot. Compose clear space at readable size; no automatic bottom box, rotated text or silent cuts.','proposed_extra_words':[]},'continuity':{'source_encounter_unchanged':True,'landmarks':p['encounter'].get('persistent_landmarks',[]),'rule':'Reverse angles are intentional and physically compatible. Repeated appearance means the same character seen in separate shots, never a clone inside one continuous view. Existing prop/damage state persists.'},'page_turn_out':turn,'grammar_references':refs,'approval_scope':'Applied working shot direction requested by Jake; no generated-pixel or publication approval.'}

# Opening four: composition variety does not force documentary pages into comic panels.
add(1,'editorial_double_exposure','EDITORIAL_JUXTAPOSITION_NOT_A_MEETING','How did two very different characters break 200?',[
 shot('dominant','hmb','Low three-quarter standing champion, gift presentation scale','His Majesty’s Blood holds the wrapped gift in the established birthday context.','The first 200-point performance has a social, teasing signature.'),
 shot('counterpoint','llc','Medium seated executive, command-chair eyeline','The LLC sits with cigar in his mountain-command atmosphere.','The other performance expresses controlled force, not the same victory pose.')],
 'One cover with two distinct story territories joined by weather and tonal atmosphere; not a literal meeting or two equal portrait cards. Keep both exact named scores by their own subject.',
 'The shared sky yields to the Opening Drive briefing; no cover event is asserted as a real meeting.',[(9,17)])
add(2,'inhabited_briefing_master','ONE_CONTINUOUS_MOMENT','How do six episodes belong to one week?',[
 shot('dominant','','Over-table oblique with strong near-to-far depth','A sealed folio, mapped routes and the already specified lasso/paving/delivery/gift/assault symbols gather in the briefing space.','A common world frames six different consequences without six miniature posters.')],
 'Keep the recognizable published Opening Drive as one inhabited composition. Foreground objects and distant banners guide the eye; full narration lives around—not below a detached picture of—the table.',
 'Move from the week’s shared pressure to the commissioner’s human consequences.')
add(3,'civic_breathing_page','ONE_CONTINUOUS_MOMENT','What remains after scores are posted?',[
 shot('dominant','','Eye-level desk-to-threshold interior','An attendant secures the weather-marked door beside the records desk.','An ordinary action makes the civic space feel inhabited while the address carries the argument.')],
 'A calm full scene with asymmetrical reading space; no invented commissioner portrait or reaction montage.',
 'The address yields to the neutral record of all six results.')
add(4,'documentary_results_master','ONE_CONTINUOUS_MOMENT','What actually happened before the issue dramatizes it?',[
 shot('dominant','','Level result standard in deep arbiter-pavilion setting','Readers consult the six exact completed results.','All twelve teams are accounted for without making six fictional aftermath pictures.')],
 'The single scoreboard surface is the visual information, not a backdrop for another caption. Preserve all rows, hierarchy and exact digits.',
 'Cut from the public result standard to the public rodeo galleries.')

# Matchup 1: opening viewpoints, physical mechanism, then public consequence.
add(5,'establishing_strip_and_opposed_pov','SIMULTANEOUS_SAME_LOCATION','Who controls the ring, and what escape does the outlaw see?',[
 shot('establishing','','High gallery view down the same ring','Show the rear-left service gate, wet track and both contestants on the pursuit axis.','The reader knows the only visible exit before the chase tightens.'),
 shot('subjective','chili','Close third-person behind The Chili Cheesers toward the gate','The outlaw runs and looks toward the exit, with the spectators beyond.','Escape and audience-consciousness are his immediate priorities.'),
 shot('dominant','dk','Low three-quarter following D0nkey K0ng on the same pursuit axis','The integrated gorilla-centaur closes with four legs readable and his lasso turning.','His control of rope and ground is the opposing intention.')],
 'A narrow spatial overture above two unequal connected POV areas. Shared gate and gallery landmarks identify the same instant; avoid decorative profile portraits. Keep typography subordinate to the pursuit.',
 'Page turn follows the open loop toward The Chili Cheesers, not yet a completed capture.',[(9,12),(9,17)])
add(6,'causal_three_beat_action','CHRONOLOGICAL_SAME_LOCATION','How does the catch become a fall rather than an instant hogtie?',[
 shot('setup','chili','Tight lateral torso-and-rope view','The moving loop closes around the torso, never the neck.','Capture occurs before the runner loses his footing.','first'),
 shot('dominant','chili','Low lateral full action including the same boot and wet groove','His continued running pulls him into a skid through the mud.','His momentum supplies the physical cause of the fall.','next'),
 shot('counterforce','dk','Wider rear-quarter view with uninterrupted rope line','D0nkey K0ng braces on four hooves, keeping the captured outlaw and gate in the same geography.','The rope stays controlled by the centaur; tying has not magically happened.','then')],
 'Small cause view, dominant slipping action, compact counterforce view. No separate witness-reaction panel here; the rope route and cause must be immediately readable.',
 'End with controlled capture so the following page can show deliberate binding.',[(9,13),(9,24)])
add(7,'payoff_master_and_reaction_detail','SIMULTANEOUS_SAME_LOCATION','What has changed for the man who wanted the crowd?',[
 shot('dominant','dk','Low public wide with all four hooves and the captive visible','D0nkey K0ng finishes the manual binding in the center-ring mud; the hat lies beyond reach.','The full body mechanics prove the payoff has been earned.'),
 shot('reaction','chili','Close third-person toward the spectators from the tied outlaw','His face and glance return to the entrance and crowd.','The emotional cost is public embarrassment rather than invented injury.')],
 'Give the aftermath most of the folio; one smaller reaction window adds information, not another full pose. Put the exact FINAL receipt once in readable arena shadow.',
 'Visual match on churned wet ground leads to the old soccer ruts—not a claim that the two venues adjoin.',[(9,13)])

# Matchup 2: two real places and present-tense responses, never a fabricated flashback.
add(8,'repair_opposition_and_detail','CHRONOLOGICAL_SAME_LOCATION','What is Red trying to preserve, and why does the effort fail?',[
 shot('dominant','red','Over Red Leopards’ near shoulder across the damaged soccer terrace','He actively lowers another sandbag with the damaged goal and old ruts visible.','His effort is specific and deliberate, not a defeated pose.','first'),
 shot('opposed_pov','nino','Reverse long view from embodied El Niño’s side of the same pitch','The elemental regards the small repair effort through the rain.','The opponent sees a failing boundary rather than a repair triumph.','same repair moment'),
 shot('detail','red','Ground-level close view at the end of the placed bag','Shallow water curls around the exposed edge into the established tire rut.','The precise failure is visible without a tidal wall.','next')],
 'A dominant working view, narrow opposing view and small water-path detail. Reuse the known terrace geometry. No basketball hoop, invented historical storm or disembodied face in a cloud.',
 'Use a clear temporal cut to the later Central Basin court; mud carried on Red establishes continuity without false adjacency.',[(9,12),(9,13)])
add(9,'arrival_then_impact','CHRONOLOGICAL_SAME_LOCATION','Will a familiar place offer relief, and what interrupts it?',[
 shot('setup','red','Close third-person arrival echoing the Week7 court angle','Red Leopards looks toward the familiar upper-right wall-mounted basket.','The later destination is recognizable and separate from the soccer field.','arrival'),
 shot('dominant','red','Wider upward view preserving the same wall and approach','The gust brings the old limb onto the backboard while Red looks up.','Arrival turns into another material loss, with the force and target visible.','moments later')],
 'Use a smaller arrival view and a tall dominant branch-impact composition. The word Later remains in the existing prose; the source’s court—not an invented game—controls geometry.',
 'The falling diagonal becomes the wrong-hanging rim in the next page.',[(7,8),(9,13)])
add(10,'aftermath_and_opposing_look','SIMULTANEOUS_SAME_LOCATION','Does he surrender, or have to decide to repair again?',[
 shot('dominant','red','Still low court view, seated figure under the broken hoop','Red Leopards rests with the same mud on his hands and the limb against the wall.','The loss registers as accumulated damage and remembered disappointment.'),
 shot('counterpoint','nino','Reverse view across the same court from the elemental’s side','Embodied El Niño laughs across the wet space, with Red still seated beyond.','The victor and loser experience the same aftermath differently.')],
 'Let one quiet image dominate and use a restrained opposing view. Keep the exact 2022 memory in text only; do not stage a fictional historical event or mark the current season over.',
 'The moving leaves and rain continue into The Roads Between as weather, not a character teleport.',[(9,12),(7,8)])
add(11,'regional_weather_overture','EDITORIAL_REGIONAL_VIEWS_NOT_ADJACENT','How does one front affect different parts of the Commonwealth?',[
 shot('regional','','Low coastal retaining-edge detail','Runoff follows existing damage at the already established coast.','Exposure produces water effects here, not everywhere.','regional comparison; no single moment claimed'),
 shot('dominant','','High oblique at the current bridge connector','Travelers tighten covers beneath inland gusts and early lamps.','The shared road is the editorial anchor for the transition.','regional comparison'),
 shot('regional','','Low wetland-channel detail without principal cast','Later runoff moves through familiar southern channels.','Wetland consequences lag behind exposed ground.','later runoff explicitly not simultaneous')],
 'Three flowing landscape windows separated by unmistakable editorial boundaries; no fake continuous map or new borders. The bridge remains the anchor setting; coastal and wetland windows are documented regional comparisons.',
 'The storm’s noise yields to the temple’s waterfall, then a man-made interruption.')

# Matchup 3: simultaneous vertical relationship, then time-based comedy, one large payoff.
add(12,'vertical_opposed_pov_overture','SIMULTANEOUS_SAME_LOCATION','Who needs quiet and who is enjoying the interruption?',[
 shot('dominant','chins','Courtyard-low upward view through jackhammer, operator and balcony','Seven Deadly Chins starts the localized paving damage below the protected household.','The source of the new noise and the vertical distance are established.'),
 shot('opposed_pov','tds','Close third-person at the balcony rail looking down','Three heads on one body arrive at the rail; the same operator is below.','The father’s perspective connects the interruption to the doorway behind him.')],
 'Vertically opposed views use shared stair, rail and doorway anchors. Separate the angles without placing two copies of either character in one scene. Family remains inside/offscreen.',
 'The father’s downward eyeline leads into the visitor’s acknowledgement.',[(9,12)])
add(13,'pause_hope_choice_sequence','CHRONOLOGICAL_SAME_LOCATION','Did he fail to hear, or hear and decide not to care?',[
 shot('setup','chins','Tight courtyard view of paused tool and upward glance','Seven Deadly Chins lets the jackhammer fall quiet and looks up.','The request has definitely been heard.','first'),
 shot('reaction','tds','Medium balcony view of three distinct head angles','One head turns toward the protected doorway while the others listen in a brief hopeful pause.','Hope makes the next decision sting; the father remains one body.','the pause'),
 shot('dominant','chins','Low three-quarter hand-and-face view with speaker and drill separated','He laughs, reaches for the volume control, then returns attention to the paving.','Renewed noise is a choice, not an unexplained continuous racket.','next; tool paused while hand adjusts music')],
 'Three clearly ordered unequal beats: silence, hope, deliberate refusal. Do not put both hands on the jackhammer while a third hand turns the knob. No new speech bubble, song title or private quote.',
 'The restarted drill carries the movement into the large destructive payoff.',[(9,24)])
add(14,'single_climactic_vertical_master','ONE_CONTINUOUS_MOMENT','What does the deliberate encore leave behind?',[
 shot('dominant','chins,tds','Courtyard-height wide looking up through the same tool and rubble to the rail','Seven Deadly Chins drills the widened patch while the three-headed father reacts above.','Accumulated damage, exhausted frustration and delighted indifference are visible together.')],
 'One big vertical payoff after the multi-view interruption. The expanding crescent of rubble, not an entirely collapsed temple, shows progression. Keep the exact final result once; no extra comic strip.',
 'Cut from chosen racket to the ordinary engine of a delivery truck.')

# Matchup 4: unequal perspectives and a pass, not a new contest.
add(15,'low_high_opposed_pov','SIMULTANEOUS_SAME_LOCATION','Why does the hound think the road belongs to him, and what does the driver see?',[
 shot('dominant','mud','Low over the hound’s shoulder past the existing entrance marker','Mud Dogs asserts himself at the road edge with the loaded flatbed approaching on the higher firm strip.','His territorial claim feels large from his own viewpoint.'),
 shot('opposed_pov','slob','Cab-height close third-person past Slob on my Dobb toward the passable road','The driver checks his mirror and available clearance, the hound small at the safe edge.','To the driver, the confrontation is merely a routine route consideration.')],
 'Unequal low/high POVs connected by the same sign, truck and two ground levels. Paws stay outside the wheel track. Do not turn the asserted blockade into an unavoidable collision.',
 'The driver’s mirror check introduces the uninterrupted pass.',[(9,12),(9,17)])
add(16,'routine_pass_three_beat','CHRONOLOGICAL_SAME_LOCATION','How can doing nothing dramatic be the decisive answer?',[
 shot('detail','slob','Close driver profile and mirror in the cab','Slob on my Dobb gives an ordinary mirror check without a grin or victory signal.','He refuses to perform the confrontation.','first'),
 shot('dominant','slob,mud','Side-on wide across the established service strip','The loaded truck rolls safely past; wheels remain on stone and Mud Dogs follows on the soft shoulder.','The difference in ground and scale—not a stunt—allows the delivery to continue.','next'),
 shot('reaction','mud','Low rear-quarter alongside the hound as the trailer clears','Mud Dogs barks after the last stretch of intact cargo.','His increased effort has not affected the truck’s pace.','then')],
 'Small calm detail, broad pass, modest reaction. No thrown keg, wheel contact, racing acceleration, unloaded cargo or anthropomorphic human body for the hound.',
 'Moving trailer lines empty into the receding road of the final page.',[(9,24)])
add(17,'single_receding_aftermath','ONE_CONTINUOUS_MOMENT','What is left when nobody takes the challenge?',[
 shot('dominant','mud,slob','Wide receding road with the hound small below his own sign','The loaded truck departs into reeds; the small Cancún card flutters beside Mud Dogs.','Silence and lost authority land without a victory pose or eviction.')],
 'A full quiet image with generous depth after the three-beat pass. The postcard is a minor taunt; existing survival and elimination-condition copy stays exact. No actual holiday booking.',
 'The quiet aftermath cuts to the record room where the real player contributions explain the week.')
add(18,'documentary_performance_master','ONE_CONTINUOUS_MOMENT','Which real contributions explain the apparent spectacle?',[
 shot('dominant','','Oblique scoring desk with level, readable records','A clerk works beside the six source-bound leaders and the already supplied performance narrative.','The statistical distinctions—not invented athlete portraits—provide the new information.')],
 'Keep one main information composition. Differentiate starter production, aggregate trios, bench observation and late response by editorial hierarchy, not fictional replays or tiny panels.',
 'The scored-performance folio yields to a newly arrived availability report.')
add(34,'current_report_and_retained_record','EDITORIAL_DOCUMENTARY_COMPARISON','Which report changes the next decision, and which is carried forward?',[
 shot('detail','','Close rain-marked dispatch beside an older ledger','A courier places the fresh dated reports on the existing desk.','New reporting has an arrival and a date; it is not a dramatized medical scene.'),
 shot('dominant','','Wider fixed-lamp reading scene with two document groups','An attendant compares current reports with retained notes.','Current and carry-forward information remain distinct while the complete qualified copy stays readable.')],
 'A restrained documentary detail opens into the reading master. No injured-body vignette, invented diagnosis or certainty beyond the exact supplied copy.',
 'Shift from restrained public reporting to the warm, personal birthday interior.')

# Matchup 5: hospitality, discovery, reaction; preserve the single contact payoff.
add(19,'host_guest_pov_overture','SIMULTANEOUS_SAME_LOCATION','What does the host expect from this apparently generous guest?',[
 shot('dominant','hmb','Low close third-person following the gift-bearing champion down the dining aisle','His Majesty’s Blood enters toward Dr. Duckhook with the oversized wrapped box.','The gift and controlled entrance create apparent generosity.'),
 shot('opposed_pov','duck','Reverse medium from beside the birthday chair toward the same aisle','Dr. Duckhook welcomes the guest; the separate cake remains on its established sideboard.','The host’s social obligation and the rival’s arrival are seen from the other side.')],
 'Two opposing views share window mullion, aisle and cake sideboard. Establish a continuous room, not two unrelated portrait backgrounds; no named new guests or invented age.',
 'Eye-lines converge on the still-wrapped box.',[(9,17)])
add(20,'opening_reveal_reaction','CHRONOLOGICAL_SAME_LOCATION','When does the present become an insult?',[
 shot('detail','duck','Close hands at ribbon and lid','Dr. Duckhook begins opening the existing wrapped gift.','Anticipation precedes knowledge.','first'),
 shot('dominant','hmb,duck','Table-height three-quarter reveal on the same gift axis','The lid clears the colossal double-decker hamburger and exact 200 BURGER flag.','The score-based joke becomes visually legible before narration explains it.','next'),
 shot('reaction','duck','Close host’s bill and eyes with familiar guests soft behind','The host’s gracious expression strains as the guests begin to understand.','Delayed recognition makes the humiliation personal.','after recognition')],
 'Small opening detail, dominant burger reveal, compact reaction. The separate cake stays on the sideboard, the box on the table, and the host in the same seat. No duplicate burger or repeated masthead.',
 'The already visible separate cake becomes the instrument of the payoff.',[(9,13),(9,24)])
add(21,'single_contact_payoff','ONE_CONTINUOUS_MOMENT','How does the birthday itself deliver the consequence?',[
 shot('dominant','duck,hmb','Unobstructed three-quarter contact wide enough for both props','His Majesty’s Blood presses the separate soft cake, candles removed, onto the recognizable orange bill; the untouched burger stays in its open box.','Cake contact, witnesses and the still-visible gift resolve the social mechanism in one strong image.')],
 'Let this moment fill the folio instead of another split. Keep hands, bill, vest, cake and untouched burger distinct, with fixed furniture. Final result once; no sword duel or falling table.',
 'Contrast warm party humiliation with cold mountain resistance; this is an editorial cut, not simultaneous travel.',[(9,18)])

# Matchup 6: establish both forces, earn the counters and preserve active defeat.
add(22,'opposed_forces_then_first_counter','CHRONOLOGICAL_SAME_LOCATION','What must the defender protect, and what resources does the commander have?',[
 shot('setup','obi','Close third-person from the inner arch toward the causeway','ObiWan Jacoby braces with green blade, the separate retriever sheltered behind the threshold.','Home and companion establish what is being defended.','before counter'),
 shot('opposed_pov','llc','Medium three-quarter command-shelf view','The suited LLC commands with the two distinct emplacements visible in the established terrain.','Both batteries exist before one is destroyed.','same pre-counter moment'),
 shot('dominant','obi','Low wide along the established fire line','ObiWan Jacoby’s visible deflection strikes the first emplacement.','The first counterattack earns a real success; the other battery survives.','next')],
 'Two compact opposing intentions lead into one dominant first-counter action. Use neutral terrain landmarks to orient the reverse view; do not reverse advancing direction without the establish. Red fire denotes color, not another team.',
 'The first smoking wreck opens the visual route toward the ridge flank.',[(9,17),(9,24)])
add(23,'counterattack_command_response','CHRONOLOGICAL_SAME_LOCATION','How does the commander answer a meaningful second attempt?',[
 shot('setup','obi','Over-shoulder from the established upper ridge with the first wreck below','ObiWan Jacoby commits to the flank.','The second attempt uses a different route, not a repeated defensive pose.','first'),
 shot('detail','llc','Close medium on the suited executive’s command gesture','The LLC signals from the same command shelf.','His economy of movement contrasts with the defender’s effort.','next'),
 shot('dominant','obi,llc','Wide same-side approach showing one smoking wreck and the sole remaining emplacement turning','The surviving battery rotates into the ridge approach.','The gesture has a physical consequence and no extra battery appears.','response')],
 'Make route, command and response separate visual beats with the battery state carried through all three. Smoke direction and landmark positions stay fixed. No third counterattack or concealed new weapon.',
 'The rotating barrels motivate the retreat into the defended inner arch.',[(9,24)])
add(24,'resistance_and_command_counterview','SIMULTANEOUS_SAME_LOCATION','How can the defense remain brave while the loss remains clear?',[
 shot('dominant','obi','Human-height inward/outward arch view with readable blade, hands and sheltered retriever','ObiWan Jacoby holds under continuing fire; the first emplacement smokes beyond him.','He protects his threshold without being falsely shown victorious or helpless.'),
 shot('counterpoint','llc','Long command-side view aimed back across the same gap','The LLC remains in control as the single surviving battery continues firing toward the arch.','The victor still has resources after both earned counterattacks.')],
 'Dominant active defense plus a smaller command counterview. Never describe the scene as a quiet-ended battle. Keep the surviving battery active and the destroyed battery dead; exact final receipt appears once.',
 'The defended threshold gives way to the practical question of what every team can field next.',[(9,12)])

# League intelligence: documentary detail supports information, not decorative action panels.
add(25,'logistics_detail_and_records_master','EDITORIAL_DOCUMENTARY_COMPARISON','Where are the actual gaps before the next round?',[
 shot('detail','','Close empty equipment hooks and packed kit','The already specified unused hooks contrast with ready traveling equipment.','Absence is a practical logistical fact, not a diagnosis.'),
 shot('dominant','','Wide inhabited loggia with level needs list','The seven required specialist gaps across six teams remain exactly readable.','The list explains the visual absence without implying completed acquisitions.')],
 'A small observational detail and one main readable roster composition; do not break seven needs into seven tiny illustrated cards.',
 'Unfilled needs lead to the distinction between completed moves and proposals.')
add(26,'record_arrival_and_transaction_trails','EDITORIAL_DOCUMENTARY_COMPARISON','What reached a roster rather than remaining a request?',[
 shot('detail','','Close clerk’s hand placing a completed folio','A completed transaction joins the worn archive shelf.','The threshold between requested and recorded is an ordinary visible action.'),
 shot('dominant','','Three-quarter intake master with four level narrative trails','The four existing source-backed move stories share one readable record scene.','Chronology and receiving rosters—not invented manager motives—carry the story.')],
 'Use a documentary action detail, then the main archive composition. The four supplied narratives remain complete and exact, not four invented cinematic events.',
 'Completed moves yield to the actual official table.')
add(27,'single_official_table_master','ONE_CONTINUOUS_MOMENT','What does the official order say that equal records do not?',[
 shot('dominant','','Deep hall with one level twelve-row record','The viewer reads all twelve exact entries in provider order.','The six-team cluster and cutoff are visible without turning points order into seeds.')],
 'One confident information master; do not fracture the standings into panels, crop out teams or duplicate it as a lower paragraph-card illustration.',
 'The league table opens into three different divisional pressures.')
add(28,'single_shared_terrace_three_pressures','ONE_CONTINUOUS_MOMENT','How does the same record create different divisional pressure?',[
 shot('dominant','','Wide public terrace with three existing league standards','Burgers, Pizza and Wings share the institution and landscape while their supplied summaries remain distinct.','The divisions are competitive groupings, not new geographic nations.')],
 'One scene with three coordinated information regions, not three separate realms or disconnected photo panels. Keep the full intro and three exact callouts.',
 'The reader moves from race position to a different question: scoring form.')
add(29,'single_scoring_form_landscape','ONE_CONTINUOUS_MOMENT','Who is producing points, independently of official seeding?',[
 shot('dominant','','Bridge/lake landscape with level ranking in clear atmosphere','The twelve exact scoring-form entries sit beside the visible unchanged 70/30 method.','The different order is explicitly an editorial scoring measure.')],
 'Retain a calm single image and a complete comparative table. No invented probabilities or in-world tournament finish implied by rank.',
 'The ranking yields to routes that remain possible, not to a forecast.')
add(30,'single_depth_playoff_road','ONE_CONTINUOUS_MOMENT','What remains between the teams and the seven places?',[
 shot('dominant','','Upward alpine path with four already specified week markers in depth','The visible climb narrows through the remaining regular-season rounds.','Depth provides sequential anticipation without crowning anyone at the summit.')],
 'One expansive route image. The supplied qualification conditions and seven-berth note remain exact; no odds, winners at the summit or fake branches on a geographic map.',
 'The nearest marker becomes the immediate six Week11 decisions.')
add(31,'dispatch_intent_and_outward_master','EDITORIAL_DOCUMENTARY_COMPARISON','Why do these six next fixtures matter?',[
 shot('detail','','Close secured route-dispatch ribbons under the existing colonnade','The next round’s six assignments await departure.','The fixture list represents imminent commitments, not anonymous decoration.'),
 shot('dominant','','Broad outward terrace with readable fixture/stakes pairs','Each complete away-at-home fixture sits immediately with its existing implication.','Top-seed races, bubble pressure and the verified loss-elimination condition are visibly distinct.')],
 'Small dispatch detail plus one principal outward-looking composition. All six fixtures stay in order; head-to-head and the three divisional rounds occupy a clear closing reading point. No six miniature predicted matches.',
 'Move from the six fixtures to a deliberately spacious two-contender preview.')
add(35,'bridge_establish_and_opposed_pov','SIMULTANEOUS_SAME_LOCATION','What tension exists before either contender acts?',[
 shot('establishing','','Wide oblique of the established bridge with a long empty span','D0nkey K0ng and His Majesty’s Blood occupy opposite approaches.','Distance and shared geometry are explicit before the perspective cuts.'),
 shot('dominant','dk','Close third-person from the centaur’s near approach','D0nkey K0ng looks across unoccupied stone; keep enough of his integrated anatomy visible.','The host-side expectation is a viewpoint, not a declared outcome.'),
 shot('opposed_pov','hmb','Reverse over the champion’s shoulder along the same span','His Majesty’s Blood regards the centaur beyond the opposite pier.','The visitor sees the same unresolved encounter from the other end.')],
 'A thin location overture and two unequal opposing viewpoints. Match parapets, piers and eyelines. No first strike, winner, shared trophy or future damage.',
 'Cut from poised rivalry to the quiet camp preparing for another visitor.',[(9,12),(9,17)])
add(33,'single_quiet_return_of_weather','ONE_CONTINUOUS_MOMENT','How does the same front change a confident winner’s next concern?',[
 shot('dominant','slob','Wide from under the established camp canopy toward Hearthroad and cloud','Slob on my Dobb stands with secured kegs and lamplight while the existing front approaches.','The ordinary cargo links to his delivery, but his own home now faces the next test.')],
 'One lingering full scene after the split preview. Only Slob is physically present; El Niño is implied by the supplied weather/schedule, never an extra unbound figure or guaranteed future win.',
 'End on preparation and incoming weather; no forced cliffhanger explosion.')

arcs=[]
for i,(ids,causal,turn) in enumerate([
([5,6,7],'Visible exit/rope control -> torso catch -> slipping momentum -> controlled fall -> deliberate binding -> public reaction.','The open loop becomes a catch; the taut line becomes a visible knot.'),
([8,9,10],'Attempted repair -> water finds the gap -> explicit later travel -> familiar court arrival -> branch breaks hoop -> present-day recognition.','A material loss follows him through memory and carried mud, not by merging venues.'),
([12,13,14],'Drilling wakes household -> father asks -> tool pauses -> hope -> volume rises -> same paving patch expands.','The silence between pages/within P13 makes the renewed racket meaningful.'),
([15,16,17],'Territorial display -> driver assesses usable road -> safe ordinary pass -> increased barking -> departure -> empty road.','The delivery never stops; the final stillness belongs to the hound.'),
([19,20,21],'Guest welcomed -> box opened -> burger understood -> host reacts -> separate cake contacts face.','Reveal is not payoff; the established cake carries the last page.'),
([22,23,24],'Two forces/two batteries established -> first destroyed -> ridge counter -> command gesture -> survivor turns -> arch defended under continuing fire.','The first wreck and the remaining battery are visual state memory, not replaceable scenery.')],1):
 arcs.append({'id':f'W10-M{i:02}','pages':[f'W10-P{x:02}' for x in ids],'cause_and_effect':causal,'page_turn':turn})
assert set(D)==set(order)
global_rules=[
 'One complete 1080x1920 folio is the output artifact, not a rule requiring one camera view. Multiple shots/POV areas within that folio are explicitly authorized working direction.',
 'Use a visual sequence only when the additional view reveals new information: intention, cause, response or consequence. Do not pad with duplicate crops of the same pose.',
 'Distinguish simultaneous opposing POV from chronological action. Temporal cuts must not read as cloned characters or objects in one continuous space.',
 'Each action folio has a dominant image; subsidiary views earn their space. Avoid identical grids, mandatory equal splits and three strips on every page.',
 'Canon and exact factual lettering outrank novelty. Use each character’s current reference assets in every shot, preserve morphology, costume, companions and named location geometry.',
 'Preserve full publication copy once and in source order. Distribute it deliberately through the visual reading path; no additional mandatory caption below each image, no extra invented dialogue.',
 'A quiet master image and a level documentary table are intentional storytelling choices. Do not panelize every supporting page or turn Opening Drive into six miniature matchup posters.',
 'Match meaningful objects, material states and weather between pages. Editorial visual echoes do not prove physical adjacency, contemporaneity or character travel.',
 'Inspect each native folio and 390px reading proof for POV legibility, coherent cause, readable text and exact score before visual acceptance. Tests verify instructions only, never artistic success.'
]
reg={'schema_version':'1.0','status':'APPLIED_WORKING_VISUAL_STORYTELLING_DIRECTION','one_folio_may_contain_multiple_shots':True,'images_generated':False,'source_basis':['User current visual-storytelling request','Week9 inspected physical pages12/13/17/18/24','Week7 inspected physical page8','Current six-sheet overview','Current PR315 page/copy/cast/encounter contracts'],'global_rules':global_rules,'matchups':arcs,'issue_rhythm':{'opening':'Two characters with contrasting signatures -> inhabited briefing -> civic breath -> exact results.','body':'Vary POV overtures, causal strips, sustained master scenes, reaction details and quiet consequences. No new page count or relabeled scores.','world_connections':['Public scoreboard -> rodeo spectators','Wet rodeo track -> old soccer ruts as editorial match, not adjacency','Falling branch -> wrong-hanging hoop -> regional storm transition','Temple racket -> ordinary truck engine','Delivery silence -> records desk','Archive reports -> warm birthday room','Warm humiliation -> cold mountain resistance','Remaining firepower -> next available lineup','Official standings -> division pressure -> distinct scoring form -> possible routes','Immediate fixtures -> unresolved opposing bridge POVs -> quiet camp and incoming front'],'breathing_pages':['W10-P02','W10-P03','W10-P04','W10-P14','W10-P17','W10-P21','W10-P27','W10-P28','W10-P29','W10-P30','W10-P33']},'pages':[D[pid] for pid in order]}
(P/'visual-storytelling-pass-20261117.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
md=['# Week 10 — sequential visual storytelling pass','', '**Working shot direction applied to the existing 34-folio issue. No new artwork or final visual approval.**','', 'The correction is from illustrated summaries to visual scenes with intention, cause, response and consequence. A complete PNG may contain several authored camera views; that is not the same as generating a six-up approximation. Prior approved story, full prose, final facts and character/location references remain controlling.','', '## Source precedent versus new proposal','', 'Inspected Week9 physical12 pairs opposite viewpoints across the same terrace. Physical13 uses damage/intent, hood impact and driver reaction. Physical17 combines a wide establishing strip with opposing character views; physical18 instead gives the mechanism room in a single wide. Physical24 uses an opening movement strip, dominant action and counter-move. Week7 physical8 demonstrates an effective single-image court composition. These are source observations. The following Week10 shots are newly authored applications, not claims that revised artwork already exists.','', '## Issue-wide rhythm','',reg['issue_rhythm']['opening'],'',reg['issue_rhythm']['body'],'']
for a in arcs:
 md+=['### '+a['id']+' · '+ ' / '.join(a['pages']),a['cause_and_effect'],'',a['page_turn'],'']
md+=['## Page-by-page direction','']
for p in reg['pages']:
 md+=['### '+p['page_id']+' — '+pages[p['page_id']]['title'],'','**Visual question:** '+p['visual_question'],'','**Structure:** '+p['structure']+' · '+p['time_logic'],'']
 for s in p['shots']:md+=['**'+s['id']+' · '+s['role']+'** — '+s['camera']+'. '+s['action']+' '+s['new_information']+' Time: '+s['time_relation']+'.','']
 md+=['**Page composition:** '+p['layout_direction'],'','**Turn to next page:** '+p['page_turn_out'],'']
md+=['## Acceptance: not more pictures for their own sake','', 'Each additional view must reveal something not available in the dominant view. Opposed POVs must agree on place and time; sequential views must show physical change. Result text appears once on the existing payoff, all original narration remains, and original tables retain exact rows. Single-image breathing pages are deliberate. A six-up view can show rhythm but cannot certify native-page readability or character consistency.','', 'The actual revised page images still require Jake’s visual judgment; source and test validation do not establish that the rendering meets his taste.']
(P/'VISUAL_STORYTELLING_PASS_2026-11-17.md').write_text('\n'.join(md)+'\n')
print(json.dumps({'pages':len(D),'cinematic_pages':18,'visual_beats':sum(len(p['shots']) for p in D.values()),'multi_view_folios':sum(len(p['shots'])>1 for p in D.values()),'single_master_folios':sum(len(p['shots'])==1 for p in D.values()),'new_images':0},indent=2))
