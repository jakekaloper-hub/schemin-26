import importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ux=load("cp9_ux",Path("member-gateway/member_experience.py"))
truth=load("cp9_truth",Path("member-gateway/truth_plane_adapter.py"))
flaim=load("cp9_flaim",Path("data-gateway/flaim_adapter.py"))
receipt=json.loads((ROOT/"data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json").read_text())
def packet():
 return truth.from_normalized_data_gateway(flaim.normalize_capture(receipt))

def test_pitts_discovers_jobs_without_director_or_architecture_knowledge(tmp_path):
 x=ux.MemberExperience(tmp_path/"runs.json")
 jobs=x.available_jobs("pitts-chatgpt")
 names={j["capability"] for j in jobs}
 assert "pittys_book.inputs" in names
 assert not any("director" in n or "bullpen" in n or "mercer" in n for n in names)

def test_pitts_can_request_book_inputs_and_get_understandable_stale_state(tmp_path):
 x=ux.MemberExperience(tmp_path/"runs.json")
 out=x.run_book_inputs(client_id="pitts-chatgpt",season=2026,week=5,truth_packet=packet())
 assert out["status"]=="PASSED"
 assert out["freshness"]["stale"] is True
 assert "stale" in out["message"].lower()
 assert out["authority_status"]=="BULLPEN_ROUTED"

def test_duplicate_book_request_is_not_reexecuted(tmp_path):
 x=ux.MemberExperience(tmp_path/"runs.json")
 one=x.run_book_inputs(client_id="pitts-chatgpt",season=2026,week=5,truth_packet=packet())
 two=x.run_book_inputs(client_id="pitts-chatgpt",season=2026,week=5,truth_packet=packet())
 assert one["request_id"]==two["request_id"]
 assert two["duplicate"] is True

def test_no_truth_is_clear_block_not_fabrication(tmp_path):
 x=ux.MemberExperience(tmp_path/"runs.json")
 out=x.run_book_inputs(client_id="pitts-chatgpt",season=2026,week=5,truth_packet=None)
 assert out["status"]=="BLOCKED"
 assert "no Book inputs were fabricated" in out["message"]

def test_pitts_cannot_discover_mutation_or_private_tools(tmp_path):
 x=ux.MemberExperience(tmp_path/"runs.json")
 jobs=x.available_jobs("pitts-chatgpt")
 labels=" ".join(j["label"]+" "+j["capability"] for j in jobs).lower()
 assert "write" not in labels and "mercer" not in labels and "director" not in labels
