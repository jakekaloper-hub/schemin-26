#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'manuscript/2017-jake-turning/SCENE_REGISTER.json').read_text())
expected={'ESPN1417621-2017-P01-E001','ESPN1417621-2017-P02-E007','ESPN1417621-2017-P03-E013','ESPN1417621-2017-P04-E019','ESPN1417621-2017-P05-E025','ESPN1417621-2017-P06-E031','ESPN1417621-2017-P07-E042','ESPN1417621-2017-P08-E047','ESPN1417621-2017-P09-E052','ESPN1417621-2017-P10-E057','ESPN1417621-2017-P11-E062','ESPN1417621-2017-P12-E067','ESPN1417621-2017-P13-E074','ESPN1417621-2017-P14-E084','ESPN1417621-2017-P15-E089','ESPN1417621-2017-P16-E095'}
actual={e for s in reg['scenes'] for e in s['source_event_ids']}; errors=[]
if actual!=expected: errors.append('EVENT_SET_MISMATCH')
if any(s['pov_character_id']!='CHAR-JAKE-KALOPER' or s['pov_class']!='PRINCIPAL_CHARACTER' for s in reg['scenes']): errors.append('POV_SCOPE_INVALID')
result={'scope':'ALL_2017_FLAIM_JOINED_TEAM_1_EVENTS','linked_events':len(actual),'scene_count':len(reg['scenes']),'errors':errors,'status':'PASS' if not errors else 'FAIL'}
(ROOT/'review/2017_JAKE_LANE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2)); raise SystemExit(bool(errors))
