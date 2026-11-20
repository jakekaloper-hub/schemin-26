/**
 * @agent-contract
 * @handles ESPN Fantasy data layer — pure parse (parseESPNPayload), primary sync fetch
 *          (fetchESPNFull), league accessibility probe (checkLeagueAccessibility), and individual
 *          fetches for teams/matchups/standings/week matchups. All HTTP via espnClient.js.
 *          Public leagues only — no cookies, no auth.
 * @model none — data fetch and parse only, no LLM
 * @commissioner_facing false
 * @allowed ESPN public API reads via espnClient (fetchPublic, getGameCode); pure data parsing
 * @forbidden ESPN private league auth bypass; DB writes (handled by ingestionAgent); LLM calls
 */

// lib/agents/espnAgent.js
// ESPN Fantasy Football data layer.
//
// HTTP is handled by lib/espnClient.js (public leagues only, no cookies, no auth).
// This module contains:
//   - parseESPNPayload()      — pure parse function for raw ESPN JSON (exported for client fallback)
//   - fetchESPNFull()         — primary sync fetch (settings + teams + matchups in one request)
//   - checkLeagueAccessibility() — pre-sync league probe
//   - fetchESPNTeams/League/Matchups/Standings/WeekMatchups — individual fetches
//   - probeESPNRaw()          — diagnostic probe (never used in production sync path)

const espnClient = require('../espnClient');
const { SCORING_TYPES, ESPN_SCORING_TYPE_MAP } = require('../executive-control/scoringTypeRegistry');
const { parseESPNScoringCode } = require('../contracts/externalBoundaries');
const { emit } = require('../eventBus');

// ── ESPN call volume telemetry (DO-SETUP-MAN-032) ────────────────────────────
// Wraps fetchPublic to emit ESPN_API_CALL on every outbound request.
// Downstream: Netlify function logs + eventBus consumers can aggregate per-league call volume.
async function _fetchPublicWithTelemetry(leagueId, season, views, params, sport) {
  const result = await espnClient.fetchPublic(leagueId, season, views, params, sport);
  emit('ESPN_API_CALL', {
    source: 'espnAgent',
    leagueId,
    season,
    sport,
    views,
    callType: Array.isArray(views) ? views.join(',') : String(views),
    ok: result.ok,
    errorCode: result.ok ? null : (result.error?.code || 'UNKNOWN'),
  });
  return result;
}

// ── Constants ─────────────────────────────────────────────────────────────────

const FULL_VIEWS = ['mSettings', 'mTeam', 'mMatchup', 'mRoster'];

// Top-level fields required to be present in the ESPN response for each view.
// Used by validateEspnResponse() to detect schema drift before parsing.
const VIEW_REQUIRED_FIELDS = {
  mSettings:     ['settings'],
  mTeam:         ['teams'],
  mMatchup:      ['schedule'],
  mRoster:       ['teams'],
  mMatchupScore: ['schedule'],
  mScoreboard:   ['schedule'],
  mBoxscore:     ['schedule'],
  mStandings:    ['teams'],
};

// ── Response Validation ───────────────────────────────────────────────────────

/**
 * Validate that an ESPN API response contains expected top-level fields for
 * each requested view. Emits ESPN_SCHEMA_DRIFT_DETECTED if any required field
 * is absent. Never throws — returns false on drift so callers can decide
 * whether to abort or continue degraded.
 *
 * @param {object} data  raw ESPN JSON
 * @param {string[]} views  the view= params that were requested
 * @param {string|number} espnLeagueId  for event context
 * @returns {boolean}  true if all expected fields present, false if drift detected
 */
