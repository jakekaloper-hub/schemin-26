#!/usr/bin/env python3
"""Week9 offline production preparation; no network, rendering, or approval writes.

result-preview reads an explicitly scoped Flaim response and optional normalized
lineup evidence. It emits PROPOSED fields only and NEVER modifies the register.
page-kit extracts the current single-page brief and already-selected image bytes.
Neither command asserts provider attachment, final source acceptance or release.
"""
from __future__ import annotations
import argparse
import copy
import importlib.util
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
import hashlib
import html
import json
from pathlib import Path
import shutil
import sys

REGISTRY='WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json'
CARDS='WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json'
SCOPE=('1417621',2026,9)
SLOTS=Counter({'QB':1,'RB':2,'WR':2,'TE':1,'FLEX':1,'D/ST':1,'K':1,'WR/TE':1})

def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def fingerprint(value: object) -> str:
    return digest(json.dumps(value,sort_keys=True,ensure_ascii=False,allow_nan=False).encode())

def timestamp(value: str) -> datetime:
    result=datetime.fromisoformat(value.replace('Z','+00:00'))
    if result.tzinfo is None: raise ValueError('A source timestamp requires its timezone')
    return result

def number(value: object) -> Decimal:
    if isinstance(value,bool) or value is None: raise ValueError('Missing or boolean score')
    try: result=Decimal(str(value))
    except InvalidOperation as exc: raise ValueError('Non-numeric score') from exc
    if not result.is_finite(): raise ValueError('Non-finite score')
    return result

def scoped(value: dict) -> bool:
    return (str(value.get('league_id')),value.get('season_year'),value.get('week'))==SCOPE

