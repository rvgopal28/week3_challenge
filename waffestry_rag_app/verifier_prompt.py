def get_verification_prompt(answer, question):
    return f"""
You are a helpful fact-checker.

Question: {question}
Answer Given: {answer}

Is this answer factually correct based on known facts and reliable knowledge?

If it is correct, respond: "VALID".
If it has hallucinations, respond: "INVALID".
Only respond with one of these two words.
"""