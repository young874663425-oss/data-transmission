import heapq


def load_bits_heap(g, budget, gap, bmax):
    """用最小堆在总能量预算内分配整数比特。"""
    bits = [0] * len(g)
    if bmax == 0:
        return bits

    remaining = budget

    # 元组按成本排序。成本相同时，下标较小的子载波优先。
    heap = [(gap / gain, i) for i, gain in enumerate(g)]
    heapq.heapify(heap)

    while heap:
        cost, i = heap[0]
        if cost > remaining:
            break

        heapq.heappop(heap)
        remaining -= cost
        bits[i] += 1

        # 没有达到上限时，将该子载波的下一比特成本放回堆。
        if bits[i] < bmax:
            heapq.heappush(heap, (2 * cost, i))

    return bits


if __name__ == "__main__":
    from baseline import load_bits_scan

    cases = [
        ([1, 1], 0, 1, 2),   # 零预算
        ([1, 1], 3, 1, 2),   # 剩余预算买不起下一比特
        ([1, 1], 4, 1, 2),   # 刚好买得起第三比特，平局时选下标 0
        ([1, 1], 6, 1, 2),   # 所有子载波达到上限
        ([1, 1], 10, 1, 0),  # 每个子载波的上限为零
        ([1, 2, 4], 2, 1, 2),  # 不同信道增益
    ]

    for g, budget, gap, bmax in cases:
        expected = load_bits_scan(g, budget, gap, bmax)
        actual = load_bits_heap(g, budget, gap, bmax)
        assert actual == expected, (
            f"g={g}, budget={budget}, gap={gap}, bmax={bmax}: "
            f"heap={actual}, scan={expected}"
        )

    print("Heap and scan allocations match.")