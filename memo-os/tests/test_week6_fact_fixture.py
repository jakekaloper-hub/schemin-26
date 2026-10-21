"""Week 6 final score source-lock regression (facts from published editorial packet).

These known results are regression anchors only, not a live ESPN refresh or an
authentication of player/event reports.
"""
import unittest

WEEK6=[
("D0nkey K0ng","Red Leopards","118.96","108.08"),
("Dr. Duckhook","El Niño","132.40","119.86"),
("Slob on my Dobb","ObiWan Jacoby","143.70","123.38"),
("Seven Deadly Chins","The Chili Cheesers","131.78","125.24"),
("His Majesty's Blood","Mud Dogs","136.92","136.80"),
("Three Dreaded Snake","The LLC","138.06","137.69"),
]
class Week6Fixture(unittest.TestCase):
    def test_six_winners_and_unique_teams(self):
        teams=[t for row in WEEK6 for t in row[:2]]
        self.assertEqual(len(WEEK6),6)
        self.assertEqual(len(set(teams)),12)
    def test_scores_are_exact_decimal_cents_and_winners_correct(self):
        from decimal import Decimal
        for winner,loser,w,l in WEEK6:
            self.assertGreater(Decimal(w),Decimal(l))
            self.assertEqual(Decimal(w).as_tuple().exponent,-2)
            self.assertEqual(Decimal(l).as_tuple().exponent,-2)
    def test_narrow_margins(self):
        from decimal import Decimal
        margins={w:Decimal(s)-Decimal(t) for w,l,s,t in WEEK6}
        self.assertEqual(margins["His Majesty's Blood"],Decimal("0.12"))
        self.assertEqual(margins["Three Dreaded Snake"],Decimal("0.37"))
    def test_canonical_name_zeros(self):
        self.assertIn("D0nkey K0ng",[row[0] for row in WEEK6])
        self.assertNotIn("Donkey Kong",[row[0] for row in WEEK6])
if __name__=="__main__":unittest.main()
