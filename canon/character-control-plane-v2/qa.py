from models import QACheck
def decide(checks:list[QACheck],reference_available:bool):
    if not reference_available: return {"status":"HUMAN_REVIEW_REQUIRED","reason":"MISSING_REFERENCE","checks":checks}
    failures=[c for c in checks if c.expected!=c.observed]
    if any(c.severity in ("FATAL","IMPORTANT") for c in failures): return {"status":"REGENERATE","failures":failures}
    return {"status":"PASS","failures":failures}
