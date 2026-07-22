"""Deterministic, score-independent hint-credit economy shared by builders.

The generated YAML retains hint text, but its native point cost is deliberately
zero: production CTFd unlocks these managed tiers through the hint-wallet
plugin, never through the global scoreboard.
"""
from math import ceil


def tier_costs(value: int) -> tuple[int, int, int]:
    if not isinstance(value, int) or value <= 0:
        raise ValueError("challenge value must be a positive integer")
    costs = (ceil(value / 10), ceil(2 * value / 10), ceil(3 * value / 10))
    if not (costs[0] < costs[1] < costs[2] and sum(costs) <= value):
        raise ValueError(f"invalid progressive hint split for value {value}")
    return costs


def managed_tiers(value: int, tiers):
    """Keep authored content while deriving every price from challenge value."""
    texts = [tier[0] if isinstance(tier, tuple) else tier for tier in tiers]
    if len(texts) != 3:
        raise ValueError("wallet-managed challenges require exactly three hint tiers")
    return list(zip(texts, tier_costs(value)))


def bootstrap_reserve(values: list[int]) -> int:
    costs = [sum(tier_costs(value)) for value in values]
    return max(
        (costs[k] + costs[k + 1]) - sum(values[i] - costs[i] for i in range(k))
        for k in range(len(values) - 1)
    )


def simulate(values: list[int]) -> int:
    """Prove the pessimistic all-hints path can buy up to six next hints."""
    reserve = bootstrap_reserve(values)
    balance = reserve
    for index, value in enumerate(values):
        remaining = len(values) - index
        upcoming = []
        for future_value in values[index:index + 2]:
            upcoming.extend(tier_costs(future_value))
        upcoming = upcoming[:min(6, 3 * remaining)]
        if balance < sum(upcoming):
            raise ValueError(f"reserve cannot cover six upcoming hints at level {index}")
        balance -= sum(tier_costs(value))
        balance += value
    return reserve
