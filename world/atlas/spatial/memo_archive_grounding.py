"""Publication evidence lookup for Atlas spatial candidates; read-only, never an auto-canon promotion."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INTAKE = ROOT / 'governance/publication-manifest/WEEKS_04_06_COMMISSIONER_SOURCE_INTAKE_2026_10_22.json'
EVIDENCE = ROOT / 'world/atlas/foundation/WEEKS_04_06_PUBLISHED_VISUAL_GEOGRAPHY_INTAKE_V1.json'


def resolve_evidence(location_id):
    intake = json.loads(INTAKE.read_text())
    atlas = json.loads(EVIDENCE.read_text())
    evidence = []
    for record in atlas['records']:
        if record.get('existing_location_id') != location_id:
            continue
        file = next((f for f in intake['files'] if f['week'] == record['week']), None)
        if file is None or file.get('archive_status') != 'VERIFIED_STORED':
            raise ValueError('MISSING_VERIFIED_MEMO_SOURCE')
        if file.get('sha256') != file.get('verified_retrieval_sha256'):
            raise ValueError('SOURCE_HASH_RECEIPT_MISMATCH')
        path = ROOT / file['archive_path']
        if not path.is_file():
            raise ValueError('SOURCE_BYTES_MISSING')
        contents = path.read_bytes()
        if contents.startswith(b'version https://git-lfs.github.com/spec/v1\n'):
            pointer = contents.decode('ascii')
            if ('oid sha256:' + file['sha256']) not in pointer or ('size ' + str(file['size_bytes'])) not in pointer:
                raise ValueError('SOURCE_LFS_POINTER_INVALID')
        elif len(contents) != file['size_bytes'] or hashlib.sha256(contents).hexdigest() != file['sha256']:
            raise ValueError('SOURCE_CONTENT_HASH_MISMATCH')
        if record.get('coordinate_authority') is not False or record.get('canon_effect') != 'NONE_AUTOMATIC':
            raise ValueError('UNAUTHORIZED_GEOGRAPHIC_PROMOTION')
        evidence.append({'evidence_id':record['evidence_id'],'week':record['week'],
                         'pdf_pages':record['pdf_pages'],'scene':record['scene'],
                         'sha256':file['sha256'],'archive_path':file['archive_path'],
                         'spatial_inference':'NOT_APPROVED'})
    return evidence


def resolve_central_basin_evidence():
    ids = ('LOC-LEAGUE-CHAMBER', 'LOC-LEAGUE-ARCHIVE', 'LOC-PITTSYS-BOOK',
           'LOC-DK-MUD-HILL', 'LOC-SOUTHERN-SPEEDWAY')
    return {'status':'VERIFIED_PUBLICATION_EVIDENCE_ONLY','locations':
            {key:resolve_evidence(key) for key in ids},'metric_geometry_approved':False}
