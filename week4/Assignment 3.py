SCORER_MODEL = MODEL

GRADING_INSTRUCTIONS = """You are a strict math grader. 
Compare the model's answer to the target answer. 
They might use different formats (e.g. 1/2 vs 0.5 or \frac{1}{2}). 
If they are mathematically equivalent, reply with 'C' (Correct). 
If they are not mathematically equivalent, reply with 'I' (Incorrect).
Reply ONLY with 'C' or 'I'."""

MATH_SCORER = model_graded_qa(template=GRADING_INSTRUCTIONS, model=SCORER_MODEL)