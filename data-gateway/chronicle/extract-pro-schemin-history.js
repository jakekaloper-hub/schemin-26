#!/usr/bin/env node
/**
 * Schemin '26 Historical Data Gateway — Chronicle evidence extractor
 *
 * AUTHORITATIVE HOME: jakekaloper-hub/schemin-26
 *
 * This project owns historical evidence capture for the Pro Schemin' Chronicle.
 * Fantasy League Artworks may provide upstream/reference ESPN parsing patterns,
 * but Schemin '26 owns this extractor, its evidence contract, validation gates,
 * provenance, and canon admission rules.
 *
 * Target:
 *   ESPN league 1417621
 *   Historical seasons, beginning with 2025
 *
 * Runtime adapter contract:
 *   The caller must provide an ESPN fetch adapter returning:
 *   { leagueData, teams, rawMatchups }
 *
 * No DB writes. No narrative generation. No automatic canon writes.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function stableJson(value) {
  return JSON.stringify(value, null, 2) + '\n';
}

function sha256(text) {
  return crypto.createHash('sha256').update(text).digest('hex');
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function atomicWrite(file, content) {
  const tmp = file + '.tmp';
  fs.writeFileSync(tmp, content, 'utf8');
  fs.renameSync(tmp, file);
}

function validateSeason(raw, leagueId, season) {
  const errors = [];
  const warnings = [];

  if (!raw || !raw.leagueData || !Array.isArray(raw.teams) || !Array.isArray(raw.rawMatchups)) {
    return { ok: false, errors: ['INVALID_FETCH_SHAPE'], warnings };
  }

  if (String(raw.leagueData.id) !== String(leagueId)) {
    errors.push(`LEAGUE_ID_MISMATCH expected=${leagueId} actual=${raw.leagueData.id}`);
  }
  if (Number(raw.leagueData.season) !== Number(season)) {
    errors.push(`SEASON_MISMATCH expected=${season} actual=${raw.leagueData.season}`);
  }

  const ids = raw.teams.map(t => String(t.platformTeamId));
  if (new Set(ids).size !== ids.length) errors.push('DUPLICATE_TEAM_IDS');

  if (String(leagueId) === '1417621' && Number(season) === 2025 && raw.teams.length !== 12) {
    errors.push(`TEAM_COUNT_MISMATCH expected=12 actual=${raw.teams.length}`);
  }

  const teamIds = new Set(ids);
  const seen = new Set();
  const byWeek = new Map();

  for (const m of raw.rawMatchups) {
    const week = Number(m.week);
    if (!Number.isInteger(week) || week < 1) {
      warnings.push('MATCHUP_WITH_INVALID_WEEK');
      continue;
    }

    const home = String(m.homeTeamId);
    const away = String(m.awayTeamId);
    if (!teamIds.has(home) || !teamIds.has(away)) {
      warnings.push(`MATCHUP_UNKNOWN_TEAM week=${week} home=${home} away=${away}`);
    }

    const key = [week, ...[home, away].sort()].join(':');
    if (seen.has(key)) errors.push(`DUPLICATE_MATCHUP ${key}`);
    seen.add(key);

    if (!byWeek.has(week)) byWeek.set(week, []);
    byWeek.get(week).push(m);
  }

  for (const [week, rows] of byWeek.entries()) {
    const participants = new Set();
    for (const m of rows) {
      participants.add(String(m.homeTeamId));
      participants.add(String(m.awayTeamId));
    }
    if (participants.size === 12 && rows.length !== 6) {
      errors.push(`FULL_SLATE_PAIRING_COUNT week=${week} expected=6 actual=${rows.length}`);
    }
  }

  return { ok: errors.length === 0, errors, warnings };
}

function normalizeEvidence(raw) {
  const nameById = Object.fromEntries(
    raw.teams.map(t => [String(t.platformTeamId), t.teamName])
  );

  return {
    league: raw.leagueData,
    teams: raw.teams.map(t => ({
      platformTeamId: t.platformTeamId,
      teamName: t.teamName,
      wins: t.wins ?? null,
      losses: t.losses ?? null,
      ties: t.ties ?? null,
      pointsFor: t.pointsFor ?? null,
      pointsAgainst: t.pointsAgainst ?? null,
    })),
    matchups: raw.rawMatchups.map(m => ({
      week: m.week,
      homeTeamId: m.homeTeamId,
      homeTeamName: nameById[String(m.homeTeamId)] ?? null,
      homeScore: m.homeScore ?? null,
      awayTeamId: m.awayTeamId,
      awayTeamName: nameById[String(m.awayTeamId)] ?? null,
      awayScore: m.awayScore ?? null,
      winner: m.winner ?? null,
    })),
    playoffResolution: {
      status: 'UNRESOLVED',
      champion: null,
      runnerUp: null,
      rule: 'Requires authoritative bracket/final-placement evidence. Never infer from highest-scoring final-week matchup or best regular-season record.',
    },
  };
}

async function loadAdapter(adapterPath) {
  if (!adapterPath) {
    throw new Error('ADAPTER_REQUIRED: pass a module exporting fetchHistoricalLeague(leagueId, season)');
  }
  const absolute = path.resolve(adapterPath);
  const adapter = require(absolute);
  if (typeof adapter.fetchHistoricalLeague !== 'function') {
    throw new Error('INVALID_ADAPTER: expected fetchHistoricalLeague(leagueId, season)');
  }
  return adapter;
}

async function main() {
  const leagueId = process.argv[2] || '1417621';
  const season = Number(process.argv[3] || 2025);
  const adapterPath = process.argv[4] || process.env.SCHEMIN_ESPN_ADAPTER;
  const outputDir = path.resolve(
    process.argv[5] || path.join(process.cwd(), 'world', 'history', String(season), 'evidence')
  );
  const fetchedAt = new Date().toISOString();

  ensureDir(outputDir);

  let raw;
  try {
    const adapter = await loadAdapter(adapterPath);
    raw = await adapter.fetchHistoricalLeague(leagueId, season);
  } catch (err) {
    const failure = {
      source: 'Schemin Data Gateway adapter',
      league_id: String(leagueId),
      season,
      fetched_at: fetchedAt,
      stale: true,
      failure_reason: err?.code || err?.message || 'UNKNOWN',
    };
    atomicWrite(path.join(outputDir, 'FETCH_FAILURE.json'), stableJson(failure));
    process.exitCode = 2;
    return;
  }

  const rawText = stableJson(raw);
  const rawHash = sha256(rawText);
  const rawFile = path.join(
    outputDir,
    `espn-${leagueId}-${season}-raw-${rawHash.slice(0, 12)}.json`
  );

  if (!fs.existsSync(rawFile)) atomicWrite(rawFile, rawText);

  const validation = validateSeason(raw, leagueId, season);
  const evidence = normalizeEvidence(raw);

  atomicWrite(path.join(outputDir, 'PROVENANCE.json'), stableJson({
    source: 'Schemin Data Gateway adapter',
    league_id: String(leagueId),
    season,
    fetched_at: fetchedAt,
    stale: false,
    failure_reason: null,
    raw_payload_sha256: rawHash,
    parser: 'data-gateway/chronicle/extract-pro-schemin-history.js',
    validation,
    canon_write_permitted: false,
  }));

  atomicWrite(path.join(outputDir, 'VALIDATED_EVIDENCE.json'), stableJson(evidence));

  if (!validation.ok) {
    process.exitCode = 3;
    return;
  }

  console.log(`Schemin historical evidence captured: ${rawFile}`);
  console.log(`SHA-256: ${rawHash}`);
  console.log('Historical canon remains locked pending Umpire review and playoff resolution.');
}

main().catch(err => {
  console.error(err);
  process.exitCode = 1;
});

module.exports = { validateSeason, normalizeEvidence };
