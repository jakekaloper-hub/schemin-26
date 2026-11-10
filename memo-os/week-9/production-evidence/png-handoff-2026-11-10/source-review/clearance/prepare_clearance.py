"""Prepare a source-preserving content review. No network, approvals, or image generation."""
from __future__ import annotations
import copy, hashlib, html, json, re
from pathlib import Path

BASE='ca4212dea0a331138969fca2db4d02f03694006a'
NAMES={
'CHAR-JAKE-KALOPER':'ObiWan Jacoby','CHAR-ZACH-WILSON':'Dr. Duckhook',
'CHAR-BOBBY-MITCHELL':'Mud Dogs','CHAR-MANNING-WELTY':'El Niño',
'CHAR-KEVIN-ZEEK':'Red Leopards','CHAR-BEN-WHIPPLE':'Seven Deadly Chins',
'CHAR-BRANDON-PRYOR':'The Chili Cheesers','CHAR-AUSTIN-BYARS':"His Majesty's Blood",
'CHAR-WILSON-LOOK':'D0nkey K0ng','CHAR-DAVID-BABB':'The LLC',
'CHAR-JORDAN-HOLLINGSHEAD':'Slob on my Dobb','CHAR-PHILLIP-PITTS':'Three Dreaded Snake'}
ALIASES={'Duckhook':'Dr. Duckhook','ObiWan':'ObiWan Jacoby','Slob':'Slob on my Dobb',
'Red':'Red Leopards','Chins':'Seven Deadly Chins','Chili':'The Chili Cheesers',
'DK':'D0nkey K0ng','HMB':"His Majesty's Blood",'TDS':'Three Dreaded Snake','LLC':'The LLC'}
PROTECTED=list(NAMES.values())+['The Red Card','Red Leopard Ruins','Red Leopard','Chili Stable','Chili Outlaw','Arsenal Red']
PLAYER_ALIASES={'Lamb':'CeeDee Lamb','Irving':'Bucky Irving','McCaffrey':'Christian McCaffrey','Allen':'Josh Allen','Reichard':'Will Reichard','Hockenson':'T.J. Hockenson','Goff':'Jared Goff','Cook':'James Cook III','Higgins':'Tee Higgins','McConkey':'Ladd McConkey','Addison':'Jordan Addison','Bass':'Tyler Bass','Walker':'Kenneth Walker III','Nacua':'Puka Nacua','London':'Drake London','Judkins':'Quinshon Judkins','Lawrence':'Trevor Lawrence','DeVonta':'DeVonta Smith','Robinson':'Bijan Robinson','Prescott':'Dak Prescott','Burrow':'Joe Burrow','Watson':'Christian Watson','Young':'Bryce Young','Bowers':'Brock Bowers','Jefferson':'Justin Jefferson','Kincaid':'Dalton Kincaid','Chase':"Ja'Marr Chase",'Shrader':'Spencer Shrader'}

def _protect(s,phrases):
    saved=[]
    for phrase in sorted(set(phrases),key=len,reverse=True):
        pat=re.compile(r'(?<![\w])'+re.escape(phrase)+r'(?![\w])')
        def stash(m):
            token=f'\x01{len(saved)}\x02';saved.append(m.group());return token
        s=pat.sub(stash,s)
    return s,saved

def _restore(s,saved):
    for i,v in enumerate(saved):s=s.replace(f'\x01{i}\x02',v)
    return s

def expand_names(s):
    # Stable identifiers, paths and digests are not prose and must not be rewritten.
    if re.match(r'^(?:CHAR-|LOC-|REG-|W09-|https?://)',s) or re.search(r'\.(?:json|png|jpeg|jpg|svg|html|md|py)(?:#.*)?$',s):return s
    for name in NAMES.values():
        s=re.sub(r'(?<!\w)'+re.escape(name)+r'(?!\w)',lambda _, n=name:n,s,flags=re.IGNORECASE)
    s=re.sub(r'\bthe LLC\b','The LLC',s)
    s=re.sub(r'\b(?:the |The )?Belt Keeper\b',"His Majesty's Blood",s)
    s=re.sub(r'\bthe Outlaw\b','The Chili Cheesers',s)
    s,saved=_protect(s,PROTECTED)
    s=re.sub(r'\bChili Cheesers\b','The Chili Cheesers',s)
    # Protect the newly expanded name before replacing other single-word aliases.
    s=s.replace('The Chili Cheesers','\x03')
    for short,full in (ALIASES | {k.upper():v for k,v in ALIASES.items()}).items():s=re.sub(r'\b'+re.escape(short)+r'\b',lambda _:full,s)
    s=s.replace('\x03','The Chili Cheesers')
    s=_restore(s,saved)
    s=re.sub(r"(Red Leopards|The Chili Cheesers)(['’])s\b",r'\1\2',s)
    return s

