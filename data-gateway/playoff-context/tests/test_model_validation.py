import copy
import importlib.util
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location('validate_playoff_model', Path(__file__).resolve().parents[1] / 'validate_model.py')
VALIDATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATION)


class TestWalkForwardValidation(unittest.TestCase):
    def setUp(self):
        self.names = {'1': 'One', '2': 'Two', '3': 'Three', '4': 'Four'}
        self.weeks = {}
        for week in range(1, 6):
            self.weeks[week] = {'week': week, 'matchups': [
                {'winner': 'HOME', 'home': {'teamId': '1', 'totalPoints': 120 + week},
                 'away': {'teamId': '2', 'totalPoints': 100 + week}},
                {'winner': 'AWAY', 'home': {'teamId': '3', 'totalPoints': 90 + week},
                 'away': {'teamId': '4', 'totalPoints': 110 + week}},
            ]}

    def predict(self, weeks):
        return VALIDATION.walk_forward_predictions(weeks, self.names, start_week=3, end_week=4)

    def test_predictions_use_only_strictly_prior_scores(self):
        original = self.predict(self.weeks)
        self.assertEqual(len(original), 4)
        for row in original:
            self.assertEqual(row['training_last_week'], row['week'] - 1)
            self.assertEqual(set(row['training_scores_per_team'].values()), {row['week'] - 1})
            self.assertFalse(row['provider_projections_used'])

        future = copy.deepcopy(self.weeks)
        future[5]['matchups'][0]['home']['totalPoints'] = 99999
        self.assertEqual(self.predict(future), original)

        # All Week 4 strengths are frozen before ANY Week 4 game score is read.
        same_week = copy.deepcopy(self.weeks)
        same_week[4]['matchups'][0]['home']['totalPoints'] = 99999
        altered = self.predict(same_week)
        probability_fields = ('home_win_probability', 'home_strength_mean', 'home_strength_sigma',
                              'away_strength_mean', 'away_strength_sigma')
        for before, after in zip(original, altered):
            self.assertEqual({key: before[key] for key in probability_fields},
                             {key: after[key] for key in probability_fields})

        # A control perturbation to actual training data changes the forecast.
        past = copy.deepcopy(self.weeks)
        past[2]['matchups'][0]['home']['totalPoints'] = 999
        self.assertNotEqual(self.predict(past)[0]['home_win_probability'], original[0]['home_win_probability'])

    def test_unplayed_or_missing_prior_week_does_not_become_training_data(self):
        missing = copy.deepcopy(self.weeks)
        del missing[2]
        with self.assertRaises(ValueError):
            self.predict(missing)
        undecided = copy.deepcopy(self.weeks)
        undecided[2]['matchups'][0]['winner'] = 'UNDECIDED'
        with self.assertRaises(RuntimeError):
            self.predict(undecided)


if __name__ == '__main__':
    unittest.main()
