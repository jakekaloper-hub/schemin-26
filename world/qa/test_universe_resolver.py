#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("ur",ROOT/"world"/"engine"/"universe_resolver.py")
ur=importlib.util.module_from_spec(spec); spec.loader.exec_module(ur)

class ResolverTests(unittest.TestCase):
    def test_obiwan_location(self):
        r=ur.where_is("CHAR-JAKE-KALOPER")
        self.assertEqual(r["location_id"],"LOC-TRADE-JEDI-MOUNTAIN-BASE")
        self.assertEqual(r["division_id"],"DIV-BURGERS")

    def test_obiwan_jedi_population(self):
        p=" ".join(ur.who_lives("LOC-TRADE-JEDI-MOUNTAIN-BASE")).lower()
        self.assertIn("jedi",p)

    def test_shared_march_route(self):
        r=ur.how_to_travel("LOC-TDS-WATERFALL-TEMPLE","LOC-CHILI-STABLE")
        self.assertIsNotNone(r)
        self.assertIn("LOC-TDS-CHILI-SHARED-MARCH",r["locations"])

    def test_neutral_access(self):
        for char in ur._maps()["domains"].values():
            start=char["primary_location_id"]
            self.assertIsNotNone(ur.how_to_travel(start,"LOC-LEAGUE-CHAMBER"), start)

    def test_country_club_memory(self):
        m=ur.what_happened("LOC-COUNTRY-CLUB-JACKSON")
        self.assertTrue(any(x["event_id"]=="EVT-W3-COUNTRY-CLUB-CHILI" for x in m))

if __name__=="__main__":
    unittest.main(verbosity=2)
