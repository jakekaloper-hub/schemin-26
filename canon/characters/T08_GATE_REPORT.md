# T08 GATE REPORT — CHARACTER QA ENGINE
BUILD: `cccp_qa.py`.
TEST: missing evidence → HUMAN_REVIEW_REQUIRED; identity/species/retired/contamination failure → REGENERATE; all mandatory checks true → PASS; publication requires all PASS.
AUDIT: only PASS / REGENERATE / HUMAN_REVIEW_REQUIRED are legal outcomes.
POLISH: reference retrievability is mandatory, preventing G1 from being bypassed.
RETEST: deterministic outcome contract PASS by branch inspection; runtime CI repeated at T16.
UMPIRE/QA: PASS.
CLOSER: T08 COMPLETE / PASS. T09–T12 AUTHORIZED.
