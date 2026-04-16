import sympy
from inspect_ai import Task, eval
from inspect_ai.dataset import Sample
from inspect_ai.agent import react
from inspect_ai.scorer import model_graded_qa
from inspect_ai.tool import tool

MODEL = "ollama/qwen2.5:7b"
SCORER_MODEL = MODEL
MAX_MESSAGES = 10

@tool
def modular_arithmetic():
    async def execute(a: int, b: int) -> str:
        """
        Compute a mod b.

        Args:
            a (int): The number to be divided.
            b (int): The divisor (modulus).
        """
        try:
            if int(b) == 0:
                return "Error: modulo by zero."
            return str(int(a) % int(b))
        except Exception as e:
            return f"Error: {e}"
    return execute

@tool
def sympy_solve():
    async def execute(equation: str) -> str:
        """
        Solve an algebraic equation for x. 

        Args:
            equation (str): The equation to solve, e.g., '2*x + 5 = 21'.
        """
        try:
            x = sympy.Symbol('x')
            if '=' in equation:
                left, right = equation.split('=')
                eq = sympy.Eq(sympy.sympify(left), sympy.sympify(right))
            else:
                eq = sympy.Eq(sympy.sympify(equation), 0)
            sols = sympy.solve(eq, x)
            if not sols: 
                return "No solution found."
            return ", ".join([str(s) for s in sols])
        except Exception as e:
            return f"Error: {e}"
    return execute

ALL_TOOLS = [modular_arithmetic(), sympy_solve()]

GRADING_INSTRUCTIONS = """
You are a helpful math teacher.
1. Look at the Model's full response and find their final numerical answer.
2. Compare it to the Correct Answer: {criterion}.
3. If the core numerical value is the same (even if formatting differs, e.g., 0.5 and 1/2), reply with 'C'.
4. Otherwise, reply with 'I'.

Reply ONLY with 'C' or 'I' (no explanation).
"""

from inspect_ai.scorer import includes
MATH_SCORER = includes()

MY_REACT_PROMPT = """You are a precise mathematical assistant.
1. Solve the problem step-by-step using tools.
2. For EVERY calculation, use modular_arithmetic or sympy_solve.
3. Once you have the final number, call the submit() tool.
4. IMPORTANT: Your final answer must be JUST the number. No sentences, just the digits."""

TEST_SET = [
    Sample(input="Solve for x: 2*x + 5 = 21", target="8"),
    Sample(input="What is 10 mod 3?", target="1")
]

def _first_score(sample):
    if not sample.scores or len(sample.scores) == 0:
        return type('Obj', (object,), {'value': 'I'})()
    
    val = list(sample.scores.values())[0]
    return val[0] if isinstance(val, list) else val

if __name__ == "__main__":
    print("Запуск оценки Агента...")
    results = eval(
        Task(
            dataset=TEST_SET,
            solver=react(
                prompt=MY_REACT_PROMPT,
                tools=ALL_TOOLS,
                attempts=3,
            ),
            scorer=MATH_SCORER,
            message_limit=MAX_MESSAGES,
        ),
        model=MODEL,
        limit=len(TEST_SET),
    )
    
    log_test = results[0]

    print("\n=== ДЕТАЛЬНЫЙ РАЗБОР ОТВЕТОВ ===")
    for s in log_test.samples:
        print(f"Вопрос: {s.input}")
        agent_answer = s.output.completion if s.output else "НЕТ ОТВЕТА"
        print(f"Ответ Агента: {agent_answer}")
        print(f"Правильный ответ: {s.target}")
        
        verdict = _first_score(s).value
        print(f"Вердикт: {verdict}")
        print("-" * 30)
    
    n_test = len(TEST_SET)
    n_correct_test = sum([1 for s in log_test.samples if _first_score(s).value == "C"])
    
    print(f"\n--- РЕЗУЛЬТАТЫ ---")
    print(f"Total tested: {n_test}")
    print(f"Correct answers: {n_correct_test}")
    print(f"Accuracy: {(n_correct_test/n_test)*100 if n_test > 0 else 0}%")