def get_verification_prompt(answer, question):
    return f"""
You are a fact-checking AI that verifies if an answer is specific and based on known facts.

Question: {question}
Answer Given: {answer}

If the answer is generic, evasive, or lacks specific details (like "I don't know", "visit the website", "check online"), respond with: INVALID.
If the answer provides factual and specific details grounded in known knowledge, respond with: VALID.
Only respond with one of these two words.
"""