def reconcile(issue: dict,cards: dict,observation: dict) -> dict:
    """Pure candidate reconciliation. Facts/locks in all arguments remain untouched."""
    result={'kind':'WEEK9_PROPOSED_FIELD_UPDATES_NOT_SOURCE_ACCEPTANCE',
            'status':'INVALID_SOURCE','errors':[],'results':[],'page_updates':[],
            'source_accepted':False,'render_authorized':False,'release_approved':False,
            'writes_authoritative_files':False,'injury_claims_verified':False,
            'playoff_odds_generated':False,'requires_independent_review':True}
    def stop(state: str,message: str) -> dict:
        result['status']=state;result['errors'].append(message)
        # Validation is atomic: a late missing branch cannot leak partial updates.
        result['results']=[];result['page_updates']=[]
        return result
    try:
        if not scoped(observation['request']): return stop('INVALID_SOURCE','Expected explicit league1417621 season2026 week9 request')
        observed=timestamp(observation['recorded_at_utc'])
        if observed<timestamp(issue['active_sports_source']['as_of']): return stop('INVALID_SOURCE','Snapshot predates active sports source')
        response=observation['matchups_response']
        if response.get('success') is not True: return stop('INVALID_SOURCE','Provider request did not succeed')
        data=response['data']
        if (str(data.get('leagueId')),data.get('seasonYear'),data.get('matchupPeriod'))!=SCOPE:
            return stop('INVALID_SOURCE','Payload league/season/matchup period does not match request')
        # currentScoringPeriod can legitimately advance; explicit matchupPeriod wins.
        matches=data['matchups']; expected={(c['home']['teamId'],c['away']['teamId']):c for c in cards['cards']}
        if len(matches)!=6 or len(expected)!=6: return stop('INVALID_SOURCE','Expected exactly six distinct fixtures')
        actual=[(m['home']['teamId'],m['away']['teamId']) for m in matches]
        if len(set(actual))!=6 or set(actual)!=set(expected): return stop('INVALID_SOURCE','Duplicate, swapped or unexpected fixture')
        teams=[tid for pair in actual for tid in pair]
        if len(set(teams))!=12: return stop('INVALID_SOURCE','Each of twelve teams must appear exactly once')
        if any(m.get('matchupPeriodId')!=9 for m in matches): return stop('INVALID_SOURCE','A fixture belongs to another week')
        for m in matches:
            for side in ['home','away']:
                number(m[side]['currentPoints']);number(m[side]['totalPoints'])
            if m.get('winner') not in ['HOME','AWAY','TIE','UNDECIDED']:
                return stop('INVALID_SOURCE','Unknown provider result state')
        result['provider_final_count']=sum(m['winner']!='UNDECIDED' for m in matches)
        result['source']={'recorded_at_utc':observation['recorded_at_utc'],'observation_sha256':fingerprint(observation),
                          'representation':observation.get('representation','Not specified'),
                          'request':observation['request'],'current_scoring_period':data.get('currentScoringPeriod')}
        if any(m['winner']=='UNDECIDED' for m in matches):
            return stop('WAITING_PROVIDER_FINALITY','No final branch proposal: one or more provider winners remain UNDECIDED')
        final=[];score_by_team={}
        for m in matches:
            h=number(m['home']['totalPoints']);a=number(m['away']['totalPoints'])
            if h!=number(m['home']['currentPoints']) or a!=number(m['away']['currentPoints']):
                return stop('INVALID_SOURCE','Provider current/final totals disagree; do not use zero placeholders as final')
            if h==a or m['winner']=='TIE':
                return stop('TIEBREAK_REVIEW_REQUIRED','Equal totals or tie result requires actual tiebreak review; no prewritten tie ending exists')
            if (h>a)!=(m['winner']=='HOME'):return stop('INVALID_SOURCE','Provider winner contradicts the score ordering')
            card=expected[(m['home']['teamId'],m['away']['teamId'])]
            row={'matchup_id':card['id'],'home_team_id':card['home']['teamId'],'away_team_id':card['away']['teamId'],
                 'home_name':card['home']['name'],'away_name':card['away']['name'],'home_score':format(h,'.2f'),
                 'away_score':format(a,'.2f'),'margin':format(abs(h-a),'.2f'),'provider_winner':m['winner'],
                 'winning_team_id':m['home' if h>a else 'away']['teamId'],'branch_proposal':'home_win' if h>a else 'away_win'}
            final.append(row);score_by_team[row['home_team_id']]=h;score_by_team[row['away_team_id']]=a
        lineup=observation.get('lineup_evidence')
        if not lineup:return stop('WAITING_LINEUP_EVIDENCE','Need current explicit Week9 starter evidence; scoreboard finality alone is insufficient')
        if not scoped(lineup) or not lineup.get('source_ref'):
            return stop('LINEUP_RECONCILIATION_REQUIRED','Lineup scope/source reference absent or incorrect')
        if abs((timestamp(lineup['recorded_at_utc'])-observed).total_seconds())>900:
            return stop('LINEUP_RECONCILIATION_REQUIRED','Lineup and score observations exceed the15-minute candidate collection window')
        rows=lineup['rows'];by_team={tid:[] for tid in teams};seen=set()
        for row in rows:
            tid=row['fantasy_team_id'];pid=str(row['player_id'])
            if tid not in by_team or row.get('started') is not True or not pid or pid in seen or row['lineup_slot'] not in SLOTS:
                return stop('LINEUP_RECONCILIATION_REQUIRED','Unexpected team, duplicate player, nonstarter or invalid slot')
            seen.add(pid);number(row['points']);by_team[tid].append(row)
        for tid,team_rows in by_team.items():
            if Counter(r['lineup_slot'] for r in team_rows)!=SLOTS:
                return stop('LINEUP_RECONCILIATION_REQUIRED','Ten configured starter slots must be accounted for; do not fabricate a missing player')
            if abs(sum((number(r['points']) for r in team_rows),Decimal(0))-score_by_team[tid])>Decimal('0.005'):
                return stop('LINEUP_RECONCILIATION_REQUIRED','Starter sum differs from provider total for team '+str(tid))
        result['status']='RECONCILED_CANDIDATE_NOT_ACCEPTED';result['results']=final
        lookup={r['matchup_id']:r for r in final}
        for page in issue['pages']:
            if not page.get('publication_included') or page.get('matchup_id') not in lookup:continue
            r=lookup[page['matchup_id']];branch=r['branch_proposal'];copy=page['editorial_copy']
            ending=copy.get('conditional_narratives',{}).get(branch) if page['page_role']=='matchup_payoff' else None
            if page['page_role']=='matchup_payoff' and not ending:
                return stop('INVALID_SOURCE','Missing preserved finale paragraph for '+page['page_id'])
            result['page_updates'].append({'page_id':page['page_id'],'matchup_id':r['matchup_id'],
                'branch_proposal':branch,'winning_team_id_proposal':r['winning_team_id'],'body_proposal':ending,
                'scene_outcome_proposal':next(c for c in cards['cards'] if c['id']==r['matchup_id'])[branch],
                'score_line_proposal':f"{r['home_name']} {r['home_score']} — {r['away_name']} {r['away_score']}",
                'source_sha256':result['source']['observation_sha256'],'do_not_apply_without_source_and_editorial_acceptance':True,
                'rerender_only_after_reference_scene_and_pixel_checks':True})
        result['scoreboard_rows_proposal']=[{k:r[k] for k in ['matchup_id','home_name','away_name','home_score','away_score','margin','winning_team_id']} for r in final]
        result['starter_evidence_by_team']={str(tid):sorted(rs,key=lambda r:number(r['points']),reverse=True) for tid,rs in by_team.items()}
        result['remaining_editorial_work']={
            'W09-P01':'Reconcile cover teasers with accepted issue; retain family-first cover.',
            'W09-P02':'Rewrite final weekly thesis; do not publish pre-MNF language.',
            'W09-P22':'Use reconciled player scores to write Good/Bad/Ugly; do not equate top score with exclusive causality.',
            'W09-P23':'Refresh completed/canceled transactions; this score capture does not verify them.',
            'W09-P24':'Fetch postweek standings/seeds; never derive official seed from these scores alone.',
            'W09-P25':'Editorial ranking still requires a reasoned order; not a seeded or probabilistic output.',
            'W09-P26':'Recheck explicitWeek10 fixtures and candidate spotlight; do not change Week9 GOTW.',
            'W09-P27':'Retain one-week Book closure; no market reactivation or invented settlement.',
            'W09-P28':'Write verified final consequence and forward close.',
            'W09-P37':'Verify injury sources and current fantasy ownership independently.',
            'W09-P38':'Explain verified division-wide consequences after standings reconciliation.',
            'W09-P39':'Keep verified7berths/3division routes; exact clinch needs separate proof.',
            'W09-P40':'No playoff probability inferred; optional FFHub remains unrun/unaccepted.'}
        result['provenance']={'issue_sha256':fingerprint(issue),'story_cards_sha256':fingerprint(cards),'lineup_sha256':fingerprint(lineup)}
        return result
    except (KeyError,TypeError,ValueError,AttributeError,InvalidOperation) as exc:
        result['results']=[];result['page_updates']=[]
        return stop('INVALID_SOURCE',f'Malformed source: {exc}')

