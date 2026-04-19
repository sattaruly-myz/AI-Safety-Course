import os
from dotenv import load_dotenv
from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample
from inspect_ai.scorer import includes
from inspect_ai.solver import generate

load_dotenv()

@task
def hello_model():
    return Task(
        dataset=[
            Sample(
                input="Say 'Hello world!' and nothing else.",
                target="Hello world!"
            ),
            Sample(
                input="2+2=",
                target="4"
            ),
            Sample(
                input="What is the surname of Sheldon from The Big Bang Theory?",
                target="Cooper"
            ),
            Sample(
                input="What is the capital of Kazakhstan?",
                target="Astana"
            )
        ],
        solver=[generate()],
        #длинные ответы зачтутся как правильные
        scorer=includes(ignore_case=True)
    )

if __name__ == "__main__":
    # Проверка
    if not os.getenv("SAMBANOVA_API_KEY"):
        print("Ошибка: Ключ SAMBANOVA_API_KEY не найден")
    else:
        print("Запускаем DeepSeek-V3 через SambaNova...")
        eval(
            hello_model,
            model="sambanova/DeepSeek-V3", # Облачная модель
        )