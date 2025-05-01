import unittest
from src.investments import predict_income, compound_interest, anual_rate_to_monthly, cagr

class TestInvestments(unittest.TestCase):
    def test_predict_income(self):
        # Test case 1: Basic calculation
        self.assertAlmostEqual(predict_income(1000, 1500), 50.0)
        
        # Test case 2: No change
        self.assertAlmostEqual(predict_income(1000, 1000), 0.0)
        
        # Test case 3: Loss
        self.assertAlmostEqual(predict_income(1000, 800), -20.0)

    def test_compound_interest(self):
        # Test case 1: Basic calculation
        self.assertAlmostEqual(compound_interest(1000, 10, 2), 1210.0)
        
        # Test case 2: Zero rate
        self.assertAlmostEqual(compound_interest(1000, 0, 2), 1000.0)
        
        # Test case 3: Zero time
        self.assertAlmostEqual(compound_interest(1000, 10, 0), 1000.0)

    def test_anual_rate_to_monthly(self):
        # Test case 1: Basic conversion
        self.assertAlmostEqual(anual_rate_to_monthly(12), 0.949, places=3)
        
        # Test case 2: Zero rate
        self.assertAlmostEqual(anual_rate_to_monthly(0), 0.0)
        
        # Test case 3: Negative rate
        self.assertAlmostEqual(anual_rate_to_monthly(-12), -1.0596, places=4)

    def test_cagr(self):
        # Test case 1: Basic calculation
        self.assertAlmostEqual(cagr(1000, 1210, 2), 10.0, places=1)
        
        # Test case 2: No growth
        self.assertAlmostEqual(cagr(1000, 1000, 2), 0.0)
        
        # Test case 3: Loss
        self.assertAlmostEqual(cagr(1000, 800, 2), -10.6, places=1)

if __name__ == '__main__':
    unittest.main() 