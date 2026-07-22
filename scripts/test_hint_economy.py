import unittest

try:  # Supports both `python scripts/test_hint_economy.py` and unittest.
    from hint_economy import simulate, tier_costs
except ModuleNotFoundError:
    from scripts.hint_economy import simulate, tier_costs


class HintEconomyTests(unittest.TestCase):
    def test_required_reserves_and_six_hint_coverage(self):
        self.assertEqual(simulate([100 + 50 * i for i in range(34)]), 170)
        self.assertEqual(simulate([200 + 50 * i for i in range(7)]), 270)
        self.assertEqual(simulate([200 + 50 * i for i in range(15)]), 270)

    def test_formula_is_strict_and_bounded(self):
        for value in [100 + 50 * i for i in range(34)] + [200 + 50 * i for i in range(15)]:
            first, second, third = tier_costs(value)
            self.assertLess(first, second)
            self.assertLess(second, third)
            self.assertLessEqual(first + second + third, value)


if __name__ == "__main__":
    unittest.main()
