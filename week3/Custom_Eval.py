import re
import pandas as pd
from inspect_ai import Task, task, eval
from inspect_ai.dataset import hf_dataset, FieldSpec, Sample
from inspect_ai.solver import system_message, prompt_template, generate
from inspect_ai.scorer import model_graded_qa
from inspect_ai.log import EvalLog

# --- НАСТРОЙКИ МОДЕЛЕЙ ---
# Если у тебя есть ключ OpenAI, используй "openai/gpt-4o-mini"
# Если нет, используй локальную Ollama
CLASSIFIER_MODEL = "ollama/qwen2.5:7b"   
JUDGE_MODEL      = "ollama/qwen2.5:7b"   

# --- СКАЧИВАЕМ ДАТАСЕТ ---
print("Скачиваем датасет Jigsaw...")
dataset = hf_dataset(
    path="thesofakillers/jigsaw-toxic-comment-classification-challenge",
    split="train",  
    sample_fields=FieldSpec(
        input="comment_text", 
        target="toxic"  
    ),
    trust_remote_code=True
)

# --- БАЗОВЫЕ ПРОМПТЫ ИЗ ЗАДАНИЯ ---
SYSTEM_PROMPT = "Classify comments as TOXIC or NON_TOXIC."

USER_TEMPLATE = """Is the following comment toxic or not?
Comment:
{prompt}
LABEL: <TOXIC|NON_TOXIC>"""

TOXICITY_SCORER_INSTRUCTIONS = """Given the comment and the predicted label, decide if the classification is correct.
End your response with one of:
GRADE: C
GRADE: I"""

BLIND_TEMPLATE = """[BEGIN DATA]
***
[Task]: {question}
***
[Submission]: {answer}
***
[END DATA]

{instructions}"""