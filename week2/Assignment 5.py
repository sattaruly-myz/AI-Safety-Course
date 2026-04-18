from typing import Tuple
import numpy as np
from scipy.stats import ttest_rel

def significance_by_paired_ttest(
    scores1: np.ndarray,
    scores2: np.ndarray,
    alpha: float = 0.05,
    two_tailed: bool = True,
) -> Tuple[float, float, bool]:
    """
    Paired t-test between two sets of per-question scores.

    Returns (p_value, mean_difference scores1 - scores2, is_significant).
    """
    assert len(scores1) == len(scores2), "arrays must cover the same questions"
    
    alternative = "two-sided" if two_tailed else "greater"
    
    _, p_value = ttest_rel(scores1, scores2, alternative=alternative)
    mean_diff = np.mean(scores1 - scores2)
    
    return p_value, mean_diff, bool(p_value < alpha)