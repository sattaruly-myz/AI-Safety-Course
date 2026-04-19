import random
from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice, system_message

#честного сравнения двух тестов
random.seed(42)

#простые математические вопросы
def generate_questions(n: int) -> list[tuple[str, str]]:
    problems = []
    for _ in range(n):
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        op = random.choice(['+', '-'])
        res = a + b if op == '+' else a - b
        problems.append((f"What is {a} {op} {b}?", str(res)))
    return problems

#правдоподобные неправильные ответы
def generate_distractors(correct: str, n: int = 3) -> list[str]:
    correct_int = int(correct)
    distractors = set()
    while len(distractors) < n:
        offset = random.choice([-2, -1, 1, 2, 5, 10])
        wrong = str(correct_int + offset)
        if wrong != correct:
            distractors.add(wrong)
    return list(distractors)

#Формируем Samples
def create_samples(questions: list[tuple[str, str]], correct_position: int | None = None) -> list[Sample]:
    samples = []
    for q_text, correct in questions:
        distractors = generate_distractors(correct)
        
        if correct_position is not None:
            options = distractors.copy()
            options.insert(correct_position, correct)
            target_index = correct_position
        else:
            options = distractors + [correct]
            random.shuffle(options)
            target_index = options.index(correct)
        
        samples.append(Sample(
            input=q_text,
            choices=options,
            target="ABCD"[target_index]
        ))
    return samples

@task
def position_bias_task(questions: list[tuple[str, str]], correct_position: int | None = None):
    return Task(
        dataset=create_samples(questions, correct_position),
        solver=[
            system_message("You are a mathematical assistant. Solve the problem and pick the correct letter."),
            multiple_choice()
        ],
        scorer=choice(),
    )

if __name__ == "__main__":
    MODEL_NAME = "ollama/qwen2.5:7b"
    N = 20
    
    test_questions = generate_questions(N)

    print("\n--- RUNNING TEST 1: BIASED (Correct is always 'A') ---")
    eval(position_bias_task, model=MODEL_NAME, task_args={"questions": test_questions, "correct_position": 0})

    print("\n--- RUNNING TEST 2: UNBIASED (Random positions) ---")
    eval(position_bias_task, model=MODEL_NAME, task_args={"questions": test_questions, "correct_position": None})