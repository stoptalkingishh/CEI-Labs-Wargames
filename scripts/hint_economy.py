"""Deterministic, score-independent hint-cost economy shared by builders.

The generated YAML retains hint text, but its native point cost is deliberately
zero: production CTFd unlocks these managed tiers through the hint-wallet
plugin, never through the global scoreboard.

Cost model (see cei-labs-event#7): each tier's cost is a PERCENTAGE of the
challenge's own point value, not a flat/absolute number of points spent from
a shared team currency. Opening a tier does not debit anything -- it records
that this owner peeked at that tier for that specific challenge. The percent
is applied at solve time as a reduction of THAT challenge's own award: a
player who solves after opening tier N keeps `100 - tier_costs(value)[N-1]`
percent of the challenge's point value. Tiers are cumulative, not additive --
opening tier 3 costs 85% of the value (not 10+50+85), leaving 15%.
"""

# Cumulative percent-of-value cost for opening tier 1/2/3 (fully opening all
# three hints leaves 100 - 85 = 15% of the challenge's value on a solve).
TIER_PERCENTS = (20, 50, 85)


def tier_costs(value: int) -> tuple:
    """Return the (tier1, tier2, tier3) percent-of-value costs for a
    challenge worth `value` points. The percents themselves don't depend on
    `value` (they're a fixed schedule), but this keeps the same call shape
    every builder already uses and validates `value` is sane."""
    if not isinstance(value, int) or value <= 0:
        raise ValueError("challenge value must be a positive integer")
    costs = TIER_PERCENTS
    if not (costs[0] < costs[1] < costs[2] and costs[2] < 100):
        raise ValueError(f"invalid progressive hint percent schedule for value {value}")
    return costs


def managed_tiers(value: int, tiers):
    """Pair authored hint text with the formula-derived percent cost for
    each tier.

    `tiers` is a plain sequence of hint-text strings (one per tier, cheapest
    first) -- there is no authored cost field anywhere in this economy.
    Every percent is derived exclusively from `tier_costs(value)`, per this
    module's docstring: production CTFd unlocks these tiers through the
    hint-wallet plugin, and the only "cost" ever actually enforced is the
    percent-of-value score reduction applied at solve time.
    """
    texts = list(tiers)
    if len(texts) != 3:
        raise ValueError("wallet-managed challenges require exactly three hint tiers")
    return list(zip(texts, tier_costs(value)))


def retained_percent(opened_tier) -> int:
    """The percent of a challenge's value a player keeps on solve, given the
    highest hint tier they opened for it (None/0 = no hint opened -> 100%)."""
    if not opened_tier:
        return 100
    if opened_tier not in (1, 2, 3):
        raise ValueError(f"tier must be 1, 2, 3, or falsy, got {opened_tier!r}")
    return 100 - TIER_PERCENTS[opened_tier - 1]
