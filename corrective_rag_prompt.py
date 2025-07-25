def get_context_evaluation_prompt(query, retrieved_context):
    return f"""
You are a Corrective RAG system that evaluates retrieved context quality and corrects retrieval when necessary.

EVALUATE_CONTEXT:
Query: {query}
Retrieved Context: {retrieved_context}

Evaluation Criteria:
1. Relevance Score (0-1)
2. Completeness Score (0-1)
3. Accuracy Score (0-1)
4. Specificity Score (0-1)

Overall Quality: [EXCELLENT/GOOD/FAIR/POOR]

Respond ONLY in the following format:
Relevance: <score>
Completeness: <score>
Accuracy: <score>
Specificity: <score>
Overall Quality: <rating>
"""