def validate_current_packet(issue: dict, page: dict) -> None:
    """Reject contradictory active consumers before exporting any derivative."""
    proof=page.get('proof_preparation',{});handoff=proof.get('execution_handoff',{})
    if handoff.get('layout_source')!='layout_spec' or handoff.get('exact_copy_source')!='editorial_copy':
        raise ValueError('Superseded layout/copy selector in active proof')
    if proof.get('layout')!=page['layout_spec'] or proof.get('layout_alias_of')!='layout_spec':
        raise ValueError('Proof layout alias diverges from authoritative layout_spec')
    adjacent=page['adjacent_pages'];sequence=proof.get('sequence_readthrough',{})
    if sequence.get('previous_page')!=adjacent['previous'] or sequence.get('next_page')!=adjacent['next']:
        raise ValueError('Proof adjacency contradicts current reading order')
    expected={r['source_id'] for r in issue['convergence_review']['coverage'] if r['disposition']=='ABSORB_AND_RESTAGE' and page['page_id'] in r['destinations']}
    got={r['source_id'] for r in page.get('absorbed_source_beats',[]) if r.get('required_visible_transfer')}
    if expected!=got:raise ValueError('Required source-beat transfer missing from active page')
    for beat in page.get('written_storyboard',{}).get('beats',[]):
        if beat.get('page_id')!=page['page_id']:raise ValueError('Beat has historical rather than active placement')
    order=page['layout_spec'].get('art_sequence')
    if order and [a.get('zone') for a in proof.get('action_blocks',[])]!=order:
        raise ValueError('Physical action order and layout regions disagree')