def expand_players(s):
    s,saved=_protect(s,list(PLAYER_ALIASES.values())+['Kenneth Walker III','James Cook III','Tyler Warren','George Kittle','Christian Watson'])
    for short,full in PLAYER_ALIASES.items():s=re.sub(r'\b'+re.escape(short)+r'\b',lambda _:full,s)
    return _restore(s,saved)

def strings(value):
    if isinstance(value,str):yield value
    elif isinstance(value,list):
        for x in value:yield from strings(x)
    elif isinstance(value,dict):
        for x in value.values():yield from strings(x)

def walk(value,player=False):
    if isinstance(value,str):return expand_players(expand_names(value)) if player else expand_names(value)
    if isinstance(value,list):return [walk(x,player) for x in value]
    if isinstance(value,dict):return {k:walk(v,player) for k,v in value.items()}
    return value

def find_aliases(value):
    found=[]
    for s in strings(value):
        if re.match(r'^(?:CHAR-|LOC-|REG-|W09-|https?://)',s) or re.search(r'\.(?:json|png|jpeg|jpg|svg|html|md|py)$',s):continue
        t,_=_protect(s,PROTECTED)
        found += re.findall(r'\b(?:Duckhook|ObiWan|Slob|Red|Chins|Chili|DK|HMB|TDS|LLC)\b',t)
    return found

# These edits compress repeated wording without changing the selected event or outcome.
BODY_EDITS={
'W09-P02':"The Commonwealth welcomes a new arrival and a crowded playoff race. Dr. Duckhook stands alone at 6–3; seven teams follow at 5–4. Slob on my Dobb overturned a Monday deficit, Red Leopards survived by 6.40, and The Chili Cheesers sent His Majesty's Blood home wearing the cookout. Five regular-season weeks remain. Every result now reaches beyond its two competitors.",
'W09-P07':"ObiWan Jacoby's recovery found sand again. The approach ran wide; the putt stopped short. Dr. Duckhook answered with a controlled finish, the ball disappearing into the cup. ObiWan Jacoby watched the green while the charity banner lifted behind him. The magnificent morning made the loss worse.",
'W09-P10':"The rear wheel dug instead of climbing. Each burst deepened the rut beneath Mud Dogs and the racing rig. Water reached the low frame. Beyond the channel, the finish banner remained absurdly close. El Niño held the far bank. The storm had not needed to chase its opponent. It had taken away the road.",
'W09-P13':"Red Leopards sprang clear. Seven Deadly Chins followed into the stone bottleneck, where the truck's width became a liability. The wheels churned without room to turn. Beside the wrecked goal, Red Leopards watched the driver's expression change. The pitch needed repair. For now, its owner preferred to inspect the trespasser who could not leave.",
'W09-P15':"The Chili Cheesers braced the cart and released its catch. The cooled contents rolled over His Majesty's Blood, coating black armor, gold ornament and ragged cloak. The town froze. The Chili Cheesers raised the ladle in a professional salute. The hood stayed dark; the eyes stayed red. His Majesty's Blood kept the belt, but not clean dignity.",
'W09-P18':"The LLC caught the blade and drove into the parry. D0nkey K0ng turned around that pressure. Four hooves changed the line; the elegant guard faced empty sand. D0nkey K0ng forced The LLC backward onto one armored knee, then stopped the sword short. The crowd rose. The armor remained expensive. The lesson had cost more.",
'W09-P21':"Slob on my Dobb slid clear as paint struck the bunker behind him. From behind his shoulder, the marker found Three Dreaded Snake downrange. Bright splashes crossed the three protected masks and shared torso. All three heads recoiled. Slob on my Dobb stopped with the barrel level. He had reached the dangerous ground first.",
'W09-P23':"Drake London contributed 11.80 for Slob on my Dobb; Quinshon Judkins added 7.00 for The LLC after their completed exchange.",
'W09-P39':"Five games per team remain. Three division winners qualify; four further places are shared. Weeks 12–14 return to division play.",
'W09-P25':"A scoring-form ranking, not an official seed: 70% season points per game plus 30% Week 9 points. Roster health and playoff probability are not included.",
'W09-P37':"Observed Week 9 fantasy reserve slots. These entries do not confirm National Football League injured-reserve status, a new injury, or a return date.",
'W09-P38':"Seven teams share a 5–4 record. The Chili Cheesers currently sit outside the seven-team field; division outcomes affect everyone’s route.",
'W09-P40':"Current seed and projected rank are different ESPN fields. This table reports both; the source did not supply playoff percentages. No position is a clinch.",
'W09-P26':"The Chili Cheesers and D0nkey K0ng meet at 5–4: current seeds 8 and 3. The proposed spotlight remains subject to approval.",
'W09-P28':"The results are settled; the league is not. Seven teams share 5–4. Dr. Duckhook has a lead, not a guarantee. ObiWan Jacoby and Three Dreaded Snake need ground back; The LLC and Mud Dogs cannot waste the road ahead. Five weeks remain. The next victory will matter to more than the two teams playing for it."
}
FINAL_NOTES={
'W09-P07':'Matthew Golden: 33.40. Drake Maye: 24.36. Kenneth Walker III and Puka Nacua combined for 75.30 in defeat.',
'W09-P10':'James Cook III and Tee Higgins combined for 41.00. No Mud Dogs starter scored more than 10.50.',
'W09-P13':"Ja'Marr Chase: 34.50. Justin Jefferson gained only 3.00 on Dalton Kincaid, short of the required 9.40.",
'W09-P15':'Christian Watson, Bryce Young and Brock Bowers combined for 80.94. His Majesty\'s Blood lost by 17.76.',
'W09-P18':'Bijan Robinson and Dak Prescott combined for 56.30. Joe Burrow scored 37.84 for The LLC.',
'W09-P21':"Josh Allen and Will Reichard outscored T.J. Hockenson by 17.16 on Monday, overturning an 11.06 deficit."
}

