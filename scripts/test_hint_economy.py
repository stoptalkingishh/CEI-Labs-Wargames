import unittest

try:  # Supports both `python scripts/test_hint_economy.py` and unittest.
    from hint_economy import TIER_PERCENTS, ctfd_tiers, managed_tiers, retained_percent, tier_costs
except ModuleNotFoundError:
    from scripts.hint_economy import TIER_PERCENTS, ctfd_tiers, managed_tiers, retained_percent, tier_costs


class HintEconomyTests(unittest.TestCase):
    def test_tier_costs_is_the_fixed_20_50_85_percent_schedule(self):
        for value in [100, 150, 200, 3200]:
            self.assertEqual(tier_costs(value), (20, 50, 85))

    def test_tier_costs_rejects_non_positive_or_non_int_value(self):
        for bad in (0, -1, 1.5, "100"):
            with self.assertRaises(ValueError):
                tier_costs(bad)

    def test_formula_is_strict_and_bounded_under_100_percent(self):
        for value in [100 + 50 * i for i in range(34)] + [200 + 50 * i for i in range(15)]:
            first, second, third = tier_costs(value)
            self.assertLess(first, second)
            self.assertLess(second, third)
            self.assertLess(third, 100)

    def test_managed_tiers_pairs_text_with_percent(self):
        result = managed_tiers(100, ["nudge", "bigger nudge", "answer"])
        self.assertEqual(result, [("nudge", 20), ("bigger nudge", 50), ("answer", 85)])

    def test_managed_tiers_requires_exactly_three_hint_texts(self):
        with self.assertRaises(ValueError):
            managed_tiers(100, ["only one"])
        with self.assertRaises(ValueError):
            managed_tiers(100, ["one", "two", "three", "four"])

    def test_retained_percent_no_hint_opened_keeps_everything(self):
        self.assertEqual(retained_percent(None), 100)
        self.assertEqual(retained_percent(0), 100)

    def test_retained_percent_matches_tier_percents_schedule(self):
        self.assertEqual(retained_percent(1), 100 - TIER_PERCENTS[0])
        self.assertEqual(retained_percent(2), 100 - TIER_PERCENTS[1])
        self.assertEqual(retained_percent(3), 100 - TIER_PERCENTS[2])

    def test_retained_percent_rejects_invalid_tier(self):
        for bad in (4, -1, "1"):
            with self.assertRaises(ValueError):
                retained_percent(bad)

    def test_ctfd_tiers_numbers_tiers_from_one_in_order(self):
        self.assertEqual(
            ctfd_tiers(100, ["nudge", "bigger nudge", "answer"]),
            [
                {"tier": 1, "cost": 20, "content": "nudge"},
                {"tier": 2, "cost": 50, "content": "bigger nudge"},
                {"tier": 3, "cost": 85, "content": "answer"},
            ],
        )

    def test_ctfd_tiers_does_not_bypass_the_three_tier_arity_guard(self):
        # ctfd_tiers() is only a reshape adapter -- a track must not be able
        # to ship two or four hint tiers by going through it. This was a real
        # bug: build_threadline.py used to reimplement the tier pairing
        # locally and silently zipped whatever it was given (#102).
        for bad in (["only one"], ["one", "two", "three", "four"]):
            with self.assertRaises(ValueError):
                ctfd_tiers(100, bad)


if __name__ == "__main__":
    unittest.main()
