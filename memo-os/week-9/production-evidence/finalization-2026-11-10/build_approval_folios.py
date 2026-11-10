#!/usr/bin/env python3
"""Build Week9 final-result APPROVAL candidates; never approve/render/publish.

Uses the already-merged November10 source packet, corroborated by fresh Flaim
reads in this session. Existing canonical-release fields stay on HOLD. Each
active page receives an explicitly separate approval_folio consumed by the
new reading proof; the old provisional copy is historical, not this review.
No network, image generation, secrets, paid provider or scheduled work.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import copy
import hashlib
import html
import importlib.util
import json
import re

ROOT=Path(__file__).resolve().parents[4]
W=ROOT/'memo-os/week-9'
E=Path(__file__).resolve().parent
BASE='5767fd46f1b383420c061b1ab59bacdfc1fa4b79'
DATE='2026-11-10'
NAME='WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10'
REG='WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json'
DESK='WEEK_9_FINAL_SPORTS_DESK_EVIDENCE_2026-11-10.json'
CARDS='WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json'
RECEIPT='production-evidence/finalization-2026-11-10/REVALIDATION.json'
# Selected-field transcription of the actual fresh Flaim responses, not a
# fabricated example or a replacement for the preserved earlier full payload.
LIVE=[('W09-M01',12,1,'166.56','144.46','HOME'),('W09-M02',10,9,'84.20','125.54','AWAY'),('W09-M03',2,11,'118.58','112.18','HOME'),('W09-M04',7,8,'152.84','135.08','HOME'),('W09-M05',5,4,'158.70','129.89','HOME'),('W09-M06',3,6,'165.66','159.56','HOME')]
# id,wins,losses,pointsFor,pointsAgainst,playoffSeed,currentProjectedRank
LIVE_STANDINGS=[(12,6,3,'1324.48','1285.07',1,1),(9,5,4,'1260.95','1207.81',2,7),(5,5,4,'1255.15','1238.09',3,3),(2,5,4,'1256.69','1157.64',4,8),(8,5,4,'1243.19','1218.94',5,6),(11,5,4,'1210.40','1145.84',6,4),(3,5,4,'1420.70','1291.30',7,2),(7,5,4,'1291.09','1299.60',8,5),(1,4,5,'1217.98','1217.93',9,9),(6,4,5,'1196.68','1255.96',10,10),(4,3,6,'1245.29','1340.89',11,11),(10,2,7,'1067.73','1331.26',12,12)]
W10=[(7,5),(2,9),(6,11),(10,3),(12,8),(1,4)]
# The120 actual starter player IDs/points were freshly re-read through six
# Flaim detail=players calls. Compare them to the preserved full source packet.
LIVE_STARTERS={
12:'4429795=15.40;4569173=15.40;4701936=33.40;4429205=4.80;4431452=24.36;4711533=9.00;4361370=16.80;-16030=17.00;3917232=13.00;15847=17.40',
1:'3043078=7.28;4567048=39.10;4372016=3.20;4426515=36.20;-16014=16.80;4428331=9.90;4360310=17.68;3055899=5.00;3116164=3.10;3117256=6.20',
10:'3929630=9.50;4890973=7.60;4430027=7.20;3040151=9.80;3916433=10.50;3046779=5.70;4429059=10.20;15818=6.60;4249087=7.00;-16005=10.10',
9:'4379399=20.80;4362238=11.40;4239993=20.20;4572680=2.10;2976212=8.10;4258173=15.50;4428718=9.50;2971573=17.00;14880=14.84;-16018=6.10',
2:'4362628=34.50;4429615=5.60;4688813=5.40;4385690=5.80;4426385=11.20;4430737=10.60;4571557=16.00;4695883=6.70;4433970=7.68;-16003=15.10',
11:'4262921=8.80;4259545=4.30;4567750=7.00;3139477=20.68;4431459=8.40;4429096=12.90;-16026=18.80;4373626=8.30;3150744=10.00;4869645=13.00',
7:'4374302=16.60;4595348=9.30;4248528=31.10;4432665=23.40;2473037=6.00;3046439=6.50;4685720=26.44;5081397=8.60;-16019=19.00;4241555=5.90',
8:'4430878=12.10;4426388=5.10;4241416=15.20;4697815=8.70;4430539=4.20;5083754=7.30;4702555=20.50;4686361=17.00;-16008=15.00;4361741=29.98',
5:'4430807=29.60;4361307=12.40;4427366=13.20;2577417=26.70;3953687=10.00;-16034=15.80;3054850=8.50;4384852=13.40;4686422=13.30;4832800=15.80',
4:'4242335=10.70;4432620=16.65;4360761=12.00;3915511=37.84;4723086=9.40;4361050=16.30;4569603=4.20;-16029=6.80;17427=9.00;4685702=7.00',
3:'3117251=24.50;4241389=36.50;3918298=15.46;4685472=15.60;5083076=12.20;4047365=0.90;-16007=9.20;4596448=30.50;4567104=9.00;4426502=11.80',
6:'4870795=12.10;4361579=25.40;4431611=19.26;4036133=7.30;4685278=22.70;-16025=24.80;4882093=10.10;4870653=20.90;4612826=0.00;5082424=17.00'}

FINAL_DIRECTION={
'W09-M01':'Duckhook is the winner. Keep his controlled golf execution; ObiWan suffers the costly poor recovery/approach/short putt and emotional loss. Do not draw Duckhook losing into the pond. No invented golf stroke totals.',
'W09-M02':'El Niño wins. The four-legged Mud Dogs and adapted bike become immobilized in deep mud/water before the visible finish. The embodied storm elemental remains recognizable. Do not label Mud Dogs mathematically eliminated.',
'W09-M03':'Red Leopards wins. Damage precedes retaliation; his staged ambush and stone bottleneck defeat the lifted-truck intrusion. Do not make a goal net alone stop the truck.',
'W09-M04':'Chili wins. The established cart/catch mechanism leads to HMB covered in chili; retain hooded identity, comic rather than burn-injury tone, and no championship-belt transfer.',
'W09-M05':'DK wins. Visible parry, four-equine-leg turn and leverage overpower the recognizable armored LLC. One integrated Arsenal gorilla-centaur, not a bipedal ape.',
'W09-M06':'Slob wins. P21 camera is third person behind the sliding heavyset human winner, marker aimed downrange; losing three-headed TDS is visible with paint impacts on protected mask/body. P20 remains the build, with no premature player hit.'}
CAUSE={
'W09-M01':'Matthew Golden scored 33.40 and Drake Maye 24.36 for Duckhook. Addison and Bass added 17.80 to his pre-MNF lead. Walker and Nacua supplied ObiWan with 75.30, but the host finished 22.10 ahead.',
'W09-M02':'James Cook III scored 20.80 and Tee Higgins 20.20 for El Niño. Mud Dogs finished on 84.20 with Jared Goff at 5.70 and no starter above 10.50. The final margin was 41.34, not a verified elimination.',
'W09-M03':'Ja’Marr Chase delivered 34.50 for Red. Jefferson’s 8.80 exceeded Kincaid’s 5.80 by 3.00, but Chins had entered Monday 9.40 behind. Red retained a 6.40 advantage.',
'W09-M04':'Christian Watson, Bryce Young and Brock Bowers supplied 80.94 for Chili. HMB received 29.98 from Brock Purdy and 20.50 from Jonah Coleman but finished 17.76 short.',
'W09-M05':'Bijan Robinson and Dak Prescott combined for 56.30 as DK won by 28.81. Joe Burrow’s 37.84 gave the LLC a real response, not enough to overturn the broader gap.',
'W09-M06':'Slob entered Monday 11.06 behind. Josh Allen and Will Reichard added 24.46 against Hockenson’s 7.30: a 17.16 swing and a 6.10 win. Lamb, Irving and McCaffrey had supplied 91.50.'}
FINALES={'W09-P07':'W09-M01','W09-P10':'W09-M02','W09-P13':'W09-M03','W09-P15':'W09-M04','W09-P18':'W09-M05','W09-P21':'W09-M06'}


def load(path):
    return json.loads(Path(path).read_text())

def dump(path,value):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def money(value):
    d=Decimal(str(value))
    if not d.is_finite():
        raise ValueError('Nonfinite score')
    return d.quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def table_html(rows):
    if not rows:
        return ''
    keys=list(rows[0])
    def val(v):
        return 'Not reported' if v is None else ', '.join(map(str,v)) if isinstance(v,list) else str(v)
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+html.escape(k.replace('_',' '))+'</th>' for k in keys)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(val(row.get(k)))+'</td>' for k in keys)+'</tr>' for row in rows)+'</tbody></table></div>'


def main():
    issue=load(W/REG);cards=load(W/CARDS);src=load(W/DESK)
    before=copy.deepcopy(issue)
    assert len(issue['reading_order'])==35 and len(issue['pages'])==40
    assert str(src['league_id'])=='1417621' and src['season']==2026 and src['week']==9
    names={int(c[s]['teamId']):c[s]['name'].strip() for c in cards['cards'] for s in ['home','away']}
    owners=load(ROOT/'world/data/owner_domains.json')['domains']
    divisions={int(d['team_id']):d['division_id'].replace('DIV-','').title() for d in owners}
    standings=[]
    for tid,wins,losses,pf,pa,seed,projected in LIVE_STANDINGS:
        standings.append({'team_id':tid,'team':names[tid],'division':divisions[tid],'wins':wins,'losses':losses,'ties':0,'record':f'{wins}–{losses}','points_for':pf,'points_against':pa,'current_seed':seed,'projected_rank':projected,'clinched':None})
    by_stand={r['team_id']:r for r in standings}
    source_match={m['pair']:m for m in src['matchups']}
    side_sources={};rows=[];matchups=[];normal_matches=[]
    for mid,hid,aid,hp,ap,winner in LIVE:
        m=source_match[f'{hid}:{aid}'];card=next(c for c in cards['cards'] if c['id']==mid)
        assert m['winner']==winner
        winner_id=hid if winner=='HOME' else aid
        nm={'matchupPeriodId':9,'winner':winner}
        for side,tid,pts in [('home',hid,hp),('away',aid,ap)]:
            v=m[side];assert int(v['teamId'])==tid and money(v['points'])==money(pts)
            players=[p for p in v['players'] if p['started']]
            observed={str(p['playerId']):money(p['points']) for p in players}
            fresh={k:money(n) for k,n in (pair.split('=') for pair in LIVE_STARTERS[tid].split(';'))}
            assert len(players)==10 and observed==fresh,(tid,'fresh starter mismatch')
            assert sum(observed.values())==money(pts),(tid,'starter sum')
            side_sources[tid]=v
            for p in players:
                rows.append({'fantasy_team_id':tid,'player_id':str(p['playerId']),'name':p['name'],'lineup_slot':p['lineupSlot'],'points':float(money(p['points'])),'started':True})
            old=[int(n) for n in re.findall(r'\d+',card[side]['record'])]
            assert old[0]+int(tid==winner_id)==by_stand[tid]['wins']
            assert old[1]+int(tid!=winner_id)==by_stand[tid]['losses']
            nm[side]={'teamId':tid,'teamName':names[tid],'currentPoints':float(money(pts)),'totalPoints':float(money(pts))}
        normal_matches.append(nm)
        matchups.append({'matchup_id':mid,'home_team_id':hid,'home':names[hid],'home_score':hp,'away_team_id':aid,'away':names[aid],'away_score':ap,'provider_winner':winner,'winner_team_id':winner_id,'winner':names[winner_id],'margin':str(abs(money(hp)-money(ap))),'selected_branch':'home_win' if winner=='HOME' else 'away_win','home_postweek_record':by_stand[hid]['record'],'away_postweek_record':by_stand[aid]['record'],'sports_cause':CAUSE[mid],'final_visual_direction':FINAL_DIRECTION[mid]})
    assert len(rows)==120 and len(side_sources)==12
    # Actual fresh fields revalidated this morning's complete preserved packet.
    observation={'request':{'league_id':'1417621','season_year':2026,'week':9},'recorded_at_utc':'2026-11-10T15:33:00+00:00','representation':'Selected-field transcript of current-session Flaim reads; source values normalized to two displayed decimals. Earlier full player packet reused only after all120 fresh ID/point values match. Not native HTTP wire.','matchups_response':{'success':True,'data':{'leagueId':'1417621','seasonYear':2026,'currentScoringPeriod':10,'matchupPeriod':9,'matchups':normal_matches}},'lineup_evidence':{'league_id':'1417621','season_year':2026,'week':9,'recorded_at_utc':'2026-11-10T15:33:00+00:00','source_ref':'Fresh Flaim six Week9 detail=players reads; matched against '+DESK,'rows':rows},'standings':standings,'week10':W10,'transactions_recheck':{'week':9,'returned_rows':42,'truncated':False,'structured_details_incomplete':True,'completed_trade_id':'7b8c6c8e-b48c-4521-a464-a886d42a4297','completed_exchange':'London to Slob; Judkins to LLC','canceled_proposal_id':'bfcbb7d2-0375-4d98-9f14-deee8a562bdd','source':'Fresh Flaim get_transactions explicit week9 count100; selected corroboration, not a new full transcript'},'source_packet':{'path':DESK,'sha256':sha(W/DESK),'base_commit':BASE},'capture_note':'Session lookup timestamp2026-11-10T15:23:59.564Z; selected-field receipt timestamp is an end-bound transcription time, not a provider HTTP timestamp.','source_accepted':False,'new_scene_images':0}
    spec=importlib.util.spec_from_file_location('existing_week9_preparer',W/'prepare_production_inputs.py');preparer=importlib.util.module_from_spec(spec);spec.loader.exec_module(preparer)
    proposal=preparer.reconcile(issue,cards,observation)
    assert proposal['status']=='RECONCILED_CANDIDATE_NOT_ACCEPTED',proposal
    dump(E/'REVALIDATION.json',observation);dump(E/'RESULT_PREVIEW.json',proposal)
    finals={m['matchup_id']:m for m in matchups};source_path='memo-os/week-9/'+RECEIPT
    pages={p['page_id']:p for p in issue['pages']};folios=[]
    for position,pid in enumerate(issue['reading_order'],1):
        p=pages[pid];c=p['editorial_copy']
        f={'page_id':pid,'reading_position':position,'working_title':p['working_title'],'page_role':p['page_role'],'state':'FINAL_RESULT_DRAFT_FOR_APPROVAL_NOT_PNG_AUTHORIZATION','canvas':[1080,1920],'copy':{'headline':c['headline'],'deck':c.get('deck',''),'body':c['body']},'cast':copy.deepcopy(p['characters_present']),'references':copy.deepcopy(p.get('reference_assets',[])),'layout':copy.deepcopy(p['layout_spec']),'scene':copy.deepcopy(p.get('written_storyboard',{})),'environment':copy.deepcopy(p.get('encounter',{})),'selected_branch':None,'is_finale':pid in FINALES,'opposite_ending_in_publication_copy':False,'data_rows':[],'report_cards':[],'source_path':source_path,'render_authorized':False,'publication_approved':False,'source_acceptance':False,'pixel_fit':'NOT_TESTED_WITH_FINAL_ART_AND_POPULATED_NUMBERS','approval_notes':['Content/source review first; no PNG requested in this pass.']}
        if 'pov' in c:
            f['copy']['pov']=copy.deepcopy(c['pov'])
        mid=p.get('matchup_id')
        if mid in finals:
            m=finals[mid];f['result_context']=copy.deepcopy(m);f['selected_branch']=m['selected_branch'];f['final_visual_direction']=m['final_visual_direction']
            f['entering_records']={side:next(x for x in cards['cards'] if x['id']==mid)[side]['record'] for side in ['home','away']}
            f['postweek_records']={'home':m['home_postweek_record'],'away':m['away_postweek_record']}
            if f['is_finale']:
                f['copy']['body']=c['conditional_narratives'][m['selected_branch']]
                f['score_panel']={'home':m['home'],'home_score':m['home_score'],'away':m['away'],'away_score':m['away_score'],'winner':m['winner'],'margin':m['margin']}
                f['sports_note']=m['sports_cause']
            elif p['page_role']=='two_character_pov_overture':
                f['result_in_art']=False
                f['copy']['stakes']=f"Entering Week9: {f['entering_records']['home']} vs {f['entering_records']['away']}. Two perspectives; the outcome belongs to the finale."
            elif pid in ['W09-P05','W09-P09','W09-P12','W09-P14','W09-P17','W09-P20']:
                f['sports_note']=m['sports_cause']
            if pid=='W09-P05':
                f['performance_edit']='Retain tee/recovery/reaction choreography; favor Duckhook-controlled shots and ObiWan costly recovery. No trophy or final putt on this montage.'
            if pid=='W09-P20':
                f['performance_edit']='Both still compete aggressively. No body-hit/elimination here; final Slob-winner angle is onP21.'
        folios.append(f)
    fs={f['page_id']:f for f in folios}
    def body(pid,text,headline=None,deck=None):
        f=fs[pid];f['copy']['body']=text
        if headline:f['copy']['headline']=headline
        if deck:f['copy']['deck']=deck
    body('W09-P02','A new arrival gave the Commonwealth a reason to celebrate. The standings supplied a reason to keep checking the scoreboard. Duckhook leaves Week9 alone at 6–3; seven teams sit immediately behind him at 5–4. Slob overturned an 11.06-point Monday deficit, Red survived by 6.40, and Chili sent the Belt Keeper home wearing the cookout. Five regular-season weeks remain. The routes differ by division, but the pressure belongs to the whole league.','Seven Teams. One Record.','Week9 closes. The postseason squeeze does not.')
    body('W09-P03','Six decided matchups. Duckhook posted the high score; Slob and Red survived the two narrowest finishes.','Week 9 — The Results','ESPN/Flaim provider-final results · November10')
    fs['W09-P03']['data_rows']=[{'home':m['home'],'points':m['home_score'],'away':m['away'],'away_points':m['away_score'],'winner':m['winner'],'margin':m['margin']} for m in matchups]
    body('W09-P22','The week rewarded depth, punished a low floor, and left one of its strongest scores on the wrong side of the result.','Why the Week Turned','The Good. The Bad. The Ugly.')
    fs['W09-P22']['report_cards']=[{'label':'THE GOOD','heading':'The comeback had a foundation','text':'Lamb, Irving and McCaffrey gave Slob 91.50. Allen and Reichard then supplied 24.46 on Monday against Hockenson’s7.30, turning an11.06deficit into a6.10win.','classification':'FINAL_STARTER_CONTRIBUTIONS_AND_ARITHMETIC'}, {'label':'THE BAD','heading':'No rescue above10.50','text':'Mud Dogs scored84.20. Goff returned5.70 and no starter exceeded10.50. El Niño’s Cook and Higgins combined for41.00 in a41.34-point win.','classification':'FINAL_LINEUP_DISTRIBUTION_NOT_DIAGNOSIS'}, {'label':'THE UGLY','heading':'Third-best score. Still a loss.','text':'TDS’s159.56 was the week’s third-highest score. It would beat nine of the other eleven totals, but Slob’s165.66 was the actual opponent. McConkey’s0.00 is a lineup fact, not a claim about its cause.','classification':'DERIVED_ALL_PLAY_CONTEXT_NOT_AN_ALTERNATE_LEAGUE_RESULT'}]
    body('W09-P23','The completed London–Judkins exchange reached both starting lineups:11.80 for London with Slob and7.00 for Judkins with the LLC. Neither trade impact nor a bench score should be mistaken for a complete alternate-lineup calculation.','Moves That Mattered','Completed deals, receiving lineups, and proposals that ended.')
    fs['W09-P23']['report_cards']=[{'label':'COMPLETED EXCHANGE','heading':'New uniforms, real points','text':'November5: Drake London to Slob; Quinshon Judkins to the LLC. Both started in Week9. Fresh structured activity retains the completed trade.'},{'label':'NOT A COMPLETED TRADE','heading':'Lawrence and DeVonta stayed put','text':'The November5 proposal was canceled/declined on November6. Its historical pending row is not a live offer or a completed exchange.'},{'label':'ACQUISITION CONTEXT','heading':'The margins included new pieces','text':'Chili’s acquired Giants D/ST scored19.00; DK’s added Xavier Hutchinson scored13.30. The returned42transaction records include lifecycle events, not42completed deals.'}]
    body('W09-P24','Duckhook leads at6–3. Seven teams share5–4; Chili occupies seed8 despite the same record as seeds2–7. These are current ESPN positions, not clinched berths.','Seven Places, Twelve Teams','Post-Week9 standings · current ESPN seed, not final finish')
    fs['W09-P24']['data_rows']=copy.deepcopy(standings)
    # A deliberately disclosed editorial index: a ranking of scoring form,
    # NOT ESPN ranks, playoff odds or an injury-aware prediction.
    weekly={tid:money(side_sources[tid]['points']) for tid in side_sources}
    power=[]
    for r in standings:
        score=Decimal('0.70')*money(r['points_for'])/9+Decimal('0.30')*weekly[r['team_id']]
        power.append({'team_id':r['team_id'],'team':r['team'],'record':r['record'],'season_ppg':str((money(r['points_for'])/9).quantize(Decimal('.01'))),'week9_points':str(weekly[r['team_id']]),'scoring_form_index':str(score.quantize(Decimal('.01'))),'unrounded':score})
    power.sort(key=lambda r:(r['unrounded'],weekly[r['team_id']],-r['team_id']),reverse=True)
    for i,r in enumerate(power,1):r['power_rank']=i;r.pop('unrounded')
    body('W09-P25','Slob leads this scoring-form view; Duckhook owns the official top seed. The index blends70%season points per game with30%Week9 scoring. It measures scoring form—not playoff probability, roster health, or an official seed.','The Twelve — Power Watch','Editorial scoring-form order · methodology submitted for approval')
    fs['W09-P25'].update(data_rows=power,ranking_classification='EDITORIAL_SCORING_FORM_NOT_ESPN_SEED_OR_ODDS',methodology='0.70*(season points for/9)+0.30*Week9 points; ties by Week9 score then stable team ID. No historical movement arrows.',methodology_approved=False)
    body('W09-P26','Chili hosts DK with both5–4, but their current positions differ: Chili is seed8; DK holds seed3. That cross-divisional contest is the proposed Week10 spotlight. Duckhook–HMB remains the alternate.','The Next Six','Week10 fixtures · GOTW candidate: Chili Cheesers vs D0nkey K0ng')
    fs['W09-P26']['data_rows']=[{'home_team_id':h,'home':names[h],'home_record':by_stand[h]['record'],'away_team_id':a,'away':names[a],'away_record':by_stand[a]['record']} for h,a in W10]
    fs['W09-P26']['gotw_candidate']={'home_team_id':7,'away_team_id':5,'approved':False,'alternative':[12,8],'reason':'Shared5–4record, different qualification position; no quantified probability swing claimed.'}
    fs['W09-P27']['book_state']='CLOSED_ONE_WEEK'
    body('W09-P28','The scoreboards are settled; the league is not. Seven teams share5–4, and the line between seventh and eighth is already separating identical records. Duckhook has a lead, not a guarantee. ObiWan and TDS have ground to recover; the LLC and Mud Dogs cannot afford to waste the remaining road. Five weeks stand between this crowded table and the postseason. The next victory will matter to more than the two teams playing for it.','The Road Narrows','Five weeks remain. A place in the tournament is the next prize.')
    reserve=[]
    for tid,v in side_sources.items():
        for p in v['players']:
            if p['lineupSlot']=='IR':reserve.append({'team_id':tid,'team':names[tid],'player':p['name'],'scope':'Week9 fantasy IR slot','NFL_IR_verified':False})
    body('W09-P37','Reserve slots show which names were outside the Week9 scoring lineup, not a new NFL diagnosis. The observations below preserve the actual fantasy ownership. Return dates and medical explanations remain unreported until an official source supports them.','Availability Watch','Week9 fantasy-reserve snapshot · not newly confirmed NFL IR news')
    fs['W09-P37'].update(availability_scope='WEEK9_FANTASY_IR_SLOTS_NOT_NEW_NFL_IR_NEWS',official_injury_news_verified=False,data_rows=reserve)
    groups=[('QUARTERBACK DEPTH',[2,9]),('TDS AND THE LLC',[6,4]),('OTHER RESERVE PRESSURE',[1,3,5,7,8,11,12])]
    for label,tids in groups:
        vals=[x for x in reserve if x['team_id'] in tids]
        text='; '.join(x['team']+': '+x['player'] for x in vals)
        fs['W09-P37']['report_cards'].append({'label':label,'heading':'Observed fantasy reserve occupancy','text':text,'status':'FACTUAL_SLOT_REPORT_MEDICAL_NEWS_NOT_VERIFIED'})
    fs['W09-P37']['approval_notes'].append('Official injury/return-timetable reporting remains a source gap. Approve a strictly labeled reserve snapshot or obtain official reporting before enriching this page; do not label all17 as new NFL IR placements.')
    body('W09-P38','Three division races feed one shared cutoff. Duckhook, El Niño and DK occupy the current division-leader seeds. The next group has little separation: seven teams are5–4, while Chili is the first team outside the present seven-place field.','State of the Realm','Different division stories. The same shrinking margin.')
    fs['W09-P38']['report_cards']=[{'label':'BURGERS','heading':'DK takes the front','text':'DK stands5–4 at seed3. ObiWan and TDS are4–5 at seeds9and10; Mud Dogs is2–7. The arena win gives DK separation within the division, not a clinch.'},{'label':'PIZZA','heading':'Three tied records, different seeds','text':'El Niño, HMB and Chins are all5–4. ESPN assigns them seeds2,5and6; the LLC is3–6 at11. El Niño’s current division-leader position comes from the provider order, not a fabricated tiebreak explanation.'},{'label':'WINGS','heading':'The leader and the squeeze','text':'Duckhook is6–3. Red, Slob and Chili are5–4 at seeds4,7and8. Slob leads season scoring with1420.70, yet sits on the current cut line; Chili shares the record but stands just outside.'}]
    body('W09-P39','Nine weeks are complete; five regular-season games remain for each team. Three division winners qualify, with four additional places determined by the league’s standings and seeding rules. Weeks12–14 return to division play. Current seed does not mean clinched, and a poor record does not by itself prove elimination.','Five Weeks. Seven Places.','Weeks10–14: five games per team; thirty league fixtures')
    fs['W09-P39']['report_cards']=[{'label':'THREE DIVISION ROUTES','heading':'Win your race','text':'The division winners take automatic berths. Current leaders are Duckhook in Wings, El Niño in Pizza, and DK in Burgers; none is labeled clinched here.'},{'label':'FOUR OTHER PLACES','heading':'The whole league is your scoreboard','text':'Remaining berths are shared across divisions. The configured head-to-head seeding tiebreak applies under its league rules; equal records do not guarantee equal seeds.'},{'label':'THE DIVISIONAL RETURN','heading':'Weeks12–14','text':'The final three regular-season weeks are divisional in the verified schedule. Five games remain after Week9; those final meetings can alter both an automatic route and the shared cutoff.'}]
    body('W09-P40','Slob is current seed7 but ESPN projected rank2; Chili is seed8 and projected rank5. Those are different views of the race, not promises. The feed supplies no playoff percentages, so this tracker reports positions and projected ranks only.','The Race to Seven','Current ESPN seed versus ESPN projected rank · not playoff probabilities')
    fs['W09-P40'].update(percentages_available=False,data_rows=[{'team_id':r['team_id'],'team':r['team'],'current_seed':r['current_seed'],'projected_rank':r['projected_rank'],'clinched':None} for r in standings])
    fs['W09-P01']['cover_teasers']=['Duckhook takes the GOTW','Slob flips Monday night','Seven teams at5–4']
    fs['W09-P01']['approval_notes'].append('Retain the established family-first cover; no invented birth measurements, medical detail or real-family likeness.')
    # Publication spacing: authoring above uses compact numerals; reader copy
    # is normalized without changing exact team names, statistics or meaning.
    def readable(s):
        # Canonical team names with digits are not typography mistakes.
        protected='CANONICALDONKEYALIAS'
        s=s.replace('D0nkey K0ng',protected)
        s=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ',s)
        s=re.sub(r'(?<=\d)(?=[A-Za-z])', ' ',s)
        s=re.sub(r'%(?=[A-Za-z])', '% ',s)
        return s.replace(protected,'D0nkey K0ng')
    for f in folios:
        for k,v in list(f['copy'].items()):
            if isinstance(v,str):f['copy'][k]=readable(v)
        for card in f['report_cards']:
            for k in ['label','heading','text']:
                if k in card:card[k]=readable(card[k])
        # Finales are exact previously prepared paragraphs, not regenerated.
        if f['is_finale']:
            f['copy']['body']=pages[f['page_id']]['editorial_copy']['conditional_narratives'][f['selected_branch']]
        f['copy']['body_word_count']=len(f['copy']['body'].split())
        f['copy_fit_review']='FINAL_VALUES_SELECTED; COMBINED1080x1920ART/TABLE/ENDINGFITSTILLREQUIRESREVIEW'
        if f['page_id'] in ['W09-P25','W09-P37','W09-P40']:
            f['approval_notes'].append('Data is populated for editorial review. Final density/typography must be measured on the actual page; do not shrink text to force fit.')
        pages[f['page_id']]['approval_folio']=copy.deepcopy(f)
    revalidation={'date':DATE,'source':RECEIPT,'status':'SIX_PROVIDER_FINALS_AND120STARTERVALUES_RECONCILED','source_accepted':False,'render_authorized':False,'review_artifact':NAME+'.md','execution':'GitHub-hosted deterministic preparation while authorized Mac offline; no live local ConsultEngine consultation claimed.'}
    issue['finalization_review']={'version':'W09-FINAL-APPROVAL-2026-11-10','state':'READY_FOR_CONTENT_APPROVAL_WITH_EXPLICIT_REMAINING_GAPS','source':revalidation,'approval_packet':NAME+'.json','reading_proof':NAME+'.html','page_selector':'pages[page_id].approval_folio','effective_review_copy':'approval_folio.copy supersedes provisional editorial_copy ONLY for this approval review; formal source/copy/art locks remain untouched.','preserve_baseline':'Original provisional fields stay as the unaccepted production baseline; do not mistake them for the current approval draft.','founder_approved':False,'render_authorized':False,'release_approved':False}
    for c in cards['cards']:
        c['finalization_candidate']=copy.deepcopy(finals[c['id']]);c['finalization_candidate']['source_acceptance']=False
    canonical_before=digest(before['resolved_character_appearances'])
    approval={'schema':'schemin26.week9.final_approval_folios.v1','date':DATE,'base_commit':BASE,'state':'FINAL_RESULTS_RECONCILED_CONTENT_APPROVAL_PENDING_PNG_HOLD','source':revalidation,'matchups':matchups,'standings':standings,'folios':folios,'approval':{'founder_approved':False,'independent_source_acceptance':False,'render_authorized':False,'release_approved':False,'requires':['Source acceptance under existing#268','Founder content/creative approval','Correct reference-bound proof and actual final-page fit before batching'],'page_specific':['P25 scoring-form methodology for review','P37 fantasy-reserve report is not verified official injury news','Map presentation/labels and all final image quality remain unrendered']},'verification':{'fresh_starter_values_matched':len(rows),'twelve_starter_sums_match':True,'standings_records_reconciled':12,'six_decided_results':6,'reading_order_unchanged':issue['reading_order']==before['reading_order'],'character_authority_unchanged':digest(issue['resolved_character_appearances'])==canonical_before,'new_scene_images':0,'previous_outcome_branches_preserved':True,'no_hidden_source_approval':True,'registered_folio_count':35}}
    assert all(not p['render_authorized'] and p['actual_winner_team_id'] is None for p in issue['pages'])
    assert all(not q.get('render_authorized',False) for q in issue['production_queue'])
    for c in issue['resolved_character_appearances'].values():
        assert sha(ROOT/c['appearance_authority_path'])==c['appearance_authority_sha256']
    dump(W/REG,issue);dump(W/CARDS,cards);dump(W/(NAME+'.json'),approval)
    # Separate audience order from generation order; never sort by stable ID.
    orderfile=W/'WEEK_9_READING_AND_PRODUCTION_ORDER_2026-11-09.json'
    order=load(orderfile);order['source_register_sha256']=sha(W/REG);order['approval_folios']=NAME+'.json';order['approval_copy_selector']='pages[page_id].approval_folio';order['png_state']='HOLD_UNTIL_APPROVAL';dump(orderfile,order)
    ctxfile=W/'THREAD_CONTINUITY.json';ctx=load(ctxfile);ctx['latest_finalization_review']=revalidation;ctx['latest_finalization_review']['selected_winners']={m['matchup_id']:m['winner_team_id'] for m in matchups};ctx['resume']['next_action']='Review the35final-result approval folios and resolve genuine source/creative gaps; no PNG generation until approval. Use approval_folio.copy, not archived pre-MNF copy. Do not restart characters/layout or consult source date to invent acceptance.';dump(ctxfile,ctx)
    note='\n## November10 — final-results folios prepared for approval\n\nFresh Flaim confirms all six results. The current35-page review is ['+NAME+']('+NAME+'.md) with [HTML reading proof]('+NAME+'.html) and [structured folios]('+NAME+'.json). Each active register page now contains `approval_folio`; selected finales and supporting reporting use provider-final data. Earlier provisional `editorial_copy` remains the unaccepted baseline, not the current review. No source/Founder/art/release approval or PNG generation is claimed. The actual Mac is offline; this bounded compile ran in GitHub Actions without a local Director/Steward ACK.\n'
    for fn in ['THREAD_CONTINUITY.md','_INDEX.md']:
        p=W/fn;t=p.read_text()
        if '## November10 — final-results folios prepared for approval' not in t:
            if fn=='_INDEX.md':
                first,rest=t.split('\n',1);t=first+'\n'+note+'\n## Earlier checkpoints — historical unless superseded above\n'+rest
            else:t+=note
        p.write_text(t)
    md=['# Week9 — Final-results folios for approval','', '**35 retained pages. Six provider-decided outcomes. No PNGs generated or authorized.**','', 'The following is the current editorial approval edition. It supersedes pre-MNF wording for REVIEW, not an independent source certificate or a final release. Character references, layouts, geography and reading order remain the existing package.','', '## Confirmed results','', '| Matchup | Result | Margin |','|---|---|---:|']
    for m in matchups:md.append(f"| {m['home']} vs {m['away']} | {m['home_score']}–{m['away_score']}; {m['winner']} wins | {m['margin']} |")
    md+=['','## Approval boundaries','','Source/Founder approval and all actual image-quality checks remain open. P25 is an explicitly proposed editorial scoring-form index. P37 reports observed fantasy IR slots only; official injury diagnoses/return dates are not claimed. Current seeds are not clinches; projected ranks are not percentages. No extra pages or reopened character approvals.','']
    sections=[]
    for f in folios:
        c=f['copy'];md += [f"## {f['reading_position']:02d} · {f['page_id']} — {c['headline']}",'',c['deck'],'',c['body'],'']
        extra=''
        if 'pov' in c:
            for side,text in c['pov'].items():md += [f'**{side.title()} POV:** {text}',''];extra+='<p><b>'+side.title()+' POV:</b> '+html.escape(text)+'</p>'
        if f.get('score_panel'):md+=['**Score panel:** '+json.dumps(f['score_panel'],ensure_ascii=False),'']
        if f.get('sports_note'):md+=['**Football basis:** '+f['sports_note'],''];extra+='<aside><b>Football basis:</b> '+html.escape(f['sports_note'])+'</aside>'
        for r in f['report_cards']:
            md += ['**'+r['label']+' — '+r['heading']+'**',r['text'],''];extra+='<section class="report"><h3>'+html.escape(r['label']+' — '+r['heading'])+'</h3><p>'+html.escape(r['text'])+'</p></section>'
        if f['data_rows']:
            keys=list(f['data_rows'][0]);md += ['| '+' | '.join(keys)+' |','|'+'|'.join(['---']*len(keys))+'|']
            for row in f['data_rows']:md.append('| '+' | '.join('Not reported' if row.get(k) is None else str(row.get(k)) for k in keys)+' |')
            md.append('');extra+=table_html(f['data_rows'])
        if f.get('final_visual_direction'):md += ['**Selected visual consequence:** '+f['final_visual_direction'],'']
        md += ['**Approval:** pending; PNG hold. **Final combined page fit:** pending actual artwork and populated data.','']
        sections.append('<article id="'+f['page_id']+'"><div class="kicker">'+str(f['reading_position']).zfill(2)+' / 35 · '+f['page_id']+'</div><h2>'+html.escape(c['headline'])+'</h2><p class="deck">'+html.escape(c['deck'])+'</p><p>'+html.escape(c['body'])+'</p>'+extra+'<details><summary>Production and approval notes</summary><p>'+html.escape(f.get('final_visual_direction','Retain existing scene and current character references.'))+'</p><p>'+html.escape(' '.join(f['approval_notes']))+'</p><p>No PNG generation; final source/creative/image acceptance remains pending.</p></details></article>')
    (W/(NAME+'.md')).write_text('\n'.join(md).rstrip()+'\n')
    css='body{margin:0;background:#10191b;color:#f4eddf;font:18px/1.6 Georgia,serif}header,main{max-width:1050px;margin:auto;padding:24px}header{border-bottom:1px solid #c2a565}h1,h2,h3{line-height:1.15}h1{font-size:38px}article{padding:35px 0;border-bottom:1px solid #69604d}.kicker,.deck,aside,details,table,nav{font-family:system-ui,sans-serif}.kicker{color:#dec18a;font-size:14px}.deck{color:#d0c2a8;font-size:17px}aside,.report{padding:16px;border:1px solid #635b49;margin:18px 0}.table-wrap{overflow-x:auto}table{border-collapse:collapse;font-size:14px;width:100%;min-width:580px}td,th{padding:9px;border-bottom:1px solid #53605a;text-align:left}th{color:#dec18a}details{font-size:14px;color:#d0d6d2;margin-top:20px}summary{cursor:pointer}nav a{color:#e4c987;display:inline-block;padding:8px;margin:3px}p{overflow-wrap:anywhere}@media(max-width:500px){header,main{padding:16px}body{font-size:17px}h1{font-size:30px}}'
    nav=''.join('<a href="#'+f['page_id']+'">'+str(f['reading_position'])+'</a>' for f in folios)
    doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week9 final-result approval folios</title><style>'+css+'</style></head><body><header><h1>Week9 — Final-results approval edition</h1><p>35 retained folios · six decided outcomes · PNG production remains on hold.</p><p>This is a flowing content review, not a1080×1920 raster proof. Tables may scroll; final page density and image acceptance still require review.</p><nav>'+nav+'</nav></header><main>'+''.join(sections)+'</main></body></html>'
    (W/(NAME+'.html')).write_text(doc)
    readme='''# November10 finalization execution

Fresh authenticated Flaim reads confirmed all6Week9 winners, all120starter ID/score values,12postweek records/seeds,6Week10pairings and42returned Week9 transaction rows. Current data matches the morning packet already merged on main5767fd46. The compiler reuses that full source, preserves its original status/timestamps, and saves a new selected-field revalidation receipt. This is not native HTTP wire or an independent Steward signature.

Each of the existing35included pages now has an approval_folio containing the current review copy, selected result-dependent direction, exact current references/layout and explicit approval holds. The6finales select the exact previously written paragraph; opposite branches remain backstage. Supporting scoreboard, Realm, Power Watch, forecast, player desk, transactions and Week10review are populated. The source-level40records and original provisional fields are preserved as the unaccepted publication baseline, not the latest review.

The current approval artifact is WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.md/.html/.json. No PNG or new illustration was requested/generated. Source acceptance under268, Founder approval, correct provider-reference binding, actual final-data/image fit, map composition and release remain open. Injury coverage is limited to observed fantasy IR slots; no NFL diagnosis or return timetable is invented. The editorial scoring-form method is explicitly submitted for approval, not presented as ESPN rankings. FFHub was not run and no percentages were invented.

Execution used a bounded GitHub-hosted compile because the authorized Mac was offline. No local ConsultEngine consultation, background worker or independent approval is claimed. The temporary branch-only workflow removes itself after successful execution. The existing55tests remain valid; six new tests failed before build and must pass after. The normal Memo CI gains that finalization test; all authorization gates remain closed.
'''
    (E/'README.md').write_text(readme)
    ci=ROOT/'.github/workflows/weekly-memo-authority-ci.yml';text=ci.read_text();step="      - name: Verify Week9 provider-final approval folios without enabling PNGs\n        run: python -m unittest discover -s memo-os/tests -p 'test_week9_final_approval_folios.py' -v\n"
    anchor='      - name: Validate publication manifest'
    if 'test_week9_final_approval_folios.py' not in text:
        assert anchor in text;text=text.replace(anchor,step+anchor,1);ci.write_text(text)
    dump(E/'VERIFICATION.json',approval['verification']|{'red_test_workflow_run':42846678818,'readiness':'CONTENT_REVIEW_CANDIDATE_NOT_SOURCE_OR_ART_ACCEPTANCE','source_checks':proposal['status'],'official_results_decided':True,'source_release_approval':False})
    print(json.dumps({'folios':len(folios),'finales':6,'fresh_starter_values':len(rows),'reserve_slots':len(reserve),'source_reconciliation':proposal['status'],'source_acceptance':False,'render_authorized':False,'new_images':0},indent=2))

if __name__=='__main__':
    main()
