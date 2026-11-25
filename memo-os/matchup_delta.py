"""Pure provisional matchup delta planning; consumes normalized weekly_matchup_receipt output.
No writes, Fact Lock, rendering, source acceptance or release authority.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation


def plan(previous, current, dependencies):
    """Return affected matchup and artifact IDs; retain all inputs unchanged.

    Dependencies map artifact IDs to fixture keys (e.g. W12-H05-A01).
    Scope-independent creative artifacts use an empty dependency list.
    """
    def timestamp(meta):
        value = datetime.fromisoformat(meta["captured_at"].replace("Z", "+00:00"))
        if value.tzinfo is None:
            raise ValueError("timezone required")
        return value

    def score(value):
        if value is None or isinstance(value, bool):
            raise ValueError("invalid score")
        try:
            result = Decimal(str(value))
        except InvalidOperation as exc:
            raise ValueError("invalid score") from exc
        if not result.is_finite():
            raise ValueError("invalid score")
        return result

    def rows(receipt):
        meta = receipt["meta"]
        if (meta["provider"], meta["platform"], meta["league_id"], meta["season_year"]) != ("flaim", "espn", 1417621, 2026):
            raise ValueError("provider or scope mismatch")
        week = meta["week"]
        if type(week) is not int or not 1 <= week <= 18:
            raise ValueError("invalid week")
        if meta.get("authority") != "PROVIDER_OBSERVATION_NOT_FACT_LOCK":
            raise ValueError("expected provisional observation")
        result, teams = {}, []
        for row in receipt["matchups"]:
            h, a = row["home"], row["away"]
            ids = (h["team_id"], a["team_id"])
            if any(type(x) is not int for x in ids):
                raise ValueError("invalid team")
            teams.extend(ids)
            key = f"W{week:02d}-H{ids[0]:02d}-A{ids[1]:02d}"
            winner = row["winner"]
            if winner not in ("HOME", "AWAY", "TIE", "UNDECIDED"):
                raise ValueError("invalid winner")
            hp, ap = score(h["points"]), score(a["points"])
            ht, at = score(h["total_points"]), score(a["total_points"])
            if winner != "UNDECIDED":
                if (hp, ap) != (ht, at):
                    raise ValueError("final/current mismatch")
                if winner == "HOME" and hp <= ap or winner == "AWAY" and ap <= hp or winner == "TIE" and hp != ap:
                    raise ValueError("winner conflicts with scores; manual review required")
            result[key] = (winner, hp, ap, ht, at)
        if len(result) != 6 or sorted(teams) != list(range(1, 13)):
            raise ValueError("six distinct fixtures and twelve teams required")
        return result

    before, after = rows(previous), rows(current)
    if before.keys() != after.keys():
        raise ValueError("fixture mismatch")
    old_time, new_time = timestamp(previous["meta"]), timestamp(current["meta"])
    if new_time < old_time or (new_time == old_time and before != after):
        raise ValueError("stale or conflicting observation")
    if not isinstance(dependencies, dict) or any(not isinstance(v, list) or any(k not in after for k in v) for v in dependencies.values()):
        raise ValueError("unknown dependency")
    changed = sorted(key for key in after if before[key] != after[key])
    # A decided result is an observation only. Even a correction or tie is routed for review.
    transitions = {}
    for key in changed:
        old, new = before[key][0], after[key][0]
        if old != "UNDECIDED":
            transitions[key] = "REVIEW_PREVIOUS_FINAL_CHANGE"
        elif new == "TIE":
            transitions[key] = "TIEBREAK_REVIEW_REQUIRED"
        elif new in ("HOME", "AWAY"):
            transitions[key] = "PROVISIONAL_FINAL_BRANCH_REVIEW"
        else:
            transitions[key] = "LIVE_UPDATE_ONLY"
    affected = sorted(a for a, keys in dependencies.items() if set(keys).intersection(changed))
    return {
        "changed_matchups": changed, "transitions": transitions,
        "review_artifacts": affected,
        "preserve_artifacts": sorted(set(dependencies) - set(affected)),
        "provider_final_count": sum(row[0] != "UNDECIDED" for row in after.values()),
        "source_accepted": False, "fact_lock": False,
        "render_authorized": False, "release_approved": False,
        "writes_authoritative_files": False,
    }
