from pathlib import Path
import json
R=Path(__file__).resolve().parents[4];P=R/'memo-os/week-10/preproduction';E=Path(__file__).parent
v=json.loads((P/'visual-storytelling-pass-20261117.json').read_text());vb={p['page_id']:p for p in v['pages']}
f=P/'design-review-20261117/composition-directions.json';c=json.loads(f.read_text())
if not (E/'composition-before.json').exists():(E/'composition-before.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
for p in c['pages']:
 s=vb[p['page_id']];p['shot_structure']=s['structure'];p['time_logic']=s['time_logic']
 p['reading_path']=' → '.join(x['new_information'] for x in s['shots'])
 p['narration_placement']=s['copy_flow']['flow_rule']+' '+s['layout_direction']
 p['scope']='Sequential shot/layout direction within the approved existing fictional event. No new publication copy, private anecdote, statistic, cast or permanent geography.'
c['status']='SCENE_LED_DESIGN_WITH_EXPLICIT_WITHIN_FOLIO_SHOT_SEQUENCES';c['visual_storytelling_source']='visual-storytelling-pass-20261117.json'
c['global_rules']=[r for r in c['global_rules'] if not r.startswith('One complete 1080x1920')]
c['global_rules'].insert(0,'One complete 1080x1920 portrait folio may contain multiple deliberate camera views. The current visual_storytelling shot contract controls the sequence; a complete artwork is not limited to one shot.')
f.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
f=P/'reconcile_render_inputs.py';s=f.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise ValueError('Expected one patch anchor, found '+str(s.count(a))+': '+a[:110])
 s=s.replace(a,b)
once("composition_by={c['page_id']:c for c in composition_registry['pages']}","composition_by={c['page_id']:c for c in composition_registry['pages']}\nvisual_registry=read('visual-storytelling-pass-20261117.json')\nvisual_by={p['page_id']:p for p in visual_registry['pages']}\nif set(visual_by)!=set(order):raise ValueError('Shot plans must cover all 34 included folios exactly')")
once("asset_log=[];manifest=[]", "style_rule+='\\n\\nSEQUENTIAL VISUAL STORYTELLING\\n'+'\\n'.join('- '+r for r in visual_registry['global_rules'])\nstyle_rule+='\\nThe visual_storytelling shot plan defines all within-page views. Existing camera/foreground fields describe the anchor scene, not a ban on supplementary or opposing views. Do not copy old paragraph-strip placement from a precedent.'\nasset_log=[];manifest=[]")
once("p['composition_direction']=deepcopy(composition_by[id]);p['personalization_direction']", "p['visual_storytelling']=deepcopy(visual_by[id]);p['composition_direction']=deepcopy(composition_by[id]);p['personalization_direction']")
once(" scene={k:deepcopy(p.get(k)) for k in", " # Append real inspected narrative-grammar references with strictly limited application.\n for gr in p['visual_storytelling']['grammar_references']:\n  existing=next((r for r in precedents if r['repo_path']==gr['repo_path']),None)\n  if existing is not None:existing['storytelling_application']=gr['application']\n  else:\n   nr=precedent(gr['week'],gr['physical_page']);nr['role']='visual_storytelling_precedent';nr['application']=gr['application'];precedents.append(nr)\n scene={k:deepcopy(p.get(k)) for k in")
once("'composition_direction','personalization_direction']}", "'composition_direction','personalization_direction','visual_storytelling']}")
once(" b.update({'personalization_direction':", " b.update({'visual_storytelling':deepcopy(p['visual_storytelling']),'personalization_direction':")
once(" f.update({'personalization_direction':", " f.update({'visual_storytelling':deepcopy(p['visual_storytelling']),'personalization_direction':")
once("d['composition_direction']=deepcopy(p['composition_direction']);d['personalization_direction']", "d['visual_storytelling']=deepcopy(p['visual_storytelling']);d['composition_direction']=deepcopy(p['composition_direction']);d['personalization_direction']")
once("  beat.update({'personalization_direction':", "  beat.update({'visual_storytelling':deepcopy(p['visual_storytelling']),'personalization_direction':")
once("current=pages[p['page_id']];p.update({'personalization_direction':", "current=pages[p['page_id']];p.update({'visual_storytelling':deepcopy(current['visual_storytelling']),'personalization_direction':")
once("p=pages[dep['page_id']];dep.update({'personalization_direction':", "p=pages[dep['page_id']];dep.update({'visual_storytelling':deepcopy(p['visual_storytelling']),'personalization_direction':")
once("issue['design_direction_source']=", "issue['visual_storytelling_source']='visual-storytelling-pass-20261117.json'\nissue['design_direction_source']=")
once("'composition_family':p['composition_direction']['family'],'characters':", "'composition_family':p['composition_direction']['family'],'visual_structure':p['visual_storytelling']['structure'],'visual_beat_count':len(p['visual_storytelling']['shots']),'characters':")
once("'creative_stage':'DESIGN_AND_PERSONALIZATION_PASS_COMPLETE'", "'visual_storytelling_source':'visual-storytelling-pass-20261117.json','creative_stage':'SEQUENTIAL_VISUAL_STORYTELLING_INPUTS_READY'")
once("'Scene-led reading path: '+p['composition_direction']['reading_path']", "'Visual shot sequence: '+p['visual_storytelling']['structure'],'','Scene-led reading path: '+p['composition_direction']['reading_path']")
f.write_text(s)
# A persistent human entrypoint records the new meaning of the output contract.
f=P/'illustrated-png-direction.md';old=f.read_text();prefix='## November 17 — sequential visual storytelling authority\n\nOne completed folio is not one camera view. Follow `visual-storytelling-pass-20261117.json` for each page’s explicit POV, shot sequence and time relation. Cinematic overtures, unequal split POVs, causal action views and reaction details are intentional; single-image breathing pages and level documentary tables are retained where specified. Keep the complete supplied manuscript in reading order, never duplicate it beneath each inset. Earlier “one artwork” language means one coherent deliverable, not a prohibition on authored multiple views. No new artwork is claimed by this revision.\n\n'
if not old.startswith('## November 17 — sequential visual'):f.write_text(prefix+old)
print('Integrated shot contract into compiler and all current consumer paths; no copy/fact/cast/venue changes requested.')