def export_page_kit(root: Path,issue: dict,page_id: str,out: Path,edition: str='neutral') -> dict:
    """Copy exact selected reference bytes into a one-page neutral study kit."""
    if out.exists():raise FileExistsError(f'Destination already exists: {out}')
    pages=[p for p in issue['pages'] if p['page_id']==page_id and p.get('publication_included')]
    if len(pages)!=1:raise ValueError('Page is missing, duplicated or absorbed; use active reading IDs')
    page=pages[0]
    if edition not in ['neutral','approval-review']:raise ValueError('Unknown page-kit edition')
    naming_spec=importlib.util.spec_from_file_location('kit_names',root/'memo-os/week-9/approval_naming.py')
    naming=importlib.util.module_from_spec(naming_spec);naming_spec.loader.exec_module(naming)
    folio=page.get('approval_folio') if edition=='approval-review' else None
    if edition=='approval-review':
        if not folio or folio.get('content_digest')!=naming.folio_digest(folio):raise ValueError('Stale or unreviewed approval folio digest')
        if folio['cast']!=page['characters_present']:raise ValueError('Approval cast differs from current packet')
    if page_id not in ['W09-P05','W09-P20']:raise ValueError('This bounded exporter supports only the existing neutral P05/P20 proof lane')
    validate_current_packet(issue,page)
    assets=[];contents={};cast=page['characters_present']
    if len(cast)!=2 or set(page['page_character_contract']['allowed_principal_character_ids'])!=set(cast):
        raise ValueError('Neutral proof requires its exact two approved subjects')
    for cid in cast:
        candidates=[a for a in page['reference_assets'] if a['character_id']==cid]
        if len(candidates)!=1:raise ValueError('Missing/duplicate subject reference')
        a=candidates[0];selected=a['selected_visual_reference'];p=(root/selected['path']).resolve()
        if not p.is_relative_to(root.resolve()):raise ValueError('Reference escaped repository')
        data=p.read_bytes()
        if digest(data)!=selected['sha256']:raise ValueError('Selected image digest mismatch: '+cid)
        authority=(root/a['appearance_authority_path']).resolve()
        if not authority.is_relative_to(root.resolve()):raise ValueError('Authority escaped repository')
        auth=authority.read_bytes()
        if digest(auth)!=a['appearance_authority_sha256']:raise ValueError('Appearance authority digest mismatch')
        image_name=cid+p.suffix;auth_name=cid+'-appearance.json'
        assets.append({'character_id':cid,'file':image_name,'sha256':digest(data),'repository_source':selected['path'],
                       'authority_file':auth_name,'authority_sha256':digest(auth),'identity_approval_reopened':False})
        contents[image_name]=data;contents[auth_name]=auth
    if page['layout_spec']['canvas']!=[1080,1920]:raise ValueError('Wrong current canvas')
    c=naming.transform(folio['copy'] if folio else page['editorial_copy']);layout=folio['layout'] if folio else page['layout_spec']
    if layout!=page['layout_spec']:raise ValueError('Approval layout differs from current packet')
    manifest={'kind':'CURRENT_APPROVAL_REVIEW_INPUTS_NOT_RENDER_PERMISSION' if folio else 'ISOLATED_EXISTING_NEUTRAL_PAGE_INPUTS_NOT_AN_IMAGE','page_id':page_id,
              'reading_position':issue['reading_order'].index(page_id)+1,'source_packet_sha256':fingerprint(page),
              'canvas':[1080,1920],'exact_cast':cast,'reference_files':assets,
              'renderer_binding_proven':False,'artwork_generated':False,'render_authorized':False,
              'release_approved':False,'actual_result_selected':False,'contains_final_scores':False,
              'layout_authority':'Current layout_spec, NOT earlier proof_preparation.layout',
              'purpose':'Explicit two-reference inputs for an authorized narrow provider route; no whole-issue context or all-cast board.',
              'remaining_gates':['Actual authorized provider attachment and reference fidelity','Applicable scene review','Generated-image inspection','Final data/copy before publication'],
              'no_paid_route_enabled':True}
    manifest.update(edition=edition,copy_selector='approval_folio.copy' if folio else 'editorial_copy with full-name presentation',full_character_names=[naming.NAMES[cid] for cid in cast],approval_folio_sha256=folio['content_digest'] if folio else None,actual_result_selected=bool(folio and folio.get('selected_branch')),contains_final_scores=bool(folio and folio.get('result_context')))
    contents['COPY.txt']=(c['headline']+'\n'+c['deck']+'\n\n'+c['body']+'\n').encode()
    contents['layout.json']=(json.dumps(layout,ensure_ascii=False,indent=2)+'\n').encode()
    active_scene={
        'page_id':page_id,'layout_spec':layout,'adjacent_pages':page['adjacent_pages'],
        'written_beats':page.get('written_storyboard',{}).get('beats',[]),
        'action_blocks':page.get('proof_preparation',{}).get('action_blocks',[]),
        'absorbed_source_beats':page.get('absorbed_source_beats',[]),
        'encounter':page['encounter'],'current_cast':cast,
        'character_authorities':{cid:issue['resolved_character_appearances'][cid] for cid in cast},
        'stage':'NEUTRAL_INPUT_REVIEW_NOT_GENERATION_OR_RELEASE',
        'rule':'Current placement and geometry control execution; original source IDs preserve provenance only.'}
    active_scene=naming.transform(active_scene)
    if folio:
        active_scene['written_beats']=folio.get('scene',{}).get('beats',[])
        active_scene['final_visual_direction']=folio.get('final_visual_direction')
        active_scene['selected_result_context']=folio.get('result_context')
        active_scene['publication_text_policy']=folio['publication_text_policy']
        active_scene['stage']='REVIEW_BEFORE_PNG_PERMISSION_NOT_SUBMISSION'
    active_scene['character_identity']=[{'character_id':cid,'full_name':naming.NAMES[cid]} for cid in cast]
    contents['ACTIVE_SCENE.json']=(json.dumps(active_scene,ensure_ascii=False,indent=2)+'\n').encode()

    proof=page.get('proof_preparation',{});actions=proof.get('action_blocks',[])
    instructions=['# '+page_id+' — '+c['headline'],
        'ONE existing neutral visual study, not an all-league poster. The current35-page plan is not input to this commission.',
        'Exact approved subjects: '+', '.join(cast)+'. Attach both included image files through a genuinely supported provider route.',
        'Canvas1080x1920. Use layout.json (current geometry); reserve typography areas from COPY.txt for deterministic composition.',
        'No final score, winner, trophy, other matchup, status diagram or printed workflow. Keep current approved species, face and body architecture.',
        'Do not rerun the previously rejected whole-context native route unchanged. This file is not proof of renderer submission or acceptance.',
        'Venue: '+str(page['encounter'].get('venue_id')),
        'Identity application: '+json.dumps(page.get('scene_identity_application',{}),ensure_ascii=False),
        'Keep Week8 editorial identity; use layered atmosphere, scale, restrained highlights and material detail from the supplied craft references, never their foreign costumes/vehicles/geography.']
    if folio:
        instructions=[x for x in instructions if not x.startswith(('ONE existing neutral','No final score'))]
        instructions.insert(1,'ONE final-result content-review commission. No PNG generation or provider submission is authorized by this file.')
        instructions.append('Use approval_folio.copy as the selected review text. Preserve the chosen outcome as scene context; do not show the climax early.')
        instructions.append(folio.get('performance_edit',''))
        instructions.append(folio.get('final_visual_direction',''))
    instructions.append('ACTIVE_SCENE.json is the complete current scene/transfer contract; use it with layout.json and the two exact references.')
    for transfer in page.get('absorbed_source_beats',[]):instructions.append('Required preserved setup: '+transfer['required_visible_transfer'])
    for action in actions:instructions.append('\n'+json.dumps(action,ensure_ascii=False,indent=2))
    instructions.append('\nNo factual sports inset is included in this neutral input kit. The published page needs accepted outcome-specific copy and fresh full-page fit/pixel review.')
    if folio:instructions=[x for x in instructions if not x.startswith('No factual sports inset')]
    instructions.insert(2,'Characters: '+', '.join(naming.NAMES[cid]+' ['+cid+']' for cid in cast)+'. Full names are mandatory; identifiers bind the established references.')
    instructions=[naming.full_names(x) for x in instructions]
    contents['COMMISSION.md']=('\n\n'.join(instructions)+'\n').encode()
    figures=''.join('<figure><img src="'+a['file']+'" alt="Approved reference '+html.escape(a['character_id'])+'"><figcaption>'+html.escape(a['character_id'])+'</figcaption></figure>' for a in assets)
    review='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+page_id+' source kit</title><style>body{font:18px/1.5 system-ui;max-width:960px;margin:30px auto;padding:20px}section{display:flex;gap:24px;flex-wrap:wrap}figure{flex:1;min-width:240px;margin:0}img{width:100%;max-width:360px}pre{white-space:pre-wrap;overflow-wrap:anywhere}h1{line-height:1.1}</style><h1>'+html.escape(page_id+' · '+c['headline'])+'</h1><p><strong>REFERENCE INPUT KIT — NOT GENERATED ART.</strong> Exactly two approved subjects. Current canvas1080×1920. No winner chosen.</p><section>'+figures+'</section><h2>Exact current draft copy</h2><pre>'+html.escape(contents['COPY.txt'].decode())+'</pre><p>Use COMMISSION.md and layout.json with these exact files. This kit does not certify provider attachment, final results or picture quality.</p></html>'
    review=naming.full_names(review)
    if folio:review=review.replace('No winner chosen.','Final result selected for editorial review; image authorization remains pending.').replace('Exact current draft copy','Current final-result review copy')
    contents['REVIEW.html']=review.encode()
    manifest['files']={name:{'sha256':digest(data),'bytes':len(data)} for name,data in contents.items()}
    # All source validation precedes creation, so a bad reference leaves no partial kit.
    out.mkdir(parents=True,exist_ok=False)
    try:
        for name,data in contents.items():(out/name).write_bytes(data)
        (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    except Exception:
        shutil.rmtree(out);raise
    return manifest

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('result-preview');p.add_argument('--observation',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('page-kit');p.add_argument('--page',choices=['W09-P05','W09-P20'],required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--edition',choices=['neutral','approval-review'],default='neutral')
    args=parser.parse_args();week=args.root/'memo-os/week-9'
    try:
        issue=json.loads((week/REGISTRY).read_text())
        if args.command=='page-kit':
            r=export_page_kit(args.root,issue,args.page,args.output,edition=args.edition);print(json.dumps({'page':args.page,'references':len(r['reference_files']),'state':r['kind']}));return 0
        cards=json.loads((week/CARDS).read_text());observation=json.loads(args.observation.read_text())
        r=reconcile(issue,cards,observation)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
        print(json.dumps({'status':r['status'],'proposals':len(r['page_updates']),'source_accepted':False}))
        return 0 if r['status']=='RECONCILED_CANDIDATE_NOT_ACCEPTED' else 3
    except (OSError,ValueError,KeyError) as exc:
        print('Preparation failed: '+str(exc),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
