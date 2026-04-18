print("\n--- Запуск Assignment 3 (Сетка моделей) ---")

TEST_MODELS = [ollama/qwen2.5:7b] 

results_grid = []

for clf_model in TEST_MODELS:
    for judge_model in TEST_MODELS:
        print(f"Тестируем: Классификатор={clf_model} | Судья={judge_model}")
        log = eval(
            jigsaw_toxic_binary(grade_model_name=judge_model, dataset=dataset[20:25]),
            model=clf_model,
            limit=5
        )[0]
        
        rates = compute_error_rates(log)
        rates['Classifier'] = clf_model
        rates['Judge'] = judge_model
        results_grid.append(rates)

df_grid = pd.DataFrame(results_grid)
print(df_grid[['Classifier', 'Judge', 'clf_fp_rate', 'clf_fn_rate', 'clf_failure_rate', 'judge_fp_rate', 'judge_fn_rate', 'judge_failure_rate']])