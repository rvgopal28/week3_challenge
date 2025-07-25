from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from verifier_prompt import get_verification_prompt
from chroma_db import load_chroma_db

llm = ChatOpenAI(temperature=0)

def verify_answer(question, answer):
    prompt = get_verification_prompt(answer, question)
    result = llm.invoke(prompt)
    return result.content.strip().upper() == "VALID"

FORCE_CORRECTION_KEYWORDS = ["menu", "vendor", "offer", "price", "inventory"]

def should_force_corrective_rag(question, answer):
    generic_refusal_phrases = ["I don't know", "I recommend visiting", "check online", "I do not have access"]
    if any(phrase.lower() in answer.lower() for phrase in generic_refusal_phrases):
        return True
    if any(keyword in question.lower() for keyword in FORCE_CORRECTION_KEYWORDS):
        return True
    return False


def run_corrective_rag(query):
    first_answer = llm.invoke(query)

    if hasattr(first_answer, 'content'):
        first_answer_text = first_answer.content
    else:
        first_answer_text = str(first_answer)

    # First, check for forced correction triggers
    if should_force_corrective_rag(query, first_answer_text):
        is_valid = False
    else:
        is_valid = verify_answer(query, first_answer_text)

    response = {
        "initial_answer": first_answer_text,
        "verified": is_valid,
        "corrected_answer": None
    }

    if not is_valid:
        retriever = load_chroma_db().as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        corrected = qa_chain.invoke(query)

        if hasattr(corrected, 'content'):
            corrected_text = corrected.content
        elif isinstance(corrected, dict) and 'result' in corrected:
            corrected_text = corrected['result']
        else:
            corrected_text = str(corrected)

        response["corrected_answer"] = corrected_text

    return response
