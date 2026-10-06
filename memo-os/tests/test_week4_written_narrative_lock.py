from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"memo-os/week-4/publication-readiness"
MANUSCRIPT=BASE/"WEEK_04_FINAL_WRITTEN_MANUSCRIPT.md"
PACKET=BASE/"WEEK_04_OFFICIAL_MANUAL_PRODUCTION_PACKET.md"
AUDIT=BASE/"WEEK_04_WRITING_RECOVERY_AUDIT_2026-10-06.md"

def text(p): return p.read_text()

def test_final_manuscript_has_exact_27_pages():
    s=text(MANUSCRIPT)
    nums=[int(x) for x in re.findall(r"^## PAGE (\d+)",s,re.M)]
    assert nums==list(range(1,28))

def test_packet_binds_final_manuscript_as_reader_facing_authority():
    s=text(PACKET)
    assert "WEEK_04_FINAL_WRITTEN_MANUSCRIPT.md" in s
    assert "manuscript controls" in s
    assert "Silence is permitted" in s

def test_page2_is_specific_and_short():
    s=text(MANUSCRIPT)
    p2=s.split("## PAGE 2",1)[1].split("## PAGE 3",1)[0]
    assert "The last unbeaten owner in Schemin' spent Week 4 looking downhill." in p2
    assert "D0nkey K0ng" in p2
    assert "ObiWan Jacoby" in p2
    assert "Whipple's lawn furniture had joined the weather." in p2
    assert "Nobody traveled far." in p2
    assert len(re.findall(r"\b[\w’'-]+\b",p2)) <= 120

def test_banned_generic_openers_are_absent():
    s=text(MANUSCRIPT).lower()
    banned=["not just","this wasn't just","the stakes couldn't be higher","only time will tell","the league took notice","the battle was far from over"]
    for phrase in banned:
        assert phrase not in s

def test_page3_is_data_only():
    s=text(MANUSCRIPT)
    p3=s.split("## PAGE 3",1)[1].split("# GAME OF THE WEEK",1)[0]
    assert "No narrative body copy." in p3

def test_copy_does_not_overexplain_high_ground():
    s=text(MANUSCRIPT)
    p6=s.split("## PAGE 6",1)[1].split("## PAGE 7",1)[0]
    assert len(re.findall(r"\b[\w’'-]+\b",p6)) <= 25

def test_audit_declares_every_surviving_word_has_a_job():
    assert "EVERY SURVIVING WORD HAS A JOB." in text(AUDIT)
