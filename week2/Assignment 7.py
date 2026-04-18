from typing import List
import numpy as np

def estimate_variance_components(
    logs_a: List[EvalLog],
    logs_b: List[EvalLog],
) -> dict:
    df_a = log_to_df(logs_a[0])
    df_b = log_to_df(logs_b[0])

    mean_a = df_a.groupby("id")["score"].mean()
    mean_b = df_b.groupby("id")["score"].mean()

    var_a = df_a.groupby("id")["score"].var(ddof=1).fillna(0)
    var_b = df_b.groupby("id")["score"].var(ddof=1).fillna(0)

    sigma2_a = var_a.mean()
    sigma2_b = var_b.mean()

    diff = mean_a - mean_b
    total_var = diff.var(ddof=1)

    omega2 = total_var - (sigma2_a + sigma2_b)
    omega2 = max(0.0, omega2)

    return {
        "omega2": float(omega2),
        "sigma2_a": float(sigma2_a),
        "sigma2_b": float(sigma2_b),
    }