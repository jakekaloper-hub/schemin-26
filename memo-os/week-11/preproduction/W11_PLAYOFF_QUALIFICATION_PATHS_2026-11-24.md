# Who can still make the seven after Week 11?

**Every team has at least one way into the playoffs and at least one way to miss.** This follows from specific possible Week 12–14 results and ESPN's automatic seeding rules. It takes no assumption about the probability of those results. All examples assume the league's settings stay in force and the commissioner leaves automatic seeding in place.

The league has fourteen regular-season weeks, three divisions of four, and seven playoff places. Each division champion qualifies. The four remaining places go by winning percentage among non-champions. Pro Schemin’ uses head-to-head record to break equal records when the tied clubs have met equally often. The standings entering Week 12, the three remaining schedules and division membership were checked against ESPN. [Final Week 11 and Week 12 fixtures](W11_POST_MNF_FLAIM_ESPN_SOURCE_2026-11-24.json) · [Weeks 13–14](W11_WEEK13_14_REMAINING_ESPN_SCHEDULE_2026-11-24.json) · [Pinned ESPN gateway snapshot with settings, division IDs and Weeks 2–4 results](https://github.com/jakekaloper-hub/schemin-26/blob/dc0e42830543ba10ad524c979de48cafe6d9a66e/data/snapshots/1417621/latest.json) · [ESPN's H2H playoff seeding rules](https://support.espn.com/hc/en-us/articles/47190901074708-H2H-Points-League-Playoff-Seeding-Tiebreakers)

## Five possible finishes where record settles the field

Each row represents a separate future for all eighteen remaining games. Every team outside the seven listed in that row misses. The same seven qualify under every possible ordering of clubs tied for a division title in that example. No wild-card boundary falls on equal records. The verifier lists the six hypothetical winners each week and replays the choices against the official schedule. [Run the examples](verify_week11_qualification_witnesses.py)

| Example | Seven qualifiers, listed without seed order |
|---|---|
| A | Slob on my Dobb, Three Dreaded Snake, The Chili Cheesers, His Majesty’s Blood, El Niño, Seven Deadly Chins, Dr. Duckhook |
| B | ObiWan Jacoby, Red Leopards, Slob on my Dobb, D0nkey K0ng, His Majesty’s Blood, El Niño, Dr. Duckhook |
| C | Red Leopards, Slob on my Dobb, D0nkey K0ng, Three Dreaded Snake, The Chili Cheesers, El Niño, Seven Deadly Chins |
| D | Red Leopards, D0nkey K0ng, Three Dreaded Snake, The Chili Cheesers, His Majesty’s Blood, Seven Deadly Chins, Dr. Duckhook |
| E | Slob on my Dobb, The LLC, Three Dreaded Snake, The Chili Cheesers, His Majesty’s Blood, Seven Deadly Chins, Dr. Duckhook |

In example B, ObiWan Jacoby beats D0nkey K0ng, Mud Dogs and Three Dreaded Snake to reach 7–7. Seven Deadly Chins makes the field in A, C, D and E. Even current No. 1 His Majesty’s Blood can miss, as example C shows.

## How 3–8 Mud Dogs can still win Burgers

These six scores are hypothetical. The other two divisions cannot change this division-title example.

| Week | First Burgers result | Second Burgers result |
|---|---|---|
| 12 | ObiWan Jacoby 120–100 D0nkey K0ng | Mud Dogs 200–100 Three Dreaded Snake |
| 13 | Mud Dogs 200–100 ObiWan Jacoby | Three Dreaded Snake 120–100 D0nkey K0ng |
| 14 | ObiWan Jacoby 120–100 Three Dreaded Snake | Mud Dogs 200–100 D0nkey K0ng |

All four teams finish 6–8. Every pair has played twice. Counting the actual Weeks 2–4 division games and these six example games, Mud Dogs and ObiWan Jacoby would each go 4–2 against the tied field. D0nkey K0ng and Three Dreaded Snake would each go 2–4. Mud Dogs beat ObiWan Jacoby in both meetings in this example, and also finish first in division points for at **1,932.61**. D0nkey K0ng would finish at 1,841.57, ObiWan at 1,808.30 and Three Dreaded Snake at 1,725.20. Both head-to-head between the co-leaders and the points-for comparison favor Mud Dogs.

TheFFHub estimated Mud Dogs at 0.26% after Week 11. Its odds describe likelihood. The six games above show how qualification remains possible regardless of the simulated rate. These conclusions cover automatic seeding under the verified rules. The independent Data Release Steward and Umpire own publication. [Captured model probabilities](W11_FFHUB_POST_WEEK11_ODDS_2026-11-24.json)
