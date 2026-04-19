from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import system_message, generate
from inspect_ai.scorer import exact
import os
from dotenv import load_dotenv

load_dotenv()
print(f"Ключ найден: {os.getenv('SAMBANOVA_API_KEY')[:5]}...")

@task
def sentiment_classification():
    return Task(
        dataset=[
            Sample(
                input="I absolutely love this new Python library, it's so easy to use!",
                target="Positive"
            ),
            Sample(
                input="The documentation is okay, but some parts are confusing.",
                target="Neutral"
            ),
            Sample(
                input="This is the worst experience I've ever had with an API. Constant errors.",
                target="Negative"
            ),
            Sample(
                input="I went to the store and bought some milk.",
                target="Neutral"
            ),
        ],
        solver=[
            system_message("""
                You are a sentiment analysis expert. 
                Classify the user's input into one of these three categories: 
                Positive, Negative, or Neutral. 
                Reply with ONLY the category name.
            """),
            generate()
        ],
        scorer=exact(),
    )

if __name__ == "__main__":
    eval(sentiment_classification, model="sambanova/Meta-Llama-3.3-70B-Instruct")