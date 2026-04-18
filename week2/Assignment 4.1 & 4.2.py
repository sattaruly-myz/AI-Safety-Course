np.random.seed(42)
base_p = np.random.uniform(0.4, 0.8, 100)
for k in k_values:
    sim_scores = [np.mean(np.random.binomial(1, p, k)) for p in base_p]
    l, m, u = ci_accuracy_basic(np.array(sim_scores))
    accuracies.append(m)
    ci_lowers.append(l)
    ci_uppers.append(u)