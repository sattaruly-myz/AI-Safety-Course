import numpy as np
from scipy import stats

def required_sample_size(
    delta: float,
    omega2: float,
    sigma2_a: float = 0.0,
    sigma2_b: float = 0.0,
    ka: int = 1,
    kb: int = 1,
    alpha: float = 0.05,
    power: float = 0.80,
) -> int:
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta  = stats.norm.ppf(power)

    variance = omega2 + sigma2_a / ka + sigma2_b / kb

    n = ((z_alpha + z_beta) ** 2) * variance / (delta ** 2)

    return int(np.ceil(n))