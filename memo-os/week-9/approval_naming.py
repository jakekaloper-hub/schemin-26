"""Full-name presentation only. Never rewrite canon, IDs or captured source facts."""
from __future__ import annotations
import copy, hashlib, json, re

NAMES={
 'CHAR-JAKE-KALOPER':'ObiWan Jacoby',
 'CHAR-WILSON-LOOK':'D0nkey K0ng',
 'CHAR-PHILLIP-PITTS':'Three Dreaded Snake',
 'CHAR-AUSTIN-BYARS':"His Majesty's Blood",
 'CHAR-BRANDON-PRYOR':'The Chili Cheesers',
 'CHAR-JORDAN-HOLLINGSHEAD':'Slob on my Dobb',
 'CHAR-ZACH-WILSON':'Dr. Duckhook',
 'CHAR-KEVIN-ZEEK':'Red Leopards',
 'CHAR-BOBBY-MITCHELL':'Mud Dogs',
 'CHAR-BEN-WHIPPLE':'Seven Deadly Chins',
 'CHAR-DAVID-BABB':'The LLC',
 'CHAR-MANNING-WELTY':'El Niño',
}
# Source-established place/descriptive names are not abbreviations of a competitor.
PROTECTED=['The Red Card','Red sauce','Red-and-gold','Chili Stable','Red Leopard Ruins','Red Leopards Ruins','Chili Outlaw','Dark Horse','The Dark Horse','Pittsy’s Book',"Pittsy's Book"]
ALIASES={'Duckhook':'Dr. Duckhook','DrD':'Dr. Duckhook','ObiWan':'ObiWan Jacoby','OBJ':'ObiWan Jacoby','Slob':'Slob on my Dobb','TDS':'Three Dreaded Snake','HMB':"His Majesty's Blood",'DK':'D0nkey K0ng','Chins':'Seven Deadly Chins','Chili':'The Chili Cheesers','Red':'Red Leopards','LLC':'The LLC'}
# These unambiguous shortened player names occur in the approved source-based paragraphs.
PLAYERS={'Addison':'Jordan Addison','Bass':'Tyler Bass','Walker':'Kenneth Walker III','Nacua':'Puka Nacua','Jefferson':'Justin Jefferson','Kincaid':'Dalton Kincaid','Cook':'James Cook III','Higgins':'Tee Higgins','Goff':'Jared Goff','Lamb':'CeeDee Lamb','Irving':'Bucky Irving','McCaffrey':'Christian McCaffrey','Allen':'Josh Allen','Reichard':'Will Reichard','Hockenson':'T.J. Hockenson','McConkey':'Ladd McConkey','London':'Drake London','Judkins':'Quinshon Judkins','Lawrence':'Trevor Lawrence','DeVonta':'DeVonta Smith'}

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def full_names(text: str) -> str:
    """Expand established shorthand once, protecting complete identities/locations."""
    if not isinstance(text,str):return text
    if re.match(r'^(?:CHAR-|LOC-|REG-|DIV-|W09-|canon/|world/|memo-os/|production-evidence/)',text):return text
    saved={}
    def save(value):
        key='ZZNAMETOKEN'+chr(65+len(saved)//26)+chr(65+len(saved)%26)+'ZZ'
        saved[key]=value;return key
    candidates={n:n for n in [*NAMES.values(),*PLAYERS.values(),*PROTECTED]}
    candidates.update({'Chili Cheesers':'The Chili Cheesers','the LLC':'The LLC','THE LLC':'The LLC','The LLC.':'The LLC.',"His Majesty’s Blood":"His Majesty's Blood"})
    for term,replacement in sorted(candidates.items(),key=lambda x:len(x[0]),reverse=True):
        text=re.sub(r'(?<!\w)'+re.escape(term)+r'(?!\w)',lambda _:save(replacement),text)
    for alias,name in ALIASES.items():
        # Do not turn a capitalized material description into a character.
        pattern=r'\b'+re.escape(alias)+r'\b'
        if alias=='Red':pattern+=r'(?![- ]and[- ]gold|\s+(?:cap|cloth|fabric|light|paint))'
        text=re.sub(pattern,lambda _:save(name),text)
    for alias,name in PLAYERS.items():text=re.sub(r'\b'+re.escape(alias)+r'\b',lambda _:save(name),text)
    text=text.replace('GOTW','Game of the Week').replace('pre-MNF','pre-Monday-night').replace('MNF','Monday Night Football')
    for key,value in saved.items():text=text.replace(key,value)
    text=text.replace('the The LLC','The LLC').replace('the The Chili Cheesers','The Chili Cheesers')
    return text

def transform(value):
    if isinstance(value,str):return full_names(value)
    if isinstance(value,list):return [transform(x) for x in value]
    if isinstance(value,dict):return {k:transform(v) for k,v in value.items()}
    return value

def unresolved_aliases(value):
    findings=[]
    if isinstance(value,str):
        transformed=full_names(value)
        if transformed!=value:findings.append(value)
    elif isinstance(value,list):
        for x in value:findings.extend(unresolved_aliases(x))
    elif isinstance(value,dict):
        for x in value.values():findings.extend(unresolved_aliases(x))
    return findings

def folio_digest(folio):
    x=copy.deepcopy(folio)
    x.pop('content_digest',None)
    return digest(x)

def apply_clearance(folios,matchups,issue,root):
    """Derive reviewed wording without touching historical paragraphs or authorities."""
    for m in matchups:
        for key in ['home','away','winner','sports_cause','final_visual_direction']:
            if key in m:m[key]=full_names(m[key])
    result={}
    for f in folios:
        for key in ['copy','scene','report_cards','data_rows','final_visual_direction','sports_note','performance_edit','cover_teasers','approval_notes','result_context','working_title']:
            if key in f:f[key]=transform(f[key])
        f['character_identity']=[]
        for cid in f['cast']:
            source=issue['resolved_character_appearances'][cid]
            path=root/source['appearance_authority_path']
            if hashlib.sha256(path.read_bytes()).hexdigest()!=source['appearance_authority_sha256']:raise ValueError('Changed character authority: '+cid)
            f['character_identity'].append({'character_id':cid,'full_name':NAMES[cid],'appearance_source':source['appearance_authority_path'],'appearance_sha256':source['appearance_authority_sha256'],'identity_reapproval_required':False})
        f['publication_text_policy']={'body':'POV_HALVES_ONLY_NO_DUPLICATE_JOINED_BODY' if f['page_role']=='two_character_pov_overture' else 'EXACT_COPY_BODY','sports_note':'PRINT_ON_FINALE_ONLY' if f.get('is_finale') else 'PRODUCTION_CONTEXT_NOT_EXTRA_PRINTED_PARAGRAPH','numeric_data':'DETERMINISTIC_COMPOSITION_FROM_REVIEWED_FIELDS','no_character_abbreviations':True}
        if f['is_finale']:
            allowed=['COMMON',f['selected_branch'].upper()]
            f['archived_opposite_beat_ids']=[b['beat_id'] for b in f['scene'].get('beats',[]) if b.get('branch') not in allowed]
            f['scene']['beats']=[b for b in f['scene'].get('beats',[]) if b.get('branch') in allowed]
            f['scene']['state']='SELECTED_PROVIDER_OUTCOME_FOR_CONTENT_REVIEW_NOT_IMAGE_APPROVAL'
            page=next(p for p in issue['pages'] if p['page_id']==f['page_id'])
            original=page['editorial_copy']['conditional_narratives'][f['selected_branch']]
            f['selected_ending_source_sha256']=hashlib.sha256(original.encode()).hexdigest()
            f['selected_ending_transform']='Full established names only; source paragraph preserved in original register.'
            if f['copy']['body']!=full_names(original):raise ValueError('Finale changed beyond name expansion')
        f['copy']['body_word_count']=len(f['copy']['body'].split())
        result[f['page_id']]=f
    ranking=result['W09-P25']
    ranking['working_title']=ranking['copy']['headline']='The Twelve — Scoring-Form Index'
    ranking['copy']['deck']='Season scoring and Week 9 form. Not playoff odds.'
    ranking['copy']['body']='Slob on my Dobb leads this scoring-form index; Dr. Duckhook holds the official top seed. The index weights season points per game at 70% and Week 9 scoring at 30%. It is not a roster-health assessment or playoff forecast.'
    reserve=result['W09-P37']
    reserve['working_title']=reserve['copy']['headline']='The Reserve List'
    reserve['copy']['deck']='Observed Week 9 fantasy reserve slots. Not an injury-news bulletin.'
    reserve['copy']['body']='Seventeen fantasy reserve slots were occupied in the captured Week 9 rosters. These players were outside the scoring lineup. Reserve placement does not establish a new injury, a National Football League designation, or a return date.'
    reserve['report_cards']=[]
    reserve['presentation_scope']='Full observed roster-slot list; official injury-news enrichment remains unverified and is not silently claimed complete.'
    configure_populated_layouts(folios,issue)
    for f in folios:f['copy']['body_word_count']=len(f['copy']['body'].split());f['content_digest']=folio_digest(f)
    return result


def configure_populated_layouts(folios,issue):
    """Reserve full-size type for actual data and selected endings, not dashes."""
    pages={p['page_id']:p for p in issue['pages']}
    captions={'W09-P07':'Matthew Golden: 33.40 points. Winning margin: 22.10.',
              'W09-P10':'James Cook III and Tee Higgins: 41.00 combined points.',
              'W09-P13':'Ja’Marr Chase: 34.50 points. Winning margin: 6.40.',
              'W09-P15':'Christian Watson: 31.10 points. Winning margin: 17.76.',
              'W09-P18':'Bijan Robinson and Dak Prescott: 56.30 combined points.',
              'W09-P21':'Monday scoring swung the margin by 17.16 points.'}
    for f in folios:
        pid=f['page_id'];l=f['layout'];k=l['archetype']
        if k=='split_pov':
            l['zones']['home_art']=[60,325,960,335]
            l['zones']['home_pov']=[60,680,960,280]
            l['zones']['away_art']=[60,1060,960,335]
            l['zones']['away_pov']=[60,1415,960,280]
        elif k=='dense_table':
            l['zones']={'header':[60,50,960,250],'landscape':[60,325,960,150],'table':[60,505,960,1000],'note':[60,1535,960,320]}
        elif k=='report_cards' and pid!='W09-P37':
            l['zones']={'header':[60,50,960,250],'landscape':[60,325,960,100],'report_cards':[60,450,960,1130],'note':[60,1605,960,250]}
        elif k=='realm':
            l['zones']={'header':[60,50,960,250],'division_panels':[60,325,960,1260],'consequence':[60,1610,960,245]}
            f['publication_note']='Three division races feed four shared places. Equal records do not guarantee equal seeds; the current positions are not clinched berths.'
        if pid=='W09-P37':
            l['archetype']='reserve_grid'
            l['zones']={'header':[60,50,960,250],'reserve_groups':[60,350,960,1260],'note':[60,1630,960,225]}
            f['publication_note']='Seventeen fantasy reserve slots were occupied in the Week 9 snapshot. These roster placements do not establish injuries, professional reserve designations, or return dates.'
        if pid=='W09-P39':
            f['publication_note']='Three division winners qualify. Four additional places are shared across the league. Weeks 12–14 are divisional. Current seeds are not clinched berths.'
        if f['is_finale']:
            l['zones']={'header':[60,50,960,250],'art':[60,325,960,640],'body':[60,990,960,865]}
            f['football_caption']=captions[pid]
            f['publication_text_policy']['sports_note']='COMPACT_SOURCE_BOUND_FOOTBALL_CAPTION; full explanation retained for editorial/source review'
        l['populated_copy_state']='MEASUREMENT_PENDING_NO_IMAGE_ACCEPTANCE'
        pages[pid]['layout_spec']=copy.deepcopy(l)
        if pages[pid].get('proof_preparation',{}).get('layout_alias_of')=='layout_spec':
            pages[pid]['proof_preparation']['layout']=copy.deepcopy(l)
