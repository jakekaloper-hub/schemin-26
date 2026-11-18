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
export function exportConsumers(cards,topology,contract,broadcast){
  must(cards.schema==='schemin.inklings_postseason_compiled_cards.v1','Inklings compiled cards absent');
  must(cards.cards.length===56&&cards.annual.length===11,'Historical coverage incomplete');
  must(topology.schema==='schemin.championship_island_topology.founder_v2','Founder bridge topology absent');
  must(contract.schema==='schemin.postseason_island_event_contract.founder_v2','Founder 2026 bracket absent');
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
    read('CHAMPIONSHIP_ISLAND_BROADCAST_HERITAGE_2015_2026.proposal.json')
  );
  const out=path.join(dir,'POSTSEASON_CROSS_OS_PREPRODUCTION_EXPORT.founder_v2.json');
  fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({status:'PASS',export:out,history:result.historical_totals,release:result.publication_status}));
}