function validateEspnResponse(data, views, espnLeagueId) {
  const driftFields = [];
  for (const view of (views || [])) {
    const required = VIEW_REQUIRED_FIELDS[view] || [];
    for (const field of required) {
      if (data[field] === undefined) {
        driftFields.push({ view, field });
      }
    }
  }
  if (driftFields.length > 0) {
    emit('ESPN_SCHEMA_DRIFT_DETECTED', {
      source: 'espnAgent',
      espnLeagueId: String(espnLeagueId),
      driftFields,
    });
    return false;
  }
  return true;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

/**
 * Validate that an ESPN league ID is a numeric string within a plausible range.
 * Throws INVALID_LEAGUE_ID before making any HTTP request if invalid.
 */
function validateLeagueId(espnLeagueId) {
  const id = String(espnLeagueId).trim();
  if (!/^\d{1,10}$/.test(id)) {
    throw new Error('INVALID_LEAGUE_ID');
  }
}

/**
 * Convert an espnClient error object into a named Error.
 * Preserves the full error metadata on error.espnError for callers that need it.
 */
function toError(espnError) {
  return Object.assign(new Error(espnError.code), { espnError });
}

// ── Parse ─────────────────────────────────────────────────────────────────────

/**
 * Parse a raw ESPN Fantasy v3 JSON payload into the normalized shape used
 * throughout the ingestion pipeline.
 *
 * Pure function — no I/O. Used directly by the client-assisted fallback path
 * (api/league-sync-import) so the same parsing runs whether data came from the
 * server-side fetch or a browser-assisted fetch.
 *
 * Throws ESPN_SCHEMA_CHANGED if required keys are missing.
 *
 * @param {object} data  raw JSON from ESPN API
 * @returns {{ leagueData: object, teams: Array, rawMatchups: Array }}
 */
function parseESPNPayload(data) {
  if (data.settings === undefined) throw new Error('ESPN_SCHEMA_CHANGED');
  if (data.teams    === undefined) throw new Error('ESPN_SCHEMA_CHANGED');
  if (data.schedule === undefined) throw new Error('ESPN_SCHEMA_CHANGED');

  const leagueData = {
    id:                         data.id ?? null,
    name:                       data.settings?.name || null,
    season:                     data.seasonId || null,
    scoringType:                (() => {
      const raw = data.settings?.scoringSettings?.scoringType;
      if (typeof raw === 'number') return parseESPNScoringCode(raw);
      if (typeof raw === 'string') return raw;
      return null;
    })(),
    matchupPeriodCount:         data.settings?.scheduleSettings?.matchupPeriodCount || null,
    playoffMatchupPeriodLength: data.settings?.scheduleSettings?.playoffMatchupPeriodLength || 1,
    currentWeek:                data.scoringPeriodId || null,
    // ESPN's authoritative current matchup week counter (weekly, not daily).
    // For non-football: scoringPeriodId is a daily counter — this field is the correct weekly period.
    // Available from mSettings view on data.status.currentMatchupPeriod. BUG-PIPELINE-007.
    // Integer guard: reject non-numeric/float/negative values at the trust boundary.
    currentMatchupPeriod:       (() => { const r = data.status?.currentMatchupPeriod; return (typeof r === 'number' && Number.isInteger(r) && r > 0) ? r : null; })(),
    members:                    data.members || [],
  };

  if (!leagueData.scoringType) {
    emit('SCORING_TYPE_UNRESOLVED', {
      source: 'espnAgent',
      leagueId: data.id,
      rawValue: data.settings?.scoringSettings?.scoringType,
      sport: data.sport,
    });
  }

  // Build stat ID → abbreviation map from scoring settings (H2H_CATEGORY leagues only).
  // Used below to label per-category results with human-readable names (e.g. "HR", "ERA").
  const scoringCatMap = {};
  (data.settings?.scoringSettings?.scoringItems || []).forEach(item => {
    if (item.statId != null && item.abbrev) {
      scoringCatMap[String(item.statId)] = item.abbrev;
    }
  });

  // Build member map: memberId → displayName
  const memberMap = {};
  (data.members || []).forEach(m => {
    memberMap[m.id] = m.displayName
      || `${m.firstName || ''} ${m.lastName || ''}`.trim()
      || null;
  });

  const teams = (data.teams || []).map(team => ({
    platformTeamId: String(team.id),
    teamName: team.name
      || `${team.location || ''} ${team.nickname || ''}`.trim()
      || `Team ${team.id}`,
    ownerName: team.primaryOwner ? (memberMap[team.primaryOwner] || null) : null,
    wins:      team.record?.overall?.wins     || 0,
    losses:    team.record?.overall?.losses   || 0,
    ties:      team.record?.overall?.ties     || 0,
    pointsFor: team.record?.overall?.pointsFor || 0,
    // Playoff + final ranking data (populated after season ends)
    playoffSeed:         team.playoffSeed ?? null,
    rankCalculatedFinal: team.rankCalculatedFinal ?? null,
    rankFinal:           team.rankFinal ?? null,
    // Player-level roster data (from mRoster view — empty array if view not included)
    roster: (team.roster?.entries || []).map(entry => {
      const player = entry.playerPoolEntry?.player;
      if (!player) return null;
      return {
        playerId:        String(player.id),
        name:            player.fullName || `${player.firstName || ''} ${player.lastName || ''}`.trim() || `Player ${player.id}`,
        defaultPosition: player.defaultPositionId,
        proTeamId:       player.proTeamId,
        injured:         player.injured || false,
        injuryStatus:    player.injuryStatus || 'ACTIVE',
        lineupSlotId:    entry.lineupSlotId,
        acquisitionType: entry.acquisitionType,
        // Projected points for current scoring period (statSourceId=1)
        projectedPoints: (() => {
          const currentPeriod = data.scoringPeriodId;
          const proj = (player.stats || []).find(
            s => s.statSourceId === 1 && s.scoringPeriodId === currentPeriod
          );
          return proj?.appliedTotal ?? null;
        })(),
        // Player stats for current scoring period (if available)
        stats: (player.stats || []).map(s => ({
          seasonId:        s.seasonId,
          scoringPeriodId: s.scoringPeriodId,
          statSourceId:    s.statSourceId,   // 0 = actual, 1 = projected
          appliedTotal:    s.appliedTotal ?? null,
        })),
      };
    }).filter(Boolean),
  }));

  // H2H category leagues (baseball, basketball) use category wins as score,
  // not totalPoints (which is always 0). Detect and use cumulativeScore.wins.
  if (!leagueData.scoringType) {
    throw new Error(`scoringType is null after ESPN_SCORING_TYPE_MAP lookup — cannot determine scoring format for league ${leagueData.id}`);
  }
  const isH2HCategory = leagueData.scoringType === SCORING_TYPES.H2H_CATEGORY ||
    leagueData.scoringType === SCORING_TYPES.H2H_EACH_CATEGORY ||
    leagueData.scoringType === SCORING_TYPES.H2H_MOST_CATEGORIES;

  const _seenMatchups = new Set();
  const rawMatchups = (data.schedule || [])
    .filter(entry => entry.home && entry.away)
    .filter(entry => {
      // ESPN can return the same matchup twice (home/away swapped) across syncs.
      // Deduplicate by canonical key: matchupPeriodId + sorted team IDs.
      const key = `${entry.matchupPeriodId}_${[String(entry.home.teamId), String(entry.away.teamId)].sort().join('_')}`;
      if (_seenMatchups.has(key)) return false;
      _seenMatchups.add(key);
      return true;
    })
    .map(entry => {
      let winner = 'pending';
      if (entry.winner === 'HOME') winner = 'home';
      else if (entry.winner === 'AWAY') winner = 'away';
      else if (entry.winner === 'TIE')  winner = 'tie';

      // For H2H category scoring, use category wins as the matchup score.
      // totalPoints is always 0 for these league types.
      const homeScore = isH2HCategory
        ? (entry.home.cumulativeScore?.wins ?? entry.home.totalPoints ?? null)
        : (entry.home.totalPoints != null ? Number(entry.home.totalPoints) : null);
      const awayScore = isH2HCategory
        ? (entry.away.cumulativeScore?.wins ?? entry.away.totalPoints ?? null)
        : (entry.away.totalPoints != null ? Number(entry.away.totalPoints) : null);

      // For H2H_CATEGORY leagues, extract per-category breakdown from scoreByStat.
      // Shape: { "HR": { homeResult: "WIN", homeScore: 12, awayResult: "LOSS", awayScore: 4 }, ... }
      // Keys are abbreviations from the league's scoring settings (e.g. "HR", "ERA") or
      // fallback "stat_N" if not in the category map. NULL when not a category league or
      // scoreByStat is absent (e.g. week not yet finalized).
      let categoryBreakdown = null;
      if (isH2HCategory) {
        const homeSBS = entry.home.cumulativeScore?.scoreByStat;
        const awaySBS = entry.away.cumulativeScore?.scoreByStat;
        if (homeSBS && awaySBS && Object.keys(homeSBS).length > 0) {
          categoryBreakdown = {};
          for (const statId of Object.keys(homeSBS)) {
            const label = scoringCatMap[statId] || `stat_${statId}`;
            categoryBreakdown[label] = {
              homeResult: homeSBS[statId].result || null,
              homeScore:  homeSBS[statId].score  ?? null,
              awayResult: awaySBS[statId]?.result || null,
              awayScore:  awaySBS[statId]?.score  ?? null,
            };
          }
        }
      }

      return {
        week:      entry.matchupPeriodId,
        homeTeamId: String(entry.home.teamId),
        homeScore:  homeScore != null ? Number(homeScore) : null,
        awayTeamId: String(entry.away.teamId),
        awayScore:  awayScore != null ? Number(awayScore) : null,
        winner,
        categoryBreakdown,
      };
    });

  return { leagueData, teams, rawMatchups };
}

// ── League accessibility check ────────────────────────────────────────────────

/**
 * Probe ESPN to determine whether a given league is publicly accessible.
 * Returns a structured result — never throws.
 *
 * @param {string|number} espnLeagueId
 * @param {number} season
 * @returns {Promise<
 *   { accessible: true, leagueName: string, teamCount: number } |
 *   { accessible: false, reason: string, message: string }
 * >}
 */
async function checkLeagueAccessibility(espnLeagueId, season, sport = 'football') {
  try {
    validateLeagueId(espnLeagueId);
  } catch {
    return { accessible: false, reason: 'invalid_id', message: `Invalid ESPN league ID: "${espnLeagueId}". Must be numeric.` };
  }

  const { ok, data, error } = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mSettings'], {}, sport);

  if (!ok) {
    if (error.code === 'ESPN_AUTH_REQUIRED') {
      return {
        accessible: false,
        reason: 'not_supported',
        message: 'This ESPN league requires authentication (private league). FLA only supports public leagues. Go to ESPN → LM Tools → Edit League Settings → Accessibility → Public League.',
      };
    }
    if (error.code === 'ESPN_NOT_FOUND') {
      return { accessible: false, reason: 'not_found', message: `ESPN league ${espnLeagueId} not found for season ${season}.` };
    }
    if (error.code === 'ESPN_REDIRECT' || error.code === 'ESPN_HTML_BLOCKED') {
      emit('ESPN_LEAGUE_BLOCKED', { source: 'espnAgent', espnLeagueId, code: error.code });
    } else {
      emit('ESPN_LEAGUE_ACCESSIBILITY_ERROR', { source: 'espnAgent', espnLeagueId, code: error.code });
    }
    return {
      accessible: false,
      reason: 'espn_unavailable',
      message: 'Unable to verify league accessibility. Check the league ID and season, then try again.',
    };
  }

  if (data.settings === undefined) {
    return { accessible: false, reason: 'espn_unavailable', message: 'Unexpected response from ESPN. Try again.' };
  }

  const teamCount = data.teams?.length ?? 0;
  const leagueName = data.settings.name || `ESPN League ${espnLeagueId}`;

  if (teamCount === 0) {
    return { accessible: false, reason: 'not_found', message: `No teams found for ESPN league ${espnLeagueId} in season ${season}.` };
  }

  return { accessible: true, leagueName, teamCount };
}

// ── Combined full-league fetch (primary sync path) ────────────────────────────

/**
 * Fetch league settings, teams, and full-season matchups in a single ESPN API request.
 * Uses multiple view= parameters to get all data at once.
 *
 * Throws a named Error on failure — error.code is one of the ESPN_* error codes.
 * error.espnError contains the full structured error object from espnClient.
 *
 * @param {string|number} espnLeagueId
 * @param {number} season
 * @returns {Promise<{ leagueData: object, teams: Array, rawMatchups: Array }>}
 */
async function fetchESPNFull(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const { ok, data, error } = await _fetchPublicWithTelemetry(espnLeagueId, season, FULL_VIEWS, {}, sport);
  if (!ok) throw toError(error);
  const valid = validateEspnResponse(data, FULL_VIEWS, espnLeagueId);
  if (!valid) throw Object.assign(new Error('ESPN_SCHEMA_DRIFT_DETECTED'), { code: 'ESPN_SCHEMA_DRIFT_DETECTED' });
  return parseESPNPayload(data);
}

// ── Individual fetches (used by scheduleAgent, verifyAgent, etc.) ─────────────

async function fetchESPNTeams(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const { ok, data, error } = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mTeam'], {}, sport);
  if (!ok) throw toError(error);
  if (data.teams === undefined) throw new Error('ESPN_SCHEMA_CHANGED');

  const memberMap = {};
  (data.members || []).forEach((m) => {
    memberMap[m.id] = m.displayName
      || `${m.firstName || ''} ${m.lastName || ''}`.trim()
      || null;
  });

  return (data.teams || []).map((team) => ({
    platformTeamId: String(team.id),
    teamName: team.name
      || `${team.location || ''} ${team.nickname || ''}`.trim()
      || `Team ${team.id}`,
    ownerName: team.primaryOwner ? (memberMap[team.primaryOwner] || null) : null,
    wins:      team.record?.overall?.wins     || 0,
    losses:    team.record?.overall?.losses   || 0,
    ties:      team.record?.overall?.ties     || 0,
    pointsFor: team.record?.overall?.pointsFor || 0,
  }));
}

async function fetchESPNLeague(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const { ok, data, error } = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mSettings'], {}, sport);
  if (!ok) throw toError(error);
  if (data.settings === undefined) throw new Error('ESPN_SCHEMA_CHANGED');
  return {
    id:                         data.id,
    name:                       data.settings?.name || null,
    season:                     data.seasonId || season,
    scoringType:                (() => {
      const raw = data.settings?.scoringSettings?.scoringType;
      if (typeof raw === 'number') return parseESPNScoringCode(raw);
      if (typeof raw === 'string') return raw;
      return null;
    })(),
    matchupPeriodCount:         data.settings?.scheduleSettings?.matchupPeriodCount || null,
    playoffMatchupPeriodLength: data.settings?.scheduleSettings?.playoffMatchupPeriodLength || 1,
    currentWeek:                data.scoringPeriodId || null,
    currentMatchupPeriod:       (() => { const r = data.status?.currentMatchupPeriod; return (typeof r === 'number' && Number.isInteger(r) && r > 0) ? r : null; })(),
    members:                    data.members || [],
  };
}

async function fetchAllMatchups(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const { ok, data, error } = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mMatchup'], {}, sport);
  if (!ok) throw toError(error);
  if (data.schedule === undefined) throw new Error('ESPN_SCHEMA_CHANGED');

  const _seen = new Set();
  return (data.schedule || [])
    .filter(entry => entry.home && entry.away)
    .filter(entry => {
      const key = `${entry.matchupPeriodId}_${[String(entry.home.teamId), String(entry.away.teamId)].sort().join('_')}`;
      if (_seen.has(key)) return false;
      _seen.add(key);
      return true;
    })
    .map(entry => {
      let winner = 'pending';
      if (entry.winner === 'HOME') winner = 'home';
      else if (entry.winner === 'AWAY') winner = 'away';
      else if (entry.winner === 'TIE')  winner = 'tie';
      // H2H category detection at the standalone fetch level (scoringType not available
      // here, so fall back to cumulativeScore presence as the signal)
      const hasCategories = entry.home.cumulativeScore != null;
      const homeScore = hasCategories
        ? (entry.home.cumulativeScore?.wins ?? entry.home.totalPoints ?? null)
        : (entry.home.totalPoints != null ? Number(entry.home.totalPoints) : null);
      const awayScore = hasCategories
        ? (entry.away.cumulativeScore?.wins ?? entry.away.totalPoints ?? null)
        : (entry.away.totalPoints != null ? Number(entry.away.totalPoints) : null);
      return {
        week:      entry.matchupPeriodId,
        homeTeamId: String(entry.home.teamId),
        homeScore:  homeScore != null ? Number(homeScore) : null,
        awayTeamId: String(entry.away.teamId),
        awayScore:  awayScore != null ? Number(awayScore) : null,
        winner,
      };
    });
}

async function fetchESPNWeekMatchups(espnLeagueId, season, week, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const url = espnClient.buildURL(espnLeagueId, season, ['mMatchup'], { scoringPeriodId: week }, undefined, sport);
  const { ok, data } = await espnClient.fetchURL(url);
  if (!ok || !data.schedule) return {};

  const matchups = {};
  (data.schedule || []).forEach((game) => {
    if (game.matchupPeriodId !== week) return;
    const key = game.id || game.matchupPeriodId;
    if (!matchups[key]) matchups[key] = [];
    if (game.away) matchups[key].push({ teamId: game.away.teamId, teamName: game.away.teamName, score: game.away.totalPoints });
    if (game.home) matchups[key].push({ teamId: game.home.teamId, teamName: game.home.teamName, score: game.home.totalPoints });
  });
  return matchups;
}

async function fetchESPNStandings(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const { ok, data } = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mTeam'], {}, sport);
  if (!ok) return [];
  return (data.teams || [])
    .map((team) => ({
      teamId:    team.id,
      teamName:  team.name || `Team ${team.id}`,
      wins:      team.record?.overall?.wins || 0,
      losses:    team.record?.overall?.losses || 0,
      pointsFor: team.record?.overall?.pointsFor || 0,
    }))
    .sort((a, b) => b.wins - a.wins);
}

// ── Player-level matchup scoring (mScoreboard) ──────────────────────────────

/**
 * Fetch player-level scoring within each matchup for a specific week.
 * Uses mMatchupScore + mScoreboard views — separate from FULL_VIEWS to avoid
 * over-fetching during sync. Used during storyline/narrative generation.
 *
 * @param {string|number} espnLeagueId
 * @param {number} season
 * @param {number} week - matchup period (weekly)
 * @param {string} sport
 * @returns {Promise<Array<{ matchupPeriodId, home: { teamId, totalPoints, roster }, away: { ... } }>>}
 */
async function fetchESPNMatchupScoreboard(espnLeagueId, season, week, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const { ok, data, error } = await _fetchPublicWithTelemetry(
    espnLeagueId, season, ['mMatchupScore', 'mScoreboard'], { scoringPeriodId: week }, sport
  );
  if (!ok) throw toError(error);
  if (!data.schedule) return [];

  return (data.schedule || [])
    .filter(entry => entry.matchupPeriodId === week && entry.home && entry.away)
    .map(entry => {
      const parseTeamScoreboard = (side) => {
        const rosterEntries = (side.rosterForCurrentScoringPeriod?.entries || side.rosterForMatchupPeriod?.entries || []);
        return {
          teamId: String(side.teamId),
          totalPoints: side.totalPoints ?? null,
          roster: rosterEntries.map(re => {
            const player = re.playerPoolEntry?.player;
            if (!player) return null;
            const actualStat = (player.stats || []).find(s => s.statSourceId === 0);
            return {
              playerId: String(player.id),
              name: player.fullName || `Player ${player.id}`,
              lineupSlotId: re.lineupSlotId,
              appliedTotal: actualStat?.appliedTotal ?? null,
            };
          }).filter(Boolean),
        };
      };
      return {
        matchupPeriodId: entry.matchupPeriodId,
        home: parseTeamScoreboard(entry.home),
        away: parseTeamScoreboard(entry.away),
      };
    });
}

// ── ESPN standings with projections (mStandings) ────────────────────────────

/**
 * Fetch ESPN's own playoff projections and standings data.
 * Returns playoff projection data when available (clinch/elimination scenarios).
 *
 * @param {string|number} espnLeagueId
 * @param {number} season
 * @param {string} sport
 * @returns {Promise<Array<{ teamId, teamName, wins, losses, pointsFor, playoffPct, clinched, eliminated }>>}
 */
async function fetchESPNStandingsWithProjections(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const { ok, data } = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mStandings', 'mTeam'], {}, sport);
  if (!ok) return [];

  return (data.teams || [])
    .map(team => ({
      teamId:     String(team.id),
      teamName:   team.name || `Team ${team.id}`,
      wins:       team.record?.overall?.wins || 0,
      losses:     team.record?.overall?.losses || 0,
      pointsFor:  team.record?.overall?.pointsFor || 0,
      playoffPct: team.currentProjectedRank != null ? team.playoffPct : null,
      clinched:   team.clinched || false,
      eliminated: team.eliminated || false,
      draftDayProjectedRank: team.draftDayProjectedRank ?? null,
      currentProjectedRank:  team.currentProjectedRank ?? null,
    }))
    .sort((a, b) => b.wins - a.wins);
}

// ── Diagnostic probe ──────────────────────────────────────────────────────────

/**
 * Raw HTTP probe — returns metadata without classifying or throwing.
 * Only used by the diagnostic endpoint (?diag=1 on league-exists).
 *
 * @param {string} espnLeagueId
 * @param {number} season
 */
async function probeESPNRaw(espnLeagueId, season, sport = 'football') {
  const url = espnClient.buildURL(espnLeagueId, season, ['mSettings'], {}, undefined, sport);
  const result = await espnClient.fetchURL(url);

  if (!result.ok) {
    return {
      url,
      statusCode:    result.error.status,
      location:      result.error.location || null,
      contentType:   result.error.contentType || null,
      bodyPreview:   result.error.bodySnippet || null,
      hasSettingsKey: null,
      error:         result.error.code,
    };
  }

  return {
    url,
    statusCode:    200,
    location:      null,
    contentType:   'application/json',
    bodyPreview:   null,
    hasSettingsKey: 'settings' in result.data,
  };
}

// ── Transaction Parsing ────────────────────────────────────────────────────

/**
 * Parse ESPN mTransactions2 response into normalized transaction objects.
 * Pure function — no I/O.
 *
 * @param {object} data - Raw ESPN response with transactions array
 * @returns {Array<object>} Normalized transactions
 */
function parseTransactions(data) {
  if (!data?.transactions || !Array.isArray(data.transactions)) return [];

  return data.transactions
    .filter(t => t.status === 'EXECUTED')
    .map(t => ({
      transactionId: String(t.id),
      type: t.type,
      scoringPeriodId: t.scoringPeriodId,
      teamId: t.teamId,
      bidAmount: t.bidAmount || 0,
      processDate: t.processDate ? new Date(t.processDate).toISOString() : null,
      items: (t.items || []).map(item => ({
        playerId: item.playerId,
        fromTeamId: item.fromTeamId,
        toTeamId: item.toTeamId,
        action: item.type || 'UNKNOWN',
      })),
    }));
}

/**
 * Fetch league transactions from ESPN (mTransactions2 view).
 */
async function fetchESPNTransactions(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const resp = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mTransactions2'], {}, sport);
  if (!resp.ok) throw toError(resp.error);
  return parseTransactions(resp.data);
}

// ── Boxscore Parsing ───────────────────────────────────────────────────────

function _parseBoxscoreRoster(side) {
  if (!side?.rosterForCurrentScoringPeriod?.entries) return [];
  return side.rosterForCurrentScoringPeriod.entries.map(e => ({
    playerId: e.playerId,
    name: e.playerPoolEntry?.player?.fullName || `Player ${e.playerId}`,
    positionId: e.playerPoolEntry?.player?.defaultPositionId || null,
    lineupSlotId: e.lineupSlotId,
    appliedTotal: e.playerPoolEntry?.appliedStatTotal ?? null,
  }));
}

/**
 * Parse ESPN mBoxscore response into per-player scoring breakdown.
 * Pure function — no I/O.
 *
 * @param {object} data - Raw ESPN response
 * @param {number} week - matchupPeriodId to filter
 * @returns {Array<object>} Per-matchup boxscore with players
 */
function parseBoxscore(data, week) {
  if (!data?.schedule || !Array.isArray(data.schedule)) return [];

  return data.schedule
    .filter(entry => entry.matchupPeriodId === week)
    .map(entry => ({
      matchupPeriodId: entry.matchupPeriodId,
      home: {
        teamId: entry.home?.teamId,
        players: _parseBoxscoreRoster(entry.home),
      },
      away: {
        teamId: entry.away?.teamId,
        players: _parseBoxscoreRoster(entry.away),
      },
    }));
}

/**
 * Fetch boxscore for a specific week.
 */
async function fetchESPNBoxscore(espnLeagueId, season, week, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const resp = await _fetchPublicWithTelemetry(
    espnLeagueId, season, ['mBoxscore'], { scoringPeriodId: week }, sport
  );
  if (!resp.ok) throw toError(resp.error);
  return parseBoxscore(resp.data, week);
}

// ── Draft Detail Parsing ───────────────────────────────────────────────────

/**
 * Parse ESPN mDraftDetail response.
 * Pure function — no I/O.
 */
function parseDraftDetail(data) {
  const dd = data?.draftDetail;
  if (!dd || !dd.picks || !Array.isArray(dd.picks)) {
    return { drafted: false, picks: [] };
  }

  return {
    drafted: dd.drafted !== false,
    picks: dd.picks.map(p => ({
      round: p.roundId,
      roundPick: p.roundPickNumber,
      overallPick: p.overallPickNumber,
      teamId: p.teamId,
      playerId: p.playerId,
      keeper: p.keeper || false,
      bidAmount: p.bidAmount || 0,
      nominatingTeamId: p.nominatingTeamId || null,
    })),
  };
}

/**
 * Fetch draft detail from ESPN.
 */
async function fetchESPNDraftDetail(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const resp = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mDraftDetail'], {}, sport);
  if (!resp.ok) throw toError(resp.error);
  return parseDraftDetail(resp.data);
}

// ── League Status (mStatus) ────────────────────────────────────────────────

/**
 * Fetch league operational status — current scoring period, whether scores are
 * finalized, waiver schedule. Uses mStatus view.
 */
async function fetchESPNStatus(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const { ok, data, error } = await _fetchPublicWithTelemetry(
    espnLeagueId, season, ['mStatus'], {}, sport
  );
  if (!ok) throw toError(error);
  return {
    currentScoringPeriod: (() => { const r = data?.status?.currentMatchupPeriod; return (typeof r === 'number' && Number.isInteger(r) && r > 0) ? r : null; })(),
    latestScoringPeriod:  data?.status?.latestScoringPeriod  ?? null,
    isActive:             data?.status?.isActive              ?? null,
    waiverSchedule:       data?.status?.waiverSchedule        ?? null,
  };
}

// ── Positional Ratings Parsing ─────────────────────────────────────────────

/**
 * Parse ESPN mPositionalRatings response.
 * Returns { [positionId]: Array<{ proTeamId, rank, avgPointsAllowed }> }
 */
function parsePositionalRatings(data) {
  if (!data?.positionalRatings) return {};

  const result = {};
  for (const [posId, posData] of Object.entries(data.positionalRatings)) {
    if (posData?.ratings && Array.isArray(posData.ratings)) {
      result[posId] = posData.ratings.map(r => ({
        proTeamId: r.proTeamId,
        rank: r.rank,
        avgPointsAllowed: r.avgPointsAllowed,
      }));
    }
  }
  return result;
}

/**
 * Fetch defense-vs-position ratings.
 */
async function fetchESPNPositionalRatings(espnLeagueId, season, sport = 'football') {
  validateLeagueId(espnLeagueId);
  const resp = await _fetchPublicWithTelemetry(espnLeagueId, season, ['mPositionalRatings'], {}, sport);
  if (!resp.ok) throw toError(resp.error);
  return parsePositionalRatings(resp.data);
}

// ── Exports ───────────────────────────────────────────────────────────────────

module.exports = {
  parseESPNPayload,
  validateEspnResponse,
  checkLeagueAccessibility,
  fetchESPNFull,
  fetchAllMatchups,
  fetchESPNLeague,
  fetchESPNWeekMatchups,
  fetchESPNStandings,
  fetchESPNStandingsWithProjections,
  fetchESPNMatchupScoreboard,
  fetchESPNTeams,
  probeESPNRaw,
  // Phase A+C expansions
  parseTransactions,
  fetchESPNTransactions,
  parseBoxscore,
  fetchESPNBoxscore,
  parseDraftDetail,
  fetchESPNDraftDetail,
  parsePositionalRatings,
  fetchESPNPositionalRatings,
  fetchESPNStatus,
};
