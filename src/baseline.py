def load_bits_scan(g, budget, gap, bmax):
    """在总能量预算内，为每个子载波分配整数比特。"""
    bits = [0] * len(g)
    next_cost = [gap / gain for gain in g]
    remaining = budget

    while True:
        eligible = (i for i in range(len(g)) if bits[i] < bmax)
        i = min(eligible, key=lambda i: (next_cost[i], i), default=None)

        if i is None or next_cost[i] > remaining:
            return bits

        remaining -= next_cost[i]
        bits[i] += 1
        next_cost[i] *= 2



if __name__ == "__main__":
    from itertools import product

    gains = [1, 2, 4]
    cap = 2

    for budget in range(6):
        best_total = max(
            sum(candidate)
            for candidate in product(range(cap + 1), repeat=len(gains))
            if sum((2**b - 1) / g for b, g in zip(candidate, gains)) <= budget
        )
        bits = load_bits_scan(gains, budget=budget, gap=1, bmax=cap)
        assert sum(bits) == best_total, f"Failed at budget={budget}"
        assert sum((2**b - 1) / g for b, g in zip(bits, gains)) <= budget
    assert load_bits_scan([1, 1], budget=3, gap=1, bmax=2) == [1, 1]
    assert load_bits_scan([1, 1], budget=4, gap=1, bmax=2) == [2, 1]
    assert load_bits_scan([1, 1], budget=0, gap=1, bmax=2) == [0, 0]
    print("All baseline checks passed.")