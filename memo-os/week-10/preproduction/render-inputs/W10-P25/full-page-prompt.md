One individual 1080×1920 grayscale integrated illustrated memo folio: complete supplied headline, department heading, deck, narration and source-qualified lettering in the exact intended final composition. No annotation cards, miniature scene summaries, detached document exports, or generated six-up grids.

Image authority is explicit: current_appearance_override controls current face and costume; approved_lineup_crop supplies canonical identity; published_memo_precedent supplies only its stated layout/geometry application and never replaces current character anatomy or current scores. Follow the actual published memo references: one continuous cinematic world, prominent editorial hierarchy, slender ornament where appropriate, full narrative typography inside deliberate atmospheric reading space, and scene-led differences between departments. Grayscale affects palette, not the amount of copy, character identity, panel proportions, camera or final-page geometry.

PAGE W10-P25 · READING POSITION 26

IDENTITY INPUTS
[]

SCENE AND CONTINUITY
{
  "camera_and_composition": "Wide view along an inhabited open loggia, equipment hooks and the road in depth; seven short needs are lettered in the continuous atmosphere.",
  "foreground": "Packed traveling equipment and empty hooks with team emblems.",
  "midground": "Covered roster station under old columns; it is ordinary logistics, not a new infirmary.",
  "background": "Cold open route with steady lamps and sheltered working people.",
  "image_tells": "Wide view along an inhabited open loggia, equipment hooks and the road in depth; seven short needs are lettered in the continuous atmosphere. Packed traveling equipment and empty hooks with team emblems. Covered roster station under old columns; it is ordinary logistics, not a new infirmary. Cold open route with steady lamps and sheltered working people.",
  "encounter": {
    "venue_id": "LOC-LEAGUE-CHAMBER",
    "set_id": "SET-W10-CHAMBER-RESERVE-LOGGIA",
    "venue_type": "Editorial department within existing Atlas parent; local staging proposed",
    "division_context": "League-wide; divisions are overlays",
    "route_required": false,
    "world_state_in": "Existing place with selective wear and maintenance",
    "persistent_landmarks": [
      "League Chamber outer loggia"
    ],
    "provisional_location": true,
    "formal_atlas_promotion": false
  },
  "continuity_in": [
    "LOC-LEAGUE-CHAMBER",
    "Existing Commonwealth use and inherited approved weather state"
  ],
  "continuity_out": [
    "Seven positions across six teams; Seven Deadly Chins needs both specialist slots. Current starters are not presumed to be the submitted Week11 lineup."
  ],
  "forbidden_mutations": [
    "New medical diagnosis from a fantasy slot flag",
    "Guaranteed return or future starter without confirmation",
    "Final Week10 record or clinch from live score",
    "New permanent location or belt transfer"
  ]
}

EXACT FULL PUBLICATION COPY
{
  "headline": "THE NEXT STARTING SHEET",
  "deck": "Week 11 • Seven uncovered required positions",
  "body": "Six NFL clubs are on bye. On the current Schemin rosters, six teams lack an owned replacement at seven required positions. These are planning needs, not completed moves. The separate reserve ledger still records fantasy IR occupancy without turning that placement into a diagnosis.",
  "callouts": [],
  "rows": [
    {
      "team": "ObiWan Jacoby",
      "need": "D/ST"
    },
    {
      "team": "Slob on my Dobb",
      "need": "TE"
    },
    {
      "team": "The Chili Cheesers",
      "need": "K"
    },
    {
      "team": "El Niño",
      "need": "TE"
    },
    {
      "team": "Mud Dogs",
      "need": "D/ST"
    },
    {
      "team": "Seven Deadly Chins",
      "need": "D/ST + K"
    }
  ],
  "department_heading": "RESERVE WATCH"
}

