from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class BookTime(str, Enum):
    PRESEASON="PRESEASON"; W1="W1"; W2="W2"; W3="W3"

ORDER={BookTime.PRESEASON:0,BookTime.W1:1,BookTime.W2:2,BookTime.W3:3}

@dataclass(frozen=True)
class Fact:
    fact_id: str
    became_true_at: BookTime
    knowable_at: BookTime
    retroactive_use_prohibited: bool=True

def eligible(fact: Fact, target: BookTime) -> bool:
    if ORDER[fact.knowable_at] > ORDER[target]:
        return False
    if fact.retroactive_use_prohibited and ORDER[fact.became_true_at] > ORDER[target]:
        return False
    return True

def require_eligible(fact: Fact, target: BookTime) -> None:
    if not eligible(fact,target):
        raise ValueError(f"TEMPORAL_VIOLATION:{fact.fact_id}:{target.value}")

def classify_sequence(*, evidence_supports_material_change: bool, interpretation_only: bool=False) -> str:
    if interpretation_only:
        return "INTERPRETATION"
    if evidence_supports_material_change:
        return "SUPPORTED_CAUSATION"
    return "FACTUAL_SEQUENCE"
