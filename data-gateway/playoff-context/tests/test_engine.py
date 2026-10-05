import unittest
from playoff_context import TeamState, Game, LeagueRules, simulate, exact_bounds_status, conditional_leverage

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.teams={
            "A":TeamState("A","A",3,0,points_for=450,scores=(140,150,160)),
            "B":TeamState("B","B",2,1,points_for=390,scores=(130,125,135)),
            "C":TeamState("C","C",1,2,points_for=360,scores=(120,120,120)),
            "D":TeamState("D","D",0,3,points_for=300,scores=(100,100,100)),
        }
        self.rules=LeagueRules(playoff_teams=2,regular_season_weeks=5)
        self.games=[Game(4,"A","D"),Game(4,"B","C"),Game(5,"A","B"),Game(5,"C","D")]
    def test_reproducible(self):
        self.assertEqual(simulate(self.teams,self.games,self.rules,3000,7),simulate(self.teams,self.games,self.rules,3000,7))
    def test_strength_direction(self):
        x=simulate(self.teams,self.games,self.rules,5000,9)
        self.assertGreater(x["A"]["playoff_probability"],x["D"]["playoff_probability"])
    def test_exact_bounds_no_false_certainty(self):
        x=exact_bounds_status(self.teams,self.games,self.rules)
        self.assertEqual(x["A"]["class"],"EXACT")
        self.assertIn(x["D"]["status"],{"ALIVE","ELIMINATED"})
    def test_leverage(self):
        x=conditional_leverage(self.teams,self.games,self.rules,self.games[1],3000,4)
        self.assertGreaterEqual(x["B"]["leverage_delta_pp"],0)
        self.assertGreaterEqual(x["C"]["leverage_delta_pp"],0)

if __name__=="__main__": unittest.main()
