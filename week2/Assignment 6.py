def ci_accuracy_for_difference(scores1: np.ndarray, scores2: np.ndarray, ci: float=0.95):
    diffs = scores1 - scores2
    n = len(diffs)
    mean_diff = np.mean(diffs)
    se = np.std(diffs, ddof=1) / np.sqrt(n)
    z = stats.norm.ppf((1 + ci) / 2)
    return mean_diff - z * se, mean_diff + z * se

# Вывод:
scores_a = np.random.binomial(1, 0.6, 50)
scores_b = np.random.binomial(1, 0.5, 50)
l, u = ci_accuracy_for_difference(scores_a, scores_b)
print(f"95% CI для разницы: [{l:.3f}, {u:.3f}]")