from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample
from inspect_ai.scorer import match
from inspect_ai.solver import generate
from inspect_ai.scorer import includes

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
        scorer=match(
            location="end",
            ignore_case=True,
            numeric=False
        )
    )

if __name__ == "__main__":
    eval(
        hello_model,
        model="ollama/qwen2.5:7b", 
    )