from __future__ import annotations

from typing import Optional

import numpy as np


def luhn_check(card_num: str) -> bool:
    """Return True if *card_num* passes the Luhn (mod-10) check."""
    digits = [int(d) for d in reversed(card_num)]
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def _luhn_sum(partial: str) -> int:
    """Compute Luhn running sum for *partial* (used to derive check digit)."""
    digits = [int(d) for d in reversed(partial)]
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total


def generate_card_number(
    rng: np.random.Generator,
    bin_prefix: Optional[str] = None,
) -> str:
    """Return a Luhn-valid 16-digit card number string.

    If *bin_prefix* (6 digits) is provided, uses it as the BIN; otherwise
    defaults to '400000' (Visa-style). Step 17 can read card[:6] to get
    Bank_Identification_Num.
    """
    prefix = bin_prefix or '400000'
    body_len = 15 - len(prefix)
    body = ''.join(str(int(rng.integers(0, 10))) for _ in range(body_len))
    partial = prefix + body + '0'
    check = (10 - (_luhn_sum(partial) % 10)) % 10
    return prefix + body + str(check)


def generate_cvv(rng: np.random.Generator) -> str:
    """Return a zero-padded 3-digit CVV string ('000'–'999')."""
    return f'{int(rng.integers(0, 1000)):03d}'


if __name__ == '__main__':
    rng = np.random.default_rng(42)

    # (a) 1000 card numbers all pass luhn_check
    cards = [generate_card_number(rng) for _ in range(1000)]
    assert all(luhn_check(c) for c in cards), "Some cards failed mod-10"

    # (b) All 1000 are unique
    assert len(set(cards)) == 1000, f"Duplicate cards: {1000 - len(set(cards))}"

    # (c) Every card is a 16-character digit string
    assert all(len(c) == 16 and c.isdigit() for c in cards), "Card format error"

    # (d) generate_cvv returns a 3-character digit string
    cvv = generate_cvv(rng)
    assert len(cvv) == 3 and cvv.isdigit(), f"Bad CVV: {cvv!r}"

    # (e) Known bad number fails
    assert not luhn_check('4111111111111112'), "Bad number should fail"

    # (f) Known good number passes
    assert luhn_check('4111111111111111'), "Known-good Visa number should pass"

    print('luhn OK')
