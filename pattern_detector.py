# pattern_detector.py

def detect_rag_pattern(query, internal_context):
    query_lower = query.lower()
    context_lower = internal_context.lower()

    # Pattern 1: Verification Mode (Critical facts/statistics/numbers)
    if any(keyword in context_lower for keyword in ["percent", "study", "survey", "report", "statistics"]):
        return "VERIFICATION_PROTOCOL"

    # Pattern 2: Gap-Filling Mode (Placeholders or missing info)
    if any(phrase in context_lower for phrase in ["tbd", "not available", "to be updated"]):
        return "GAP_FILLING_PROTOCOL"

    # Pattern 3: Update Mode (Outdated data indicators)
    if any(year in context_lower for year in ["2022", "2023", "2024"]):
        return "UPDATE_PROTOCOL"

    # Trigger Update if Query demands recency
    if any(term in query_lower for term in ["latest", "current", "this year", "as of"]):
        return "UPDATE_PROTOCOL"

    return "DEFAULT"
