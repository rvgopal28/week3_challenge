# adaptive_classifier.py

def classify_query(query, user_context="intermediate"):
    query_lower = query.lower()

    # Example simple classification rules (can be replaced with ML/NLP models later)
    complexity = "SIMPLE" if len(query.split()) < 10 else "MODERATE"
    if any(term in query_lower for term in ["analyze", "compare", "evaluate"]):
        complexity = "COMPLEX"

    domain = "GENERAL"
    if any(term in query_lower for term in ["technical", "sop", "specification"]):
        domain = "TECHNICAL"

    task_type = "FACTUAL"
    if any(term in query_lower for term in ["step-by-step", "how to", "procedure"]):
        task_type = "PROCEDURAL"
    elif any(term in query_lower for term in ["creative", "idea", "design"]):
        task_type = "CREATIVE"
    elif any(term in query_lower for term in ["analyze", "compare", "differences"]):
        task_type = "ANALYTICAL"

    urgency = "ROUTINE"
    if any(term in query_lower for term in ["today", "latest", "urgent"]):
        urgency = "IMMEDIATE"

    detail = "STANDARD"
    if any(term in query_lower for term in ["detailed", "comprehensive"]):
        detail = "COMPREHENSIVE"

    audience = user_context.upper()

    return {
        "complexity": complexity,
        "domain": domain,
        "task_type": task_type,
        "urgency": urgency,
        "detail": detail,
        "audience": audience
    }
