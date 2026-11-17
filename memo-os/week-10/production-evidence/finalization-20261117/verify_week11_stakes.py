"""Check user-supplied Week11 stakes against official records and schedule.
Constructive qualification witnesses refute automatic loss-elimination labels.
No probability estimates are calculated from this search.
"""
from pathlib import Path
from copy import deepcopy
import importlib.util,json,random
E=Path(__file__).resolve().parent;P=E.parents[3]/'memo-os/week-10/preproduction'
spec=importlib.util.spec_from_file_location('playoffs',E/'revalidate_playoffs.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rng=random.Random(20261117);fixtures=sorted(m.remaining);results={}
for tid in (2,6,7,1,4):
 found=None
 for trial in range(20000):
  winners=[]
  for week,h,a in fixtures:
   if tid in (h,a):win=(a if h==tid else h) if week==11 else tid
   else:win=rng.choice([h,a])
   winners.append({'week':week,'home_team_id':h,'away_team_id':a,'winner_team_id':win})
  outcome=m.recalc({'winners':winners})
  if tid in outcome['qualified_team_ids']:
   found=outcome;break
 assert found is not None,('No witness found; cannot assert automatic elimination or continued viability',tid)
 results[str(tid)]={'team':m.base[tid]['name'],'week11_loss_automatically_eliminates':False,'counterexample_to_automatic_elimination':found,'search_trials':trial+1,'search_frequency_is_not_probability':True}
report={'scope':'USER_SCREENSHOT_WEEK11_STAKES_AUDIT','source_screenshot':'Screenshot 2026-11-17 at11.35.31.png','source_file_id':'file_00000000a75c81f59b51b4c14332d1e0','source_folio_screenshot':'file_00000000478881f5bac082e8c6728fd6','target_page_id':'W10-P31','reading_position':32,'sheet':6,'source_interpretation':'Screenshot owner shorthand resolved through provider Week11 pairings, not character invention. Wilson=D0nkey K0ng; me=His Majesty’s Blood in this pairing; Manning=El Niño; Holli=Slob on my Dobb; Zeek=Red Leopards; Pitts=Three Dreaded Snake; Chili=The Chili Cheesers; you=ObiWan Jacoby; LLC=The LLC; Zack/h=Dr. Duckhook.','accepted':['His Majesty’s Blood at D0nkey K0ng:6–4 vs6–4, top-seed contention','El Niño at Slob on my Dobb:6–4 vs6–4, top-seed contention','Red Leopards at Three Dreaded Snake:5–5 vs4–6, high-leverage bubble matchup','The Chili Cheesers at ObiWan Jacoby:5–5 vs4–6, high-leverage bubble matchup','The LLC at Dr. Duckhook:4–6 vs6–4, recovery/playoff pressure versus top-seed contention','Head-to-head can matter in tiebreaks; all three closing regular-season rounds are divisional'], 'corrected_claim':'The screenshot’s LLC elimination-game wording is not a mathematical win-or-out claim: a verified qualifying path survives a Week11 loss. Same distinction applies to the other bubble teams.','bubble_loss_witnesses':results,'true_loss_elimination_game':{'away':'Seven Deadly Chins','home':'Mud Dogs','basis':'Mud Dogs drops to2–9 on a loss and can finish with at most5 wins; six teams already have6, and Red Leopards/The Chili Cheesers remaining meeting guarantees another superior record. Division leader D0nkey K0ng already has6.','week11_loss_eliminates_mud_dogs':True},'references':['final-league-snapshot.json','playoff-witnesses-final.json','https://support.espn.com/hc/en-us/articles/47190901074708-H2H-Points-League-Playoff-Seeding-Tiebreakers'],'no_odds_claimed':True}
(E/'week11-implications-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'target':'W10-P31','non_eliminating_loss_witnesses':{v['team']:v['search_trials'] for v in results.values()},'mud_loss_eliminates':True},ensure_ascii=False,indent=2))
