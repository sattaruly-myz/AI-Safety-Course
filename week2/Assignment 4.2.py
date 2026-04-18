scores_full = run_and_get_scores(MODEL_A, MY_SUBSET, epochs=1)
question_ids = np.arange(len(scores_full))

from scipy.stats import t
import numpy as np

for n in dataset_sizes:
    subset_scores = scores_full[:n]
    
    mean_acc = np.mean(subset_scores)
    std = np.std(subset_scores, ddof=1)
    
    t_crit = t.ppf(0.975, df=n-1)
    margin = t_crit * (std / np.sqrt(n))
    
    accuracies.append(mean_acc)
    ci_lowers.append(mean_acc - margin)
    ci_uppers.append(mean_acc + margin)