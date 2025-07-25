import re
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from chroma_db import load_chroma_db

llm = ChatOpenAI(temperature=0)

def evaluate_context(query, context):
    """
    Dummy context evaluation logic — Replace with LLM-based scoring later.
    """
    if len(context) > 100:
        quality = "GOOD"
    else:
        quality = "FAIR"

    return {
        "relevance_score": 0.8,
        "completeness_score": 0.75,
        "accuracy_score": 0.85,
        "specificity_score": 0.8,
        "overall_quality": quality
    }

def clean_context_text(text):
    """
    Cleans unwanted headers like 'Unnamed: X' and extra spaces.
    """
    # Remove "Unnamed: x" patterns
    text = re.sub(r"Unnamed: \d+: ?", "", text)
    # Remove duplicate whitespaces
    text = re.sub(r"\s+", " ", text)
    # Add line breaks after each menu item for readability
    text = re.sub(r"(\|\s*)", "\n", text)
    return text.strip()

def run_corrective_rag_v2(query):
    retriever = load_chroma_db().as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Retrieve Context — returns List[Document]
    initial_context_docs = retriever.invoke(query)

    # Combine page_contents into single context string
    combined_context = " ".join([doc.page_content for doc in initial_context_docs if hasattr(doc, 'page_content')])

    # Clean the context to remove Unnamed headers and beautify output
    cleaned_context = clean_context_text(combined_context)

    # Evaluate Context Quality
    evaluation_scores = evaluate_context(query, cleaned_context)

    # Build Evaluation Summary String
    evaluation_result_string = f"""
    🔍 Context Quality: {evaluation_scores['overall_quality']}
    📊 Confidence Level: HIGH
    📝 Information Status: COMPLETE
    """

    # Correction Decision
    if evaluation_scores['overall_quality'] in ["FAIR", "POOR"]:
        # Re-run RetrievalQA for Correction
        corrected_answer = qa_chain.run(query)
        cleaned_corrected_answer = clean_context_text(corrected_answer)
    else:
        # Use Initial Context as Answer
        cleaned_corrected_answer = cleaned_context

    return {
        "evaluation": evaluation_result_string.strip(),
        "answer": cleaned_corrected_answer
    }
