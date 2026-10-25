#!/usr/bin/env python3
"""Validate this development packet's provenance, not artistic acceptance."""
from pathlib import Path
import hashlib, json, re
root = Path(__file__).resolve().parents[6]
base = Path(__file__).resolve().parent.parent
stage = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
checks = []
for item in json.loads((base / 'SOURCE_HASHES.json').read_text())['files']:
    assert sha((root / item['path']).read_bytes()) == item['sha256'], item['path']
checks.append('16 retained authority/source files unchanged')
m = json.loads((stage / 'SAGA_READING_SOURCE_MAP.json').read_text())
a = (stage / 'SAGA_READING_ASSEMBLY.md').read_text()
assert sha(a.encode()) == m['assembly_sha256']
sections = list(re.finditer(r'^## (.+)$', a, re.M))
assert len(sections) == len(m['units']) == 40
for n, (heading, item) in enumerate(zip(sections, m['units'])):
    assert item['unit'] == n + 1
    assert heading.group(1) == f"{n + 1}. {item['title']}"
    body = a[heading.end():sections[n+1].start() if n+1 < len(sections) else len(a)].strip()
    assert sha(body.encode()) == item['body_sha256'], item['title']
    source = (base / item['source']).read_bytes()
    assert sha(source) == item['source_sha256'], item['source']
    text = source.decode()
    headings = list(re.finditer(r'^## (.+)$', text, re.M))
    matched = [i for i,h in enumerate(headings) if h.group(1) == item['source_heading']]
    assert len(matched) == 1
    i = matched[0]
    original = text[headings[i].end():headings[i+1].start() if i+1 < len(headings) else len(text)].strip()
    assert sha(original.encode()) == item['original_body_sha256']
    for edit in item.get('edits', []):
        assert edit['old'] in original, item['title']
        original = original.replace(edit['old'], edit['new'])
    original = re.sub(r'\n{3,}', '\n\n', original).strip()
    assert body == original, item['title']
checks.append('40 ordered units match mapped source bodies plus explicit editorial edits and hashes')
checks.append('assembly SHA256 ' + m['assembly_sha256'])
print(json.dumps({'status':'PASS','checks':checks,'limits':'Mechanical provenance only; no factual, audience, runtime or canon acceptance.'}, indent=2))
