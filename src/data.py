import numpy as np


def make_loading_case(seed, tones=64, taps=8, noise_var=0.1, pilots=20):
    """生成一个合成多径信道，返回真实和估计的信道质量数组。"""
    rng = np.random.default_rng(seed)

    # 路径功率随延迟衰减，归一化后总功率为 1。
    power = np.exp(-np.arange(taps) / 2.0)
    power /= power.sum()
    channel_taps = np.sqrt(power / 2.0) * (
        rng.normal(size=taps) + 1j * rng.normal(size=taps)
    )
    h = np.fft.fft(channel_taps, n=tones)

    # 用带噪的单位导频估计每个子载波的信道响应。
    shape = (pilots, tones)
    scale = np.sqrt(noise_var / 2.0)
    pilot_noise = scale * (rng.normal(size=shape) + 1j * rng.normal(size=shape))
    h_hat = (h[None, :] + pilot_noise).mean(axis=0)

    # 用独立的纯噪声样本估计噪声方差。
    noise_only = scale * (rng.normal(size=shape) + 1j * rng.normal(size=shape))
    variance_hat = np.mean(np.abs(noise_only) ** 2, axis=0)

    g_true = np.abs(h) ** 2 / noise_var
    g_hat = np.abs(h_hat) ** 2 / np.maximum(variance_hat, 1e-12)
    return g_true, np.maximum(g_hat, 1e-12)


if __name__ == "__main__":
    from baseline import load_bits_scan
    from modified import load_bits_heap

    for label, gains in zip(("g_true", "g_hat"), make_loading_case(seed=0)):
        assert gains.shape == (64,)
        assert np.all(np.isfinite(gains)) and np.all(gains > 0)

        scan = load_bits_scan(gains, budget=64, gap=2, bmax=8)
        heap = load_bits_heap(gains, budget=64, gap=2, bmax=8)
        assert scan == heap, f"Allocation mismatch for {label}"
        print(f"{label}: 64 tones, {sum(scan)} bits, allocations match")