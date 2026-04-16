from inspect_ai.tool import tool

@tool
def modular_arithmetic():
    async def execute(a: int, b: int) -> str:
        """Compute a mod b."""
        try:
            if int(b) == 0:
                return "Error: modulo by zero."
            return str(int(a) % int(b))
        except Exception as e:
            return f"Error: {e}"
    return execute