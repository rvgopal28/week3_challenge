import os
import re
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from chroma_db import load_chroma_db
from langchain_openai import ChatOpenAI
from utils import is_uncertain

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

def clean_web_rag_response(text):
    """
    Cleans unwanted headers like 'Unnamed: X' and formats output for user-friendly display.
    """
    # Remove "Unnamed: x" patterns
    text = re.sub(r"Unnamed: \d+: ?", "", text)
    # Remove duplicate whitespaces
    text = re.sub(r"\s+", " ", text)
    # Add line breaks after "|" separators for clarity
    text = re.sub(r"(\|\s*)", "\n", text)
    return text.strip()

def is_internal_context_sufficient(context):
    """
    Heuristic to check if internal retrieval is meaningful.
    """
    if context.count("Name") > 2 or context.count("Description") > 2 or context.count("Price") > 2:
        return False
    if len(context.strip()) < 50:
        return False
    return True

def run_web_search_rag(query):
    db = load_chroma_db()
    retriever = db.as_retriever(search_kwargs={"k": 5})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Internal Retrieval First
    internal_results = retriever.invoke(query)
    combined_internal_context = " ".join([doc.page_content for doc in internal_results if hasattr(doc, 'page_content')])
    cleaned_internal_context = clean_web_rag_response(combined_internal_context)

    # Determine if Web Search is needed
    needs_web_search = (
        "latest" in query.lower()
        or "current" in query.lower()
        or "today" in query.lower()
        or not is_internal_context_sufficient(cleaned_internal_context)
    )

    web_sources = []
    final_answer = cleaned_internal_context
    search_strategy = "INTERNAL_ONLY"

    if needs_web_search:
        # Simulated Web Search Call
        web_response = llm.invoke(f"Search the latest information about: {query}")
        web_text = web_response.content if hasattr(web_response, 'content') else str(web_response)

        if is_uncertain(web_text):
            # Web search yielded no solid results
            web_sources = []
            final_answer = cleaned_internal_context  # Fallback to internal
            search_strategy = "WEB_SUPPLEMENTED"
        else:
            # Hybrid Mode: Combine Internal + Web info
            final_answer = f"{cleaned_internal_context}\n\nAdditional Info from Web:\n{web_text}"
            web_sources = ["Web Search (Simulated)"]
            search_strategy = "HYBRID"

    response = {
        "strategy": search_strategy,
        "currency": "HISTORICAL" if not needs_web_search else "MIXED",
        "confidence": "HIGH" if not needs_web_search else "MEDIUM",
        "answer": final_answer.strip(),
        "internal_sources": ["ChromaDB"],
        "web_sources": web_sources,
        "notes": "Internal context used." if not needs_web_search else "Web results integrated due to insufficient internal data.",
        "last_updated": "2025-07-25"
    }

    return response
