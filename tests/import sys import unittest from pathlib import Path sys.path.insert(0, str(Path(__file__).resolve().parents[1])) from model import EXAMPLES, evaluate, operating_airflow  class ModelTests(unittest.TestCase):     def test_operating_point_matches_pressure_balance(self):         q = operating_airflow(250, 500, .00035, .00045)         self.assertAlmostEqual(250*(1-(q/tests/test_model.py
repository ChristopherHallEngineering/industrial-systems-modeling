import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import EXAMPLES, evaluate, operating_airflow

class ModelTests(unittest.TestCase):
    def test_operating_point_matches_pressure_balance(self):
        q = operating_airflow(250, 500, .00035, .00045)
        self.assertAlmostEqual(250*(1-(q/500)**2), (.00035+.00045)*q*q)
    def test_all_results_bounded(self):
        for c in EXAMPLES:
            r = evaluate(c)
            self.assertGreater(r.airflow, 0)
            self.assertGreater(r.cadr, 0)
            self.assertLessEqual(r.cadr, r.airflow)
            self.assertGreater(r.service_life_proxy, 0)
    def test_added_resistance_reduces_flow(self):
        self.assertGreater(operating_airflow(250, 500, .00035, .0001), operating_airflow(250, 500, .00035, .001))
    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            operating_airflow(0, 500, .00035, .0001)

if __name__ == "__main__":
    unittest.main()
