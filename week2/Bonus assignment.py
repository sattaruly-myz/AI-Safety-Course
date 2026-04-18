import numpy as np
import pandas as pd
from scipy import stats

def clustered_ci(df: pd.DataFrame, cluster_col: str, alpha: float = 0.05):
    cluster_means = df.groupby(cluster_col)["score"].mean().values
    G = len(cluster_means)
    mu = cluster_means.mean()
    se = cluster_means.std(ddof=1) / np.sqrt(G)
    t_crit = stats.t.ppf(1 - alpha/2, df=G-1)
    return mu, mu - t_crit*se, mu + t_crit*se, (t_crit*se)*2

def naive_ci(df: pd.DataFrame, alpha: float = 0.05):
    x = df["score"].values
    n = len(x)
    mu = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
    return mu, mu - t_crit*se, mu + t_crit*se, (t_crit*se)*2

def clustered_paired_test(df_a, df_b, cluster_col: str, alpha=0.05):
    merged = df_a.merge(df_b, on=["id", cluster_col], suffixes=("_a", "_b"))
    merged["diff"] = merged["score_a"] - merged["score_b"]

    cluster_diff = merged.groupby(cluster_col)["diff"].mean().values
    G = len(cluster_diff)

    mean_diff = cluster_diff.mean()
    se = cluster_diff.std(ddof=1) / np.sqrt(G)

    t_stat = mean_diff / se if se > 0 else 0.0
    p = 2 * (1 - stats.t.cdf(abs(t_stat), df=G-1))

    return p, mean_diff, p < alpha

logs_a = eval(reading_benchmark_subset(MY_SUBSET), model=MODEL_A, epochs=1)
logs_b = eval(reading_benchmark_subset(MY_SUBSET), model=MODEL_B, epochs=1)

df_a = log_to_df(logs_a[0])
df_b = log_to_df(logs_b[0])

CLUSTER_COL = "passage_id"

mu_n, lo_n, hi_n, w_n = naive_ci(df_a)
mu_c, lo_c, hi_c, w_c = clustered_ci(df_a, CLUSTER_COL)

print(f"Naive CI width     = {w_n:.4f}")
print(f"Clustered CI width = {w_c:.4f}")
print(f"Ratio (clustered / naive) = {w_c / w_n:.2f}")

p_naive, d_naive, sig_naive = significance_by_paired_ttest(
    df_a.groupby("id")["score"].mean().sort_index().values,
    df_b.groupby("id")["score"].mean().sort_index().values,
)

p_clust, d_clust, sig_clust = clustered_paired_test(df_a, df_b, CLUSTER_COL)

print("\nNaive paired test:")
print(f"p={p_naive:.4f}, Δ={d_naive:.4f}, sig={sig_naive}")

print("\nClustered paired test:")
print(f"p={p_clust:.4f}, Δ={d_clust:.4f}, sig={sig_clust}")