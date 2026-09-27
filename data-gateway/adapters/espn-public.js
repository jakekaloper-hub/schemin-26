/**
 * Schemin '26 — ESPN Fantasy public read adapter
 *
 * Read-only. No cookies. No DB writes. No narrative.
 * Returns the extractor contract:
 *   { leagueData, teams, rawMatchups }
 */

const https = require('https');
const zlib = require('zlib');

const PRIMARY_HOST = 'lm-api-reads.fantasy.espn.com';
const FALLBACK_HOST = 'fantasy.espn.com';
const TIMEOUT_MS = 8000;
const RETRY_DELAYS = [0, 250, 750];

const VIEWS = ['mSettings', 'mTeam', 'mMatchup', 'mStandings'];

function buildUrl(host, leagueId, season) {
  const query = VIEWS.map(v => `view=${encodeURIComponent(v)}`).join('&');
  return `https://${host}/apis/v3/games/ffl/seasons/${season}/segments/0/leagues/${leagueId}?${query}`;
}

function requestJson(url) {
  return new Promise(resolve => {
    const parsed = new URL(url);
    const req = https.request({
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 Schemin26-Historical-Gateway/1.0',
        Accept: 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
      },
    }, res => {
      const status = res.statusCode;
      const contentType = res.headers['content-type'] || '';
      if ([301,302,303].includes(status)) {
        res.resume();
        return resolve({ok:false,error:{code:'ESPN_REDIRECT',status}});
      }
      if (status === 401 || status === 403) {
        res.resume();
        return resolve({ok:false,error:{code:'ESPN_AUTH_REQUIRED',status}});
      }
      if (status === 404) {
        res.resume();
        return resolve({ok:false,error:{code:'ESPN_NOT_FOUND',status}});
      }
      if (status === 429) {
        res.resume();
        return resolve({ok:false,error:{code:'ESPN_RATE_LIMIT',status}});
      }
      if (status >= 500) {
        res.resume();
        return resolve({ok:false,error:{code:'ESPN_UPSTREAM_ERROR',status}});
      }
      if (status !== 200 || contentType.includes('text/html')) {
        res.resume();
        return resolve({ok:false,error:{code:'ESPN_HTML_BLOCKED',status,contentType}});
      }

      const enc = res.headers['content-encoding'] || '';
      let stream = res;
      if (enc.includes('gzip')) stream = res.pipe(zlib.createGunzip());
      else if (enc.includes('deflate')) stream = res.pipe(zlib.createInflate());
      else if (enc.includes('br')) stream = res.pipe(zlib.createBrotliDecompress());

      const chunks = [];
      stream.on('data', c => chunks.push(c));
      stream.on('end', () => {
        try {
          const raw = Buffer.concat(chunks).toString('utf8');
          if (/^\s*</.test(raw)) return resolve({ok:false,error:{code:'ESPN_HTML_BLOCKED',status}});
          resolve({ok:true,data:JSON.parse(raw)});
        } catch {
          resolve({ok:false,error:{code:'ESPN_JSON_PARSE_ERROR',status}});
        }
      });
      stream.on('error', e => resolve({ok:false,error:{code:'ESPN_UPSTREAM_ERROR',detail:e.message}}));
    });

    const timer = setTimeout(() => {
      req.destroy();
      resolve({ok:false,error:{code:'ESPN_TIMEOUT'}});
    }, TIMEOUT_MS);
    req.on('close', () => clearTimeout(timer));
    req.on('error', e => resolve({ok:false,error:{code:'ESPN_TIMEOUT',detail:e.message}}));
    req.end();
  });
}

async function withRetry(url) {
  let last;
  for (let i=0;i<RETRY_DELAYS.length;i++) {
    if (i) await new Promise(r => setTimeout(r, RETRY_DELAYS[i]));
    last = await requestJson(url);
    if (last.ok) return last;
    if (!['ESPN_TIMEOUT','ESPN_UPSTREAM_ERROR'].includes(last.error.code)) return last;
  }
  return last;
}

function teamName(t) {
  const location = t.location || '';
  const nickname = t.nickname || '';
  return [location,nickname].filter(Boolean).join(' ').trim() || t.name || t.abbrev || String(t.id);
}

function parse(data) {
  if (!data || !data.settings || !Array.isArray(data.teams) || !Array.isArray(data.schedule)) {
    const e = new Error('ESPN_SCHEMA_CHANGED');
    e.code = 'ESPN_SCHEMA_CHANGED';
    throw e;
  }

  const teams = data.teams.map(t => {
    const overall = t.record?.overall || {};
    return {
      platformTeamId: t.id,
      teamName: teamName(t),
      wins: overall.wins ?? null,
      losses: overall.losses ?? null,
      ties: overall.ties ?? null,
      pointsFor: overall.pointsFor ?? null,
      pointsAgainst: overall.pointsAgainst ?? null,
      finalStanding: t.rankCalculatedFinal ?? t.playoffSeed ?? null,
      ownerIds: t.owners || [],
    };
  });

  const rawMatchups = data.schedule.map(m => ({
    week: m.matchupPeriodId,
    homeTeamId: m.home?.teamId ?? null,
    homeScore: m.home?.totalPoints ?? null,
    awayTeamId: m.away?.teamId ?? null,
    awayScore: m.away?.totalPoints ?? null,
    winner: m.winner ?? null,
    playoffTierType: m.playoffTierType ?? null,
  })).filter(m => m.homeTeamId != null && m.awayTeamId != null);

  return {
    leagueData: {
      id: data.id ?? null,
      name: data.settings?.name ?? null,
      season: data.seasonId ?? null,
      scoringType: data.settings?.scoringSettings?.scoringType ?? null,
      matchupPeriodCount: data.settings?.scheduleSettings?.matchupPeriodCount ?? null,
      playoffMatchupPeriodLength: data.settings?.scheduleSettings?.playoffMatchupPeriodLength ?? null,
      currentWeek: data.scoringPeriodId ?? null,
    },
    teams,
    rawMatchups,
  };
}

async function fetchHistoricalLeague(leagueId, season) {
  const primary = await withRetry(buildUrl(PRIMARY_HOST, leagueId, season));
  let result = primary;
  if (!primary.ok && ['ESPN_REDIRECT','ESPN_HTML_BLOCKED'].includes(primary.error.code)) {
    result = await withRetry(buildUrl(FALLBACK_HOST, leagueId, season));
  }
  if (!result.ok) {
    const e = new Error(result.error.code);
    e.code = result.error.code;
    e.espn = result.error;
    throw e;
  }
  return parse(result.data);
}

module.exports = { fetchHistoricalLeague, parse, buildUrl };
