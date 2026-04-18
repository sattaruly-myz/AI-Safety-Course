import numpy as np
from scipy.stats import t

for k in k_values:
    scores = run_and_get_scores(MODEL_A, MY_SUBSET, epochs=k)
    
    mean_acc = np.mean(scores)
    std = np.std(scores, ddof=1)
    n = len(scores)
    
    t_crit = t.ppf(0.975, df=n-1)
    margin = t_crit * (std / np.sqrt(n))
    
    accuracies.append(mean_acc)
    ci_lowers.append(mean_acc - margin)
    ci_uppers.append(mean_acc + margin)