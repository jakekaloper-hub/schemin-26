#!/usr/bin/env node
/**
 * Preview-only multi-OS consumer exporter for Founder V2 Championship Island.
 * Produces NO public art, deployment, 2026 winner or canonical world change.
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=name=>JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
const must=(condition,message)=>{if(!condition)throw new Error(message);};
export function exportConsumers(cards,topology,contract,broadcast,obstacles,bindings,material,draw,impacts,scenes,body,finalesV2,storyboard){
  must(cards.schema==='schemin.inklings_postseason_compiled_cards.v1','Inklings compiled cards absent');
  must(cards.cards.length===56&&cards.annual.length===11,'Historical coverage incomplete');
  must(topology.schema==='schemin.championship_island_topology.founder_v2','Founder bridge topology absent');
  must(contract.schema==='schemin.postseason_island_event_contract.founder_v2','Founder 2026 bracket absent');
  must(obstacles?.schema==='schemin.postseason.obstacle_lexicon.v1'&&obstacles.obstacles.length===120,'Obstacle lexicon absent');
  must(bindings?.schema==='schemin.postseason.obstacle_options_for_history.v1'&&bindings.proposals.length===56,'Fixture obstacle proposals absent');
  must(material?.schema==='schemin.postseason.island_material_memory.v1'&&material.years.length===11,'Island material history absent');
  must(draw?.schema==='schemin.island_historical_draw_manifest.v1'&&draw.ceremonies.length===56,'Founder II ceremonial draw missing');
  must(impacts?.schema==='schemin.championship_island_persistent_traces.v1'&&impacts.traces.length===56,'Permanent site traces missing');
  must(scenes?.schema==='schemin.postseason.inklings_interview_ii_scene_contracts.v1'&&scenes.cards.length===56,'Direct owner stage scripts missing');
  must(body?.schema==='schemin.postseason.owner_stage_body_continuity.proposal.v1'&&body.games.length===56,'Physical opponent consequences missing');
  const byFixture=id=>[
    draw.ceremonies.find(x=>x.fixture_id===id),
    impacts.traces.find(x=>x.fixture_id===id),
    scenes.cards.find(x=>x.fixture_id===id),
    body.games.find(x=>x.fixture_id===id)
  ];
  must(cards.cards.every(c=>byFixture(c.verified_fixture_id).every(Boolean)),'Interview II fixture cross-index drift');
  must(scenes.cards.every(c=>c.acts.every(a=>a.solo_contender_A.personally_competes&&a.solo_contender_B.personally_competes)),'Surrogate actor detected');
  must(finalesV2?.schema==='schemin.inklings.last_field_championship_scenes.interview_ii.v2'&&finalesV2.scenes.length===11,'Founder II final scene reconciliation missing');
  must(storyboard?.schema==='schemin.postseason.interview_ii_visual_storyboards.v1'&&storyboard.cards.length===56&&storyboard.counts.shot_contracts===672,'Visual storyboard release packets missing');
  must(finalesV2.scenes.every(f=>draw.ceremonies.some(x=>x.fixture_id===f.verified.fixture_id && x.selected_obstacle_id===f.ceremonial_draw.obstacle_id)),'Outdated final challenge incompatible with ceremonial draw');
  const bindingByFixture=new Map(bindings.proposals.map(x=>[x.fixture_id,x]));
  must(bindingByFixture.size===56,'Duplicate challenge fixture IDs');
  must(cards.cards.every(c=>bindingByFixture.has(c.verified_fixture_id)),'Challenge/ESPN scene mismatch');

  must(broadcast?.schema==='schemin.championship_island_broadcast_continuity.proposal.v1'&&broadcast.years.length===11,'Broadcast chronology absent');
  const ids=new Set(topology.nodes.map(n=>n.id));
  must(topology.edges.every(e=>ids.has(e.from)&&ids.has(e.to)),'Island topology edge dangling');
  must(contract.schedule.qualification_count===7&&contract.schedule.rounds.reduce((a,r)=>a+r.fixture_count,0)===6,'2026 bracket arithmetic mismatch');
  const historicalFinals=cards.cards.filter(c=>c.round==='FINAL');
  must(historicalFinals.length===11,'Every season must have one final');
  for(const c of cards.cards)must(c.creative_status==='NONCANON_WORKSHOP_OUTPUT' && c.verified.score_class==='ESPN_HISTORICAL_FACT','Canon/source classification mismatch');
  const historical=cards.cards.map(c=>({
    encounter_id:c.verified_fixture_id,year:c.season,round:c.round,score:c.verified,
    venue_candidate_id:c.venue.id,site_name:c.venue.name,scene_beats:c.beat_sequence,
    creative_status:c.creative_status,visual_release:'HOLD',verified_winner_slot:c.verified.winner_slot
  }));
  return {
    schema:'schemin.postseason_cross_os_preview.founder_v2',
    status:'PREPRODUCTION_EXPORT_NOT_PUBLICATION',
    founder_source:'planning/postseason/FOUNDER_CHAMPIONSHIP_ISLAND_DECISIONS_2026-11-18.md',
    no_mutation:'world/data, canon, deployed website, active Memo and current Novel publication are untouched',
    consensus:{
      creator:'Inklings under Beat Writer',fact_owner:'Scout / League Truth',geography_owner:'Atlas/Architect',
      heritage_owner:'Librarian',independent_qa:'Umpire',final_delivery:'Closer/Memo/Novel owning publishers'
    },
    memo_os:{
      target:'Weekly Memo OS postseason preproduction, after official league locks',
      media_style:'Modern professional broadcast island event, source-labeled editorial vs verified league facts',
      landscape:'Fixed round venues and linked broadcast desk',
      history_cards:historical.map(c=>({encounter_id:c.encounter_id,round:c.round,venue:c.site_name,stages:c.scene_beats.length,status:c.creative_status})),
      release_gate:'NO_RENDER_UNTIL_PROMOTED_SITE_CHARACTER_REFERENCES_AND_FACT_LOCK'
    },
    novel_os:{
      target:'Historical Chronicle / twelve selectable principal POVs',
      encounter_contracts:historical.map(c=>({id:c.encounter_id,year:c.year,round:c.round,score:c.score,venue_candidate_id:c.venue_candidate_id,stage_beats:c.scene_beats,owner_identity_status:'HOLD_HISTORIC_SLOT_NOT_PERSON',narrative_status:'WORKSHOP_STAGE_DRAFT'})),
      chapter_mode:'Eleven annual movements + match-by-match scripts after history/owner/POV reconciliation',
      release_gate:'NO_CHAPTER_PUBLICATION_WITH_UNVERIFIED_OWNER_OR_ERA_CHARACTER'
    },
    atlas:{
      zone_affiliation:'REG-INNER-SEA-LITTORAL',coordinate_space:'ABSTRACT_UNMEASURED',
      nodes:topology.nodes.map(n=>({id:n.id,zone:n.zone,use:n.use,status:n.status})),
      edges:topology.edges.map(e=>({from:e.from,to:e.to,modes:e.modes})),
      source_geo:'planning/postseason/ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json',
      release_gate:'NO_WORLD_WRITEBACK_UNTIL_ROUTE_HYDROLOGY_AND_LAST_FIELD_SUPERSESSION'
    },
    commonwealth_site:{
      target:'Living World Atlas preview; site publishing not currently authorized',
      years:cards.annual.map(y=>{
        const final=historicalFinals.find(f=>f.season===y.season);
        const winningSide=final.verified.home.team_slot===final.verified.winner_slot?final.verified.home:final.verified.away;
        return {year:y.season,champion_name:winningSide.name,champion_slot:winningSide.team_slot,
          historical_source:'ESPN',fictional_final_site:'Last Field',site_status:'DRAFT_PROPOSAL',
          encounters:y.card_ids.length};
      }),
      renders_available:false,deployed:false
    },
    broadcast_os:{history:broadcast.years,unit_packages:broadcast.venue_unit_packages,technology_governance:broadcast.technical_doctrine.governance,distribution:broadcast.technical_doctrine.distribution_to_mainland,release:'HOLD_WORLD_TECH'},
    obstacle_os:{
      source_registry:'planning/postseason/OBSTACLE_LEXICON_120_V1.json',
      status:'FICTIONAL_CHALLENGE_PROPOSALS_NOT_CANON',
      count:obstacles.obstacles.length,
      families:obstacles.families.map(x=>({slug:x.slug,name:x.label,risk:x.risk})),
      scene_assignments:bindings.proposals.map(x=>({
         fixture_id:x.fixture_id,venue_candidate_id:x.venue_candidate_id,year:x.year,round:x.round,
         selected_obstacle_id:x.picked_obstacle_id,
         match_result_source:'ESPN_FLAIM_VERIFIED',
         material_state:'SCARS_PENDING_WORLD_REVIEW',
         release:'HOLD'
      })),
      physical_compatibility_references:'planning/postseason/arena_physical_affordances.mjs',
      risk_controls:'Explicitly evaluated per candidate scene'
    },
    temporal_site_memory:{
      years:material.years.map(x=>({year:x.year,era:x.era,site_states:x.legacy_sites.map(s=>({site_id:s.id,activation:s.activation,fixture_count:s.matched_fixtures.length}))})),
      dormant_heritage:material.perimeter_ruins.map(x=>({id:x.id,name:x.name,status:x.state,narrative:x.narrative})),
      release:'HOLD_NO_WORLD_MEMORY_WRITEBACK'
    },
    interview_ii:{
      founder_source:'planning/postseason/FOUNDER_INTERVIEW_II_DECISION_REGISTER_2026_11_19.md',
      ceremonial_draws:draw.ceremonies.map(d=>({fixture_id:d.fixture_id,chosen_obstacle:d.selected_obstacle_id,ticket:d.draw_ticket_sha256,ceremony_status:d.ceremonial_status})),
      permanent_traces:impacts.traces.map(t=>({fixture_id:t.fixture_id,site_id:t.site_id,trace_id:t.trace_id,physical_anchor:t.original_material_anchor,kind:t.trace_kind,restored_function:t.year_after.restored_function})),
      annual_trace_history:impacts.annual_states.map(y=>({year:y.year,cumulative_traces_at_close:y.cumulative_traces_at_close})),
      in_world_direct_competition:scenes.cards.map(s=>({fixture_id:s.fixture_id,drawn_challenge:s.draw.name,phases:s.acts.map(a=>({phase:a.number,solo_a:a.solo_contender_A.personally_competes,solo_b:a.solo_contender_B.personally_competes}))})),
      body_consequence_counts:body.counts,
      release:'NO_OWNER_PERSONAL_HISTORY_OR_SPATIAL_CANON_PROMOTION'
    },
    visual_preproduction:{
      source:'INKLINGS_INTERVIEW_II_VISUAL_STORYBOARDS_56.proposal.json',
      fixture_count:56,shot_count:672,
      stage_and_camera_packets:storyboard.cards.map(c=>({
        fixture_id:c.fixture_id,
        visual_sequence_ids:c.production_cameras.map(v=>v.shot_id),
        reference_heritage:c.protected_heritage,
        art_status:c.cut_release
      })),
      final_prose_reconciliation:finalesV2.scenes.map(s=>({
        year:s.year,verified_fixture_id:s.verified.fixture_id,
        ceremonial_obstacle:s.ceremonial_draw.obstacle_id,
        maintained_stadium:s.venue_id,
        status:s.release
      })),
      release:'NO_REAL_CHARACTER_RENDER_OR_2026_PUBLICATION'
    },
    postseason_2026:{
      event_structure:contract.schedule,round_venues:contract.venue_assignment.rounds,
      qualifiers:null,fixtures:null,winners:null,finalists:null,champion:null,
      release_gate:'POST_WEEK14_SOURCE_LOCK_AND_ISLAND_CANON_APPROVAL'
    },
    publication_status:'HOLD_NO_INDEPENDENT_UMPIRE_OR_ACTIVE_ATLAS_PROMOTION',
    historical_totals:{years:11,matchups:56,stages:168,unique_island_nodes:topology.nodes.length}
  };
}
if(process.argv[1]&&fs.realpathSync(process.argv[1])===fs.realpathSync(fileURLToPath(import.meta.url))){
  const result=exportConsumers(
    read('INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json'),
    read('ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json'),
    read('POSTSEASON_2026_ISLAND_EVENT_CONTRACT.proposal.json'),
    read('CHAMPIONSHIP_ISLAND_BROADCAST_HERITAGE_2015_2026.proposal.json'),
    read('OBSTACLE_LEXICON_120_V1.json'),
    read('HISTORICAL_CHALLENGE_OPTION_BINDINGS_56_V1.json'),
    read('ISLAND_MATERIAL_MEMORY_2015_2025_V1.json'),
    read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json'),
    read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json'),
    read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json'),
    read('INKLINGS_OWNER_BODY_CONSEQUENCE_2015_2025.proposal.json'),
    read('INKLINGS_ELEVEN_CHAMPIONSHIP_FINALES_INTERVIEW_II_V2.proposal.json'),
    read('INKLINGS_INTERVIEW_II_VISUAL_STORYBOARDS_56.proposal.json')
  );
  const out=path.join(dir,'POSTSEASON_CROSS_OS_PREPRODUCTION_EXPORT.founder_v2.json');
  fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({status:'PASS',export:out,history:result.historical_totals,release:result.publication_status}));
}
