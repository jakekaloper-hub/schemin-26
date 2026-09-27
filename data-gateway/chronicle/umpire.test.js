const assert=require('assert');
const {validateSeason}=require('./validate-history');

function base(){
  const teams=Array.from({length:12},(_,i)=>({platformTeamId:i+1,teamName:`T${i+1}`}));
  const rawMatchups=[];
  for(let i=0;i<6;i++) rawMatchups.push({week:1,homeTeamId:i+1,awayTeamId:i+7,homeScore:100+i,awayScore:90+i});
  return {leagueData:{id:1417621,season:2025},teams,rawMatchups};
}

function run(){
  let r=validateSeason(base(),1417621,2025);
  assert.equal(r.ok,true,'clean six-matchup slate should pass');

  const duplicate=base();
  duplicate.rawMatchups.push({...duplicate.rawMatchups[0]});
  r=validateSeason(duplicate,1417621,2025);
  assert.equal(r.ok,false);
  assert(r.errors.some(x=>x.startsWith('DUPLICATE_MATCHUP')),'duplicate pairing must fail');

  const eleven=base();
  eleven.teams.pop();
  r=validateSeason(eleven,1417621,2025);
  assert.equal(r.ok,false);
  assert(r.errors.some(x=>x.startsWith('TEAM_COUNT_MISMATCH')),'2025 team-count corruption must fail');

  const impossible=base();
  impossible.rawMatchups.push({week:1,homeTeamId:1,awayTeamId:2,homeScore:1,awayScore:2});
  r=validateSeason(impossible,1417621,2025);
  assert.equal(r.ok,false,'seven rows with all 12 participants must fail');

  // No champion resolver exists by design. Umpire must never infer a title from scores.
  console.log('PASS: Schemin historical Umpire validation');
}
run();
