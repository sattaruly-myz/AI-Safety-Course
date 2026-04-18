from inspect_ai.solvers import multiple_choice, chain_of_thought
import numpy as np

def run_scores_with_solver(model_name, dataset, solver, epochs=1):
    logs = eval(mmlu_subset(dataset), model=model_name, solver=solver, epochs=epochs)
    df = log_to_df(logs[0])
    return df.groupby("id")["score"].mean().sort_index().values, df

# overall comparison
scores_base, df_base = run_scores_with_solver(MODEL_A, MY_SUBSET, multiple_choice(), epochs=1)
scores_cot,  df_cot  = run_scores_with_solver(MODEL_A, MY_SUBSET, chain_of_thought(), epochs=1)

p, d, sig = significance_by_paired_ttest(scores_cot, scores_base)

print(f"CoT vs baseline: p={p:.4f}, Δ={d:.4f}, significant={sig}")

# per-subject comparison
merged = df_base.merge(df_cot, on=["id", "subject"], suffixes=("_base", "_cot"))

results = []
for subject, g in merged.groupby("subject"):
    base = g.groupby("id")["score_base"].mean().sort_index().values
    cot  = g.groupby("id")["score_cot"].mean().sort_index().values
    
    p_s, d_s, sig_s = significance_by_paired_ttest(cot, base)
    results.append((subject, p_s, d_s, sig_s))

for subject, p_s, d_s, sig_s in results:
    print(f"{subject:20s} p={p_s:.4f} Δ={d_s:.4f} sig={sig_s}")