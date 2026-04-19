import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from string import ascii_uppercase
from typing import Tuple, List

from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample, hf_dataset, FieldSpec
from inspect_ai.solver import multiple_choice
from inspect_ai.scorer import choice
from inspect_ai.log import EvalLog

MODEL_A = "ollama/llama3.2:1b"
MODEL_B = "ollama/qwen2.5:0.5b"

def record_to_sample(record: dict) -> Sample:
    """
    Конвертирует сырую запись MMLU в формат Sample для inspect_ai.
    MMLU хранит ответы как индексы (0=A, 1=B, 2=C, 3=D).
    Мы переводим их в буквы.
    """
    answer_idx = int(record["answer"])
    return Sample(
        input=record["question"],
        choices=record["choices"],
        target=ascii_uppercase[answer_idx],
        metadata=dict(subject=record.get("subject"))
    )

dataset = hf_dataset(
    path="cais/mmlu",
    name="all",
    split="test",
    sample_fields=record_to_sample,
    cached=True
)


MY_SUBJECT = "college_computer_science"

MY_SUBSET = dataset.filter(
    lambda s: s.metadata.get("subject") == MY_SUBJECT
)

print(f"--- Dataset Info ---")
print(f"Subject selected: {MY_SUBJECT}")
print(f"Total questions in subset: {len(MY_SUBSET)}")

@task
def mmlu_subset(subset):
    """Задача MMLU для выбранного подмножества."""
    return Task(
        dataset=subset,
        solver=[multiple_choice()],
        scorer=choice()
    )


if __name__ == "__main__":
    print(f"\n--- Running Evaluation ---")
    logs: List[EvalLog] = eval(
        mmlu_subset(MY_SUBSET),
        model=MODEL_A,
        limit=10 
    )

    log = logs[0]
    print(f"\n--- Results for {MODEL_A} ---")
    print(f"Status  : {log.status}")
    print(f"Model   : {log.eval.model}")
    
    accuracy = log.results.scores[0].metrics["accuracy"].value
    print(f"Accuracy: {accuracy * 100:.2f}%")