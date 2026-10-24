"""Project existing interpretive character text without importing old visual/history locks."""
import hashlib
import re

FIELDS = ['Public reputation', 'Interior logic — INTERPRETIVE CANON', 'Desire', 'Blind spot', 'Vulnerability']


def character_narratives(root, characters, revision):
    directory = root / 'living-novel/characters'
    records = {}; by_first = {}
    for character in characters:
        owner = character['owner']; first = owner.split()[0]
        if first in by_first:
            raise ValueError('Ambiguous fictional relationship identity')
        by_first[first] = character['id']
        matches = [p for p in directory.glob('[0-9][0-9]_*.md') if p.stem[3:] == owner.upper().replace(' ', '_')]
        if len(matches) != 1:
            raise ValueError(f'Missing exact character dossier: {owner}')
        path = matches[0]; text = path.read_text(); sections = {}
        for heading, body in re.findall(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)', text, re.M | re.S):
            if heading in FIELDS:
                sections[heading] = body.strip()
        if set(sections) != set(FIELDS) or not all(sections.values()):
            raise ValueError(f'Incomplete narrative dossier: {owner}')
        relative = path.relative_to(root).as_posix()
        records[character['id']] = {'sections': sections, 'relationships': [],
            'asOf': 'Opening of 2026', 'status': 'Interpretive fictional characterization',
            'sourceSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'sourceUrl': f'https://github.com/jakekaloper-hub/schemin-26/blob/{revision}/{relative}'}
    graph = directory / 'RELATIONSHIP_GRAPH.md'; text = graph.read_text()
    if 'Status: STEP 5 INTERPRETIVE CANON' not in text or 'Temporal position: opening of 2026' not in text:
        raise ValueError('Relationship interpretation authority changed')
    graph_url = f'https://github.com/jakekaloper-hub/schemin-26/blob/{revision}/living-novel/characters/RELATIONSHIP_GRAPH.md'
    for owner, counterpart, body in re.findall(r'^## (\w+) → (\w+)\n(.*?)(?=^## |^# |\Z)', text, re.M | re.S):
        if owner not in by_first or counterpart not in by_first:
            raise ValueError('Unknown relationship identity')
        stance = re.search(r'^STANCE: (.+)$', body, re.M)
        if not stance:
            raise ValueError('Missing relationship stance')
        records[by_first[owner]]['relationships'].append({'characterId': by_first[counterpart],
            'stance': stance[1], 'sourceUrl': graph_url,
            'sourceSha256': hashlib.sha256(graph.read_bytes()).hexdigest()})
    return records
