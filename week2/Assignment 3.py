def ci_accuracy_basic(scores: np.ndarray, ci: float = 0.95) -> Tuple[float, float, float]:
    n = len(scores)
    if n == 0: return 0.0, 0.0, 0.0
    mean_acc = np.mean(scores)
    if mean_acc == 1.0 or mean_acc == 0.0:
        return mean_acc, mean_acc, mean_acc
    
    se = np.sqrt((mean_acc * (1 - mean_acc)) / n)
    z = stats.norm.ppf((1 + ci) / 2)
    return max(0.0, mean_acc - z * se), mean_acc, min(1.0, mean_acc + z * se)

def ci_accuracy(df: pd.DataFrame, ci: float = 0.95) -> Tuple[float, float, float]:
    q_means = df.groupby("id")["score"].mean().values
    return ci_accuracy_basic(q_means, ci)