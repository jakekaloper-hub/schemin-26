"""Check publication receipts and candidate landmark provenance without canon promotion."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
CONSTRAINTS=ROOT/'world/atlas/spatial/references/central-basin-01/historical_constraints.json'
EXPECTED={'LOC-LEAGUE-CHAMBER','LOC-LEAGUE-ARCHIVE','LOC-PITTSYS-BOOK','LOC-DK-MUD-HILL','LOC-SOUTHERN-SPEEDWAY'}

def evaluate(check_bytes=False):
    d=json.loads(CONSTRAINTS.read_text())
    if set(d['landmark_ids'])!=EXPECTED:raise ValueError('LANDMARK_ID_DRIFT')
    if d['physical_requirements']['metric_scale_and_landmark_footprints_approved']:
        raise ValueError('IMPROPER_METRIC_PROMOTION')
    receipts=[]
    for location in sorted(d['historical_observations']):
        for obs in d['historical_observations'][location]:
            p=ROOT/obs['archive_path']
            if not p.is_file():raise ValueError('ARCHIVE_SOURCE_ABSENT:'+obs['archive_path'])
            if obs['spatial_inference']!='NOT_APPROVED':raise ValueError('UNAUTHORIZED_SPATIAL_INFERENCE')
            if check_bytes:
                actual=hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
                if actual!=obs['sha256']:raise ValueError('SOURCE_SHA_MISMATCH:'+obs['evidence_id'])
            receipts.append({'location_id':location,'evidence_id':obs['evidence_id'],
                             'archive_path':obs['archive_path'],'pages':obs['pdf_pages'],
                             'hash_checked':check_bytes,'metric_coordinate_approved':False})
    return {'scope':'CENTRAL_BASIN_HISTORICAL_PROVENANCE',
            'source_bytes_verified':check_bytes,'historical_observation_count':len(receipts),
            'landmark_identity_count':len(EXPECTED),'receipts':receipts,
            'status':'SOURCE_PROVENANCE_ONLY_NO_METRIC_APPROVAL'}
