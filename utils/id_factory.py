from __future__ import annotations

from typing import Dict, List


class IdFactory:
    """Monotonic BIGINT ID sequences per entity category.

    Each category has an independent counter seeded from ID_RANGES.
    No ID is ever shared across categories — they are logically disjoint even
    if two categories happen to share the same numeric start offset.
    """

    def __init__(self, id_ranges: Dict[str, int]) -> None:
        self._counters: Dict[str, int] = dict(id_ranges)

    def next(self, category: str) -> int:
        """Return the next BIGINT ID for *category* and advance its counter."""
        if category not in self._counters:
            raise KeyError(
                f"Unknown IdFactory category: {category!r}. "
                f"Valid categories: {sorted(self._counters)}"
            )
        val = self._counters[category]
        self._counters[category] += 1
        return val

    def next_many(self, category: str, n: int) -> List[int]:
        """Return a contiguous block of *n* IDs for *category*."""
        return [self.next(category) for _ in range(n)]

    def peek(self, category: str) -> int:
        """Return the next ID without advancing the counter (diagnostic use)."""
        if category not in self._counters:
            raise KeyError(
                f"Unknown IdFactory category: {category!r}. "
                f"Valid categories: {sorted(self._counters)}"
            )
        return self._counters[category]


if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from config.settings import ID_RANGES

    factory = IdFactory(ID_RANGES)

    # (a) Two successive next('party') calls differ by exactly 1
    p1 = factory.next('party')
    p2 = factory.next('party')
    assert p2 - p1 == 1, f"Expected diff 1, got {p2 - p1}"

    # (b) next_many('agreement', 5) returns a contiguous block of 5 ints
    block = factory.next_many('agreement', 5)
    assert len(block) == 5
    assert all(block[i + 1] - block[i] == 1 for i in range(4)), f"Non-contiguous: {block}"

    # (c) next('party') and next('agreement') never return the same integer
    party_ids = set(factory.next_many('party', 100))
    agr_ids = set(factory.next_many('agreement', 100))
    assert party_ids.isdisjoint(agr_ids), "party and agreement IDs collided"

    # (d) next('does_not_exist') raises KeyError
    try:
        factory.next('does_not_exist')
        raise AssertionError("Expected KeyError not raised")
    except KeyError:
        pass

    # (e) All returned values are positive int and >= ID_RANGES[category]
    factory2 = IdFactory(ID_RANGES)
    for cat, start in ID_RANGES.items():
        val = factory2.next(cat)
        assert isinstance(val, int), f"{cat}: not int"
        assert val >= start, f"{cat}: {val} < {start}"
        assert val > 0, f"{cat}: {val} not positive"

    print('id_factory OK')
