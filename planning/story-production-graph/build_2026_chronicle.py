#!/usr/bin/env python3
"""Character Director + Librarian: derived 2026 Chronicle across memo Weeks 1-9."""
from __future__ import annotations
import json, sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from adapt_2026_memo_season import compile_season
from chronicle_views import character_timelines, relationship_histories, place_memory, artifact_custody

def build():
    season=compile_season()
    events=season["events"]; scenes=season["scenes"]
    cutoff="2026-W09-repo-scope"
    return {
      "schema_version":"1.0",
      "season":2026,
      "source_weeks":[1,2,3,4,5,6,7,8,9],
      "event_weeks":sorted(set(e["league_time"]["week"] for e in events)),
      "character_timelines":character_timelines(events,cutoff),
      "relationship_histories":relationship_histories(events,cutoff),
      "place_memory":place_memory(events,scenes,cutoff),
      "artifact_custody":artifact_custody(events,cutoff),
      "authority":"DERIVED_READ_MODEL_ONLY",
      "notes":[
        "Weeks 1-2 remain issue-level publication nodes because exact binaries are not in GitHub.",
        "Character timelines currently draw matchup events from Weeks 3-9 only.",
        "Deleting/rebuilding this output cannot alter source canon."
      ]
    }

if __name__=="__main__":
    print(json.dumps(build(),indent=2,ensure_ascii=False))