def prepare(original):
    a=copy.deepcopy(original)
    if a.get('clearance',{}).get('version')=='FULL_NAME_CONTENT_PASS_2026_11_10':return a
    a['source']['review_artifact']='Week_9_Approval_Review_Full_Names.html'
    a['clearance']={'version':'FULL_NAME_CONTENT_PASS_2026_11_10','base_commit':BASE,
      'source_blob':'31b5ece33f3d440d093cf42a4c8960eebd62fe00','repository_synced':False,
      'review_execution':'ASSISTANT_SOURCE_REVIEW_NOT_LIVE_BULLPEN_RUNTIME',
      'scope':'Editorial correction under existing delegated scope; all approvals remain pending.',
      'decisions':["Use full established names in printed copy, cast bindings and current scene directions.","Retain the transparent 70/30 formula as Scoring Form, not a comprehensive power rating.","Limit Reserve Watch to observed fantasy slots; no unsupported official injury claims.","Print each overture viewpoint once; production constraints and statistical supporting detail remain separately accessible."]}
    for m in a['matchups']:
        for k in ['sports_cause','final_visual_direction']:m[k]=walk(m[k], k=='sports_cause')
    for f in a['folios']:
        f['copy']=walk(f['copy'])
        original_scene=copy.deepcopy(f['scene'])
        f['scene']=walk(f['scene'])
        if f['is_finale']:
            chosen=f['selected_branch'].upper()
            f['archived_unselected_beats']=[b for b in original_scene.get('beats',[]) if b.get('branch') not in ['COMMON',chosen]]
            f['scene']['beats']=[b for b in f['scene'].get('beats',[]) if b.get('branch') in ['COMMON',chosen]]
            for b in f['scene']['beats']:
                if 'pose_and_physical_action' in b:b['pose_and_physical_action']=re.sub(r'^IF .*? WINS:\s*','',b['pose_and_physical_action'])
            f['scene']['selected_branch']=f['selected_branch']
            f['scene']['state']='OUTCOME_SELECTED_FOR_CONTENT_REVIEW_NOT_RENDER_APPROVAL'
        if f['scene']:
            f['scene']['text_hidden_review_questions']=[q for q in f['scene'].get('text_hidden_review_questions',[]) if 'hypothetical' not in q]
            for b in f['scene'].get('beats',[]):
                if 'what_changes' in b:b['what_changes']=b['what_changes'].replace('Success is unassigned in the neutral study.','The confirmed outcome is resolved in the selected finale.')
        for k in ['final_visual_direction','sports_note','cover_teasers']:
            if k in f:f[k]=walk(f[k],k=='sports_note')
        f['report_cards']=walk(f['report_cards'],True)
        f['cast_binding']=[{'character_id':cid,'full_name':NAMES[cid]} for cid in f['cast']]
        f['copy']['deck']=f['copy']['deck'].replace(' vs ',' versus ').replace('GOTW','Game of the Week')
        if f['page_id'] in BODY_EDITS:f['copy']['body']=BODY_EDITS[f['page_id']]
        f['copy']['body_word_count']=len(f['copy']['body'].split())
        f['layout']['whole_page_fit_state']='REQUIRES_REMEASUREMENT_AFTER_FULL_NAME_AND_FINAL_VALUE_INSERTION'
        f['layout']['fit_limits']=['Art regions contain placeholders only.','This review uses final reported values; no finished illustration has been inspected.','Reference attachment, map-label composition and independent source acceptance remain separate.']
        pid=f['page_id']
        if pid=='W09-P25':
            f['working_title']=f['copy']['headline']='The Twelve — Scoring Form'
            f['copy']['deck']='Editorial index: season scoring with extra weight on Week 9'
        if pid=='W09-P37':
            f['working_title']=f['copy']['headline']='Reserve Watch'
            f['copy']['deck']='Fantasy roster slots, not confirmed injury news'
        if pid=='W09-P40':f['copy']['deck']='Current ESPN seed and ESPN projected rank'
        if pid=='W09-P26':f['copy']['deck']='Week 10 fixtures and the proposed Game of the Week'
        pub={'headline':f['copy']['headline'],'deck':f['copy']['deck'],'body':f['copy']['body'],'pov':[], 'rows':[], 'cards':copy.deepcopy(f['report_cards']),'score_panel':copy.deepcopy(f.get('score_panel')),'sports_note':FINAL_NOTES.get(pid,''),'teasers':f.get('cover_teasers',[])}
        if 'pov' in f['copy']:
            pub['body']=''
            pub['pov']=[{'side':'home','name':NAMES[f['cast'][0]],'text':f['copy']['pov']['home']},{'side':'away','name':NAMES[f['cast'][1]],'text':f['copy']['pov']['away']}]
            match=next(m for m in a['matchups'] if m['matchup_id']==f.get('matchup_id')) if f.get('matchup_id') else None
            # The existing stakes remain an entering-week observation, not a final record.
            pub['stakes']=f['copy'].get('stakes','').replace('Two perspectives; the outcome belongs to the finale.','')
        if f['data_rows']:pub['rows']=copy.deepcopy(f['data_rows'])
        if pid=='W09-P37':
            # Regroup the original source rows, preserving all17 names and the11fantasy teams.
            groups={}
            for row in f['data_rows']:
                name=row.get('fantasy_team',row.get('team',row.get('team_name')))
                player=row.get('player',row.get('player_name',row.get('name')))
                if name is None or player is None:raise ValueError('Unknown reserve row shape: '+str(row))
                groups.setdefault(name,[]).append(player)
            pub['rows']=[{'team':name,'players':players} for name,players in groups.items()]
            pub['cards']=[]
        f['publication_payload']=pub
        f['clearance_state']='REVIEW_COPY_UPDATED__NOT_APPROVED_FOR_RENDER'
    # Old internal fields are retained in the source artifact, never silently overwritten in GitHub.
    return a

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    src=root.parent/'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.json'
    out=root/'Week_9_Approval_Review_Full_Names.json'
    out.write_text(json.dumps(prepare(json.loads(src.read_text())),ensure_ascii=False,indent=2)+'\n')
    print(out)
