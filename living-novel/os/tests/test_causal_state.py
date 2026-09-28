from living_novel.os.engine.causal_state import BookTime, Fact, eligible, classify_sequence

def test_achane_keeper_preseason_is_legal_early():
    f=Fact("HMB-ACHANE-R15",BookTime.PRESEASON,BookTime.PRESEASON)
    assert eligible(f,BookTime.PRESEASON)
    assert eligible(f,BookTime.W1)
    assert eligible(f,BookTime.W2)
    assert eligible(f,BookTime.W3)

def test_week3_injury_cannot_leak_backward():
    f=Fact("HMB-ACHANE-W3-INJURY",BookTime.W3,BookTime.W3)
    assert not eligible(f,BookTime.PRESEASON)
    assert not eligible(f,BookTime.W1)
    assert not eligible(f,BookTime.W2)
    assert eligible(f,BookTime.W3)

def test_sequence_not_silently_causation():
    assert classify_sequence(evidence_supports_material_change=False)=="FACTUAL_SEQUENCE"
    assert classify_sequence(evidence_supports_material_change=True)=="SUPPORTED_CAUSATION"
    assert classify_sequence(evidence_supports_material_change=False,interpretation_only=True)=="INTERPRETATION"
