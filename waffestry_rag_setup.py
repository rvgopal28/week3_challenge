import os
import json
import shutil
from zipfile import ZipFile

# Project Structure
project_name = "waffestry_rag_suite"
folders = ["data", "docs"]
files = {
    "main.py": "# Streamlit Main App Code (Paste your main.py here)",
    "self_rag_chain.py": "# Self-RAG Chain Logic",
    "corrective_rag_chain.py": "# Corrective RAG Chain Logic",
    "corrective_rag_v2_chain.py": "# Corrective RAG V2 Chain Logic",
    "fallback_rag_chain.py": "# Fallback RAG Chain Logic",
    "web_search_rag_chain.py": "# Web Search RAG Chain Logic",
    "adaptive_rag_chain.py": "# Adaptive RAG Chain Logic",
    "response_formatter.py": "# Response Formatter Utility",
    "utils.py": "# Utility Functions",
    "chroma_db.py": "# Chroma DB Loader",
    "ingest_data.py": "# Data Ingestion Script",
    "requirements.txt": "streamlit\nlangchain\nchromadb\nopenai\npython-dotenv\npandas",
    ".env": "OPENAI_API_KEY=sk-xxxxxx",
    "data/chunks.json": json.dumps([], indent=2),
    "docs/README.md": "# README for Waffestry RAG Suite",
    "docs/Specs.md": "# Specification Document for Waffestry RAG Suite"
}

# Clean existing folder if exists
if os.path.exists(project_name):
    shutil.rmtree(project_name)

# Create folders
for folder in folders:
    os.makedirs(os.path.join(project_name, folder), exist_ok=True)

# Create files with content
for filepath, content in files.items():
    file_path = os.path.join(project_name, filepath)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)

# Zip the folder
zip_filename = f"{project_name}_v1.0.zip"
with ZipFile(zip_filename, 'w') as zipf:
    for root, dirs, file_list in os.walk(project_name):
        for file in file_list:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=os.path.relpath(file_path, project_name))

print(f"Package created: {zip_filename}")
