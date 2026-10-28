import importlib.util
import json
from pathlib import Path
import unittest
BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('narratives', BASE / 'character_narratives.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
ROOT = BASE.parents[1]


class NarrativeTests(unittest.TestCase):
    def test_all_twelve_use_exact_interpretive_sections_not_stale_visual_or_history_fields(self):
        lineup = json.loads((ROOT / 'canon/characters/APPROVED_LINEUP_2026_10_18.json').read_text())
        characters = [{'id': x['character_id'], 'owner': x['owner']} for x in lineup['individuals']]
        result = module.character_narratives(ROOT, characters, 'a' * 40)
        self.assertEqual(set(result), {c['id'] for c in characters})
        for character in characters:
            record = result[character['id']]
            self.assertEqual(set(record['sections']), set(module.FIELDS))
            self.assertEqual(record['asOf'], 'Opening of 2026')
            path = next(p for p in (ROOT / 'living-novel/characters').glob('[0-9][0-9]_*.md') if p.stem[3:] == character['owner'].upper().replace(' ', '_'))
            for value in record['sections'].values(): self.assertIn(value, path.read_text())
            for edge in record['relationships']:
                self.assertIn(edge['characterId'], result)
                self.assertNotIn('CAUSE', edge)
                self.assertIn('STANCE: ' + edge['stance'], (ROOT / 'living-novel/characters/RELATIONSHIP_GRAPH.md').read_text())
        self.assertTrue(result['CHAR-JAKE-KALOPER']['relationships'])
        self.assertNotIn('Identity lock', str(result))

    def test_unknown_owner_cannot_be_guessed_from_team_or_position(self):
        with self.assertRaises(ValueError):
            module.character_narratives(ROOT, [{'id': 'CHAR-INVENTED', 'owner': 'Unknown Owner'}], 'a' * 40)
