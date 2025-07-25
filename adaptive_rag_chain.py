# adaptive_rag_chain.py

from chroma_db import load_chroma_db
from langchain_openai import ChatOpenAI
from adaptive_classifier import classify_query
from search_utils import perform_web_search

llm = ChatOpenAI(temperature=0)

def run_adaptive_rag(query, user_context="intermediate"):
    classification = classify_query(query, user_context)

    # Adaptive Retrieval Parameters
    if classification["complexity"] == "SIMPLE":
        threshold = 0.85
        context_tokens = 512
        source_count = 5
    elif classification["complexity"] == "COMPLEX":
        threshold = 0.75
        context_tokens = 2048
        source_count = 10
    else:
        threshold = 0.80
        context_tokens = 1024
        source_count = 8

    db = load_chroma_db()
    retriever = db.as_retriever(search_kwargs={"k": source_count})
    docs = retriever.invoke(query)
    internal_context = " ".join([doc.page_content for doc in docs])

    # Adaptive Web Search Decision
    needs_web_search = classification["domain"] != "GENERAL" or classification["urgency"] == "IMMEDIATE"

    if needs_web_search:
        web_results = perform_web_search(query)
        web_context = " ".join([res['snippet'] for res in web_results if 'snippet' in res])
    else:
        web_context = ""

    # Adaptive Response Formatting
    if classification["task_type"] == "FACTUAL":
        response_style = "Provide a direct answer with supporting details."
    elif classification["task_type"] == "ANALYTICAL":
        response_style = "Summarize → Analyze → Evidence → Conclusion."
    elif classification["task_type"] == "PROCEDURAL":
        response_style = "Step-by-step instructions with tips and troubleshooting."
    elif classification["task_type"] == "CREATIVE":
        response_style = "Inspire with examples and techniques."

    # Audience Adaptation
    if classification["audience"] == "BEGINNER":
        tone = "Explain simply, avoid jargon, add examples."
    elif classification["audience"] == "EXPERT":
        tone = "Use advanced terminology, focus on novel insights."
    else:
        tone = "Balanced explanation with clarity."

    # Response Synthesis Prompt
    synthesis_prompt = f"""You are an adaptive RAG assistant. Based on classification:
Task Type: {classification['task_type']}
Audience: {classification['audience']}
Response Style: {response_style}
Tone: {tone}
Internal Knowledge: {internal_context}
Web Results: {web_context}
Provide a structured and context-appropriate answer.
"""

    final_answer = llm.invoke(synthesis_prompt).content

    return {
        "classification": classification,
        "adaptive_parameters": {
            "threshold": threshold,
            "context_tokens": context_tokens,
            "source_count": source_count
        },
        "answer": final_answer
    }
