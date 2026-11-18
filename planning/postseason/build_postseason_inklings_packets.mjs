#!/usr/bin/env node
/**
 * Schemin' 26 — Postseason Inklings production compiler.
 * Reads ONLY the Founder V2 historical source and physical-site proposal.
 * Emits deterministic editorial cards; never writes to canonical World/Atlas.
 * No autonomous model invocation or independently authenticated authors implied.
 *
 * Usage:
 *   node planning/postseason/build_postseason_inklings_packets.mjs \
 *     [--history path] [--sites path] [--out path]
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const DEFAULT_DIR = path.dirname(new URL(import.meta.url).pathname);
const file = (name) => path.join(DEFAULT_DIR,name);
export const DEFAULT_HISTORY = file('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
export const DEFAULT_SITES = file('ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json');
export const DEFAULT_OUT = file('INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json');

function required(v,msg) {if (!v) throw new Error(msg);}
function hash(data) {return crypto.createHash('sha256').update(data).digest('hex');}
function numeric(v) {return typeof v==='number' && Number.isFinite(v);}
function winner(f) {return f.home.points>f.away.points?f.home:f.away;}
function loser(f) {return f.home.points>f.away.points?f.away:f.home;}
function confine(s) {return String(s).replace(/\s+/g,' ').trim();}

export function validate(history,sites) {
  required(history?.schema==='schemin.postseason_island_history.founder_v2','Founder historical V2 input required');
  required(sites?.schema==='schemin.island_physical_site_evolution.founder_v2','Founder site V2 input required');
  required(history.fixtures.length===56,'Historical bracket must contain exactly 56 contests');
  required(history.annual.length===11,'Historical bracket requires eleven complete years');
  required(sites.sites.length===9,'Nine physical site candidates required');
  const ids=new Set(),siteIds=new Map(sites.sites.map(s=>[s.id,s]));
  required(siteIds.size===9,'Duplicate site IDs');
  const legal={QF:'QUARTERFINAL_ONLY',SF:'SEMIFINAL_ONLY',FINAL:'FINAL_ONLY'};
  for(const f of history.fixtures) {
    required(!ids.has(f.id),'Duplicate fixture '+f.id);
    ids.add(f.id);
    required(numeric(f.home.points)&&numeric(f.away.points),'Missing source score '+f.id);
    required(f.home.points!==f.away.points,'Unresolved tied score '+f.id);
    required(f.winner_slot===winner(f).team_slot,'Verified score/winner disagreement '+f.id);
    required(['QF','SF','FINAL'].includes(f.round),'Unknown round '+f.id);
    const s=siteIds.get(f.staging?.venue_id);
    required(s&&s.round_assignment===legal[f.round],'Venue round conflict '+f.id);
    required(s.name===f.staging.venue_name,'Venue name/ID conflict '+f.id);
    required(f.staging.stage_count===3 && f.staging.stages.length===3,'Three challenge stages required '+f.id);
    required(f.staging.stages.every((b,i)=>b.n===i+1),'Stage order conflict '+f.id);
    required(f.staging.status==='PROPOSED_NONCANON','Unapproved historical scene promoted '+f.id);
  }
  for(const y of history.annual) {
    const fixtures=history.fixtures.filter(f=>f.year===y.year);
    const q=fixtures.filter(f=>f.round==='QF'),sf=fixtures.filter(f=>f.round==='SF'),final=fixtures.filter(f=>f.round==='FINAL');
    required(sf.length===2&&final.length===1,'Season bracket invalid '+y.year);
    required(q.length===(y.year<=2016?0:y.year<=2020?2:3),'Wrong QF count '+y.year);
    required(final[0].winner_slot===y.champion_slot,'Champion mismatch '+y.year);
    required(new Set(fixtures.map(f=>f.id)).size===fixtures.length,'Duplicate season fixtures');
    for (const round of ['QF','SF','FINAL']) {
      const x=fixtures.filter(f=>f.round===round);
      required(new Set(x.map(f=>f.staging.venue_id)).size===x.length,'Same arena hosts two matches in one round '+y.year);
    }
    const semis=[...sf.flatMap(f=>[f.home.team_slot,f.away.team_slot])].sort((a,b)=>a-b);
    if(q.length) {
      const advancing=[...q.map(f=>f.winner_slot),...y.bye_slots].sort((a,b)=>a-b);
      required(JSON.stringify(semis)===JSON.stringify(advancing),'Quarterfinal progression mismatch '+y.year);
    }
    const finalists=[final[0].home.team_slot,final[0].away.team_slot].sort((a,b)=>a-b);
    required(JSON.stringify(finalists)===JSON.stringify(sf.map(f=>f.winner_slot).sort((a,b)=>a-b)),'Semifinal progression mismatch '+y.year);
    if(y.year<=2016) required(y.bye_slots.length===0,'Old four-team season cannot have bye');
    else required(y.bye_slots.length===(y.year<=2020?2:1),'Bye count invalid');
  }
  return true;
}

const cameras={
QF:['causeway spectator arrival','challengers in opposing gates','physical trial objective and safe viewing barriers','mid-stage counters','postmatch beach descent'],
SF:['grandstand capacity reveal','contenders leaving secure fortress quarters','multi-camera three-stage escalation','central desk bracket intercut','two remaining finalist gates'],
FINAL:['historic Last Field entrance','both finalists beneath fixed arch','Champions Walk crowd and private suites','decisive third-stage confrontation','Michael Farrell remembrance separated from celebration']
};
const coverage={QF:'Opening trial: 3 pairings when seven qualify, 2 pairings in six-team era; each result changes the central bracket.',SF:'Only four can compete in this round; the byed survivor is not assumed to be favored.',FINAL:'The same founding arena has one championship fixture every year; all public score captions remain source-verified.'};
const festival={
founding:'2015–16: 4-team era. Original small stands and modest media coverage; no 2025 screens retrojected.',
six:'2017–20: 6-team era. Two QF sites in use, major causeway/event expansion; displays introduced gradually, not all instantly built.',
seven:'2021–25: 7-team era. Three dedicated QF venues, premium suites, media complex, rugged fortress architecture and beach-village hospitality.'
};
export function compile(history,sites,sourceSha=null) {
  validate(history,sites);
  const siteById=new Map(sites.sites.map(s=>[s.id,s]));
  const cards=history.fixtures.map(f=>{
    const site=siteById.get(f.staging.venue_id);
    const w=winner(f),l=loser(f);
    const era=f.year<=2016?'founding':f.year<=2020?'six':'seven';
    return {
      card_id:'INKLINGS-'+f.id,
      verified_fixture_id:f.id,
      season:f.year,
      round:f.round,
      verified:{home:f.home,away:f.away,winner_slot:f.winner_slot,score_class:'ESPN_HISTORICAL_FACT',period:f.scoring_period},
      creative_status:'NONCANON_WORKSHOP_OUTPUT',
      venue:{id:site.id,name:site.name,zone:site.zone,round_class:site.round_assignment,physical_heritage:site.heritage},
      beat_sequence:f.staging.stages,
      storyroom:{
        opening:confine('The crowd converges on '+site.name+'. '+f.home.name+' and '+f.away.name+' enter from opposed gates. Their public challenge is not a deathmatch, and the history of the island does not grant either side victory.'),
        physical_contest_rule:confine('Three escalating stages, both sides exercising active counterplay, followed by one ESPN-certified decision. '+f.staging.encounter_form+'.'),
        closing:confine(w.name+' survives this '+f.round+' encounter. '+l.name+' cannot advance and joins the island shore community after the recorded official result.'),
        wider_bracket_effect:coverage[f.round],
        camp_effect:f.round==='FINAL'?'The runner-up joins the beach after the championship ceremony; the winner receives the Belt and the Farrell Trophy under protected memorial doctrine.':'The surviving side retains a secure contender house; the eliminated side leaves for Losers Beach, without granting competitive privileges to veterans.',
        long_memory:confine('The '+site.name+' site and its structures retain witnessed event history from '+f.year+' only as approved historical fiction. No human-owner continuity inferred from team slot.'),
        source_caveat:'Physical challenge stages and site placements are creative candidates, not verified 2015–2025 ESPN location facts.'
      },
      production:{
        shots:cameras[f.round],
        on_camera_roles:['play-by-play','analyst','field reporter','official results registrar'],
        island_live_screen:'Design-approved only; period-specific hardware history held for World/Tech canon.',
        media_voice:'professional, objective, rivalry-aware, not anonymous omniscience',
        contender_POVs:[{team_slot:f.home.team_slot,name:f.home.name,role:'home entrant — fictional behavior only'}, {team_slot:f.away.team_slot,name:f.away.name,role:'away entrant — fictional behavior only'}],
        era_world_state:festival[era],
        location_release:'HOLD_NOT_ACTIVE_LOC',
        art_release:'HOLD_NO_VERIFIED_CHARACTER_VISUAL_REFERENCES',
        independent_umpire:'PENDING'
      }
    };
  });
  const annual=history.annual.map(y=>{
    const entries=cards.filter(c=>c.season===y.year);
    return {season:y.year,card_ids:entries.map(x=>x.card_id),confirmed_title_holder_slot:y.champion_slot,season_rounds:y.round_counts,
      contender_berths:y.entrants.length,bye_slots:y.bye_slots,
      competing_sites:[...new Set(entries.map(x=>x.venue.id))],
      beginning_beach_population:12-y.entrants.length,
      after_first_elimination_beach_population:12-y.entrants.length+(y.round_counts.quarterfinals||2),
      before_final_beach_population:10,
      post_final_nonchampion_population:11,
      world_state:festival[y.year<=2016?'founding':y.year<=2020?'six':'seven'],
      creative_status:'NONCANON_SEASON_PRODUCTION_PACK'};
  });
  return {schema:'schemin.inklings_postseason_compiled_cards.v1',
    status:'GENERATED_CREATIVE_PRODUCTION_NOT_APPROVED_CANON',
    source_sha256:sourceSha,
    renderer:'planning/postseason/build_postseason_inklings_packets.mjs',
    team:'INKLINGS_POSTSEASON_STORYROOM',
    production_authority:'BEAT_WRITER',
    evidence_counterweights:['SCOUT','LIBRARIAN'],
    final_gate:'INDEPENDENT_UMPIRE',
    no_live_models_invoked:true,
    headline:{seasons:annual.length,matchups:cards.length,challenge_stages:cards.reduce((n,c)=>n+c.beat_sequence.length,0),modern2026_winners_generated:0},
    annual,cards};
}
function cli(args) {
  const opt={history:DEFAULT_HISTORY,sites:DEFAULT_SITES,out:DEFAULT_OUT};
  for(let i=0;i<args.length;i++) {
    if(args[i]==='--history')opt.history=args[++i];
    else if(args[i]==='--sites')opt.sites=args[++i];
    else if(args[i]==='--out')opt.out=args[++i];
    else throw new Error('Unsupported argument '+args[i]);
  }
  const raw=fs.readFileSync(opt.history,'utf8');
  const h=JSON.parse(raw),s=JSON.parse(fs.readFileSync(opt.sites,'utf8'));
  const result=compile(h,s,hash(raw));
  fs.writeFileSync(opt.out,JSON.stringify(result,null,2)+'\n','utf8');
  console.log(JSON.stringify({status:'PASSED',output:path.resolve(opt.out),...result.headline}));
}
if(process.argv[1] && fs.realpathSync(process.argv[1])===fs.realpathSync(new URL(import.meta.url)))cli(process.argv.slice(2));
