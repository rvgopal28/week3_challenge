import os
import re
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from chroma_db import load_chroma_db
from utils import is_uncertain

load_dotenv()

FORCE_RAG_KEYWORDS = ["menu", "offer", "vendor", "order", "price", "inventory"]

def should_force_rag(query):
    return any(keyword in query.lower() for keyword in FORCE_RAG_KEYWORDS)

def extract_price(text):
    match = re.search(r"\b(\d+[\.,]?\d*)\b", text)
    return match.group(1) if match else None

def run_self_rag(query):
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

    initial_response = llm.invoke(query)

    if hasattr(initial_response, 'content'):
        initial_answer_text = initial_response.content
    else:
        initial_answer_text = str(initial_response)

    if should_force_rag(query) or is_uncertain(initial_answer_text):
        db = load_chroma_db()
        retriever = db.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        retrieved_answer = qa_chain.invoke(query)

        if isinstance(retrieved_answer, dict) and 'result' in retrieved_answer:
            retrieved_answer_text = retrieved_answer['result']
        elif hasattr(retrieved_answer, 'content'):
            retrieved_answer_text = retrieved_answer.content
        else:
            retrieved_answer_text = str(retrieved_answer)

        return {
            "initial_answer": initial_answer_text.strip(),
            "retrieved_answer": retrieved_answer_text.strip(),
            "used_retrieval": True
        }

    return {
        "initial_answer": initial_answer_text.strip(),
        "retrieved_answer": None,
        "used_retrieval": False
    }