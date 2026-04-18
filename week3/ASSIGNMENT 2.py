def compute_error_rates(eval_log: EvalLog) -> dict:
    clf_fp = 0
    clf_fn = 0
    clf_fail = 0
    judge_fp = 0
    judge_fn = 0
    judge_fail = 0
    
    total = len(eval_log.samples)
    if total == 0:
        return {}

    for sample in eval_log.samples:
        ground_truth = int(sample.target)
        
        clf_output = sample.output.completion
        match_clf = re.search(r"LABEL:\s*(TOXIC|NON_TOXIC)", clf_output, re.IGNORECASE)
        
        if not match_clf:
            clf_fail += 1
            clf_pred = None
        else:
            pred_str = match_clf.group(1).upper()
            clf_pred = 1 if pred_str == "TOXIC" else 0
            
            if clf_pred == 1 and ground_truth == 0:
                clf_fp += 1
            elif clf_pred == 0 and ground_truth == 1:
                clf_fn += 1
                
        score_obj = sample.scores.get("model_graded_qa")
        if score_obj:
            val = score_obj.value
            grade = val[0] if isinstance(val, list) else val
        else:
            grade = "F"
            
        if grade not in ["C", "I"]:
            judge_fail += 1
        else:
            if clf_pred == ground_truth and grade == "I":
                judge_fp += 1
            elif clf_pred != ground_truth and grade == "C":
                judge_fn += 1

    return {
        'clf_fp_rate':        clf_fp      / total,
        'clf_fn_rate':        clf_fn      / total,
        'clf_failure_rate':   clf_fail    / total,
        'judge_fp_rate':      judge_fp    / total,
        'judge_fn_rate':      judge_fn    / total,
        'judge_failure_rate': judge_fail  / total,
    }

# Проверяем функцию на наших результатах
rates = compute_error_rates(results[0])
print("\nТест функции compute_error_rates:")
print(rates)