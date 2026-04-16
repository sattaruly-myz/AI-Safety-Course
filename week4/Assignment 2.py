from inspect_ai.tool import tool
import sympy

@tool
def sympy_solve():
    async def execute(equation: str) -> str:
        """Solve an algebraic equation for x. Input should be a string like '2*x + 5 = 21'"""
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