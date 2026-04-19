import random
from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice, system_message

random.seed(42)

def generate_questions(n: int):
    problems = []
    for _ in range(n):
        a, b = random.randint(10, 99), random.randint(10, 99)
        res = a + b
        problems.append((f"What is {a} + {b}?", str(res)))
    return problems

def generate_distractors(correct: str, n=3):
    distractors = set()
    while len(distractors) < n:
        offset = random.choice([-2, -1, 1, 2, 5])
        wrong = str(int(correct) + offset)
        if wrong != correct: distractors.add(wrong)
    return list(distractors)

def create_dataset(questions, position=None):
    samples = []
    for q, correct in questions:
        options = generate_distractors(correct)
        if position is not None:
            options.insert(position, correct)
            target = "ABCD"[position]
        else:
            options.append(correct)
            random.shuffle(options)
            target = "ABCD"[options.index(correct)]
        
        samples.append(Sample(input=q, choices=options, target=target))
    return samples

@task
def bias_comparison_task(questions, position=None, use_cot=False):
    return Task(
        dataset=create_dataset(questions, position),
        solver=[
            system_message("You are a math assistant. Solve carefully."),
            multiple_choice(cot=use_cot)
        ],
        scorer=choice(),
    )

if __name__ == "__main__":
    MODEL = "ollama/qwen2.5:7b"
    N = 15
    questions = generate_questions(N)

    configs = [
        {"name": "1. Biased (Always A) - No CoT", "pos": 0, "cot": False},
        {"name": "2. Biased (Always A) - WITH CoT", "pos": 0, "cot": True},
        {"name": "3. Random Position - No CoT", "pos": None, "cot": False},
        {"name": "4. Random Position - WITH CoT", "pos": None, "cot": True},
    ]

    for cfg in configs:
        print(f"\n>>> Running: {cfg['name']}")
        eval(
            bias_comparison_task,
            model=MODEL,
            task_args={"questions": questions, "position": cfg["pos"], "use_cot": cfg["cot"]}
        )