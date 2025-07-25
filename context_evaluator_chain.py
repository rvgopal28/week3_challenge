import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from corrective_rag_prompt import get_context_evaluation_prompt

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

def evaluate_context(query, retrieved_context):
    prompt = get_context_evaluation_prompt(query, retrieved_context)
    evaluation_response = llm.invoke(prompt)

    if hasattr(evaluation_response, 'content'):
        eval_text = evaluation_response.content
    else:
        eval_text = str(evaluation_response)

    result = {}
    for line in eval_text.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip().lower()] = value.strip()

    return result