"""Read-only, fail-closed Week 7 P005 pre-render eligibility diagnostic."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from canon.characters.runtime.renderer_capabilities import negotiate

ASSETS = {
    "CHAR-PHILLIP-PITTS": "0c6d6ee2cdd1c1f77c58cda2e5e25c0b482943279e433b16e14aa1277e201a65",
    "CHAR-ZACH-WILSON": "c0ac1b3314c32b8e85c82045268c21a0d9c52525c2fd8ad869aaff449b4cf36a",
}
SOURCE_FILES = [
    "WEEK_7_FOUNDER_34_DECISIONS_AND_CREATIVE_INTAKE_2026_10_27.md",
    "WEEK_7_SIX_MATCHUP_THREE_PHASE_MANUSCRIPTS_REVIEW_2026_10_27.md",
    "WEEK_7_FOUNDER_SIX_VENUE_SCENE_AUTHORIZATION_2026_10_27.md",
    "WEEK_7_MIRACLE_PUTT_CINEMATIC_THREE_FOLIO_PILOT_2026_10_27.md",
]
week = ROOT / "memo-os/week-7"
def assess():
    sources = {name: (week / name).is_file() for name in SOURCE_FILES}
    images = {}
    for cid, expected in ASSETS.items():
        p = ROOT / "canon/characters/assets/lineups/2026-10-18-crops" / (cid + ".png")
        images[cid] = p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == expected
    capabilities = json.loads((ROOT / "canon/characters/renderer_capabilities_v1.json").read_text())
    negotiation = negotiate("CURRENT_CHATGPT_IMAGE_RENDERER", capabilities["routes"], len(ASSETS))
    ready = all(sources.values()) and all(images.values()) and negotiation["state"] == "CAPABILITY_VERIFIED"
    return {
        "pilot": "W07-P005-MIRACLE-PUTT",
        "source_files": sources,
        "source_sha256_pass": images,
        "renderer_negotiation": negotiation,
        "ready_for_render": ready,
        "verdict": "ELIGIBLE_FOR_NEXT_PROVIDER_RECEIPT_REVIEW" if ready else "HOLD",
        "independent_umpire_accepted": False,
        "note": "Even a positive capability negotiation is not proof of an actual provider attachment, render or final QA.",
    }

if __name__ == "__main__":
    print(json.dumps(assess(), indent=2))
    sys.exit(0 if assess()["ready_for_render"] else 2)
