from __future__ import annotations
from typing import List, Mapping

def classify_candidates(
    probability: Mapping[str, dict],
    exact: Mapping[str, dict],
    leverage: Mapping[str, dict] | None = None,
    max_notes: int = 3,
    high_leverage_pp: float = 25.0,
    extreme_leverage_pp: float = 40.0,
) -> List[dict]:
    leverage = leverage or {}
    candidates: List[dict] = []
    for tid, e in exact.items():
        if e["status"] in {"CLINCHED", "ELIMINATED"}:
            candidates.append({
                "team_id": tid,
                "class": "EXACT",
                "priority": 100,
                "kind": e["status"],
                "reason": e.get("proof"),
            })
    for tid, l in leverage.items():
        delta = float(l.get("leverage_delta_pp", 0.0))
        if delta >= high_leverage_pp:
            candidates.append({
                "team_id": tid,
                "class": "PROBABILISTIC",
                "priority": 80 if delta >= extreme_leverage_pp else 60,
                "kind": "EXTREME_LEVERAGE" if delta >= extreme_leverage_pp else "HIGH_LEVERAGE",
                "leverage_delta_pp": round(delta),
                "conditional_win_probability": round(100*l["conditional_win_probability"]),
                "conditional_loss_probability": round(100*l["conditional_loss_probability"]),
            })
    candidates.sort(key=lambda x: x["priority"], reverse=True)
    return candidates[:max_notes]

def validate_wording(candidate: Mapping[str, object], wording_class: str) -> None:
    actual = candidate.get("class")
    if actual != wording_class:
        raise ValueError(f"wording class mismatch: candidate={actual} requested={wording_class}")
