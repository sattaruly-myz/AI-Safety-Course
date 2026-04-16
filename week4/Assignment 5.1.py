log_test = eval(
    Task(
        dataset=TEST_SET,
        solver=react(
            prompt=MY_REACT_PROMPT,
            tools=ALL_TOOLS,
            attempts=1,
        ),
        scorer=MATH_SCORER,
        message_limit=MAX_MESSAGES,
    ),
    model=MODEL,
    limit=len(TEST_SET),
)[0]

n_test = len(TEST_SET)
n_correct_test = sum([1 for s in log_test.samples if _first_score(s).value == "C"])