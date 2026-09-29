from models import canonical_hash
def publication_receipt(contract,qa,output_sha256,policy_version="2.0"):
    if qa.get("status")!="PASS": raise ValueError("cannot receipt non-PASS QA")
    return {"schema_version":"2.0","contract_hash":canonical_hash(contract),"qa_policy_version":policy_version,"qa_status":"PASS","output_sha256":output_sha256}
