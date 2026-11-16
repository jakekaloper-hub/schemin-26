"""Repair operative Week 10 mirrors and assemble source-backed, non-rendered page inputs.
Runs only in the existing PR 315 worktree. Does not generate art, alter Atlas canon,
select official winners, merge, publish, or claim unperformed raster acceptance.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,re,shutil
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2]
E=R/'memo-os/week-10/production-evidence/recovery-20261116';E.mkdir(parents=True,exist_ok=True)
NOW=datetime.now(timezone.utc).isoformat()
def read(name):return json.loads((P/name).read_text())
def write(name,obj):(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def image_ref(path,role,character_id=None):
 f=R/path
 with Image.open(f) as im:im.load();dims=list(im.size);fmt=im.format
 return {'repo_path':path,'sha256':digest(f),'bytes':f.stat().st_size,'dimensions':dims,'media_type':'image/png' if fmt=='PNG' else 'image/jpeg','role':role,**({'character_id':character_id} if character_id else {}),'decoded_in_preflight':True}
def precedent(week,page):return image_ref(str((E/f'precedent-w{week:02d}-p{page:02d}.jpg').relative_to(R)),'published_memo_precedent')
issue=read('issue-previs.json');briefs=read('illustrated-page-briefs.json');folio=read('storyboard-folio-plan-pass5.json');chars=read('character-world-packet.json');cards=read('storycards.json');directors=read('director-sequences.json');land=read('landscape-set-bible-pass4.json')
by={x['character_id']:x for x in chars['characters']};pages={x['page_id']:x for x in issue['pages']};bs={x['page_id']:x for x in briefs['pages']};fs={x['page_id']:x for x in folio['folios']};order=issue['recommended_reading_order']
# Explicit current visual-source precedence. The local Chili copy is visually matched
# to the authenticated Library image but is NOT falsely called the historical raw bytes.
chili_local=Path('/Users/jakekaloper/Library/Containers/com.duckduckgo.mobile.ios/Data/tmp/WebKitDropDestination-AeYHXjHz/Screenshot 2026-10-22 at 13.24.14.png')
chili_dest=R/'canon/characters/assets/CHAR-BRANDON-PRYOR/supplementary/COMMISSIONER_CHILI_OUTLAW_2026_10_22_LOCAL_COPY.png'
if not chili_dest.exists():shutil.copyfile(chili_local,chili_dest)
chili=by['CHAR-BRANDON-PRYOR'];chili['current_display_name']='The Chili Cheesers'
chili['current_override_binding']={'repo_path':str(chili_dest.relative_to(R)),'sha256':digest(chili_dest),'source_library_file_id':'libfile_5c84971362508191b1c38adb96a824f0','original_declared_sha256':'dd961918a7707e276dcd9e9fe515fef9ae64e2ff0223f1c75a18da70d3b70e10','matches_original_declared_bytes':False,'source_comparison':'Both authenticated Library image and local copy opened and visually compared in this session: same sunglasses, chili-decorated hat, dark beard, long crimson coat, cartridge bandolier and CHILI OUTLAW buckle. Local encoding/byte identity differs; preserve both hashes.','approval_scope':'Existing October 22 appearance, not a new character design'}
asset_receipts=[]
for c in chars['characters']:
 a=c['presentation_asset'];f=R/a['repo_path'];actual=digest(f)
 if actual!=a['sha256_declared']:raise ValueError('Canonical crop hash mismatch: '+c['character_id'])
 refs=[image_ref(a['repo_path'],'approved_lineup_crop',c['character_id'])]
 if c['character_id']=='CHAR-BRANDON-PRYOR':refs.insert(0,image_ref(str(chili_dest.relative_to(R)),'current_appearance_override',c['character_id']))
 override=c.get('latest_override') or {}
 if override.get('artifact_path') and (R/override['artifact_path']).exists():
  f=R/override['artifact_path']
  if override.get('sha256') and digest(f)!=override['sha256']:raise ValueError('Supplement hash mismatch')
  refs.insert(0,image_ref(override['artifact_path'],'current_appearance_override',c['character_id']))
 c['effective_reference_images']=refs;c['render_status']='SOURCE_IMAGES_DECODED_AND_BOUND_TO_PAGE_INPUTS; NEW_RASTER_NOT_GENERATED'
 c['current_recovery']={'checked_at_utc':NOW,'crop_hash_matches':True,'source_pixels_visually_inspected':True,'actual_generation_executed':False}
 asset_receipts.append({'character_id':c['character_id'],'name':c['current_display_name'],'images':refs})
# Full names in actual prose/prompt inputs; stable character IDs remain untouched.
substitutions=[(r'\bHMB\b',"His Majesty's Blood"),(r'\bTDS\b','Three Dreaded Snake'),(r'\bDK\b','D0nkey K0ng'),(r'\bChins\b(?![\w-])','Seven Deadly Chins'),(r'(?<!Dr. )\bDuckhook\b','Dr. Duckhook'),(r'(?<!The )(?<![-\w])LLC(?![-\w])','The LLC'),(r'\bRed\b(?! Leopards)','Red Leopards'),(r'\bMud\b(?! Dogs)','Mud Dogs'),(r'\bObi\b','ObiWan Jacoby'),(r'\bDuck\b','Dr. Duckhook'),(r'\bSlob\b(?! on my Dobb)','Slob on my Dobb'),(r'(?<!El )\bNiño\b','El Niño'),(r'\bChili\b(?! (?:Cheesers|Outlaw))','The Chili Cheesers')]
def fullnames(value):
 if isinstance(value,str):
  for pat,repl in substitutions:value=re.sub(pat,repl,value)
  value=value.replace('Seven Deadly Seven Deadly Chins','Seven Deadly Chins').replace('The The Chili Cheesers','The Chili Cheesers')
  value=value.replace('Red Leopards’s','Red Leopards’').replace('Mud Dogs’s','Mud Dogs’').replace('The Chili Cheesers’s','The Chili Cheesers’')
  return value
 if isinstance(value,list):return [fullnames(x) for x in value]
 if isinstance(value,dict):return {k:fullnames(v) for k,v in value.items()}
 return value
for p in pages.values():
 p['draft_copy']=fullnames(p['draft_copy'])
 for key in ['camera_and_composition','image_tells','foreground','midground','background','continuity_in','continuity_out','forbidden_mutations']:
  if key in p:p[key]=fullnames(p[key])
# Cover is an editorial synthesis of the two established storyline presentations, not
# an invented literal meeting, alliance or a roof-collapse event.
p=pages['W10-P01'];p['characters_present']=['CHAR-AUSTIN-BYARS','CHAR-DAVID-BABB'];p['owners_present']=['Austin Byars','David Babb']
p['camera_and_composition']='Low, dramatic two-subject editorial cover: canonical His Majesty\'s Blood standing with the controlled gift-bearing posture from the Jackson birthday sequence; canonical The LLC seated in his leather command chair with cigar and dark suit as in the mountain assault. Two coherent atmospheric story territories share one full-bleed composition without implying a physical meeting. The title and complete cover prose occupy deliberately quiet shadow; both characters dominate, not two empty banners.'
p['foreground']='His Majesty\'s Blood: hooded concealed face, two luminous eyes, dark segmented armor, gold chest medallion, ragged cloak, championship belt retained; wrapped birthday gift as the sequence callback.'
p['midground']='The LLC: exact short-haired sunglasses-wearing human executive in dark tailored suit and tie, cigar, leather chair; distant Imperial battery as a subordinate story cue, never a replacement character costume.'
p['background']='An editorial blend of Jackson hall warmth and the separate mountain-gate storm. Architecture remains subordinate to the two canonical figures. No literal roof break or invented common battlefield.'
p['image_tells']=' '.join(p[k] for k in ['camera_and_composition','foreground','midground','background'])
p['encounter'].update({'venue_id':None,'venue_type':'EDITORIAL_DUAL_LOCATION_COVER_NOT_LITERAL_MEETING','set_id':'SET-W10-DUAL-200-EDITORIAL-COVER','location_refs':['LOC-COUNTRY-CLUB-JACKSON','LOC-TRADE-JEDI-MOUNTAIN-BASE'],'persistent_landmarks':['Jackson birthday atmosphere','Mountain assault command position'],'formal_atlas_promotion':False,'unregistered_parent_explained':True})
p['continuity_in']=['Both canonical identities and their Week 10 cinematic presentations, not generic king/executive stand-ins.'];p['continuity_out']=['Cover editorial synthesis does not create a shared encounter, alliance, crown or belt transfer.']
# Published Weeks 7, 8 and 9 clearly establish the Opening Drive department grammar.
p=pages['W10-P02'];p['draft_copy']['department_heading']='OPENING DRIVE'
p['camera_and_composition']='Editorial briefing-table composition matching the published Weeks 7–9 Opening Drive: a perspective Commonwealth map, sealed Week 10 folio, established banners and meaningful scene props under warm lamps. OPENING DRIVE is the dominant department heading; Room Above Two Hundred is the story subheading. Full narration is integrated into two calm dark atmospheric reading zones, not replaced by captions.'
p['foreground']='Sealed Week 10 dispatch folio on the worn briefing table; lasso coil, sandbag tie, a paving fragment, beer delivery slip and two separate story tokens for the birthday and mountain assault. Props are editorial symbols, not evidence of travel.'
p['midground']='Established Commonwealth map and canonical team-banner visual language from the published Opening Drive references. No newly invented map geography or collection of generic figures.'
p['background']='League Chamber records and map room, existing neutral institutional space, windows with approaching weather and warm practical lamps.'
p['image_tells']=' '.join(p[k] for k in ['camera_and_composition','foreground','midground','background'])
p['encounter'].update({'venue_id':'LOC-LEAGUE-CHAMBER','set_id':'SET-W10-OPENING-DRIVE-BRIEFING-TABLE','venue_type':'EDITORIAL_STAGING_IN_REGISTERED_LEAGUE_INSTITUTION','persistent_landmarks':['records desk','map wall','published Opening Drive table and banner language'],'formal_atlas_promotion':False})
p['continuity_in']=['Published Opening Drive identity, inspected in official Weeks 2, 7, 8 and 9.'];p['continuity_out']=['Introduces the entire issue; not a bridge journey or a rodeo overture.']
p['holds']=[h for h in p.get('holds',[]) if 'Opening Drive reference' not in h and 'Mountain Lake Bridge geometry' not in h]
# Printed-body correction: remove backstage directions from actual reader-facing prose.
p=pages['W10-P09'];p['draft_copy']['body']=p['draft_copy']['body'].replace('Later, in the Central Basin—not a magically adjacent corner of the eastern ruins—','Later, in the Central Basin, ')
# Explicit set continuity, resolved against published source images; no Atlas promotion.
for id in ['W10-P08']:
 pages[id]['encounter']['persistent_landmarks']=['Week 9 stepped grass soccer terrace','stone approach arch on near-left','small far goal now damaged, net displaced','narrow stone exit and trapped truck position from Week 9','old tire ruts; shallow overflow uses low edge']
for id in ['W10-P09','W10-P10']:
 p=pages[id];p['encounter']['persistent_landmarks']=['Week 7 rectangular weathered backboard bracketed to the RIGHT stone wall','red-leaf ivy along right wall','wet hard court and worn lines','ascending stone tiers, ruined towers and distant waterfalls','same right-side basket and lens axis; no freestanding hoop pole']
 p['encounter']['source_location_ref']={'type':'PUBLISHED_ARTWORK_SET','week':7,'physical_pages':[8,9,10],'name':'The Forgotten Court','region_id':'REG-CENTRAL-BASIN','permanent_atlas_id':None,'exact_visual_reference_recovered':True}
for id in ['W10-P19','W10-P20','W10-P21']:pages[id]['encounter']['set_id']='SET-W10-JACKSON-BANQUET'
for id in ['W10-P22','W10-P23','W10-P24']:pages[id]['encounter']['set_id']='SET-W10-OBI-RIDGE-GATE'
# Source-adjudicated production review refinements; no invented visual evidence.
pages['W10-P07']['camera_and_composition']='Low public aftermath: The Chili Cheesers lies foreground with the wet rope secured by visible handwork, hat beside him; behind, D0nkey K0ng is one integrated gorilla-centaur with all four hooves planted. Same wet center-ring mud, gate and galleries. No championship belt or property transfer appears.'
pages['W10-P08']['camera_and_composition']='Low oblique from the known soccer-terrace edge: Red Leopards actively lowers a sandbag in the foreground while a shallow trickle curls around its exposed end into the old tire rut. The damaged goal, stone approach and narrow exit retain their Week 9 positions; no basketball basket or tidal wall.'
pages['W10-P20']['camera_and_composition']='Table-height three-quarter view along the established gift-opening axis. The open box reveals a colossal double-decker hamburger with both stacked layers legible; 200 BURGER is an earned prop label. Dr. Duckhook reacts opposite His Majesty’s Blood; the separate birthday cake remains on the sideboard. Preserve the window mullion, service-door angle and guests.'
pages['W10-P21']['camera_and_composition']='Unobstructed three-quarter cake-to-face payoff: His Majesty’s Blood has lifted the separate cake with candles removed and presses it onto Dr. Duckhook’s orange bill. Hands, cake contact and frosting on the green vest remain visible. The untouched double-decker burger stays in its open box to the side; table and witnesses stay fixed.'
pages['W10-P24']['camera_and_composition']='Human-height view outward from the inner arch: ObiWan Jacoby defends with his green blade and separate golden retriever sheltered behind him. One distant Imperial battery is destroyed and smoking; the single surviving battery has multiple barrels converging on the defended approach. Smoke and flags blow in the same established direction. No regenerated battery or second functioning emplacement.'
for refined in ['W10-P07','W10-P08','W10-P20','W10-P21','W10-P24']:
 pages[refined]['image_tells']=' '.join(pages[refined].get(k,'') for k in ['camera_and_composition','foreground','midground','background'])

# Remove optional on-page cast ambiguity and cross-location landmark leakage.
pages['W10-P08']['continuity_in']=deepcopy(pages['W10-P08']['encounter']['persistent_landmarks'])
pages['W10-P08']['background']='The low-side overflow follows the retaining edge. Far across the pitch, El Niño is a small recognizable embodied elemental watching the rain; never a face in cloud. The narrow exit and unresolved Week 9 truck position are not magically repaired.'
pages['W10-P08']['image_tells']=' '.join(pages['W10-P08'].get(k,'') for k in ['camera_and_composition','foreground','midground','background'])
for id in ['W10-P09','W10-P10']:
 pages[id]['continuity_in']=deepcopy(pages[id]['encounter']['persistent_landmarks'])+['Later in the separate Central Basin, after travel from the coastal soccer terrace.']
pages['W10-P33']['midground']='Slob on my Dobb watches from his established shelter, calm but preparing. Only Slob is physically depicted; El Niño is foreshadowed by the incoming weather, not an unbound extra figure.'
pages['W10-P33']['image_tells']=' '.join(pages['W10-P33'].get(k,'') for k in ['camera_and_composition','foreground','midground','background'])

# The data is a verified current capture, not a final-result lock. Numbers unsupported
# by a source are left blank in proofs; source-backed current numbers are qualified.
heading={'W10-P01':'SCHEMIN ’26 · WEEK 10','W10-P02':'OPENING DRIVE','W10-P03':'FROM THE COMMISSIONER','W10-P04':'SCOREBOARD','W10-P11':'THE COMMONWEALTH','W10-P18':'SPORTS DESK','W10-P34':'INJURY REPORT','W10-P25':'RESERVE WATCH','W10-P26':'TRANSACTIONS','W10-P27':'STANDINGS','W10-P28':'STATE OF THE REALM','W10-P29':'SCORING FORM','W10-P30':'THE PLAYOFF ROAD','W10-P31':'THE NEXT SIX','W10-P35':'WEEK 11 · GAME OF THE WEEK','W10-P33':'THE FINAL WORD'}
refmap={'W10-P01':[(9,1),(9,19),(9,22)],'W10-P02':[(7,2),(8,2),(9,2)],'W10-P03':[(7,3),(9,3)],'W10-P04':[(7,4),(9,4)],'W10-P05':[(9,20),(9,21)],'W10-P06':[(9,20),(9,21)],'W10-P07':[(9,22),(9,19)],'W10-P08':[(9,12),(9,14)],'W10-P09':[(7,8),(7,10)],'W10-P10':[(7,8),(7,10)],'W10-P11':[(9,15),(8,20)],'W10-P12':[(9,1),(9,23)],'W10-P13':[(9,1),(9,23)],'W10-P14':[(9,1),(9,25)],'W10-P15':[(9,9),(9,11)],'W10-P16':[(9,10),(9,11)],'W10-P17':[(9,11),(8,13)],'W10-P18':[(9,16)],'W10-P34':[(9,16),(9,26)],'W10-P19':[(9,5),(9,19)],'W10-P20':[(9,5),(9,19)],'W10-P21':[(9,5),(9,19)],'W10-P22':[(8,15),(8,17)],'W10-P23':[(8,15),(8,16)],'W10-P24':[(8,17)],'W10-P25':[(9,26)],'W10-P26':[(9,27)],'W10-P27':[(9,28)],'W10-P28':[(9,29)],'W10-P29':[(9,30)],'W10-P30':[(9,31)],'W10-P31':[(9,32)],'W10-P35':[(9,20),(9,15)],'W10-P33':[(8,7),(9,34)]}
# All supporting-reference images are styling/identity references unless explicitly
# designated as geometry; a historical arena cannot silently become the new venue.
protocol={'stage':'GRAYSCALE_FOLIO_PROOF','canvas':[1080,1920],'master_before_contact_sheet':True,'full_editorial_copy_required':True,'production_metadata_baked_into_art':False,'contact_sheet_is_downstream_composite':True,'no_reinterpretation_when_downscaling':True,'color_generation_is_later':True,'generated_output_identity_review':'RUN_ON_EACH_ACTUAL_OUTPUT_NOT_CLAIMED_BY_PREFLIGHT'}
format_rule='One individual 1080×1920 grayscale integrated illustrated memo folio: complete supplied headline, department heading, deck, narration and source-qualified lettering in the exact intended final composition. No annotation cards, miniature scene summaries, detached document exports, or generated six-up grids.'
style_rule='Image authority is explicit: current_appearance_override controls current face and costume; approved_lineup_crop supplies canonical identity; published_memo_precedent supplies only its stated layout/geometry application and never replaces current character anatomy or current scores. Follow the actual published memo references: one continuous cinematic world, prominent editorial hierarchy, slender ornament where appropriate, full narrative typography inside deliberate atmospheric reading space, and scene-led differences between departments. Grayscale affects palette, not the amount of copy, character identity, panel proportions, camera or final-page geometry.'
asset_log=[];manifest=[]
for pos,id in enumerate(order,1):
 p=pages[id];b=bs[id];f=fs[id];p['draft_copy']['department_heading']=heading.get(id,p['draft_copy'].get('deck',''))
 if id=='W10-P04':
  for row in p['draft_copy']['rows']:row['home_team']=row['home_team'].strip();row['away_team']=row['away_team'].strip();row['status']='PROVISIONAL'
 p['draft_copy_template']=deepcopy(p['draft_copy']);p['contract_status']='RECONCILED_FULL_FOLIO_INPUTS_V6';p['production_mode']='MODE_B_COMPLETE_ILLUSTRATED_GRAYSCALE_PROOF';p['output_width_px']=1080;p['output_height_px']=1920;p['output_aspect_ratio']='9:16'
 p['reference_assets']=[];castrefs=[];identities=[]
 for cid in p['characters_present']:
  c=by[cid];refs=deepcopy(c['effective_reference_images']);castrefs+=refs
  p['reference_assets'].append({'character_id':cid,'owner':c['owner'],'display_name':c['current_display_name'],'images':refs,'appearance':deepcopy(c['assertions']),'override':deepcopy(c.get('latest_override')),'reference_pixels_loaded_in_preflight':True,'generation_output_not_yet_created':True})
  identities.append({'character_id':cid,'full_name':c['current_display_name'],'owner':c['owner'],'appearance':c['assertions'],'current_override':(c.get('latest_override') or {}).get('visual_lock',(c.get('latest_override') or {}).get('scope')),'reference_paths':[x['repo_path'] for x in refs]})
 precedents=[precedent(w,n) for w,n in refmap[id]]
 geometry_ids={'W10-P08':[(9,12),(9,14)],'W10-P09':[(7,8),(7,10)],'W10-P10':[(7,8),(7,10)],'W10-P12':[(9,1)],'W10-P13':[(9,1)],'W10-P14':[(9,1)],'W10-P15':[(9,9),(9,11)],'W10-P16':[(9,10),(9,11)],'W10-P17':[(9,11),(8,13)],'W10-P22':[(8,15),(8,17)],'W10-P23':[(8,15),(8,16)],'W10-P24':[(8,17)],'W10-P33':[(8,7)]}
 for rr in precedents:
  rr['application']='Editorial hierarchy, character treatment and visual integration; do not transplant an unrelated venue or old sports values.'
  if any(rr['repo_path'].endswith(f'precedent-w{w:02d}-p{n:02d}.jpg') for w,n in geometry_ids.get(id,[])):rr['application']='Exact existing location geometry and persistent landmarks, plus current scene changes. No copy of old score values.';rr['role']='published_location_geometry'
 scene={k:deepcopy(p.get(k)) for k in ['camera_and_composition','foreground','midground','background','image_tells','encounter','continuity_in','continuity_out','forbidden_mutations']}
 sports={'official_winner_decided':False,'source_capture_scope':'CURRENT_PROVISIONAL_PRE_MNF','unresolved_numerals':'BLANK_RESERVED_FIELDS','source_backed_current_values':'May be shown only with CURRENT / PROVISIONAL qualifier; never FINAL','result_dependent_art':'Forecast branch only until provider winners decided; persistent common beats retained.','refresh_fields':deepcopy(p.get('deterministic_data_fields',[]))}
 text='\n\n'.join([format_rule,style_rule,'PAGE '+id+' · READING POSITION '+str(pos),'IDENTITY INPUTS\n'+json.dumps(identities,ensure_ascii=False,indent=2),'SCENE AND CONTINUITY\n'+json.dumps(scene,ensure_ascii=False,indent=2),'EXACT FULL PUBLICATION COPY\n'+json.dumps(p['draft_copy'],ensure_ascii=False,indent=2),'FACT POLICY\n'+json.dumps(sports,ensure_ascii=False,indent=2),'REFERENCE IMAGES\n'+json.dumps(castrefs+precedents,ensure_ascii=False,indent=2)])
 b.update({'title':p['title'],'artist_prompt':text,'publication_copy':deepcopy(p['draft_copy']),'exact_copy_template':deepcopy(p['draft_copy']),'reference_bindings':deepcopy(p['reference_assets']),'encounter':deepcopy(p['encounter']),'production_mode':p['production_mode'],'status':'RECONCILED_FULL_FOLIO_INPUTS_V6','pass3_site':{'parent_location_id':p['encounter'].get('venue_id'),'set_id':p['encounter'].get('set_id'),'working_name':p['encounter'].get('venue_type'),'formal_atlas_promotion':False},'source_precedents':precedents,'output':{'format':'PNG','width':1080,'height':1920,'aspect':'9:16','unit':'Complete integrated grayscale illustrated folio'},'render_protocol':deepcopy(protocol)})
 p['pass3_site']=deepcopy(b['pass3_site']);p['candidate_render_prompt']=text;p['illustrated_page_brief']=deepcopy(b);p['visual_precedent_receipt']={'inspection':'ACTUAL_PUBLISHED_PIXELS_INSPECTED','references':precedents};p['text_image_integration']=style_rule
 p['reference_preflight']={'status':'PASS','all_character_images_decoded':True,'per_page_attachment_manifest':'render-inputs/'+id+'/request.json','actual_render_output_review':'NOT_APPLICABLE_UNTIL_GENERATION'}
 f.update({'characters':[{'character_id':cid,'name':by[cid]['current_display_name'],'owner':by[cid]['owner'],'reference_images':deepcopy(by[cid]['effective_reference_images'])} for cid in p['characters_present']],'location':deepcopy(p['encounter']),'composition':p['camera_and_composition'],'sketch_format':format_rule,'publication_copy':deepcopy(p['draft_copy']),'continuity_in':deepcopy(p['continuity_in']),'continuity_out':deepcopy(p['continuity_out']),'reference_images':deepcopy(castrefs+precedents),'render_protocol':deepcopy(protocol),'production_status':'INPUTS_RECONCILED_AND_SOURCE_BOUND','canonical_page_id':id})
 request={'schema_version':'1.0','page_id':id,'reading_position':pos,'sheet':(pos-1)//6+1,'slot':(pos-1)%6+1,'stage':'GRAYSCALE_FOLIO_PROOF','canvas':[1080,1920],'prompt':text,'publication_copy':deepcopy(p['draft_copy']),'scene':scene,'reference_images':castrefs+precedents,'sports_policy':sports,'image_generation_executed':False,'publication_approved':False,'reference_pixels_decoded_at_utc':NOW,'render_protocol':deepcopy(protocol)}
 out=P/'render-inputs'/id;out.mkdir(parents=True,exist_ok=True);(out/'request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n');(out/'full-page-prompt.md').write_text(text+'\n')
 # A decoder ingress receipt records actual bytes loaded, not a fake image-tool call.
 for im in request['reference_images']:
  with Image.open(R/im['repo_path']) as decoded:decoded.load();assert list(decoded.size)==im['dimensions']
 (out/'reference-ingress-receipt.json').write_text(json.dumps({'page_id':id,'check':'ALL_REFERENCE_BYTES_DECODED','image_count':len(request['reference_images']),'reference_hashes':[x['sha256'] for x in request['reference_images']],'generator_invoked':False,'checked_at_utc':NOW},indent=2)+'\n')
 manifest.append({'page_id':id,'reading_position':pos,'sheet':(pos-1)//6+1,'slot':(pos-1)%6+1,'title':p['title'],'characters':[by[x]['current_display_name'] for x in p['characters_present']],'request':'render-inputs/'+id+'/request.json','reference_count':len(request['reference_images']),'copy_words':len(p['draft_copy']['body'].split()),'request_sha256':digest(out/'request.json')})
# Synchronize every current narrative consumer, including embedded prompts and the
# folio ledger which previous patches had missed.
for d in cards['departments']:
 matches=[p for p in pages.values() if p['source_card_id']==d['unit_id']]
 if not matches:continue
 p=matches[0];d['draft_copy']=deepcopy(p['draft_copy']);d['draft_copy_template']=deepcopy(p['draft_copy']);d['cast_character_ids']=deepcopy(p['characters_present']);d['pass3_site']=deepcopy(p['pass3_site']);d['composition']={k:p.get(v) for k,v in [('camera','camera_and_composition'),('foreground','foreground'),('midground','midground'),('background','background')]};d['composition']['copy_placement']=style_rule;d['third_pass']='Superseded by source-inspected full-folio reconciliation V6.';d['state']='RECONCILED_FULL_FOLIO_INPUTS_V6'
for m in cards['matchups']:
 group=[p for p in pages.values() if p['source_card_id']==m['id']]
 for beat,p in zip(m['beats'],group):
  beat.update({'title':p['title'],'copy':p['draft_copy']['body'],'camera':p['camera_and_composition'],'foreground':p['foreground'],'midground':p['midground'],'background':p['background'],'visual_action':p['image_tells'],'continuity_in':deepcopy(p['continuity_in']),'continuity_out':deepcopy(p['continuity_out']),'image_vs_prose':{'image':p['image_tells'],'prose':p['draft_copy']['body']},'copy_status':'RECONCILED_FULL_NAME_PASS4_NARRATIVE'})
 for key in ['physical_action_contract','continuity','concept']:
  if key in m:m[key]=fullnames(m[key])
for p in directors['pages']:
 current=pages[p['page_id']];p.update({'artist_prompt':bs[p['page_id']]['artist_prompt'],'controlling_narration':current['draft_copy']['body'],'reference_binding_ids':deepcopy(current['characters_present']),'prompt_status':'RECONCILED_FULL_FOLIO_INPUTS_V6'})
for seq in directors['sequences']:seq['sequence_note']=fullnames(seq['sequence_note'])
# Set-bible identifiers align to the operative page contracts, not invented aliases.
set_map={'SET-W10-RED-TERRACE':'W10-P08','SET-W10-FORGOTTEN-COURT':'W10-P09','SET-W10-TDS-TEMPLE-COURT':'W10-P12','SET-W10-MUD-SERVICE-ROAD':'W10-P15','SET-W10-JACKSON-BANQUET':'W10-P19','SET-W10-OBI-RIDGE-GATE':'W10-P22','SET-W10-DK-RODEO-GROUNDS':'W10-P05'}
for s in land['sets']:
 pid=set_map.get(s['id'])
 if pid:
  en=pages[pid]['encounter'];s['id']=en['set_id'];s['parent']=en.get('venue_id');s['source_location_ref']=en.get('source_location_ref');s['persistent_landmarks']=deepcopy(en['persistent_landmarks']);s['source_page_id']=pid
for dep in land['department_landscapes']:
 p=pages[dep['page_id']];dep.update({'site':p['encounter'].get('set_id'),'parent_location_id':p['encounter'].get('venue_id'),'camera':p['camera_and_composition'],'action':p['image_tells'],'source_location_ref':p['encounter'].get('source_location_ref'),'source_page_contract':'issue-previs.json#'+p['page_id']})
issue['render_hold_policy']='Preproduction inputs may pass source/contract checks before results. Generate only user-requested individual grayscale full-folio proofs with attached sources. Final publication requires decided ESPN winners, source refresh and actual rendered-output review.'
issue['narrative_source']='issue-draft.md (Pass 4 with full-name expansion and source-backed preflight corrections)';issue['reference_binding_status']='ALL_34_PAGE_INPUTS_ASSEMBLED_FROM_REAL_IMAGE_BYTES';issue['art_generated']=False
folio['stage']='FULL_FOLIO_PROOF_INPUTS_RECONCILED';folio['format_policy']=format_rule;folio['generation_policy']='All six sheets audited first; render individual full folios only after the preflight execution. No final art or publication authorization implied.';folio['source_authority']['published_visual_precedents']='../production-evidence/recovery-20261116/published-memo-source-receipts.json'
for name,obj in [('issue-previs.json',issue),('illustrated-page-briefs.json',briefs),('storyboard-folio-plan-pass5.json',folio),('character-world-packet.json',chars),('storycards.json',cards),('director-sequences.json',directors),('landscape-set-bible-pass4.json',land)]:write(name,obj)
# Earlier creative passes remain history, explicitly removed from current rendering
# authority. Do not destroy or rewrite earlier discussion evidence.
for name in ['whole-issue-pass-03.json','art-atlas-pass3.json','world-story-pass-01.json','world-story-pass-02.json']:
 obj=read(name);obj['consumer_status']='HISTORICAL_PASS_NOT_CURRENT_RENDER_INPUT';obj['current_render_authority']='render-inputs/manifest.json';obj['current_contract_authority']='issue-previs.json';write(name,obj)
write('render-inputs/manifest.json',{'stage':'GRAYSCALE_FOLIO_PROOF_INPUTS','canvas':[1080,1920],'page_count':34,'sheets':6,'sheet_layout':[3,2],'sheet_page_counts':[6,6,6,6,6,4],'empty_final_slots':[5,6],'pages':manifest,'source_images_resolved':True,'new_art_generated':False,'publication_approved':False})
(E/'character-byte-recovery.json').write_text(json.dumps({'checked_at_utc':NOW,'characters':asset_receipts,'chili_override_provenance':chili['current_override_binding']},ensure_ascii=False,indent=2)+'\n')
# Regenerate the human-readable operational mirrors from the SAME exact copy.
md=['# Week 10 — Full-name integrated folio copy','', 'Current source-backed production copy. Current sports values remain provisional; no final result is asserted.','']
briefmd=['# Week 10 — Complete individual grayscale folio production','',format_rule,'',style_rule,'']
planmd=['# Week 10 — Six-sheet full-folio proof ledger','',format_rule,'','Every contact-sheet cell is a scaled copy of its individual page master, never a separate scene summary.','']
for id in order:
 p=pages[id];c=p['draft_copy'];md += ['## '+id+' — '+p['title'],'',c.get('department_heading',''),'',c.get('deck',''),'',c['body'],'']
 for co in c.get('callouts',[]):
  if isinstance(co,dict) and co.get('label') and co.get('value') not in [None,'']:
   md+=['**'+str(co['label'])+'** — '+str(co['value']),'']
  else:md+=['```json',json.dumps(co,ensure_ascii=False,indent=2),'```','']
 if c.get('rows'):md+=['```json',json.dumps(c['rows'],ensure_ascii=False,indent=2),'```','']
 briefmd+=['## '+id+' — '+p['title'],'',bs[id]['artist_prompt'],'']
 f=fs[id];planmd+=['## '+str(order.index(id)+1)+' · '+id+' — '+p['title'],'',p['camera_and_composition'],'','Cast: '+(', '.join(by[x]['current_display_name'] for x in p['characters_present']) or 'No invented principal character'),'','Full copy:','',c['body'],'','Input: `render-inputs/'+id+'/request.json`','']
(P/'issue-draft.md').write_text('\n'.join(md));(P/'illustrated-page-briefs.md').write_text('\n'.join(briefmd));(P/'storyboard-folio-plan-pass5.md').write_text('\n'.join(planmd))
print(json.dumps({'page_requests':len(manifest),'canonical_crops_verified':len(asset_receipts),'reference_image_occurrences':sum(x['reference_count'] for x in manifest),'full_narratives':len(manifest),'new_images_generated':0,'output':'render-inputs/manifest.json'},indent=2))
