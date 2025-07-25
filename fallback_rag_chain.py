import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from chroma_db import load_chroma_db
from langchain_openai import ChatOpenAI
from utils import is_uncertain

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

# Keyword Expansion
def expand_keywords(query):
    expansions = {
        "menu": ["food list", "offerings"],
        "vendor": ["supplier", "provider"],
        "price": ["cost", "rate"],
        "inventory": ["stock", "materials"]
    }
    expanded_terms = []
    for word in query.lower().split():
        if word in expansions:
            expanded_terms.extend(expansions[word])
    return query + " " + " ".join(expanded_terms)

# Semantic Expansion
def semantic_expand(query):
    semantic_additions = "waffles dessert menu SOP pricing ingredients"
    return f"{query} {semantic_additions}"

# Sufficiency Evaluator (Simple Heuristic)
def evaluate_sufficiency(results_text, query):
    if "price" in query.lower() and not any(char.isdigit() for char in results_text):
        return "INSUFFICIENT"
    if results_text and len(results_text) > 50:
        return "SUFFICIENT"
    elif results_text and len(results_text) > 20:
        return "PARTIAL"
    return "INSUFFICIENT"

def run_fallback_rag(query):
    db = load_chroma_db()
    retriever = db.as_retriever(search_kwargs={"k": 5})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Level 1: Primary Vector Search
    primary_result = qa_chain.invoke(query)
    context_text = primary_result.get('result', str(primary_result))
    sufficiency = evaluate_sufficiency(context_text, query)

    if sufficiency == "SUFFICIENT":
        return {
            "retrieval_level": "PRIMARY",
            "confidence": "HIGH",
            "info_status": "COMPLETE",
            "answer": context_text,
            "sources": ["ChromaDB Primary"],
            "limitations": None,
            "suggestions": None
        }

    # Level 2: Keyword Expansion
    expanded_query = expand_keywords(query)
    secondary_result = qa_chain.invoke(expanded_query)
    secondary_text = secondary_result.get('result', str(secondary_result))
    sufficiency = evaluate_sufficiency(secondary_text, query)

    if sufficiency == "SUFFICIENT":
        return {
            "retrieval_level": "SECONDARY",
            "confidence": "MEDIUM",
            "info_status": "COMPLETE",
            "answer": secondary_text,
            "sources": ["ChromaDB Keyword Expansion"],
            "limitations": None,
            "suggestions": None
        }

    # Level 3: Semantic Expansion
    semantic_query = semantic_expand(query)
    tertiary_result = qa_chain.invoke(semantic_query)
    tertiary_text = tertiary_result.get('result', str(tertiary_result))
    sufficiency = evaluate_sufficiency(tertiary_text, query)

    if sufficiency == "SUFFICIENT":
        return {
            "retrieval_level": "TERTIARY",
            "confidence": "MEDIUM",
            "info_status": "COMPLETE",
            "answer": tertiary_text,
            "sources": ["ChromaDB Semantic Expansion"],
            "limitations": None,
            "suggestions": None
        }
    elif sufficiency == "PARTIAL":
        return {
            "retrieval_level": "TERTIARY",
            "confidence": "LOW",
            "info_status": "PARTIAL",
            "answer": tertiary_text,
            "sources": ["ChromaDB Semantic Expansion"],
            "limitations": "Partial information available",
            "suggestions": "Contact Waffestry Support for detailed info."
        }

    # Level 4: Cross-Domain Retrieval (LLM General Knowledge)
    cross_domain_response = llm.invoke(f"Provide any general knowledge you have about: {query}")
    cross_domain_text = cross_domain_response.content if hasattr(cross_domain_response, 'content') else str(cross_domain_response)
    sufficiency = evaluate_sufficiency(cross_domain_text, query)

    if sufficiency == "SUFFICIENT":
        return {
            "retrieval_level": "QUATERNARY",
            "confidence": "LOW",
            "info_status": "PARTIAL",
            "answer": cross_domain_text,
            "sources": ["LLM General Knowledge"],
            "limitations": "Cross-domain guesswork",
            "suggestions": "Verify with store."
        }

    # Level 5: Final Fallback
    return {
        "retrieval_level": "FALLBACK",
        "confidence": "INSUFFICIENT",
        "info_status": "LIMITED",
        "answer": "We couldn’t retrieve a complete answer for your query. Please contact Waffestry Support or visit our website for assistance.",
        "sources": ["None"],
        "limitations": "Information gap exists",
        "suggestions": "Contact Waffestry Support."
    }
