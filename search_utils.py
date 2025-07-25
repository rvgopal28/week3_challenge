import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def classify_search_intent(query):
    if any(word in query.lower() for word in ["latest", "current", "recent", "today", "2024"]):
        return "NEWS"
    elif "price" in query.lower() or "cost" in query.lower():
        return "FACTUAL"
    else:
        return "FACTUAL"

def perform_web_search(query, time_range="last_month"):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "num": 5,
        "hl": "en",
        "tbs": f"qdr:m" if time_range == "last_month" else ""
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        return [{"title": r["title"], "snippet": r.get("snippet", ""), "link": r["link"]} for r in results]
    else:
        return []
