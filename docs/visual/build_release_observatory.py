#!/usr/bin/env python3
from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
source=json.loads((root/'governance/release-evidence/registry.json').read_text())
systems=source['systems']
ids={x['system_id'] for x in systems}
assert len(ids)==len(systems)
receipts=source['receipts']
out={'role':'derived evidence inspection, not approval','systems':[{'id':s['system_id'],'state':s['authority_state'],'anchor':s.get('anchor_path'),'receipt_id':s.get('current_receipt_id'),'anchor_exists':(root/s.get('anchor_path','')).is_file()} for s in systems],'receipt_count':len(receipts),'source':'governance/release-evidence/registry.json'}
(root/'docs/visual/release-data.json').write_text(json.dumps(out,indent=2)+'\n')
print('SYSTEMS',len(systems),'RECEIPTS',len(receipts),'MISSING_ANCHORS',sum(not s['anchor_exists'] for s in out['systems']))
