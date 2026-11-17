# TheFFHub reference decision — 2026-11-17

**Role:** optional external reference/manual comparison. Schemin owns the
controlled implementation. No vendor league import, odds run or private-data
upload occurred, and no supported third-party API integration is claimed.

Primary source inspected: [TheFFHubClient](https://github.com/abinish/TheFFHubClient/tree/78690c5e3221e6ec4f4fbae9b1b1197a21d312dc),
revision `78690c5e3221e6ec4f4fbae9b1b1197a21d312dc`.
Its [license](https://github.com/abinish/TheFFHubClient/blob/78690c5e3221e6ec4f4fbae9b1b1197a21d312dc/LICENSE)
is MIT. No vendor code was copied.

| Surface | Inspected behavior and Schemin use |
|---|---|
| Playoff odds | 10,000 client-side simulations from season mean and rounded population deviation; qualification/regular-season seeds, not championship odds. Schemin adds recorded seeds, provenance and independent validation. |
| Playoff machine | User-selected results support scenario exploration. Schemin conditional runs retain the exact premise. |
| Schedule comparison | Weekly all-play and schedule comparisons inform useful sports context. Schemin provides disclosed all-play and opponent-scoring summaries. |
| Power rankings | UI says weekly median while helper uses a season-wide mean and early-season fallback. Schemin uses each week's actual median and makes no vendor-equivalence claim. |
| Provider interface | Client uses an internal normalized-data backend; no supported external API/export/embed contract was established. |

Pinned source files:

- [PlayoffOddsHelper.ts](https://github.com/abinish/TheFFHubClient/blob/78690c5e3221e6ec4f4fbae9b1b1197a21d312dc/src/playoffOdds/PlayoffOddsHelper.ts)
- [shared/helpers.ts](https://github.com/abinish/TheFFHubClient/blob/78690c5e3221e6ec4f4fbae9b1b1197a21d312dc/src/shared/helpers.ts)
- [ScheduleComparisonHelper.ts](https://github.com/abinish/TheFFHubClient/blob/78690c5e3221e6ec4f4fbae9b1b1197a21d312dc/src/scheduleComparison/ScheduleComparisonHelper.ts)
- [PowerRankingsHelper.ts](https://github.com/abinish/TheFFHubClient/blob/78690c5e3221e6ec4f4fbae9b1b1197a21d312dc/src/powerRankings/PowerRankingsHelper.ts)
- [leagueApi.ts](https://github.com/abinish/TheFFHubClient/blob/78690c5e3221e6ec4f4fbae9b1b1197a21d312dc/src/leagueApi.ts)

A future comparison must use the same cutoff, teams, division/seed rules and
source date. Assumption differences are not automatically defects. Analyst owns
reconciliation. No comparative vendor run was performed here.
