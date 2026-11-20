#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'manuscript/2018-jake-breakwater/SCENE_REGISTER.json').read_text())
expected={'ESPN1417621-2018-P01-E002','ESPN1417621-2018-P02-E007','ESPN1417621-2018-P03-E014','ESPN1417621-2018-P04-E021','ESPN1417621-2018-P05-E027','ESPN1417621-2018-P06-E033','ESPN1417621-2018-P07-E038','ESPN1417621-2018-P08-E043','ESPN1417621-2018-P09-E054','ESPN1417621-2018-P10-E059','ESPN1417621-2018-P11-E064','ESPN1417621-2018-P12-E072','ESPN1417621-2018-P13-E074','ESPN1417621-2018-P14-E085','ESPN1417621-2018-P15-E090','ESPN1417621-2018-P16-E095'}
actual={e for s in reg['scenes'] for e in s['source_event_ids']}; errors=[]
if actual != expected: errors.append('EVENT_SET_MISMATCH')
if any(s['pov_character_id']!='CHAR-JAKE-KALOPER' or s['pov_class']!='PRINCIPAL_CHARACTER' for s in reg['scenes']): errors.append('POV_SCOPE_INVALID')
result={'scope':'ALL_2018_FLAIM_JOINED_TEAM_1_EVENTS','linked_events':len(actual),'scene_count':len(reg['scenes']),'errors':errors,'status':'PASS' if not errors else 'FAIL'}
(ROOT/'review/2018_JAKE_LANE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2)); raise SystemExit(bool(errors))
