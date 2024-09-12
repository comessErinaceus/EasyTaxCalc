import unittest
import json
from tax_calculator import calculate_tax, update_tax_brackets, load_tax_brackets, save_tax_brackets

TEST_TAX_BRACKET_FILEPATH = './test_brackets.json'

class TestTaxCalculator(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.test_brackets = {
            'single': [
                {'lower': 0, 'upper': 10000, 'rate': 0.1},
                {'lower': 10000, 'upper': 30000, 'rate': 0.2},
                {'lower': 30000, 'upper': 1.7976931348623157e+308, 'rate': 0.3}
            ],
            'married_joint': [
                {'lower': 0, 'upper': 20000, 'rate': 0.1},
                {'lower': 20000, 'upper': 60000, 'rate': 0.2},
                {'lower': 60000, 'upper': 1.7976931348623157e+308, 'rate': 0.3}
            ]
        }
        save_tax_brackets(TEST_TAX_BRACKET_FILEPATH, self.test_brackets)  # Save initial test brackets

    def test_calculate_tax(self):
        tax_brackets = load_tax_brackets(TEST_TAX_BRACKET_FILEPATH)
        self.assertEqual(calculate_tax(15000, 'single', tax_brackets), 2000)
        self.assertEqual(calculate_tax(35000, 'single', tax_brackets), 6500)
        self.assertEqual(calculate_tax(40000, 'married_joint', tax_brackets), 6000)
    
    # def test_update_tax_brackets(self):
    #     new_brackets = {
    #         'single': [
    #             {'lower': 0, 'upper': 5000, 'rate': 0.05},
    #             {'lower': 5000, 'upper': 15000, 'rate': 0.15},
    #             {'lower': 15000, 'upper': 1.7976931348623157e+308, 'rate': 0.25}
    #         ]
    #     }
    #     update_tax_brackets('single', [5000, 15000, 0.05, 15000, 1.7976931348623157e+308, 0.25])
    #     updated_brackets = load_tax_brackets(TEST_TAX_BRACKET_FILEPATH)
    #     self.assertEqual(updated_brackets['single'], new_brackets['single'])

    def tearDown(self):
        # Clean up after tests
        save_tax_brackets(TEST_TAX_BRACKET_FILEPATH,self.test_brackets)  # Restore original brackets

if __name__ == '__main__':
    unittest.main()
