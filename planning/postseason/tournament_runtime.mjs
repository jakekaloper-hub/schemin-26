#!/usr/bin/env node
/**
 * Schemin' 26 — Championship Island tournament state engine.
 * Derives the island's state ONLY from a verified seven-team 2026 bracket.
 * Does not discover ESPN fixtures, predict winners, publish canon, or render art.
 * Script is replayable in explicit TEST mode with synthetic team identifiers.
 */
export const ROUNDS=Object.freeze([
 {key:'QF',week:15,slots:3,arenas:['CAND-POST-IRON-QUARRY','CAND-POST-SALTWIND','CAND-POST-BREAKWATER']},
 {key:'SF',week:16,slots:2,arenas:['CAND-POST-CROWN-STAIR','CAND-POST-GROVE']},
 {key:'FINAL',week:17,slots:1,arenas:['CAND-POST-LAST-FIELD']}
]);
export class IslandBracketError extends Error{
 constructor(message){super(message);this.name='IslandBracketError';}
}
const must=(condition,message)=>{if(!condition)throw new IslandBracketError(message);};
const unique=items=>new Set(items).size===items.length;
const exact=(a,b)=>a.length===b.length&&a.every(x=>b.includes(x));
const str=v=>typeof v==='string'&&v.trim()!=='';
function empty(){
 return {status:'AWAITING_QUALIFICATION',season:2026,league_id:'1417621',
  contenders:[],qualifiers:[],bye_team_id:null,round:'NOT_STARTED',beach_count:null,
  beach_identities:[],island_access:'PLANNING_ONLY',
  certified_events:[],award:null,champion:null,publication:'HOLD_UNVERIFIED_2026_QUALIFICATION'};
}
function verifyFixture(f,rule,testMode,teamIds){
 must(str(f.fixture_id),'Fixture ID required');
 must(f.round===rule.key,'Wrong round for fixture '+f.fixture_id);
 must(f.week===rule.week,'Wrong scoring week for '+f.fixture_id);
 must(rule.arenas.includes(f.venue_candidate_id),'Wrong fixed-round venue in '+f.fixture_id);
 must(teamIds.has(f.home_id)&&teamIds.has(f.away_id)&&f.home_id!==f.away_id,'Invalid participants '+f.fixture_id);
 must(['PENDING','IN_PROGRESS','FINAL'].includes(f.status),'Bad fixture status '+f.fixture_id);
 if(f.status==='FINAL'){
   must(f.certified===true,'Uncertified result '+f.fixture_id);
   must(testMode?f.source==='TEST':f.source==='ESPN','Untrusted result provider '+f.fixture_id);
   must(str(f.snapshot_id),'Missing immutable source snapshot '+f.fixture_id);
   must(Number.isFinite(f.home_points)&&Number.isFinite(f.away_points),'Missing final scores '+f.fixture_id);
   must([f.home_id,f.away_id].includes(f.winner_id),'Winner not participant '+f.fixture_id);
   if(f.home_points!==f.away_points)must((f.home_points>f.away_points?f.home_id:f.away_id)===f.winner_id,'Score does not match certified winner '+f.fixture_id);
 }else {
   must(!f.winner_id && f.certified!==true,'Provisional result is not legally certified '+f.fixture_id);
 }
}
function sequence(snapshot,testMode=false){
 must(snapshot?.season===2026 && String(snapshot?.league_id)==='1417621','Wrong league/season');
 must(snapshot.reseed===false,'2026 bracket may not reseed in this configured format');
 if(!snapshot.qualification_locked){
   must(!snapshot.entrants?.length && !snapshot.fixtures?.length,'Future participants before qualification lock');
   return empty();
 }
 must(str(snapshot.snapshot_id),'Locked official qualification needs provenance');
 must(testMode?snapshot.source==='TEST':snapshot.source==='ESPN','Qualification source invalid');
 const entrants=snapshot.entrants;
 must(Array.isArray(entrants)&&entrants.length===7,'Exactly seven official qualifiers required');
 must(entrants.every(t=>str(t.team_id)&&Number.isInteger(t.seed)&&t.seed>=1&&t.seed<=7),'Invalid contender ID or seed');
 must(unique(entrants.map(x=>x.team_id))&&unique(entrants.map(x=>x.seed)),'Duplicate entrant or seed');
 const bySeed=[...entrants].sort((a,b)=>a.seed-b.seed),bye=bySeed[0];
 must(bye.seed===1,'First seed must receive bye');
 const known=new Set(entrants.map(x=>x.team_id)), fixtures=snapshot.fixtures||[];
 must(Array.isArray(fixtures)&&fixtures.length<=6,'Too many championship-bracket fixtures');
 must(unique(fixtures.map(f=>f.fixture_id)),'Duplicate fixture IDs');
 must(fixtures.every(f=>ROUNDS.some(r=>r.key===f.round)),'Unknown future or unsupported round in bracket');
 const teamStatus=Object.fromEntries(entrants.map(t=>[t.team_id,{seed:t.seed,state:t.seed===1?'BYE_ADVANCED':'QUALIFIED',eliminated_round:null}]));
 const events=[{type:'QUALIFICATION_LOCKED',snapshot_id:snapshot.snapshot_id,qualifiers:7,initial_beach_count:5},
 {type:'FIRST_ROUND_BYE',team_id:bye.team_id,source_id:snapshot.snapshot_id}];
 let beach=5,expected=bySeed.slice(1).map(t=>t.team_id),roundNow='QF',champion=null,award=null;
 for(const rule of ROUNDS){
   const roundMatches=fixtures.filter(f=>f.round===rule.key);
   must(roundMatches.length<=rule.slots,'Too many fixtures in '+rule.key);
   for(const f of roundMatches)verifyFixture(f,rule,testMode,known);
   must(unique(roundMatches.map(f=>f.venue_candidate_id)),'Round arena duplicated '+rule.key);
   const matched=roundMatches.flatMap(f=>[f.home_id,f.away_id]);
   must(unique(matched),'Contender appears in two matches '+rule.key);
   must(matched.every(x=>expected.includes(x)),'Unqualified/eliminated team inserted into '+rule.key);
   if(roundMatches.length===rule.slots)must(exact(matched,expected),'Incorrect pairing field in '+rule.key);
   const outcomes=roundMatches.filter(f=>f.status==='FINAL');
   const winners=[];
   for(const f of outcomes){
     const loser=f.winner_id===f.home_id?f.away_id:f.home_id;
     teamStatus[f.winner_id].state=rule.key==='FINAL'?'CHAMPION':'ADVANCED';
     teamStatus[loser].state=rule.key==='FINAL'?'RUNNER_UP':'ELIMINATED_'+rule.key;
     teamStatus[loser].eliminated_round=rule.key;
     winners.push(f.winner_id);beach++;
     events.push({type:'RESULT_CERTIFIED',fixture_id:f.fixture_id,round:rule.key,venue_candidate_id:f.venue_candidate_id,winner_id:f.winner_id,loser_id:loser,snapshot_id:f.snapshot_id});
     events.push({type:'SHOREWARD_DESCENT',team_id:loser,from:'CONTENDER_FORTRESS',to:'LOSERS_BEACH',after_round:rule.key});
   }
   const locked=roundMatches.length===rule.slots&&outcomes.length===rule.slots;
   roundNow=rule.key;
   if(!locked) {
     must(!fixtures.some(f=>ROUNDS.findIndex(r=>r.key===f.round)>ROUNDS.findIndex(r=>r.key===rule.key)),
       'Future-round fixture supplied before prior-round certification');
     break;
   }
   events.push({type:'ROUND_CLOSED',round:rule.key,certified_fixture_ids:outcomes.map(f=>f.fixture_id),survivors:winners});
   if(rule.key==='QF')expected=[bye.team_id,...winners];
   if(rule.key==='SF')expected=winners;
   if(rule.key==='FINAL'){
     champion=winners[0];
     award={champion_team_id:champion,venue_candidate_id:'CAND-POST-LAST-FIELD',
       belt:'PRESENT_SUPREMACY',michael_farrell_trophy:'CHAMPIONSHIP_MEMORIAL',release:'HOLD_ATLAS_AND_INDEPENDENT_UMPIRE'};
     events.push({type:'CHAMPIONSHIP_CERTIFIED',champion_team_id:champion,source_snapshot_id:outcomes[0].snapshot_id});
     roundNow='COMPLETE';
   }
 }
 const active=entrants.filter(t=>!['ELIMINATED_QF','ELIMINATED_SF','RUNNER_UP'].includes(teamStatus[t.team_id].state));
 return {status:champion?'CHAMPIONSHIP_CERTIFIED':'TOURNAMENT_IN_PROGRESS',season:2026,
   league_id:'1417621',qualifiers:bySeed.map(t=>({team_id:t.team_id,seed:t.seed})),
   bye_team_id:bye.team_id,round:roundNow,beach_count:beach,
   contender_team_ids:active.map(t=>t.team_id),team_status:teamStatus,
   certified_events:events,champion,award,
   publication:'HOLD_ATLAS_AND_INDEPENDENT_UMPIRE',
   facts:'ESPN_RESULT_LOCK' + (testMode?'_SYNTHETIC_TEST':'')};
}
export function evaluateIslandTournament(snapshot,options={}){
 return sequence(snapshot,options.testMode===true);
}
