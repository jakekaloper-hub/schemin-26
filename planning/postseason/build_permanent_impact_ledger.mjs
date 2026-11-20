#!/usr/bin/env node
/**
 * Every one of 56 Founder Interview II historical fixture proposals leaves a
 * persistent physical trace: either visible or traceable inside the exact same
 * place's archive. Annual repair is required to maintain safe championship use.
 * Immutable source results are never converted to physical harm.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=name=>JSON.parse(fs.readFileSync(path.join(root,name),'utf8'));
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const sites=read('ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json');
const sourceByID=new Map(history.fixtures.map(f=>[f.id,f]));
const siteById=new Map(sites.sites.map(s=>[s.id,s]));
const impactKind={
 CONTACT:['scored stone ring','recessed impact abrasion','restored protective wall chipped during controlled contact'],
 PROJECTILE:['replacement target plate','backstop puncture sequence','embedded arrow-score marks preserved in protected plate'],
 VEHICLE:['sealed track groove','racing barrier replacement','historic skid-stripe in retained turn pavement'],
 SPORT:['court boundary indentation','replaced goal anchoring','cleared but preserved scuff in original competition surface'],
 TACTICAL:['controlled pyrotechnic soot','dismantled stage-breach segment','painted impact board retained in museum'],
 PSYCHOLOGICAL:['etched ceremony table surface','card-stage floor scoring grooves','sealed strategic board move on underfloor archival panel'],
 STRUCTURAL:['restored load-test slot','documented crack in expendable test rig','engineered support repair line'],
 FALL:['abrasion at protected ladder','replacement rope anchor plate','marked harness rescue track in fixed support'],
 WATER:['tide-mark on protected seawall','stained lock-stone','sealed watercourse erosion groove'],
 EXERTION:['weighted-marker pavement crack','repaired stone-lifting edge','scuff from original burden-station foundation'],
 COGNITIVE:['keyplate chisel mark','scored mechanical puzzle slot','museum-held recovered lock mechanism'],
 MIXED:['mixed apparatus foundation line','replaced multi-sport marker','capped challenge rig socket']
};
const siteAnchors={
'CAND-POST-IRON-QUARRY':['lower quarry shelf','western quarry ramp','protected impact wall','stone marshal platform'],
'CAND-POST-SALTWIND':['windward parapet','upper course turnout','southern windscreen foundations','protected finish terrace'],
'CAND-POST-BREAKWATER':['seawall inner lane','tidal marker quay','north harbor steps','dry rescue access'],
'CAND-POST-CROWN-STAIR':['grand ascent tread','upper scoring landing','ceremonial eastern arch','protected judge platform'],
'CAND-POST-GROVE':['outer standard court','stone spectator path','sheltered marker terrace','forest-edge boundary'],
'CAND-POST-LAST-FIELD':['original western gate threshold','historic northern perimeter stone','championship oval outer ring','sealed stage-rig foundation']
};
const sha=s=>crypto.createHash('sha256').update(String(s)).digest('hex');
function select(items,seed){
 if(!items||!items.length)throw Error('No named physical footprint');
 return items[Number(BigInt('0x'+sha(seed))%BigInt(items.length))];
}
export function compilePersistentTraces(historyInput,drawInput){
 if(historyInput.fixtures.length!==56||drawInput.ceremonies.length!==56)throw Error('Complete source archive required');
 const drawById=new Map(drawInput.ceremonies.map(d=>[d.fixture_id,d]));
 const traces=[],idxPerSite=new Map();
 const ordered=historyInput.fixtures.slice().sort((a,b)=>a.year-b.year || ['QF','SF','FINAL'].indexOf(a.round)-['QF','SF','FINAL'].indexOf(b.round) || a.id.localeCompare(b.id));
 for(const f of ordered){
   const d=drawById.get(f.id);if(!d)throw Error('Missing draw '+f.id);
   const site=siteById.get(d.venue_candidate_id);
   if(!site)throw Error('Invalid site '+f.id);
   const kind=impactKind[d.stage_contract?.[0]?.risk_class]||impactKind[d.risk_class]||impactKind.MIXED;
   const actualRisk=d.risk_class||({combat:'CONTACT',marksmanship:'PROJECTILE',racing:'VEHICLE',sports:'SPORT',tactical:'TACTICAL',board:'PSYCHOLOGICAL',engineering:'STRUCTURAL',traverse:'FALL',aquatic:'WATER',endurance:'EXERTION',puzzles:'COGNITIVE',hybrid:'MIXED'})[d.obstacle_family];
   const variants=impactKind[actualRisk];if(!variants)throw Error('Unknown obstacle risk '+f.id);
   const anchor=select(siteAnchors[d.venue_candidate_id],f.id+'|anchor');
   const permanentArtifact=select(variants,f.id+'|physical-consequence');
   const siteIndex=(idxPerSite.get(d.venue_candidate_id)||0)+1;idxPerSite.set(d.venue_candidate_id,siteIndex);
   const championship=f.round==='FINAL';
   traces.push({
    trace_id:'TRACE-'+f.id,
    fixture_id:f.id,year:f.year,round:f.round,site_id:d.venue_candidate_id,
    site_sequence_number:siteIndex,
    drawn_obstacle_id:d.selected_obstacle_id,draw_ticket_sha256:d.draw_ticket_sha256,
    original_material_anchor:anchor,
    persistence_contract:'PERMANENT_HISTORICAL_IMPRINT',
    trace_kind:permanentArtifact,
    material_layer:championship?'MAINTAINED_CHAMPIONSHIP_GROUND':'PERMANENT_ROUND_SITE',
    formation:'AFTER_CERTIFIED_INGAME_THREE_PHASE_FICTION',
    impact:{
      visible_staging:'A deliberate, grounded mark or damaged interchangeable element remains following an intense head-to-head trial; no principal is killed and no spectators are struck.',
      material_consequence:permanentArtifact+' at '+anchor,
      original_world_year:f.year,
      hazard_class:actualRisk,
      temporary_safety_status:'INSPECT_AND_REPAIR_BEFORE_REUSE'
    },
    year_after:{
      year:f.year+1,
      condition:'SAFE_REPAIR_WITH_VISIBLE_MARK_OR_ARCHIVED_ORIGINAL_PART',
      literal_retained_element:'An original marked plate, replaced foundation fitting, repaired stone seam, dated etched inspection line or museum-held damaged rig remains physically identifiable.',
      restored_function:true,history_not_erased:true
    },
    final_stadium_rule:championship?'Permanent original gates, footprint and ceremonial axis cannot move; the trace is confined to sacrificial inlays, visible repaired seams, dedicated preserved fixtures or museum archive; Last Field remains certified operational.':'The permanent venue retains material history, but unprotected hazards must be sealed or cordoned off.',
    source_status:'INVENTED_2015_2025_IN_WORLD_PHYSICAL_HISTORY_CANDIDATE',
    owner_action:'ONE_PRINCIPAL_EXECUTES_ALL_THREE_PHASES',
    injury_law:'Physical consequences permitted in fiction, no real-world injury claimed, no permanent principal death.',
    active_world_state_writeback:false
   });
 }
 if(traces.length!==56 || new Set(traces.map(t=>t.trace_id)).size!==56)throw Error('Unique persistent scar per fixture failed');
 const years=Array.from({length:11},(_,i)=>2015+i).map(year=>{
   const formed=traces.filter(t=>t.year===year);
   const inherited=traces.filter(t=>t.year<year);
   const siteViews=Object.keys(siteAnchors).map(siteId=>{
     const s=traces.filter(x=>x.site_id===siteId&&x.year<=year);
     return {site_id:siteId,known_traces:s.map(x=>x.trace_id),permanent_count:s.length,
       maintained_safe:true,last_founding_infrastructure_unchanged:siteId==='CAND-POST-LAST-FIELD'};
   });
   return {year,formed_this_year:formed.map(t=>t.trace_id),inherited_before_year:inherited.map(t=>t.trace_id),
     cumulative_traces_at_close:formed.length+inherited.length,site_views:siteViews,
     museum_preservation_ledger:'ALL_DAMAGED_REPLACED_ELEMENTS_TRACKED_RATHER_THAN_DISCARDED',
     state_status:'CREATIVE_PROPOSAL_UNPROMOTED'};
 });
 let prior=0;for(const y of years){if(y.cumulative_traces_at_close<=prior)throw Error('Every year must accumulate new historical markings');prior=y.cumulative_traces_at_close;}
 const end=years.at(-1);
 if(end.cumulative_traces_at_close!==56)throw Error('2015–2025 not persistent');
 return {schema:'schemin.championship_island_persistent_traces.v1',status:'FOUNDER_F15_CREATIVE_HISTORY_NOT_ACTIVE_WORLD_MUTATION',
 source:'HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json',draw_source:'HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json',
 physical_rule:'Every fixture must leave an auditable material trace that survives maintenance physically or inside a preserved original artifact. No safety hazard may be deliberately left open and no permanent Last Field foundation damage is approved.',
 counts:{historic_fixtures:56,permanent_traces:56,years:11,last_field_traces:11},
 traces,annual_states:years,
 no_spatial_gis_metrics:true,canon_promotion:false};
}
if(process.argv[1]&&fs.realpathSync(process.argv[1])===fs.realpathSync(fileURLToPath(import.meta.url))){
 const out=compilePersistentTraces(history,draw);
 const filename=path.join(root,'ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
 const serial=JSON.stringify(out,null,2)+'\n';
 if(process.argv.includes('--check'))assert.equal(fs.readFileSync(filename,'utf8'),serial,'Permanent historical traces out of date');
 else fs.writeFileSync(filename,serial);
 console.log(JSON.stringify({status:'PASS',...out.counts,first_cumulative:out.annual_states[0].cumulative_traces_at_close,last_cumulative:out.annual_states.at(-1).cumulative_traces_at_close}));
}
