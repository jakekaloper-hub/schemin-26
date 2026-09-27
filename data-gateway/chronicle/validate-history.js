/**
 * Pure validation functions for Schemin historical evidence.
 * Kept separate from CLI execution so Umpire tests can run without network I/O.
 */

function validateSeason(raw, leagueId, season) {
  const errors = [];
  const warnings = [];

  if (!raw || !raw.leagueData || !Array.isArray(raw.teams) || !Array.isArray(raw.rawMatchups)) {
    return { ok:false, errors:['INVALID_FETCH_SHAPE'], warnings };
  }

  if (String(raw.leagueData.id) !== String(leagueId))
    errors.push(`LEAGUE_ID_MISMATCH expected=${leagueId} actual=${raw.leagueData.id}`);
  if (Number(raw.leagueData.season) !== Number(season))
    errors.push(`SEASON_MISMATCH expected=${season} actual=${raw.leagueData.season}`);

  const ids = raw.teams.map(t => String(t.platformTeamId));
  if (new Set(ids).size !== ids.length) errors.push('DUPLICATE_TEAM_IDS');
  if (String(leagueId)==='1417621' && Number(season)===2025 && raw.teams.length!==12)
    errors.push(`TEAM_COUNT_MISMATCH expected=12 actual=${raw.teams.length}`);

  const teamIds = new Set(ids);
  const seen = new Set();
  const byWeek = new Map();

  for (const m of raw.rawMatchups) {
    const week = Number(m.week);
    if (!Number.isInteger(week) || week < 1) {
      warnings.push('MATCHUP_WITH_INVALID_WEEK');
      continue;
    }
    const home=String(m.homeTeamId), away=String(m.awayTeamId);
    if (!teamIds.has(home)||!teamIds.has(away))
      warnings.push(`MATCHUP_UNKNOWN_TEAM week=${week} home=${home} away=${away}`);

    const key=[week,...[home,away].sort()].join(':');
    if (seen.has(key)) errors.push(`DUPLICATE_MATCHUP ${key}`);
    seen.add(key);
    if (!byWeek.has(week)) byWeek.set(week,[]);
    byWeek.get(week).push(m);
  }

  for (const [week,rows] of byWeek.entries()) {
    const participants=new Set();
    rows.forEach(m=>{participants.add(String(m.homeTeamId));participants.add(String(m.awayTeamId));});
    if (participants.size===12 && rows.length!==6)
      errors.push(`FULL_SLATE_PAIRING_COUNT week=${week} expected=6 actual=${rows.length}`);
  }

  return {ok:errors.length===0,errors,warnings};
}

module.exports={validateSeason};