FACT POLICY
{
  "official_winner_decided": false,
  "source_capture_scope": "CURRENT_PROVISIONAL_PRE_MNF",
  "unresolved_numerals": "BLANK_RESERVED_FIELDS",
  "source_backed_current_values": "May be shown only with CURRENT / PROVISIONAL qualifier; never FINAL",
  "result_dependent_art": "Forecast branch only until provider winners decided; persistent common beats retained.",
  "refresh_fields": [
    {
      "selector": "/pass3/readiness",
      "artifact": "facts.json",
      "policy": "Rebind this source before final factual acceptance; exact qualifiers are part of the fact.",
      "snapshot_sha256": "4b296b6f793ffaf311dde11447998c1f5fca7ddb003318123d68cb56a0913cdc",
      "snapshot_value_stored_in": "facts.json/pass3/readiness"
    },
    {
      "selector": "/derived/reserve_occupancy",
      "artifact": "facts.json",
      "policy": "Rebind this source before final factual acceptance; exact qualifiers are part of the fact.",
      "snapshot_value": {
        "Bench": 84,
        "IR": 20,
        "teams_with_IR": 11
      }
    },
    {
      "selector": "/pass3/available_slots",
      "artifact": "facts.json",
      "policy": "Rebind this source before final factual acceptance; exact qualifiers are part of the fact.",
      "snapshot_value": {
        "fact_id": "W11-AVAILABLE-SLOTS",
        "artifact": "available-slots-pass3.json",
        "scope": "Current read-only non-bye coverage pool; no claims or bids placed",
        "data": {
          "schema": "schemin.week11.required-slot-availability.v1",
          "captured_at_utc": "2026-11-16T18:24:59Z",
          "league_id": "1417621",
          "season": 2026,
          "purpose": "Read-only memo-planning availability shortlist for seven uncovered required Week11 slots; no acquisition or allocation recommendation, bid or roster change.",
          "required_slots": [
            {
              "team": "Slob on my Dobb",
              "team_id": 3,
              "position": "TE"
            },
            {
              "team": "El Niño",
              "team_id": 9,
              "position": "TE"
            },
            {
              "team": "The Chili Cheesers",
              "team_id": 7,
              "position": "K"
            },
            {
              "team": "Seven Deadly Chins",
              "team_id": 11,
              "position": "K"
            },
            {
              "team": "Seven Deadly Chins",
              "team_id": 11,
              "position": "D/ST"
            },
            {
              "team": "ObiWan Jacoby",
              "team_id": 1,
              "position": "D/ST"
            },
            {
              "team": "Mud Dogs",
              "team_id": 10,
              "position": "D/ST"
            }
          ],
          "excluded_week11_bye_clubs": [
            "ATL",
            "CLE",
            "GB",
            "LAR",
            "NE",
            "SEA"
          ],
          "coverage": {
            "TE": 15,
            "K": 15,
            "DST": 14,
            "inventory_complete_claim": false,
            "ordering": "Provider platform_rostered_rate_desc; this is not a Week11 projection ranking."
          },
          "shortlist": {
            "TE": [
              {
                "id": "3117256",
                "name": "Dalton Schultz",
                "team": "HOU",
                "position": "TE",
                "injuryStatus": "Active",
                "acquisitionState": "waivers",
                "waiverClearsAt": "2026-11-18T08:00:00.000Z",
                "pointsPerGame": 8.94,
                "seasonPoints": 80.5
              },
              {
                "id": "4430802",
                "name": "Darnell Washington",
                "team": "PIT",
                "position": "TE",
                "injuryStatus": "Active",
                "acquisitionState": "waivers",
                "waiverClearsAt": "2026-11-18T08:00:00.000Z",
                "pointsPerGame": 7.1,
                "seasonPoints": 63.9
              },
              {
                "id": "4808766",
                "name": "Mason Taylor",
                "team": "NYJ",
                "position": "TE",
                "injuryStatus": "Active",
                "acquisitionState": "waivers",
                "waiverClearsAt": "2026-11-18T08:00:00.000Z",
                "pointsPerGame": 6.59,
                "seasonPoints": 52.7
              },
              {
                "id": "4243331",
                "name": "Cade Otton",
                "team": "TB",
                "position": "TE",
                "injuryStatus": "Active",
                "acquisitionState": "free_agent",
                "waiverClearsAt": null,
                "pointsPerGame": 4.9,
                "seasonPoints": 44.1
              }
            ],
            "K": [
              {
                "id": "17372",
                "name": "Chris Boswell",
                "team": "PIT",
                "position": "K",
                "injuryStatus": "Active",
                "acquisitionState": "waivers",
                "waiverClearsAt": "2026-11-18T08:00:00.000Z",
                "pointsPerGame": 9.67,
                "seasonPoints": 87
              },
              {
                "id": "4689936",
                "name": "Jake Bates",
                "team": "DET",
                "position": "K",
                "injuryStatus": "Active",
                "acquisitionState": "waivers",
                "waiverClearsAt": "2026-11-18T08:00:00.000Z",
                "pointsPerGame": 9.44,
                "seasonPoints": 85
              },
              {
                "id": "4362081",
                "name": "Cameron Dicker",
                "team": "LAC",
                "position": "K",
                "injuryStatus": "Active",
                "acquisitionState": "free_agent",
                "waiverClearsAt": null,
                "pointsPerGame": 7.75,
                "seasonPoints": 62
              },
              {
                "id": "3150744",
                "name": "Chase McLaughlin",
                "team": "TB",
                "position": "K",
                "injuryStatus": "Active",
                "acquisitionState": "free_agent",
                "waiverClearsAt": null,
                "pointsPerGame": 11,
                "seasonPoints": 99
              }
            ],
            "DST": [
              {
                "id": "-16003",
                "name": "Bears D/ST",
                "team": "CHI",
                "position": "D/ST",
                "injuryStatus": null,
                "acquisitionState": "free_agent",
                "waiverClearsAt": null,
                "pointsPerGame": 11.52,
                "seasonPoints": 103.7
              },
              {
                "id": "-16004",
                "name": "Bengals D/ST",
                "team": "CIN",
                "position": "D/ST",
                "injuryStatus": null,
                "acquisitionState": "waivers",
                "waiverClearsAt": "2026-11-18T08:00:00.000Z",
                "pointsPerGame": 10.56,
                "seasonPoints": 95
              },
              {
                "id": "-16028",
                "name": "Commanders D/ST",
                "team": "WSH",
                "position": "D/ST",
                "injuryStatus": null,
                "acquisitionState": "waivers",
                "waiverClearsAt": "2026-11-18T08:00:00.000Z",
                "pointsPerGame": 8.4,
                "seasonPoints": 75.6
              },
              {
                "id": "-16021",
                "name": "Eagles D/ST",
                "team": "PHI",
                "position": "D/ST",
                "injuryStatus": null,
                "acquisitionState": "free_agent",
                "waiverClearsAt": null,
                "pointsPerGame": 5.39,
                "seasonPoints": 48.5
              }
            ]
          },
          "excluded_returned_entries": {
            "TE": [
              {
                "id": "4242355",
                "name": "Jake Ferguson",
                "team": "DAL",
                "reasons": [
                  "provider injury designation Out"
                ]
              },
              {
                "id": "4576297",
                "name": "AJ Barner",
                "team": "SEA",
                "reasons": [
                  "Week11 bye"
                ]
              },
              {
                "id": "4831959",
                "name": "Eli Raridon",
                "team": "NE",
                "reasons": [
                  "Week11 bye"
                ]
              },
              {
                "id": "4242557",
                "name": "Colby Parkinson",
                "team": "LAR",
                "reasons": [
                  "Week11 bye"
                ]
              },
              {
                "id": "3123076",
                "name": "David Njoku",
                "team": "LAC",
                "reasons": [
                  "provider injury designation IR"
                ]
              }
            ],
            "K": [
              {
                "id": "4697745",
                "name": "Tyler Loop",
                "team": "BAL",
                "reasons": [
                  "provider injury designation IR"
                ]
              },
              {
                "id": "4574716",
                "name": "Harrison Mevis",
                "team": null,
                "reasons": [
                  "provider club not reported"
                ]
              },
              {
                "id": "4869461",
                "name": "Trey Smack",
                "team": "GB",
                "reasons": [
                  "Week11 bye"
                ]
              },
              {
                "id": "10621",
                "name": "Nick Folk",
                "team": null,
                "reasons": [
                  "provider club not reported"
                ]
              }
            ],
            "DST": [
              {
                "id": "-16009",
                "name": "Packers D/ST",
                "team": "GB",
                "reasons": [
                  "Week11 bye"
                ]
              },
              {
                "id": "-16017",
                "name": "Patriots D/ST",
                "team": "NE",
                "reasons": [
                  "Week11 bye"
                ]
              },
              {
                "id": "-16001",
                "name": "Falcons D/ST",
                "team": "ATL",
                "reasons": [
                  "Week11 bye"
                ]
              }
            ]
          },
          "availability_limits": [
            "acquisitionState is the current provider state, not a promise a manager can complete an acquisition or win a claim.",
            "Provider waiver clearance Nov18 at08:00UTC corresponds to03:00EST.",
            "The12 selected candidates are absent from all224 current roster entries at the checkpoint.",
            "Active is a provider designation that can lag news; Week11 medical/practice reports and real-team roles require rechecking.",
            "D/ST rows carry no individual injury designation; defensive personnel and opponent matchup were not assessed in this bounded check.",
            "No weekly projections were returned; pointsPerGame is a league-scored season average, not expected Week11 points.",
            "Free-agent pools change; no assignment of the same player to multiple teams is implied."
          ],
          "source_file": "available-slots-receipts-pass3.json",
          "bye_source": {
            "url": "https://www.nfl.com/schedules/2026/by-week/week-11",
            "support": "ATL,CLE,GB,LAR,NE,SEA Week11 byes",
            "sports_news_source_id": "S16",
            "sports_news_file": "w10_pass3_sports_news.json"
          }
        }
      }
    }
  ]
}

REFERENCE IMAGES
[
  {
    "repo_path": "memo-os/week-10/production-evidence/recovery-20261116/precedent-w09-p26.jpg",
    "sha256": "d70b9cf4579ff1a6151bbe8afb79bd47a3dbec5a65fb8b13afc0ef17513d2e84",
    "bytes": 522212,
    "dimensions": [
      960,
      1707
    ],
    "media_type": "image/jpeg",
    "role": "published_memo_precedent",
    "decoded_in_preflight": true,
    "application": "Editorial hierarchy, character treatment and visual integration; do not transplant an unrelated venue or old sports values."
  }
]
