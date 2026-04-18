@task
def jigsaw_toxic_binary(grade_model_name, dataset):
    return Task(
        dataset,
        solver=[
            system_message(SYSTEM_PROMPT),
            prompt_template(USER_TEMPLATE),
            generate()
        ],
        scorer=model_graded_qa(
            template=BLIND_TEMPLATE, # Судья не видит ответ
            instructions=TOXICITY_SCORER_INSTRUCTIONS,
            grade_pattern=r"(?is)(?:^|\n)\s*(?:GRADE\s*:\s*)?(C|I)\b",
            model=grade_model_name
        )
    )

@task
def jigsaw_toxic_cheat(grade_model_name, dataset):
    return Task(
        dataset,
        solver=[
            system_message(SYSTEM_PROMPT),
            prompt_template(USER_TEMPLATE),
            generate()
        ],
        scorer=model_graded_qa(
            # УБРАЛИ template=BLIND_TEMPLATE, теперь судья видит Ground Truth
            instructions=TOXICITY_SCORER_INSTRUCTIONS,
            grade_pattern=r"(?is)(?:^|\n)\s*(?:GRADE\s*:\s*)?(C|I)\b",
            model=grade_model_name
        )
    )

print("\nЗапускаем проверку слепоты судьи...")
results = eval(
    jigsaw_toxic_binary(grade_model_name=JUDGE_MODEL, dataset=dataset[6:]),
    model=CLASSIFIER_MODEL,
    limit=1,
)

results_cheat = eval(
    jigsaw_toxic_cheat(grade_model_name=JUDGE_MODEL, dataset=dataset[6:]),
    model=CLASSIFIER_MODEL,
    limit=1,
)

def get_judge_prompt(res):
    grading = res[0].samples[0].scores["model_graded_qa"].metadata["grading"]
    return grading[0]["content"]

print("\n=== WITH blind_template (normal run) ===")
print(get_judge_prompt(results))

print("\n=== WITHOUT blind_template (cheat run) ===")
print(get_judge_prompt(results_cheat))