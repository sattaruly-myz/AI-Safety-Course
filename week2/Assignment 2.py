def log_to_df(log: EvalLog) -> pd.DataFrame:
    rows = []
    for sample in log.samples:
        score_val = sample.scores.get("choice").value
        score_int = 1 if score_val == "C" else 0
        subject = sample.metadata.get("subject", "")
        
        rows.append({
            "id": sample.id,
            "epoch": sample.epoch if sample.epoch is not None else 0,
            "score": score_int,
            "subject": subject
        })
    return pd.DataFrame(rows)