"""Synchronize the accepted Week 10 playoff supplement into three existing folios.

The copy plan is an editorial input, not a generator. This operation preserves
all scenes, references, reference-inspection receipts and unselected requests.
It may be rerun after the existing full-folio reconciler without losing the
harvest or the user's current PNG-production pause.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

P = Path(__file__).resolve().parent
SELECTED = ("W10-P28", "W10-P30", "W10-P31")
GATE = {
    "status": "PREPRODUCTION_REVIEW_PNG_PAUSED",
    "authority": "Latest user direction: finalize backend and frontend before PNG production; Bullpen leads the existing Week 10 workflow.",
    "backend_source_ready": True,
    "image_generation_authorized": False,
    "image_generation_executed": False,
    "publication_approved": False,
    "next_stage": "Bullpen-led review of the existing 34-folio production package; PNG execution remains paused.",
}


def read(root, name):
    return json.loads((root / name).read_text())


def write(root, name, value):
    (root / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot_digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def compact_binding(field):
    return {k: deepcopy(v) for k, v in field.items() if k != "snapshot_value"} | {
        "snapshot_sha256": snapshot_digest(field.get("snapshot_value")),
        "value_location": field.get("artifact", "facts.json") + "#" + field["selector"],
        "source_scope": "See source field scope; exact visible values are already in publication_copy",
    }


def replace_prompt_section(prompt, heading, next_heading, value):
    before, rest = prompt.split("\n\n" + heading + "\n", 1)
    _, after = rest.split("\n\n" + next_heading + "\n", 1)
    return (before + "\n\n" + heading + "\n" +
            json.dumps(value, ensure_ascii=False, indent=2) +
            "\n\n" + next_heading + "\n" + after)


def replace_markdown_page(text, page_id, replacement):
    """Replace one existing section; preserve every other section verbatim."""
    pattern = re.compile(r"^## (?:\d+ · )?" + re.escape(page_id) +
                         r" — [^\n]*\n.*?(?=^## |\Z)", re.M | re.S)
    updated, count = pattern.subn(lambda _: replacement.rstrip() + "\n\n", text)
    if count != 1:
        raise ValueError(f"Expected one existing Markdown section for {page_id}; found {count}")
    return updated


def copy_section(page):
    c = page["draft_copy"]
    lines = ["## " + page["page_id"] + " — " + page["title"], "",
             c.get("department_heading", ""), "", c.get("deck", ""), "", c["body"], ""]
    for callout in c.get("callouts", []):
        if isinstance(callout, dict) and callout.get("label") and callout.get("value") not in (None, ""):
            lines += ["**" + str(callout["label"]) + "** — " + str(callout["value"]), ""]
        else:
            lines += ["```json", json.dumps(callout, ensure_ascii=False, indent=2), "```", ""]
    if c.get("rows"):
        lines += ["```json", json.dumps(c["rows"], ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)


def synchronize(root=P):
    root = Path(root)
    harvest = read(root, "playoff-harvest.json")
    plan = read(root, "playoff-harvest-copy.json")
    if (harvest["league_id"], harvest["season"], harvest["through_week"]) != (1417621, 2026, 10):
        raise ValueError("The playoff harvest is not the Schemin '26 Week 10 snapshot")
    if harvest["canonical_fact_bundle_sha256"] != digest(root / "facts.json"):
        raise ValueError("The finalized source changed; reconcile the harvest before using it")
    if tuple(plan["pages"]) != SELECTED:
        raise ValueError("Only the three reviewed folios may receive this supplement")

    issue = read(root, "issue-previs.json")
    briefs = read(root, "illustrated-page-briefs.json")
    folios = read(root, "storyboard-folio-plan-pass5.json")
    cards = read(root, "storycards.json")
    directors = read(root, "director-sequences.json")
    manifest = read(root, "render-inputs/manifest.json")
    pages = {p["page_id"]: p for p in issue["pages"]}
    bs = {p["page_id"]: p for p in briefs["pages"]}
    fs = {p["page_id"]: p for p in folios["folios"]}
    ds = {p["page_id"]: p for p in directors["pages"]}
    ms = {p["page_id"]: p for p in manifest["pages"]}
    markdown = {n: (root / n).read_text() for n in
                ("issue-draft.md", "illustrated-page-briefs.md", "storyboard-folio-plan-pass5.md")}
    source_hash = digest(root / "playoff-harvest.json")

    for pid in SELECTED:
        page, brief, folio = pages[pid], bs[pid], fs[pid]
        request = read(root, "render-inputs/" + pid + "/request.json")
        copy = deepcopy(plan["pages"][pid]["publication_copy"])
        claims = harvest["page_claims"][pid]
        if claims != plan["pages"][pid]["claim_ids"]:
            raise ValueError("Editorial/source claim mismatch on " + pid)
        if len(copy["body"].split()) > page["copy_budget"]["body_max_words"]:
            raise ValueError("Body exceeds the existing page budget: " + pid)
        if copy["rows"] != page["draft_copy"]["rows"]:
            raise ValueError("This harvest cannot alter the existing fixtures or tables")
        page["draft_copy"] = copy
        page["draft_copy_template"] = deepcopy(copy)
        page["copy_budget"].update(body_actual_words=len(copy["body"].split()),
                                   callout_count=len(copy["callouts"]), table_rows=len(copy["rows"]))
        page["playoff_harvest_binding"] = {
            "artifact": "playoff-harvest.json", "sha256": source_hash,
            "claim_ids": claims, "copy_authority": "playoff-harvest-copy.json",
        }
        page["copy_status"] = "HARVEST_REVIEWED_PREPRODUCTION_COPY_NOT_FOUNDER_APPROVED"
        page["backend_readiness"] = "SOURCE_READY_PNG_EXECUTION_PAUSED"
        # Retain the established finalized facts; add compact, separately scoped claims.
        fields = [f for f in page["deterministic_data_fields"]
                  if f.get("artifact") != "playoff-harvest.json"]
        for claim_id in claims:
            fields.append({
                "artifact": "playoff-harvest.json", "selector": "/claims/" + claim_id,
                "snapshot_value": deepcopy(harvest["claims"][claim_id]),
                "policy": "Accepted claim with its stated assumptions. Mathematical possibility is distinct from dated vendor estimates; hypothetical scores are not predictions.",
                "source_bundle_sha256": source_hash,
            })
        page["deterministic_data_fields"] = fields
        sports = request["sports_policy"]
        sports["refresh_fields"] = [compact_binding(f) for f in fields]
        sports["playoff_harvest"] = deepcopy(page["playoff_harvest_binding"])
        sports["playoff_harvest"]["interpretation"] = (
            "Preserve every visible condition and TheFFHub attribution. Vendor 0%/100% is not mathematical elimination/clinch. "
            "The record scenarios on P30 exclude tied future games; a further Mud Dogs loss eliminates under either scope."
        )
        prompt = replace_prompt_section(request["prompt"], "EXACT FULL PUBLICATION COPY", "FACT POLICY", copy)
        prompt = replace_prompt_section(prompt, "FACT POLICY", "REFERENCE IMAGES", sports)
        request.update(prompt=prompt, publication_copy=deepcopy(copy), sports_policy=sports,
                       production_gate=deepcopy(GATE))
        if request["image_generation_executed"] or request["publication_approved"]:
            raise ValueError("Cannot silently rewrite an executed or published request: " + pid)
        brief.update(artist_prompt=prompt, publication_copy=deepcopy(copy),
                     exact_copy_template=deepcopy(copy), playoff_harvest_binding=deepcopy(page["playoff_harvest_binding"]))
        page["candidate_render_prompt"] = prompt
        page["illustrated_page_brief"] = deepcopy(brief)
        folio["publication_copy"] = deepcopy(copy)
        folio["playoff_harvest_binding"] = deepcopy(page["playoff_harvest_binding"])
        for department in cards["departments"]:
            if department["unit_id"] == page["source_card_id"]:
                department.update(draft_copy=deepcopy(copy), draft_copy_template=deepcopy(copy),
                                  playoff_harvest_binding=deepcopy(page["playoff_harvest_binding"]))
        if pid in ds:
            ds[pid].update(artist_prompt=prompt, controlling_narration=copy["body"],
                           playoff_harvest_binding=deepcopy(page["playoff_harvest_binding"]))
        write(root, "render-inputs/" + pid + "/request.json", request)
        (root / "render-inputs" / pid / "full-page-prompt.md").write_text(prompt + "\n")
        ms[pid].update(request_sha256=digest(root / ms[pid]["request"]), copy_words=len(copy["body"].split()))
        markdown["issue-draft.md"] = replace_markdown_page(markdown["issue-draft.md"], pid, copy_section(page))
        markdown["illustrated-page-briefs.md"] = replace_markdown_page(
            markdown["illustrated-page-briefs.md"], pid, "## " + pid + " — " + page["title"] + "\n\n" + prompt)
        # The folio ledger presents body copy; preserve its composition, cast and input link.
        pattern = re.compile(r"(^## \d+ · " + re.escape(pid) + r" — [^\n]*\n.*?Full copy:\n\n)(.*?)(\n\nInput:)", re.M | re.S)
        markdown["storyboard-folio-plan-pass5.md"], count = pattern.subn(
            lambda m: m[1] + copy["body"] + m[3], markdown["storyboard-folio-plan-pass5.md"])
        if count != 1:
            raise ValueError("Missing folio ledger section: " + pid)

    issue["status"] = "FINAL_RESULTS_HARVEST_INTEGRATED_PREPRODUCTION_PNG_PAUSED"
    issue["production_gate"] = deepcopy(GATE)
    issue["render_hold_policy"] = (
        "Week 10 results and all 34 folio inputs are source-ready. The latest user direction keeps PNG production paused "
        "while Bullpen leads backend/frontend preproduction review. Grayscale generation and publication are not authorized by this harvest integration."
    )
    issue["preproduction_completion_note"] = (
        "34 included folios across six sheets; W10-P32 remains omitted. Final Week 10 values are locked to the current source. "
        "The reviewed playoff supplement is bound to P28/P30/P31; PNG execution remains paused."
    )
    folios["generation_policy"] = issue["render_hold_policy"]
    manifest["production_gate"] = deepcopy(GATE)
    manifest["playoff_harvest"] = {"artifact": "playoff-harvest.json", "sha256": source_hash,
                                   "selected_pages": list(SELECTED), "copy_authority": "playoff-harvest-copy.json",
                                   "consumption_receipt": "playoff-harvest-consumption.json"}
    for name, obj in (("issue-previs.json", issue), ("illustrated-page-briefs.json", briefs),
                      ("storyboard-folio-plan-pass5.json", folios), ("storycards.json", cards),
                      ("director-sequences.json", directors), ("render-inputs/manifest.json", manifest)):
        write(root, name, obj)
    for name, text in markdown.items():
        (root / name).write_text(text)
    dispositions = {"W10-P27": "REFERENCE_ONLY", "W10-P28": "SELECTED_CHANGE",
                    "W10-P29": "NO_MATERIAL_CANDIDATE", "W10-P30": "SELECTED_CHANGE",
                    "W10-P31": "SELECTED_CHANGE", "W10-P35": "REFERENCE_ONLY"}
    consumption = {
        "schema_version": "schemin.ffhub_page_consumption.v1",
        "baseline_commit": plan["baseline_commit"],
        "scope": "Separate accepted TheFFHub/exact-proof intake; not the descriptive-only Schemin analytics adapter.",
        "source_receipt": {"artifact": "playoff-harvest.json", "sha256": source_hash},
        "protected_source": deepcopy(harvest["protected_artifact"]),
        "canonical_fact_bundle_sha256": digest(root / "facts.json"),
        "copy_hash_encoding": "UTF-8 JSON, ensure_ascii=False, sort_keys=True, separators=(',', ':')",
        "pages": [], "production_gate": deepcopy(GATE),
    }
    for pid, disposition in dispositions.items():
        page = pages[pid]
        request_path = "render-inputs/" + pid + "/request.json"
        consumption["pages"].append({
            "page_id": pid, "disposition": disposition,
            "copy_pointer": "issue-previs.json#/pages/" + str(issue["pages"].index(page)) + "/draft_copy",
            "copy_sha256": snapshot_digest(page["draft_copy"]),
            "request": request_path, "request_sha256": digest(root / request_path),
            "claim_ids": harvest["page_claims"].get(pid, []),
            "supports_existing_copy_claims": (["all_12_alive_none_clinched", "mud_only_w11_loss_eliminates"]
                                               if pid == "W10-P30" else ["mud_only_w11_loss_eliminates"]
                                               if pid == "W10-P31" else []),
        })
    write(root, "playoff-harvest-consumption.json", consumption)
    return {"selected_pages": list(SELECTED), "source_sha256": source_hash,
            "page_count": 34, "image_generation_executed": False, "publication_approved": False}


if __name__ == "__main__":
    print(json.dumps(synchronize(), indent=2))
